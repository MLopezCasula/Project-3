import tkinter as tk
from tkinter import ttk
from data import find_similar_books
from heap import create_max_heap, draw_heap


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
    tree = ttk.Treeview(root, columns=("Title", "Similarity"), show="headings", height=5)
    tree.heading("Title", text="Title")
    tree.heading("Similarity", text="Similarity")
    tree.pack(pady=5, fill=tk.BOTH, expand=True)

    # Canvas for heap visualization
    canvas = tk.Canvas(root, width=1000, height=600, bg="white")
    canvas.pack(pady=10, fill=tk.BOTH, expand=True)

    # Run the tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()