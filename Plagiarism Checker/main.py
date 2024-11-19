import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Function to preprocess the text
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Tokenize using spaCy and remove stopwords, punctuation, and non-alphabetic tokens
    doc = nlp(text)
    processed_text = " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.is_alpha])
    
    return processed_text

# Function to compute cosine similarity between two texts
def compute_cosine_similarity(text1, text2):
    # Preprocess both documents
    text1_processed = preprocess_text(text1)
    text2_processed = preprocess_text(text2)

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the documents
    tfidf_matrix = vectorizer.fit_transform([text1_processed, text2_processed])

    # Compute cosine similarity between the documents
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    # Return the similarity score (between 0 and 1)
    return similarity_matrix[0][0]

# Sample text documents
doc1 = """Plagiarism is the act of using someone else's work or ideas without proper acknowledgment. 
It is considered unethical and can have serious consequences in academia and beyond."""

doc2 = """Plagiarism is when an individual uses another person's ideas or written work without giving credit. 
This is viewed as dishonest and may result in severe penalties in educational and professional settings."""

# Compute and print the similarity score
similarity_score = compute_cosine_similarity(doc1, doc2)
print(f"Cosine Similarity Score: {similarity_score:.4f}")

# Interpretation of the result
if similarity_score > 0.8:
    print("The documents are highly similar. Potential plagiarism detected!")
elif similarity_score > 0.5:
    print("The documents show moderate similarity.")
else:
    print("The documents are not similar.")
