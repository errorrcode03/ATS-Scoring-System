# AI Resume ATS Analyzer — System Architecture

## Overview

The **AI Resume ATS Analyzer System** is an end-to-end, ML-powered pipeline that parses resumes, processes natural language, generates semantic embeddings, computes similarity scores against a job description, and produces a ranked ATS (Applicant Tracking System) score for each candidate.

The system is modular, with each component handling a single responsibility. It is designed for desktop/CLI use and does not require a GPU.

---

## Architecture Diagram

```
[Job Description (.txt)]          [Resumes (.pdf / .docx / .txt)]
         |                                      |
         v                                      v
  +-------------+                       +-------------+
  | ResumeParser|                       | ResumeParser|
  |   (parser.py)|                      |   (parser.py)|
  +------+------+                       +------+------+
         |                                      |
         v                                      v
  +------------------+              +------------------+
  | NLPPreprocessor  |              | NLPPreprocessor  |
  | (preprocessing.py)|             | (preprocessing.py)|
  +--------+---------+              +--------+---------+
           |                                 |
           v                                 v
  +------------------+              +------------------+
  |  EmbeddingEngine |              |  EmbeddingEngine |
  |  (embeddings.py) |              |  (embeddings.py) |
  +--------+---------+              +--------+---------+
           |                                 |
           +-----------> [Cosine Similarity] <-----------+
                         (similarity.py)
                               |
                               v
                      +------------------+
                      |  ATSScoreEngine  |
                      |  (ats_score.py)  |
                      +--------+---------+
                               |
                               v
                  +------------------------+
                  | RecommendationEngine   |
                  | (recommendations.py)   |
                  +------------------------+
                               |
                               v
                  +------------------------+
                  |   AIFeedbackLayer      |
                  |   (ai_feedback.py)     |
                  +------------------------+
                               |
                               v
                  +------------------------+
                  |   Ranked ATS Output    |
                  |       (main.py)        |
                  +------------------------+
```

---

## Module Descriptions

### 1. Resume Parser — `parser.py`

**Purpose:** Extracts clean, raw text from various resume file formats.

**Supported Formats:**
- `.pdf` — Parsed using `pdfplumber` (handles multi-column layouts and tables)
- `.docx` — Parsed using `python-docx`
- `.txt` — Direct file read with UTF-8 encoding

**Key Design Decision:** `pdfplumber` was chosen over `PyPDF2` because it handles complex layout artifacts such as multi-column resumes, embedded tables, and special characters more reliably.

---

### 2. NLP Preprocessor — `preprocessing.py`

**Purpose:** Cleans, normalizes, and extracts structured information (skills, entities) from raw text.

**NLP Concepts Used:**
- **Tokenization** — Splitting text into individual words/tokens
- **Stop-word Removal** — Removing common filler words (e.g., "the", "is", "and")
- **Lemmatization** — Reducing words to their root form (e.g., "running" → "run") using spaCy
- **Named Entity Recognition (NER)** — Identifying skills, tools, and technologies

**Model:** `spaCy en_core_web_sm`

---

### 3. Embedding Engine — `embeddings.py`

**Purpose:** Converts preprocessed text into dense numerical vector representations (embeddings) that capture semantic meaning.

**ML Concepts Used:**
- **Transformer Architecture** — Self-attention mechanisms to understand context
- **Dense Embeddings** — 384-dimensional vectors where semantically similar texts are geometrically close
- **Batch Processing** — Encodes multiple texts simultaneously using matrix operations

**Model:** `all-MiniLM-L6-v2` (via `sentence-transformers`)

> **Why MiniLM?** It offers an excellent trade-off between speed and quality. It is ~5x faster than `BERT-base` while achieving comparable performance on semantic similarity benchmarks. It runs efficiently on CPU without a GPU.

**Output Dimension:** 384

---

### 4. Similarity Engine — `similarity.py`

**Purpose:** Quantifies how semantically similar a resume is to the job description.

**ML Concept:** **Cosine Similarity**

Given two embedding vectors **A** (resume) and **B** (job description):

```
Cosine Similarity = (A · B) / (||A|| × ||B||)
```

The result ranges from `0.0` (completely dissimilar) to `1.0` (identical meaning).

**Implementation:** Uses `sklearn.metrics.pairwise.cosine_similarity`, which leverages optimized BLAS/LAPACK C libraries for near-instantaneous computation.

---

