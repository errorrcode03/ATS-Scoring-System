
class RecommendationEngine:
    def __init__(self):
        pass

    def generate_recommendations(self, resume_skills: list, jd_skills: list) -> dict:
        """
        Identifies missing skills and suggests structural improvements.
        """
        r_set = set(resume_skills)
        j_set = set(jd_skills)
        
        # Skills required by JD but missing from resume
        missing_skills = list(j_set - r_set)
        
        # Skills present in resume but not explicitly asked for (Bonus skills)
        bonus_skills = list(r_set - j_set)
        
        recommendations = []
        
        if missing_skills:
            recommendations.append(
                f"Missing Keywords: Consider adding the following skills to your resume if you possess them: {', '.join(missing_skills)}."
            )
            
        if not missing_skills:
            recommendations.append("Excellent keyword coverage! Your resume hits all the identified skills in the JD.")
            
        recommendations.append("Ensure your work experience explicitly details how you utilized these skills with measurable metrics (e.g., 'improved performance by 15%').")
            
        return {
            "missing_keywords": missing_skills,
            "bonus_keywords": bonus_skills,
            "actionable_feedback": recommendations
        }
