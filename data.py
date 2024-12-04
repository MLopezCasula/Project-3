import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Loading CSV file
file_path = 'data/BooksDataset.csv'
data = pd.read_csv(file_path)


# Clean and consolidate categories 
def clean_category(category):
    if pd.isna(category):
        return 'Uncategorized'

    # Split categories on comma and get the main category
    main_category = category.split(',')[0].strip()

    # Dictionary of category mappings
    category_mapping = {
        'Antiques & Collectibles': 'Antiques & Collectibles',
        'Architecture': 'Architecture & Design',
        'Design': 'Architecture & Design',
        'Art': 'Art',
        'Biography': 'Biography & Autobiography',
        'Autobiography': 'Biography & Autobiography',
        'Business': 'Business & Economics',
        'Economics': 'Business & Economics',
        'Computers': 'Computer & Technology',
        'Technology': 'Computer & Technology',
        'Cooking': 'Cooking & Food',
        'Food': 'Cooking & Food',
        'Crafts': 'Crafts & Hobbies',
        'Hobbies': 'Crafts & Hobbies',
        'Education': 'Education',
        'Fiction': 'Fiction',
        'Health': 'Health & Fitness',
        'Fitness': 'Health & Fitness',
        'History': 'History',
        'House': 'Home & Garden',
        'Garden': 'Home & Garden',
        'Humor': 'Humor',
        'Law': 'Law',
        'Literary': 'Literature',
        'Mathematics': 'Mathematics',
        'Medical': 'Medical',
        'Music': 'Music',
        'Nature': 'Nature & Environment',
        'Philosophy': 'Philosophy',
        'Photography': 'Photography',
        'Poetry': 'Poetry',
        'Psychology': 'Psychology',
        'Reference': 'Reference',
        'Religion': 'Religion & Spirituality',
        'Science': 'Science',
        'Social Science': 'Social Sciences',
        'Sports': 'Sports & Recreation',
        'Recreation': 'Sports & Recreation',
        'Transportation': 'Transportation',
        'Travel': 'Travel'
    }

    # Look for matching category in our mapping
    for key in category_mapping:
        if key.lower() in main_category.lower():
            return category_mapping[key]

    return 'Other'


# Apply cleaning to the dataset
data['Category'] = data['Category'].apply(clean_category)

# Creates the columns for similarity calculation
data['text'] = data[['Title', 'Authors', 'Description', 'Category']].fillna('').agg(' '.join, axis=1)

# Compute TF-IDF matrix
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(data['text'])


def get_categories():
    return sorted(data['Category'].unique().tolist())


def find_similar_books(query, top_n=10, min_similarity=0.3, category_filter=None, author_filter=None):
    query_vector = tfidf_vectorizer.transform([query])
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Create DataFrame with similarities
    results = data.copy()
    results['similarity'] = similarity_scores

    # Apply filters
    if category_filter:
        results = results[results['Category'] == category_filter]

    if author_filter:
        results = results[results['Authors'].str.contains(author_filter, na=False, case=False)]

    # Filter by minimum similarity
    results = results[results['similarity'] >= min_similarity]

    # Sort and get top results
    results = results.sort_values('similarity', ascending=False).head(top_n)

    return results[['Title', 'Authors', 'similarity']]
