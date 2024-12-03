import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq
import tkinter as tk
from tkinter import ttk

# Load the CSV file
file_path = 'data/BooksDataset_copy.csv'
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
    similar_books['similarity'] = similarity_scores[top_indices]
    return similar_books[similar_books['similarity'] > 0][['Title', 'Authors', 'similarity']]

# Create a max heap from the similar books data
def create_max_heap(similar_books):
    max_heap = []
    for _, row in similar_books.iterrows():
        heapq.heappush(max_heap, (-row['similarity'], row['Title']))
    return max_heap

# Draw the heap on a tkinter canvas
def draw_heap(canvas, heap, x, y, index=0, offset=200, level=0):
    if index >= len(heap):
        return

    similarity, title = heap[index]
    similarity = -similarity
    node_text = f"{title}\n({similarity:.2f})"

    # Draw the node
    node_id = canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill="lightblue", tags=f"node_{index}")
    text_id = canvas.create_text(x, y, text=node_text, font=("Arial", 10), fill="black", tags=f"text_{index}")

    # Add hover functionality
    def on_enter(event):
        canvas.itemconfig(node_id, fill="yellow")
        canvas.itemconfig(text_id, fill="blue")

    def on_leave(event):
        canvas.itemconfig(node_id, fill="lightblue")
        canvas.itemconfig(text_id, fill="black")

    canvas.tag_bind(f"node_{index}", "<Enter>", on_enter)
    canvas.tag_bind(f"node_{index}", "<Leave>", on_leave)

    left_child_idx = 2 * index + 1
    right_child_idx = 2 * index + 2

    # Draw left child
    if left_child_idx < len(heap):
        child_x = x - offset
        child_y = y + 100
        canvas.create_line(x, y + 30, child_x, child_y - 30)
        draw_heap(canvas, heap, child_x, child_y, left_child_idx, offset // 2, level + 1)

    # Draw right child
    if right_child_idx < len(heap):
        child_x = x + offset
        child_y = y + 100
        canvas.create_line(x, y + 30, child_x, child_y - 30)
        draw_heap(canvas, heap, child_x, child_y, right_child_idx, offset // 2, level + 1)

# Main GUI application
def main():
    def search_books():
        query = query_entry.get()
        top_n = int(top_n_spinbox.get())

        similar_books = find_similar_books(query, top_n)
        max_heap = create_max_heap(similar_books)

        # Clear previous canvas content
        canvas.delete("all")

        # Draw the new heap
        canvas_width = canvas.winfo_width()
        draw_heap(canvas, max_heap, canvas_width // 2, 50)

        # Display similar books in the treeview
        for row in tree.get_children():
            tree.delete(row)

        for similarity, title in max_heap:
            similarity = -similarity
            tree.insert("", "end", values=(title, f"{similarity:.2f}"))

    # Create the main tkinter window
    root = tk.Tk()
    root.title("Book Similarity and Heap Visualization")

    # Query input
    query_label = tk.Label(root, text="Search Query:")
    query_label.pack(pady=5)
    query_entry = tk.Entry(root, width=50)
    query_entry.pack(pady=5)

    # Top N results input
    top_n_label = tk.Label(root, text="Number of Top Results:")
    top_n_label.pack(pady=5)
    top_n_spinbox = tk.Spinbox(root, from_=1, to=50, width=5)
    top_n_spinbox.pack(pady=5)

    # Search button
    search_button = tk.Button(root, text="Search", command=search_books)
    search_button.pack(pady=10)

    # Treeview to display results
    tree = ttk.Treeview(root, columns=("Title", "Similarity"), show="headings")
    tree.heading("Title", text="Title")
    tree.heading("Similarity", text="Similarity")
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Canvas for heap visualization
    canvas = tk.Canvas(root, width=800, height=600, bg="white")
    canvas.pack(pady=10, fill=tk.BOTH, expand=True)

    # Run the tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
