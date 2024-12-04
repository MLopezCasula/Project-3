import tkinter as tk
import webbrowser
from tkinter import ttk
from data import find_similar_books
from heap import create_max_heap, draw_heap, draw_heap_bfs, draw_heap_dfs

# searches up the book when clicked in the table
def open_google_search(tree, event):
    selected_item = tree.selection()
    if selected_item:
        title = tree.item(selected_item, "values")[0]
        # searches for the name + book
        search_url = f"https://www.google.com/search?q={title} book"
        webbrowser.open(search_url)

# Function to create the max heap
def get_max_heap(query, top_n):
    similar_books = find_similar_books(query, top_n)
    return create_max_heap(similar_books)

# Main GUI application
def main():
    max_heap = []

    def search_books():
        nonlocal max_heap
        query = query_entry.get()
        top_n = int(top_n_spinbox.get())

        max_heap = get_max_heap(query, top_n)

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

    # does the dfs traversal heap when the dfs button is clicked
    def perform_dfs():
        if not max_heap:
            tree.insert("", "end", values=("No data to visualize", "N/A"))
            return

        canvas.delete("all")
        draw_heap_dfs(canvas, max_heap, canvas.winfo_width() // 2, 50)

    # does the bfs traversal heap when the bfs button is clicked
    def perform_bfs():
        if not max_heap:
            tree.insert("", "end", values=("No data to visualize", "N/A"))
            return

        canvas.delete("all")
        draw_heap_bfs(canvas, max_heap, canvas.winfo_width() // 2, 50)

    # Create the main tkinter window
    root = tk.Tk()
    root.title("Book Similarity and Heap Visualization")

    # Query input
    query_label = tk.Label(root, text="Search Query:")
    query_label.pack(pady=5)
    query_entry = tk.Entry(root, width=50)
    query_entry.pack(pady=5)

    # Top N results input
    top_n_label = tk.Label(root, text="Number of Top Results (Max 31):")
    top_n_label.pack(pady=5)
    top_n_spinbox = tk.Spinbox(root, from_=1, to=31, width=5)
    top_n_spinbox.pack(pady=5)

    # Buttons frame
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Search button
    search_button = tk.Button(button_frame, text="Search", command=search_books)
    search_button.pack(side=tk.LEFT, padx=5)

    # BFS button
    bfs_button = tk.Button(button_frame, text="BFS", command=perform_bfs)
    bfs_button.pack(side=tk.LEFT, padx=5)

    # DFS button
    dfs_button = tk.Button(button_frame, text="DFS", command=perform_dfs)
    dfs_button.pack(side=tk.LEFT, padx=5)

    # Treeview to display results
    tree = ttk.Treeview(root, columns=("Title", "Similarity"), show="headings", height=5)
    tree.heading("Title", text="Title")
    tree.heading("Similarity", text="Similarity")
    tree.bind("<ButtonRelease-1>", lambda event: open_google_search(tree, event))
    tree.pack(pady=5, fill=tk.BOTH, expand=True)


    # creates the canvas to display the heap
    canvas = tk.Canvas(root, width=1000, height=600, bg="white")
    canvas.pack(pady=10, fill=tk.BOTH, expand=True)

    # Run the tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
