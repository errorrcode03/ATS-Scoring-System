"""
# 4. Similarity Engine
Purpose: To mathematically compare the resume's vector embedding against the job description's vector embedding.
ML/NLP Concepts:
- Cosine Similarity: A metric used to measure how similar two vectors are, irrespective of their size. It calculates the cosine of the angle between two vectors projected in a multi-dimensional space.
Architecture: A utility class that relies on scikit-learn's optimized mathematical operations.
Optimization: scikit-learn uses highly optimized C and Fortran BLAS/LAPACK libraries under the hood for matrix operations, ensuring similarity calculations are virtually instantaneous even for thousands of resumes.
"""

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SimilarityEngine:
    def __init__(self):
        pass

    def calculate_similarity(self, resume_embedding: np.ndarray, jd_embedding: np.ndarray) -> float:
        """
        Calculates the cosine similarity between two 1D or 2D arrays.
        Line-by-line explanation:
        1. Ensure vectors are 2D arrays (1, N) as required by sklearn using reshape.
        2. Calculate cosine similarity.
        3. Extract the single float value from the resulting matrix.
        4. Bound the result between 0.0 and 1.0 (sometimes float inaccuracies cause 1.000001).
        """
        # Reshape to (1, -1) if the input is a 1D array
        if len(resume_embedding.shape) == 1:
            resume_embedding = resume_embedding.reshape(1, -1)
        if len(jd_embedding.shape) == 1:
            jd_embedding = jd_embedding.reshape(1, -1)
            
        # Calculate similarity (returns a matrix)
        similarity_matrix = cosine_similarity(resume_embedding, jd_embedding)
        
        # Extract scalar value
        score = float(similarity_matrix[0][0])
        
        # Return percentage-based scalar between 0 and 1
        return max(0.0, min(score, 1.0))

if __name__ == "__main__":
    engine = SimilarityEngine()
    # Dummy test vectors
    vec1 = np.array([0.5, 0.5])
    vec2 = np.array([0.5, 0.5])
    print(f"Similarity Score: {engine.calculate_similarity(vec1, vec2) * 100}%")
