# Product Brief: Phish Jam Explorer (Working Title)

## 1. Product Thesis

Phish has one of the deepest improvisational archives in music history, but it is difficult to explore and understand without insider knowledge.

This product builds an AI-native discovery and interpretation layer on top of the live Phish archive.

The wedge feature combines:
1) Semantic Jam Similarity
2) AI Jam Explanation

The goal is to dramatically reduce friction in finding and understanding great jams.

---

## 2. Target User

Primary:
- Engaged Phish fans who listen to full shows and care about improvisation.
- Users who know certain legendary jams but struggle to explore beyond the obvious.

Secondary:
- Intermediate fans who want to understand *why* a jam is great.
- Musicians curious about improvisational structure.

---

## 3. Core Jobs To Be Done (MVP Focus)

### JTBD 1: Find
"When I love a jam, help me find others that feel similar."

### JTBD 2: Understand
"When I'm listening to a jam, help me understand what is happening and why it matters."

We are NOT solving Explore/Browse broadly yet. This is a precision + meaning wedge.

---

## 4. MVP User Flows

### Flow A: Find Similar Jam

1. User selects a jam (e.g., 11/17/97 Ghost).
2. System computes embedding for that jam (or retrieves precomputed).
3. System returns top N semantically similar jams.
4. User sees:
   - Jam title
   - Date
   - Duration
   - Similarity score
   - Brief AI-generated comparison summary

Success Metric:
- User discovers a jam they did not previously know.

---

### Flow B: Explain This Jam

1. User opens a jam page.
2. User clicks "Explain This Jam."
3. System generates:
   - Structural breakdown (Type I vs Type II moments)
   - Notable transitions
   - Peak description
   - Why this jam is considered strong (if applicable)
   - Comparable jams

Success Metric:
- User reports better understanding of what they heard.

---

## 5. Differentiation

Existing tools:
- phish.net = archival + stats
- Phantasy Tour = social discussion
- Streaming platforms = audio playback

This product:
- Interprets improvisation
- Enables vibe-based retrieval
- Connects jams semantically rather than by song name

This is an AI-native improvisation layer.

---

## 6. Data Assumptions (MVP)

MVP will NOT require full raw audio ingestion initially.

Phase 1 data sources:
- Setlist metadata (date, venue, duration)
- Jam length
- Song tags
- Textual descriptions (phish.net reviews if permissible)
- Community commentary summaries
- AI-generated structured jam summaries

Future Phase:
- Audio feature extraction (spectral features, harmonic change detection)

---

## 7. Technical Approach (MVP)

### Embeddings

Each jam will have:
- Text-based embedding derived from:
  - Song name
  - Era
  - Duration
  - Community description
  - AI-generated structural summary

Vector database:
- Pinecone, Supabase, or local FAISS for initial prototype

### Explanation Engine

LLM prompt structured to produce:
- Section breakdown
- Notable modulation moments
- Improvisational characteristics
- Comparative context

---

## 8. Out of Scope (MVP)

- Full social layer
- Real-time audio segmentation
- Jam clustering map
- Personalized recommendation feed
- Era explorer
- Mobile app
- Monetization

This is a focused prototype.

---

## 9. North Star Metric (Early)

"Time to Meaningful Discovery"

Definition:
Time from selecting a jam → discovering a new jam that the user saves or listens to.

---

## 10. Why This Matters

Phish has near-infinite depth but high discovery friction.

This product reduces:
- Canon anxiety
- Archive sprawl
- Insider barrier
- Interpretation ambiguity

It transforms the archive from static data into an explorable improvisational graph.
