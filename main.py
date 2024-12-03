import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load CSV
file_path = 'data/BooksDataset_copy.csv'  
data = pd.read_csv(file_path)

# Preprocess columns
data['text'] = data[['Title', 'Authors', 'Description', 'Category']].fillna('').agg(' '.join, axis=1)

# Compute TF-IDF matrix
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(data['text'])

# Function to find similar books
def find_similar_books(query, top_n=25):
    # Transform the query using the fitted TF-IDF vectorizer
    query_vector = tfidf_vectorizer.transform([query])
    
    # Compute cosine similarity between the query and all books
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    # Get the indices of the top_n most similar books
    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    
    # Get the top_n books and their similarity scores
    similar_books = data.iloc[top_indices]
    similar_books['similarity'] = similarity_scores[top_indices]
    return similar_books[['Title', 'Authors', 'similarity']]

# Create graph data structure
def create_graph(similar_books):
    graph = {}
    for _, row in similar_books.iterrows():
        title = row['Title']
        similarity = row['similarity']
        graph[title] = {'similarity': similarity}
    return graph

# Get user input
user_query = input("Enter a book title, author, description, or category to find similar books: ")

# Find similar books
similar_books = find_similar_books(user_query)

# Create graph
graph = create_graph(similar_books)

# Display graph
def display_graph(graph):
    print("Graph Representation (Adjacency List):")
    for node, edges in graph.items():
        print(f"{node}: {edges}")

# Display similar books and graph
print("Top similar books:")
print(similar_books)

# Visualize the graph
import networkx as nx

G = nx.Graph()

# Add nodes and edges from graph data structure
for title, properties in graph.items():
    G.add_node(title)
    G.add_edge("Query", title, weight=properties['similarity'])

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', font_size=10, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)})
plt.title("Graph Representation of Similar Books")
plt.show()

# Display the graph adjacency list
display_graph(graph)

print("Hello")
print("Project 3")

print("")
