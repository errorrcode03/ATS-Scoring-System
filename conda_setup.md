# Conda Environment Setup for ATS Resume Analyzer

This document explains how to set up the Conda environment required to run the AI ATS Resume Analyzer system.

### Purpose
To create an isolated Python environment that prevents dependency conflicts and ensures reproducibility. This is crucial for ML/NLP projects where specific library versions (like `spaCy` or `sentence-transformers`) can introduce breaking changes.

### Step 1: Create the Environment
We use Python 3.11 as requested for optimal compatibility and performance.
```bash
conda create -n ats_analyzer python=3.11 -y
```

### Step 2: Activate the Environment
```bash
conda activate ats_analyzer
```

### Step 3: Install Dependencies
Install all required libraries using the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### Step 4: Download spaCy Language Model
The `preprocessing.py` module relies on the English language model (`en_core_web_sm`) for tokenization, lemmatization, and NER.
```bash
python -m spacy download en_core_web_sm
```

### Step 5: Register the Conda Environment as a Jupyter Kernel
This makes the `ats_analyzer` environment available inside Jupyter Notebook.
```bash
python -m ipykernel install --user --name=ats_analyzer --display-name "ATS Analyzer (Python 3.11)"
```

### Step 6: Launch Jupyter Notebook
```bash
jupyter notebook
```
Then open `ATS_Analyzer.ipynb` and select the **"ATS Analyzer (Python 3.11)"** kernel.

### Optional: Install GPU Support for PyTorch
If you have an NVIDIA GPU and want faster embedding generation, install PyTorch with CUDA support *before* installing `requirements.txt`:
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```
