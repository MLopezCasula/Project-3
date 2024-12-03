import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq
import time
import HeapVisualizer
import heapq
import time

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


def print_heap(heap):
    for _, row in heap:
        print(row)

def max_heap_to_ordered_list(max_heap):
    # Convert max heap to ordered list by extracting nodes, sorting by negative similarity
    ordered_list = []

    # Pop elements from the heap while keeping track of the similarity and title
    while max_heap:
        similarity, title = heapq.heappop(max_heap)
        ordered_list.append((title, -similarity))

    return ordered_list

# DFS search
def dfs_search(heap, target):
    stack = heap[:]
    start_time = time.time()
    while stack:
        similarity, title = stack.pop()
        if title == target:
            return time.time() - start_time, title
    return time.time() - start_time, None

def main():
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
    visualizer = HeapVisualizer.MaxHeapVisualizer(max_heap)  # Pass the max heap, not similar_books
    visualizer.run()

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

if __name__ == "__main__":
    main()
