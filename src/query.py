#!/usr/bin/env python3
"""
Query similar jams by jam_id. Uses FAISS index + jams_meta; reads query embedding from jams_enriched.jsonl.
Usage: python src/query.py <jam_id> [--top-k 5]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import faiss
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
ENRICHED_JSONL = ROOT / "data" / "processed" / "jams_enriched.jsonl"
FAISS_PATH = ROOT / "data" / "index" / "jams.faiss"
META_PATH = ROOT / "data" / "index" / "jams_meta.json"


def load_embedding_for_jam(jam_id: str) -> list[float] | None:
    if not ENRICHED_JSONL.exists():
        return None
    with open(ENRICHED_JSONL, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("jam_id") == jam_id:
                return rec.get("embedding")
    return None


def main():
    parser = argparse.ArgumentParser(description="Find similar jams by jam_id")
    parser.add_argument("jam_id", help="e.g. ghost_1997-11-17")
    parser.add_argument("--top-k", type=int, default=5, help="Number of similar jams to return (default 5)")
    args = parser.parse_args()

    if not FAISS_PATH.exists() or not META_PATH.exists():
        print("Index not found. Run: python run_pipeline.py", file=sys.stderr)
        sys.exit(1)

    with open(META_PATH, encoding="utf-8") as f:
        meta = json.load(f)
    jam_ids = meta["jam_ids"]
    by_id = meta["by_id"]

    if args.jam_id not in by_id:
        print(f"Unknown jam_id: {args.jam_id}", file=sys.stderr)
        sys.exit(1)

    embedding = load_embedding_for_jam(args.jam_id)
    if not embedding:
        print(f"Could not load embedding for {args.jam_id} from {ENRICHED_JSONL}", file=sys.stderr)
        sys.exit(1)

    index = faiss.read_index(str(FAISS_PATH))
    query_vec = np.array([embedding], dtype="float32")
    faiss.normalize_L2(query_vec)

    k = min(args.top_k + 1, index.ntotal)  # +1 to allow excluding self
    scores, indices = index.search(query_vec, k)

    # Exclude self (first result is usually self)
    self_idx = jam_ids.index(args.jam_id)
    seen = 0
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue
        jid = jam_ids[idx]
        if jid == args.jam_id:
            continue
        seen += 1
        if seen > args.top_k:
            break
        info = by_id.get(jid, {})
        print(f"{jid}\t{info.get('song', '')}\t{info.get('date', '')}\t{float(score):.4f}\t{info.get('venue', '')}")


if __name__ == "__main__":
    main()
