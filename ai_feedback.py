"""
# 7. Optional AI Feedback Layer
Purpose: Uses Large Language Models (LLMs) to provide qualitative, human-like feedback and rewriting suggestions.
Architecture: Integrates with Google's Gemini API (or OpenAI).
Important: You must set your API key as an environment variable: GEMINI_API_KEY.
"""

import os
try:
    import google.generativeai as genai
except ImportError:
    genai = None

class AIFeedbackLayer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client_available = False
        
        if self.api_key and genai:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.client_available = True
        else:
            print("Warning: GEMINI_API_KEY environment variable not set or library missing. AI Feedback disabled.")

    def generate_feedback(self, resume_text: str, jd_text: str) -> str:
        """
        Sends the resume and job description to the LLM to get qualitative feedback.
        """
        if not self.client_available:
            return "AI Feedback is currently disabled. Please configure your API key."
            
        prompt = f"""
        Act as an expert technical recruiter and resume writer. 
        I am going to provide you with a Job Description and a Candidate's Resume.
        
        Job Description:
        {jd_text[:1500]}... # Truncated for token limit safety
        
        Candidate Resume:
        {resume_text[:2000]}...
        
        Please provide a concise 3-paragraph review of the candidate:
        1. A brief summary of their fit for the role.
        2. One major strength highlighted in their resume.
        3. One critical area of improvement or a suggested rewrite for a bullet point to make it more impactful.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while generating AI feedback: {str(e)}"
