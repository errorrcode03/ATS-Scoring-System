"""
# 3. Deep Learning Embedding Module
Purpose: To convert the text of resumes and job descriptions into high-dimensional vector representations.
ML/NLP Concepts:
- Dense Embeddings: Mapping sentences to vectors of real numbers where semantically similar sentences are close in the vector space.
- Transformer Models: Uses self-attention mechanisms to understand the context of words in sentences.

Architecture: A wrapper around `sentence-transformers`.
Optimization: We use `all-MiniLM-L6-v2`. It is incredibly fast, memory-efficient (very small footprint), and offers high quality sentence embeddings compared to larger models like BERT-base, making it perfect for desktop/CLI execution without heavy GPU reliance.
"""

from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingEngine:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the sentence transformer model.
        The first time this runs, it will download the model weights (approx 80MB).
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generates a vector embedding for a given string of text.
        Line-by-line:
        1. model.encode() converts the text into a numpy array (vector).
        2. We return this array for downstream mathematical comparison.
        """
        # If the text is empty, return a zero vector of the model's hidden size (384 for MiniLM)
        if not text.strip():
            return np.zeros(self.model.get_sentence_embedding_dimension())
            
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
        
    def generate_batch_embeddings(self, texts: list[str]) -> np.ndarray:
        """
        Generates embeddings for a list of texts simultaneously.
        Optimization: Batching utilizes matrix multiplication optimizations, which is much faster than a for-loop.
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings

if __name__ == "__main__":
    engine = EmbeddingEngine()
    emb = engine.generate_embedding("Senior Python Developer with ML experience.")
    print(f"Generated embedding of shape: {emb.shape}")
