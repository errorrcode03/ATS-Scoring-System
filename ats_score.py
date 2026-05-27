"""
# 5. ATS Score Engine
Purpose: To generate a final, human-readable Applicant Tracking System (ATS) score based on multiple signals.
ML/NLP Concepts:
- Weighted Ensemble Scoring: Combining different heuristic and ML-driven signals (semantics, exact keywords, structural length) into a single unified metric.
Architecture: Evaluates various dimensions of the resume vs JD and applies predefined weights.
Optimization: Computing the exact keyword overlap using python `sets` provides O(1) lookup time, drastically outperforming nested loops.
"""

class ATSScoreEngine:
    def __init__(self):
        # Define the weight distribution for the final score
        self.weights = {
            "semantic_similarity": 0.50, # 50% importance on overall meaning
            "keyword_matching": 0.40,    # 40% importance on exact skill matches
            "structure_length": 0.10     # 10% importance on resume density/structure
        }

    def generate_score(self, similarity_score: float, resume_skills: list, jd_skills: list, resume_text: str) -> dict:
        """
        Calculates the aggregate ATS score.
        """
        # 1. Semantic Score (0 to 100)
        semantic_points = similarity_score * 100
        
        # 2. Keyword Matching Score (0 to 100)
        # Calculate Jaccard-like overlap: (Intersection / JD Skills) * 100
        jd_skills_set = set(jd_skills)
        resume_skills_set = set(resume_skills)
        
        if not jd_skills_set:
            keyword_points = 100.0 # If JD has no extracted skills, default to perfect
        else:
            matched_skills = jd_skills_set.intersection(resume_skills_set)
            keyword_points = (len(matched_skills) / len(jd_skills_set)) * 100

        # 3. Structure / Length Score (Heuristic based on character count)
        # Ideal resume length depends on experience, but let's assume 1500 to 4000 characters is a sweet spot
        char_count = len(resume_text)
        if 1500 <= char_count <= 4500:
            structure_points = 100.0
        elif char_count < 1500:
            structure_points = max(0, (char_count / 1500) * 100)
        else:
            structure_points = max(0, 100 - ((char_count - 4500) / 100)) # Penalty for being too long

        # Final Weighted Calculation
        final_score = (
            (semantic_points * self.weights["semantic_similarity"]) +
            (keyword_points * self.weights["keyword_matching"]) +
            (structure_points * self.weights["structure_length"])
        )

        return {
            "final_score": round(final_score, 2),
            "breakdown": {
                "semantic_score": round(semantic_points, 2),
                "keyword_score": round(keyword_points, 2),
                "structure_score": round(structure_points, 2)
            }
        }
