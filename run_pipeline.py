#!/usr/bin/env python3
"""
Jam enrichment pipeline: load CSV -> AI descriptions + embeddings -> JSONL + FAISS index.
Uses OPENAI_API_KEY. Cache: skip jams already in jams_enriched.jsonl unless --force.
"""
import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
import faiss

# Load .env so OPENAI_API_KEY is set (never commit .env)
load_dotenv()

# Paths (project root = parent of this script)
ROOT = Path(__file__).resolve().parent
RAW_CSV = ROOT / "data" / "raw" / "jams_seed.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
ENRICHED_JSONL = PROCESSED_DIR / "jams_enriched.jsonl"
INDEX_DIR = ROOT / "data" / "index"
FAISS_PATH = INDEX_DIR / "jams.faiss"
META_PATH = INDEX_DIR / "jams_meta.json"

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"


def slug(song: str) -> str:
    """Lowercase, replace non-alphanumeric with underscore."""
    s = re.sub(r"[^a-z0-9]+", "_", song.lower().strip())
    return s.strip("_") or "unknown"


def normalize_date(d: str) -> str:
    """Expect YYYY-MM-DD; pass through or normalize if needed."""
    d = d.strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", d):
        return d
    # Try common variants
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            from datetime import datetime
            return datetime.strptime(d, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return d


def load_csv(path: Path) -> list[dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in row.items()}
            rows.append(row)
    return rows


def jam_id_from_row(row: dict) -> str:
    song = row.get("song", "").strip() or "unknown"
    date = normalize_date(row.get("date", ""))
    return f"{slug(song)}-{date}"


def load_existing_jsonl(path: Path) -> dict[str, dict]:
    out = {}
    if not path.exists():
        return out
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            out[rec["jam_id"]] = rec
    return out


def generate_description(client: OpenAI, row: dict, jam_id: str) -> str:
    song = row.get("song", "")
    date = row.get("date", "")
    venue = row.get("venue", "")
    duration = row.get("duration_minutes", "")
    era = row.get("era", "")
    style_tags = row.get("style_tags", "")

    prompt = f"""You are a knowledgeable Phish fan. Given the following metadata for a specific live jam, write a short factual description (2-4 sentences) of what this jam is known for. Use only the information provided; do not invent setlists, venues, or dates.

Metadata:
- Song: {song}
- Date: {date}
- Venue: {venue}
- Duration (minutes): {duration}
- Era: {era}
- Style tags (use as hints for tone/structure only): {style_tags}

Write a concise ai_description that a fan could use to recognize this jam. Stay factual and do not hallucinate."""

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    text = (resp.choices[0].message.content or "").strip()
    return text


def get_embedding(client: OpenAI, text: str) -> list[float]:
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return resp.data[0].embedding


def text_to_embed(rec: dict) -> str:
    parts = [
        rec.get("song", ""),
        rec.get("date", ""),
        rec.get("venue", ""),
        rec.get("era", ""),
        str(rec.get("duration_minutes", "")),
        rec.get("ai_description", ""),
    ]
    return " ".join(p for p in parts if p)


def main():
    parser = argparse.ArgumentParser(description="Jam enrichment + FAISS index pipeline")
    parser.add_argument("--force", action="store_true", help="Regenerate all jams and overwrite cache")
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)
    if not RAW_CSV.exists():
        print(f"Input CSV not found: {RAW_CSV}", file=sys.stderr)
        sys.exit(1)

    client = OpenAI()
    rows = load_csv(RAW_CSV)
    existing = {} if args.force else load_existing_jsonl(ENRICHED_JSONL)

    enriched: list[dict] = []
    for row in rows:
        jid = jam_id_from_row(row)
        if jid in existing and not args.force and existing[jid].get("embedding"):
            enriched.append(existing[jid])
            continue
        # Need to compute description and embedding
        ai_desc = generate_description(client, row, jid)
        rec = {
            "jam_id": jid,
            "song": row.get("song", ""),
            "date": row.get("date", ""),
            "venue": row.get("venue", ""),
            "duration_minutes": row.get("duration_minutes", ""),
            "era": row.get("era", ""),
            "style_tags": row.get("style_tags", ""),
            "ai_description": ai_desc,
        }
        text = text_to_embed(rec)
        rec["embedding"] = get_embedding(client, text)
        enriched.append(rec)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with open(ENRICHED_JSONL, "w", encoding="utf-8") as f:
        for rec in enriched:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # FAISS index: same order as enriched
    dim = len(enriched[0]["embedding"])
    index = faiss.IndexFlatIP(dim)  # inner product = cosine if vectors normalized
    import numpy as np
    vectors = np.array([r["embedding"] for r in enriched], dtype="float32")
    faiss.normalize_L2(vectors)
    index.add(vectors)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(FAISS_PATH))

    # Metadata: jam_id -> index position, and record fields for display
    jam_ids_ordered = [r["jam_id"] for r in enriched]
    meta = {
        "jam_ids": jam_ids_ordered,
        "by_id": {
            r["jam_id"]: {
                "song": r["song"],
                "date": r["date"],
                "venue": r["venue"],
                "duration_minutes": r["duration_minutes"],
                "era": r["era"],
                "ai_description": r.get("ai_description", ""),
            }
            for r in enriched
        },
    }
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"Enriched {len(enriched)} jams -> {ENRICHED_JSONL}")
    print(f"Index -> {FAISS_PATH}, meta -> {META_PATH}")


if __name__ == "__main__":
    main()
