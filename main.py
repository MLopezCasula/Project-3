import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq  
import time  
import igraph as ig
from plotly.graph_objs import Figure

# Load CSV
file_path = 'data/BooksDataset_copy.csv'  
data = pd.read_csv(file_path)

# Preprocess columns
data['text'] = data[['Title', 'Authors', 'Description', 'Category']].fillna('').agg(' '.join, axis=1)

# Compute TF-IDF matrix
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(data['text'])

# Function to find similar books
def find_similar_books(query, top_n=30):
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
        similarity = row['similarity']
        title = row['Title']
        # Store negative similarity to create a max heap with heapq (min heap by default)
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

def plot_heap_as_tree(heap):
    # Extract similarity scores and titles
    similarities = [-similarity for similarity, _ in heap]
    titles = [title for _, title in heap]
    
    # Convert heap to a true max-heap graph representation
    g = ig.Graph()
    g.add_vertices(len(heap))
    edges = []
    for i in range(len(heap)):
        left_child = 2 * i + 1
        right_child = 2 * i + 2
        if left_child < len(heap):
            edges.append((i, left_child))
        if right_child < len(heap):
            edges.append((i, right_child))
    g.add_edges(edges)
    
    # Create a layout that respects the heap property
    layout = g.layout("rt")  # Reingold-Tilford layout
    x_coords = [layout[k][0] for k in range(len(heap))]
    y_coords = [-layout[k][1] for k in range(len(heap))]  # Flip y-coordinates for top-down visualization
    edge_x = []
    edge_y = []
    for edge in g.get_edgelist():
        edge_x += [x_coords[edge[0]], x_coords[edge[1]], None]
        edge_y += [y_coords[edge[0]], y_coords[edge[1]], None]
    
    fig = Figure()
    # Add edges
    fig.add_trace(dict(
        type='scatter',
        x=edge_x,
        y=edge_y,
        mode='lines',
        line=dict(width=2, color='gray'),
        hoverinfo='none'
    ))
    # Add nodes
    fig.add_trace(dict(
        type='scatter',
        x=x_coords,
        y=y_coords,
        mode='markers+text',
        marker=dict(size=20, color='skyblue'),
        text=[f"{sim:.2f}" for sim in similarities],  # Show similarity scores as text
        textposition='top center',
        hovertext=titles,  # Show book titles on hover
        hoverinfo='text'
    ))
    fig.update_layout(
        title="Heap Tree Visualization (Enforced Max-Heap Property)",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )
    fig.show()

# Get user input
user_query = input("Enter a book title, author, description, or category to find similar books: ")

# Find similar books
similar_books = find_similar_books(user_query)

# Create max heap
max_heap = create_max_heap(similar_books)

# Display sorted heap
sorted_books = sorted(max_heap, key=lambda x: x[0])
print("Sorted Top Books:")
for similarity, title in sorted_books:
    print(f"{title} - Similarity Score = {-similarity:.2f}")

# Validate top of the heap
if max_heap:
    top_sim = -max_heap[0][0]
    top_title = max_heap[0][1]
    print(f"\nTop of Heap: {top_title} - Similarity Score = {top_sim:.2f}")

# Interactive Tree Plot
plot_heap_as_tree(max_heap)

# Allow user to search for a node
try:
    search_line_number = int(input("Enter the line number of the book to search in the graph: ")) - 1
    if 0 <= search_line_number < len(max_heap):
        target_node = max_heap[search_line_number][1]

        # Perform BFS and DFS
        bfs_time, bfs_result = bfs_search(max_heap, target_node)
        dfs_time, dfs_result = dfs_search(max_heap, target_node)

        # Display results
        print(f"Target Node: {target_node}")
        print(f"BFS found the node in {bfs_time:.6f} seconds.")
        print(f"DFS found the node in {dfs_time:.6f} seconds.")
    else:
        print("Invalid line number.")
except ValueError:
    print("Please enter a valid number.")
