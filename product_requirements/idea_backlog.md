# Idea Backlog

This document captures future feature concepts beyond the current MVP.

MVP Focus:
- Semantic Jam Similarity
- AI Jam Explanation

Everything below is intentionally out of scope for MVP.

These ideas are grouped by core Jobs To Be Done (JTBD) to inform future information architecture and sequencing.

---

# JTBD: Find (Precision Engine)

> "I know roughly what I want — help me retrieve it."

---

## 1. Segment-Level Search

Allow users to search within jams for specific structural moments:
- Bliss peaks longer than X minutes
- Ambient sections without drums
- Minor key tension builds
- Extended groove sections

Requires:
- Jam segmentation
- Audio feature extraction
- Segment-level embeddings
- Time-indexed vector storage

Effort: Large  
Dependency: Audio analysis pipeline  

Status: Idea

---

## 2. Advanced Similarity Filters

Enhance semantic similarity with structured filtering:
- Era (1.0, 2.0, 3.0, 4.0)
- Jam duration range
- Peak intensity score
- Harmonic instability score
- Groove-based vs ambient classification

Effort: Medium  
Dependency: Structured metadata scoring  

Status: Idea

---

# JTBD: Explore (Serendipity Engine)

> "I don’t know what I want — show me something interesting."

---

## 3. Jam Map (Embedding Visualization)

Interactive 2D map of jams clustered by similarity.

Users can:
- Zoom by era
- Click clusters
- Explore adjacent jams
- Toggle similarity dimension

Requires:
- Dimensionality reduction (UMAP or t-SNE)
- Frontend visualization layer
- Stable embedding space

Effort: Medium-Large  
Dependency: Working embedding engine  

Status: Idea

---

## 4. Discovery Trails

AI-generated guided listening paths such as:
- "Understanding Cow Funk in 6 Jams"
- "Evolution of Tweezer"
- "Intro to 3.0 Ambient"
- "Dark 1999 Essentials"

System builds structured progression with context and explanation.

Effort: Medium  
Dependency: Jam explanation engine  

Status: Idea

---

## 5. Era Explorer

Interactive breakdown of stylistic differences across eras:
- Signature improvisational traits
- Typical jam structures
- Harmonic tendencies
- Must-hear canonical jams

Effort: Medium  
Dependency: Canon scoring + explanation engine  

Status: Idea

---

# JTBD: Understand (Meaning Engine)

> "I’m listening — help me understand what’s happening."

---

## 6. Guided Listening Mode

Timestamped commentary alongside jam playback:
- Type I → Type II transition markers
- Modulation points
- Peak buildup annotation
- Structural segmentation

Requires:
- Time-based structural detection
- Audio segmentation
- LLM commentary prompts

Effort: Large  
Dependency: Audio segmentation  

Status: Idea

---

## 7. Jam Decomposition

Break jams into structural components:
- Harmonic shifts
- Mode changes
- Improvisational phases
- Motif repetition

Potential output:
- Visual jam timeline
- Simplified harmonic summary
- Guitar motif detection (long-term)

Effort: Large  
Dependency: Advanced audio analysis  

Status: Idea

---

# JTBD: Contextualize (Perspective Engine)

> "How does this fit in the canon?"

---

## 8. Show Fingerprints

Generate structural metrics per show:
- Type II ratio
- Jam density score
- Rarity index
- Energy variance graph
- Experimental score

Enable show comparison.

Effort: Medium  
Dependency: Jam classification model  

Status: Idea

---

## 9. Canon Index

Rank jams by:
- Historical significance
- Community sentiment
- Structural uniqueness
- Influence score

Goal: Reduce “canon anxiety.”

Effort: Medium  
Dependency: Sentiment + metadata ingestion  

Status: Idea

---

# JTBD: Identity (Future Layer)

> "Help me understand my own taste."

---

## 10. Taste Fingerprint

Cluster users by listening behavior:
- Preferred eras
- Jam length bias
- Peak intensity preference
- Groove vs ambient preference

Output:
- Personal jam profile
- Similar-user discovery
- Weekly curated picks

Effort: Large  
Dependency: User accounts + listening tracking  

Status: Idea

---

## 11. Phan Graph

Concert twin finder:
- Show overlap network
- Similar jam taste clustering
- Community micro-clusters

Effort: Large  
Dependency: Social layer + user data  

Status: Idea

---

# Long-Term Vision

These features represent expansion paths once the core embedding + explanation engine is validated.

The strategic order should follow infrastructure maturity:

1. Embedding quality
2. Explanation quality
3. Structural metadata scoring
4. Visualization
5. Audio analysis
6. Social graph

---

# Rule

Do not build these until:
- Semantic similarity works well.
- Explanation engine produces consistent value.
- MVP shows meaningful discovery.

This document protects long-term ambition while preserving short-term focus.