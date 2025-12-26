# Agentic App Review Trend Analysis

## Overview
This project implements an agentic AI system to analyze Google Play Store reviews
for Swiggy. Reviews are processed as daily batches, simulating real-world ingestion
from June 2024 onwards.

The system generates a rolling trend report (T–30 to T) that highlights
user issues, complaints, and feature requests over time.

---

## Architecture

### 1. Daily Batch Ingestion
- Reviews are grouped by date and treated as independent daily batches.
- This mirrors real production pipelines where data arrives incrementally.

### 2. Topic Extraction & Consolidation Agent
- A reasoning-based LLM agent analyzes each daily batch.
- The agent:
  - Extracts user issues, complaints, and requests
  - Semantically merges similar issues into canonical topics
  - Produces frequency counts per topic
- This avoids topic fragmentation (e.g., "delivery guy rude" vs "delivery partner impolite").

### 3. Robust Output Handling
- The agent is instructed to return strict JSON.
- Fallback parsing is implemented to handle malformed responses gracefully.
- Invalid batches are skipped without impacting downstream aggregation.

### 4. Trend Aggregation
- Topic counts are aggregated across days.
- Final output is a pivoted table showing topic frequency from T–30 to T.

---

## Why Agentic AI?
Traditional topic modeling approaches (LDA, TopicBERT) struggle with semantic
consistency and evolving language. This system uses agentic reasoning to achieve
high recall and accurate topic consolidation, making trends more reliable for
product teams.

---

## Output
The final output is a CSV table with:
- Rows: Canonical topics
- Columns: Dates (T–30 to T)
- Cells: Frequency of topic occurrence per day

Note that only a few inputs have been taken due to the compatibality issues on a beginner laptop