### 5. ATS Score Engine — `ats_score.py`

**Purpose:** Combines multiple scoring signals into a single unified ATS score (0–100).

**Scoring Components (Weighted Ensemble):**

| Signal | Weight | Method |
|---|---|---|
| Semantic Similarity | 50% | Cosine similarity of embeddings |
| Keyword Matching | 40% | Jaccard-style set intersection of extracted skills |
| Structure / Length | 10% | Heuristic: ideal resume = 1,500–4,500 characters |

**Final Score Formula:**
```
Final Score = (Semantic × 0.50) + (Keyword × 0.40) + (Structure × 0.10)
```

**Keyword Matching Formula (Jaccard-style):**
```
Keyword Score = |Resume Skills ∩ JD Skills| / |JD Skills| × 100
```

Python `set` intersection provides **O(1)** average lookup time, making this highly efficient for large skill lists.

---

### 6. Recommendation Engine — `recommendations.py`

**Purpose:** Generates actionable, human-readable recommendations for each candidate based on the ATS analysis.

Recommendations are based on:
- Missing skills identified in the job description but absent from the resume
- Resume length and structure signals
- Keyword density compared to the JD

---

### 7. AI Feedback Layer — `ai_feedback.py`

**Purpose:** Integrates with the **Google Gemini API** (`google-generativeai`) to provide GPT-quality, contextual narrative feedback for each resume.

This layer is **optional** — the pipeline runs without it if no API key is configured.

---

### 8. Main Orchestrator — `main.py`

**Purpose:** Ties all modules together in a sequential pipeline.

**Execution Flow:**
1. Initialize all module instances
2. Parse and embed the Job Description (once)
3. Iterate over all resumes in the `resumes/` directory
4. For each resume: Parse → Preprocess → Embed → Similarity → ATS Score
5. Collect results and sort by final score (descending)
6. Print ranked output to console

---

## Technology Stack

| Library | Version | Purpose |
|---|---|---|
| `sentence-transformers` | 2.5.1 | Semantic embedding generation |
| `spaCy` | 3.7.4 | NLP preprocessing & NER |
| `scikit-learn` | 1.4.1 | Cosine similarity computation |
| `pandas` | 2.2.1 | Data handling (optional analysis) |
| `numpy` | 1.26.4 | Numerical array operations |
| `pdfplumber` | 0.11.0 | PDF text extraction |
| `python-docx` | 1.1.0 | DOCX text extraction |
| `google-generativeai` | 0.4.1 | Optional Gemini AI feedback |
| `markdown-pdf` | latest | Architecture documentation export |

---

## Data Flow Summary

```
Raw Resume File
    → Text Extraction (parser.py)
    → Cleaning & Skill Extraction (preprocessing.py)
    → Vector Embedding (embeddings.py)
    → Cosine Similarity vs. JD Embedding (similarity.py)
    → Weighted ATS Score (ats_score.py)
    → Recommendations (recommendations.py)
    → [Optional] AI Narrative Feedback (ai_feedback.py)
    → Ranked Leaderboard Output (main.py)
```

---

## File Structure

```
ATS Scoring System/
│
├── main.py                  # Pipeline orchestrator
├── parser.py                # Resume text extraction
├── preprocessing.py         # NLP preprocessing & skill extraction
├── embeddings.py            # Sentence transformer embedding engine
├── similarity.py            # Cosine similarity computation
├── ats_score.py             # Weighted ATS score calculator
├── recommendations.py       # Rule-based recommendation engine
├── ai_feedback.py           # Gemini AI feedback integration
├── convert_pdf.py           # Converts this document to PDF
│
├── datasets/
│   └── job_description.txt  # Target job description input
│
├── resumes/                 # Place candidate resumes here
│   └── (*.pdf / *.docx / *.txt)
│
├── models/                  # Cached model weights (auto-downloaded)
├── requirements.txt         # Python dependencies
└── system_architecture.md   # This document
```

---

## Performance Characteristics

- **Embedding Model Size:** ~80 MB (downloaded on first run, then cached)
- **Inference Speed:** ~5–15ms per resume on CPU (MiniLM is CPU-friendly)
- **Scalability:** Batch embedding mode supports processing hundreds of resumes efficiently
- **Memory Usage:** Minimal — MiniLM-L6 requires only ~150 MB RAM at inference

---

*Generated by the ATS Scoring System — AI Resume Analyzer*
