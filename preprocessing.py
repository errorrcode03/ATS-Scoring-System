
import re
import spacy

class NLPPreprocessor:
    def __init__(self):

        try:
            self.nlp = spacy.load("en_core_web_sm", disable=["parser"])
        except OSError:
            raise OSError("spaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
            
        # A hardcoded base list of skills for rule-based extraction (can be expanded into a database/file)
        self.skill_db = {
            "python", "java", "c++", "machine learning", "nlp", "deep learning", 
            "tensorflow", "pytorch", "scikit-learn", "sql", "aws", "docker", 
            "kubernetes", "git", "api", "rest", "spacy", "pandas", "numpy", "react", "node.js"
        }

    def clean_text(self, text: str) -> str:
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove special characters except common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,-]', '', text)
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def extract_skills(self, text: str) -> list:
        doc = self.nlp(text.lower())
        extracted_skills = set()
        
        # Unigrams (e.g., "python", "sql")
        for token in doc:
            if token.text in self.skill_db:
                extracted_skills.add(token.text)
                
        # N-grams / multi-word expressions (e.g., "machine learning")
        # A simple sliding window approach for bigrams
        tokens = [token.text for token in doc]
        for i in range(len(tokens) - 1):
            bigram = f"{tokens[i]} {tokens[i+1]}"
            if bigram in self.skill_db:
                extracted_skills.add(bigram)
                
        return list(extracted_skills)

    def preprocess(self, text: str) -> dict:
        """
        End-to-end preprocessing pipeline.
        Returns a dictionary with the cleaned text, lemmas, and extracted skills.
        """
        cleaned_text = self.clean_text(text)
        doc = self.nlp(cleaned_text)
        
        # Lemmatize and remove stop words / punctuation
        lemmas = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        
        # Extract skills
        skills = self.extract_skills(cleaned_text)
        
        return {
            "cleaned_text": cleaned_text,
            "lemmatized_text": " ".join(lemmas),
            "skills": skills
        }

if __name__ == "__main__":
    preprocessor = NLPPreprocessor()
    sample = "I am a Senior Software Engineer with 5 years of experience in Python, Machine Learning, and AWS. Check my github at http://github.com/test."
    print(preprocessor.preprocess(sample))
