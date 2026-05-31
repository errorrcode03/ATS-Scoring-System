# AI Resume ATS Analyzer System

An intelligent, standalone CLI/Desktop Applicant Tracking System (ATS) Analyzer built in Python. This project utilizes Natural Language Processing (NLP) and Deep Learning Transformer models to parse resumes, extract technical skills, compute semantic similarity against job descriptions, and generate a weighted ATS match score.

## Features

- **Multi-Format Parsing**: Extracts clean text from unstructured PDF and DOCX files using `pdfplumber` and `python-docx`.
- **Intelligent Preprocessing**: Cleans noise, lemmatizes words, and extracts specific technical skills via `spaCy` Named Entity Recognition (NER).
- **Dense Vector Similarity**: Generates 384-dimensional semantic embeddings using the highly optimized `all-MiniLM-L6-v2` transformer model (via `sentence-transformers`).
- **Ensemble Scoring Engine**: Calculates an out-of-100 ATS score by combining Semantic Meaning (50%), Exact Keyword Overlap (40%), and Document Structure (10%).
- **Recommendation Engine**: Performs gap analysis to explicitly point out missing skills and suggest actionable improvements.
- **AI Feedback Layer (Optional)**: Uses Google Gemini's generative LLM to provide human-like, qualitative recruiter feedback.
- **Batch Processing**: Automatically iterates over all candidate resumes placed in the `resumes/` directory, sorting and ranking them from highest to lowest fit.

## Project Structure

```text
ATS_Project/
│
├── resumes/                 # Drop your PDF, DOCX, or TXT candidate resumes here
├── datasets/                # Contains the job_description.txt
├── models/                  # (Future) Directory for storing custom fine-tuned weights
│
├── main.py                  # Primary application entry point & batch processor
├── parser.py                # File ingestion and text extraction logic
├── preprocessing.py         # spaCy NLP cleaning and skill entity extraction
├── embeddings.py            # Sentence-Transformers vectorization engine
├── similarity.py            # Scikit-learn Cosine Similarity mathematical calculations
├── ats_score.py             # Weighted heuristic scoring engine
├── recommendations.py       # Gap analysis for missing skills
├── ai_feedback.py           # Optional Google Gemini API integration
│
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Setup Instructions

This project is built to run optimally on a standard machine without requiring heavy GPU computing. An isolated `conda` environment is highly recommended.

### 1. Create and Activate the Conda Environment
Using Python 3.11 ensures compatibility with all required ML libraries.
```bash
conda create -n ats_analyzer python=3.11 -y
conda activate ats_analyzer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the NLP Language Model
The preprocessor requires spaCy's English core model.
```bash
python -m spacy download en_core_web_sm
```
*(Note: If you run into a 404 error using the command above, use the direct URL instead: `pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz`)*

## Usage

1. **Set the Target**: Open `datasets/job_description.txt` and paste the requirements of the job you are hiring for (or applying to).
2. **Add Candidates**: Drop any number of PDF, DOCX, or TXT resumes into the `resumes/` directory.
3. **Run the Analyzer**: 
   ```bash
   python main.py
   ```

The script will batch process all files, output individual candidate metrics, and present a **Final ATS Ranking** sorted by the highest match score.

### Optional: Enabling AI Generative Feedback
If you want the system to act as a human recruiter and provide qualitative reviews:
1. Obtain an API key from Google AI Studio.
2. Run `main.py`. The `AIFeedbackLayer` will automatically detect the key and append a review paragraph to the terminal output.
