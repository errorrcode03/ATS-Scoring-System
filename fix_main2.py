import json

with open('main.ipynb', 'r', encoding='utf-8') as f:
    d = json.load(f)

source = [
    '"""\n',
    '# Main Application Pipeline\n',
    'Purpose: To tie the modules together into a complete end-to-end ATS parsing, embedding, and scoring pipeline.\n',
    'Architecture: Orchestrates data flow. Reads files -> Parses text -> Preprocesses/Extracts Skills -> Generates Embeddings -> Computes Similarity -> Generates ATS Score -> Provides Recommendations and AI Feedback.\n',
    '"""\n',
    '\n',
    'import os\n',
    'import glob\n',
    'import importnb\n',
    'with importnb.Notebook():\n',
    '    from parser import ResumeParser\n',
    '    from preprocessing import NLPPreprocessor\n',
    '    from embeddings import EmbeddingEngine\n',
    '    from similarity import SimilarityEngine\n',
    '    from ats_score import ATSScoreEngine\n',
    '    from recommendations import RecommendationEngine\n',
    '    from ai_feedback import AIFeedbackLayer\n'
]

# We want to replace everything in the original source up to the `def main():` line
original_source = d['cells'][0]['source']
main_idx = 0
for i, line in enumerate(original_source):
    if line.startswith('def main():'):
        main_idx = i
        break

d['cells'][0]['source'] = source + original_source[main_idx:]

with open('main.ipynb', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=1)
