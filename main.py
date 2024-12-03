import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq
import time
from dsplot.tree import BinaryTree  # Corrected import for DSPlot's BinaryTree

# Load CSV
file_path = 'data/BooksDataset.csv'
data = pd.read_csv(file_path)

# Preprocess columns
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
    similar_books.loc[:, 'similarity'] = similarity_scores[top_indices]
    similar_books = similar_books[similar_books['similarity'] > 0]
    return similar_books[['Title', 'Authors', 'similarity']]

# Create a max heap from the similar books data
def create_max_heap(similar_books):
    max_heap = []
    for i, row in similar_books.iterrows():
        similarity = row['similarity']
        title = row['Title']
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

# Function to plot heap as a tree using BinaryTree from dsplot
def plot_heap_as_tree(heap):
    # Extract titles for the nodes
    nodes = [title for _, title in heap]
    tree = BinaryTree(nodes=nodes)
    tree.plot()

# Main program
try:
    # Ask the user for the number of top results to return (limit to a maximum of 50)
    top_n = int(input("Enter the number of top results to display (max 50): "))
    if top_n < 1 or top_n > 50:
        raise ValueError("The number of results must be between 1 and 50.")
    
    user_query = input("Enter a book title, author, description, or category to find similar books: ")
    similar_books = find_similar_books(user_query, top_n)
    max_heap = create_max_heap(similar_books)

    # Display sorted heap
    sorted_books = sorted(max_heap, key=lambda x: x[0])
    print("Sorted Top Books:")
    for idx, (similarity, title) in enumerate(sorted_books, 1):  # Start line numbers from 1
        print(f"{idx}: {title} - Similarity Score = {-similarity:.2f}")

    # Validate top of the heap
    if max_heap:
        top_sim = -max_heap[0][0]
        top_title = max_heap[0][1]
        print(f"\nTop of Heap: {top_title} - Similarity Score = {top_sim:.2f}")

    # Interactive Tree Plot
    plot_heap_as_tree(max_heap)

    # Allow user to search for a node
    try:
        search_line_number = int(input("Enter the line number of the book to search in the graph (1 to n): ")) - 1
        if 0 <= search_line_number < len(max_heap):
            target_node = sorted_books[search_line_number][1]  # Use line number from sorted list

            # Placeholder functions for BFS and DFS
            bfs_time, bfs_result = bfs_search(max_heap, target_node)
            dfs_time, dfs_result = dfs_search(max_heap, target_node)

            print(f"Target Node: {target_node}")
            print(f"BFS found the node in {bfs_time:.6f} seconds.")
            print(f"DFS found the node in {dfs_time:.6f} seconds.")
        else:
            print("Invalid line number.")
    except ValueError:
        print("Please enter a valid number.")

except ValueError as e:
    print(f"Error: {e}")

