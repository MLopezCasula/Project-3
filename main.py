import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq
import networkx as nx
import time  

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
    query_vector = tfidf_vectorizer.transform([query])
    
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    
    similar_books = data.iloc[top_indices]
    similar_books['similarity'] = similarity_scores[top_indices]
    
    similar_books = similar_books[similar_books['similarity'] > 0]
    
    return similar_books[['Title', 'Authors', 'similarity']]

# Create a max heap from the similar books data
def create_max_heap(similar_books):
    max_heap = []
    for _, row in similar_books.iterrows():
        title = row['Title']
        similarity = row['similarity']
        heapq.heappush(max_heap, (-similarity, title))
    return max_heap

# BFS search
def bfs_search(heap, target):
    queue = heap[:]
    start_time = time.time()
    while queue:
        similarity, title = queue.pop(0)
        if title == target:
            return time.time() - start_time, title
    return time.time() - start_time, None

# DFS search
def dfs_search(heap, target):
    stack = heap[:]
    start_time = time.time()
    while stack:
        similarity, title = stack.pop()
        if title == target:
            return time.time() - start_time, title
    return time.time() - start_time, None

# Get user input
user_query = input("Enter a book title, author, description, or category to find similar books: ")

# Find similar books
similar_books = find_similar_books(user_query)

# Create max heap
max_heap = create_max_heap(similar_books)

# Visualize the graph
G = nx.Graph()

# Add nodes and edges from the max heap (before popping)
for similarity, title in max_heap:
    G.add_node(title)
    G.add_edge("Query", title, weight=-similarity)

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', font_size=10, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)})
plt.title("Graph Representation of Similar Books")
plt.show()

# Display the max heap
print("Top similar books (ordered by similarity):")
for i, (similarity, title) in enumerate(max_heap):
    print(f"{i + 1}: {title} - Similarity Score = {-similarity:.2f}")

# Allow user to search for a node
try:
    search_line_number = int(input("Enter the line number of the book to search in the graph: ")) - 1
    if 0 <= search_line_number < len(max_heap):
        target_node = max_heap[search_line_number][1]

        bfs_time, bfs_result = bfs_search(max_heap, target_node)
        dfs_time, dfs_result = dfs_search(max_heap, target_node)

        print(f"Target Node: {target_node}")
        print(f"BFS found the node in {bfs_time:.6f} seconds.")
        print(f"DFS found the node in {dfs_time:.6f} seconds.")
    else:
        print("Invalid line number.")
except ValueError:
    print("Please enter a valid number.")
