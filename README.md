# Type II (Phish Jam Explorer)

Minimal spike for jam similarity and explanation: enrich jams with AI descriptions and embeddings, build a FAISS index, query by `jam_id` for similar jams.

## Setup

1. Get an OpenAI API key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys) (sign up or log in, then Create new secret key).

2. Put the key in a `.env` file in the project root (this file is in `.gitignore` and will not be committed):
   ```bash
   echo 'OPENAI_API_KEY=sk-your-key-here' > .env
   ```
   Or create `.env` manually with one line: `OPENAI_API_KEY=sk-...`

3. Install dependencies (use `pip3` or `python3 -m pip` if `pip` is not found):
   ```bash
   pip3 install -r requirements.txt
   ```
   Or: `python3 -m pip install -r requirements.txt`

4. Seed data lives at `data/raw/jams_seed.csv`. If you only have `data/jams_seed.csv`, copy it:
   ```bash
   cp data/jams_seed.csv data/raw/jams_seed.csv
   ```

## Run pipeline

Enrich jams (AI description + embeddings) and build the FAISS index:

```bash
python run_pipeline.py
```

Skip jams already in `data/processed/jams_enriched.jsonl` unless you pass `--force`:

```bash
python run_pipeline.py --force
```

Outputs:
- `data/processed/jams_enriched.jsonl` — enriched records (cache)
- `data/index/jams.faiss` — FAISS index
- `data/index/jams_meta.json` — metadata for lookup

## Query similar jams

```bash
python src/query.py <jam_id> [--top-k 5]
```

Example (find jams similar to 11/17/97 Ghost):

```bash
python src/query.py ghost_1997-11-17 --top-k 5
```

`jam_id` format: `slug(song)-YYYY-MM-DD`, e.g. `reba_1995-12-31`, `tweezer_2015-08-22`.
