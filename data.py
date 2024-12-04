import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Loading CSV file
file_path = 'data/BooksDataset.csv'
data = pd.read_csv(file_path)

#  Creates the columns
data['text'] = data[['Title', 'Authors', 'Description', 'Category']].fillna('').agg(' '.join, axis=1)

# Compute TF-IDF matrix
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(data['text'])

# Function to find similar books
def find_similar_books(query, top_n=10):
    query_vector = tfidf_vectorizer.transform([query])
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    similar_books = data.iloc[top_indices].copy()
    similar_books['similarity'] = similarity_scores[top_indices]
    return similar_books[similar_books['similarity'] > 0][['Title', 'Authors', 'similarity']]