"""
# Main Application Pipeline
Purpose: To tie the modules together into a complete end-to-end ATS parsing, embedding, and scoring pipeline.
Architecture: Orchestrates data flow. Reads files -> Parses text -> Preprocesses/Extracts Skills -> Generates Embeddings -> Computes Similarity -> Generates ATS Score -> Provides Recommendations and AI Feedback.
"""

import os
import glob
from parser import ResumeParser
from preprocessing import NLPPreprocessor
from embeddings import EmbeddingEngine
from similarity import SimilarityEngine
from ats_score import ATSScoreEngine
from recommendations import RecommendationEngine
from ai_feedback import AIFeedbackLayer

def main():
    print("==================================================")
    print("        AI Resume ATS Analyzer System             ")
    print("==================================================\n")

    jd_path = "datasets/job_description.txt"
    resume_dir = "resumes/"

    # Step 1: Initialization
    print("[1] Initializing Modules...")
    parser = ResumeParser()
    preprocessor = NLPPreprocessor()
    embedder = EmbeddingEngine()
    similarity_engine = SimilarityEngine()
    score_engine = ATSScoreEngine()
    rec_engine = RecommendationEngine()
    ai_feedback = AIFeedbackLayer()
    print("Modules initialized successfully.\n")

    # Step 2: Parse Job Description (Done once)
    print("[2] Parsing Job Description...")
    jd_text = parser.parse(jd_path)
    if not jd_text:
        print("Error: Could not parse Job Description.")
        return
        
    jd_data = preprocessor.preprocess(jd_text)
    jd_embedding = embedder.generate_embedding(jd_data['lemmatized_text'])
    print(f"Required Skills Found: {len(jd_data['skills'])}\n")

    # Step 3: Batch Process all Resumes
    print("[3] Scanning 'resumes/' directory for candidates...")
    resume_files = [f for f in os.listdir(resume_dir) if os.path.isfile(os.path.join(resume_dir, f))]
    
    if not resume_files:
        print("No resumes found in the 'resumes/' folder. Please add some PDF, DOCX, or TXT files!")
        return
        
    print(f"Found {len(resume_files)} resumes. Processing...\n")
    
    results = []

    for filename in resume_files:
        filepath = os.path.join(resume_dir, filename)
        print(f"--- Analyzing: {filename} ---")
        
        # Extract text
        resume_text = parser.parse(filepath)
        if not resume_text:
            print(f"Skipping {filename} due to parse error.\n")
            continue
            
        # Preprocess and Embed
        resume_data = preprocessor.preprocess(resume_text)
        resume_embedding = embedder.generate_embedding(resume_data['lemmatized_text'])
        
        # Calculate Similarity
        similarity_score = similarity_engine.calculate_similarity(resume_embedding, jd_embedding)
        
        # Generate ATS Score
        ats_result = score_engine.generate_score(
            similarity_score=similarity_score,
            resume_skills=resume_data['skills'],
            jd_skills=jd_data['skills'],
            resume_text=resume_text
        )
        
        score = ats_result['final_score']
        print(f"Candidate ATS Score: {score} / 100")
        print(f"Skills Found: {len(resume_data['skills'])}")
        print("-" * 50)
        
        # Generate Recommendations
        recs = rec_engine.generate_recommendations(
            resume_skills=resume_data['skills'],
            jd_skills=jd_data['skills']
        )

        # Store for ranking later
        results.append({
            "filename": filename,
            "score": score,
            "skills": resume_data['skills'],
            "ats_result": ats_result,
            "recommendations": recs,
            "text": resume_text
        })
        
    # Final Ranking
    print("\n==================================================")
    print("                 FINAL ATS RANKING                ")
    print("==================================================")

    # Sort results highest score first
    results.sort(key=lambda x: x['score'], reverse=True)

    for rank, res in enumerate(results, 1):
        print(f"#{rank} | {res['filename']} | Score: {res['score']} / 100")

    # ── Detailed Per-Candidate Report ──────────────────────────────────────
    print("\n")
    print("==================================================")
    print("          DETAILED CANDIDATE REPORTS              ")
    print("==================================================")

    for rank, res in enumerate(results, 1):
        recs  = res['recommendations']
        breakdown = res['ats_result']['breakdown']

        print(f"\n{'='*52}")
        print(f"  RANK #{rank}  |  {res['filename']}")
        print(f"{'='*52}")

        # ── Score Breakdown ──
        print(f"\n  FINAL ATS SCORE : {res['score']} / 100")
        print(f"  {'-'*40}")
        print(f"  Semantic Similarity Score : {breakdown['semantic_score']:>6.2f} / 100  (weight 50%)")
        print(f"  Keyword Match Score       : {breakdown['keyword_score']:>6.2f} / 100  (weight 40%)")
        print(f"  Structure / Length Score  : {breakdown['structure_score']:>6.2f} / 100  (weight 10%)")

        # ── Skills Found ──
        print(f"\n  SKILLS DETECTED ({len(res['skills'])}) :")
        if res['skills']:
            skill_line = ", ".join(sorted(res['skills']))
            print(f"  {skill_line}")
        else:
            print("  None detected.")

        # ── Missing Keywords ──
        print(f"\n  MISSING KEYWORDS ({len(recs['missing_keywords'])}) :")
        if recs['missing_keywords']:
            for kw in sorted(recs['missing_keywords']):
                print(f"    [x]  {kw}")
        else:
            print("    None - full keyword coverage!")

        # ── Bonus Keywords ──
        print(f"\n  BONUS KEYWORDS ({len(recs['bonus_keywords'])}) :")
        if recs['bonus_keywords']:
            for kw in sorted(recs['bonus_keywords']):
                print(f"    [+]  {kw}")
        else:
            print("    None.")

        # ── Actionable Recommendations ──
        print(f"\n  RECOMMENDATIONS :")
        for i, tip in enumerate(recs['actionable_feedback'], 1):
            print(f"    {i}. {tip}")

        print()

    print("==================================================")
    print("  Run complete.")
    print("==================================================")

if __name__ == "__main__":
    os.makedirs("resumes", exist_ok=True)
    os.makedirs("datasets", exist_ok=True)
    main()
