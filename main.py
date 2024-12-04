import tkinter as tk
from tkinter import ttk
from data import find_similar_books, get_categories
from heap import create_max_heap, draw_heap, draw_heap_bfs, draw_heap_dfs


class AdvancedSearchFrame(ttk.LabelFrame):
    def __init__(self, parent, search_callback, bfs_callback, dfs_callback):
        super().__init__(parent, text="Advanced Search", padding="10")
        self.search_callback = search_callback
        self.bfs_callback = bfs_callback
        self.dfs_callback = dfs_callback
        self.create_widgets()

    def create_widgets(self):
        # Create the basic search bar frame
        basic_frame = ttk.Frame(self)
        basic_frame.pack(fill=tk.X, pady=5)

        # Add search query label and entry
        ttk.Label(basic_frame, text="Search Query:").pack(side=tk.LEFT, padx=5)
        self.query_entry = ttk.Entry(basic_frame, width=50)
        self.query_entry.pack(side=tk.LEFT, padx=5)

        # Create frame for all filter options
        filters_frame = ttk.LabelFrame(self, text="Filters", padding="5")
        filters_frame.pack(fill=tk.X, pady=5)

        # Add category dropdown
        ttk.Label(filters_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(filters_frame, textvariable=self.category_var, width=30)
        self.category_combo['values'] = ['All'] + get_categories()
        self.category_combo.current(0)
        self.category_combo.grid(row=0, column=1, padx=5, pady=5)

        # Add author entry field
        ttk.Label(filters_frame, text="Author:").grid(row=0, column=2, padx=5, pady=5)
        self.author_entry = ttk.Entry(filters_frame, width=30)
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)

        # Add similarity threshold spinner
        ttk.Label(filters_frame, text="Min. Similarity:").grid(row=1, column=0, padx=5, pady=5)
        self.similarity_var = tk.StringVar(value="0.3")
        similarity_spin = ttk.Spinbox(filters_frame, from_=0.0, to=1.0, increment=0.1,
                                      textvariable=self.similarity_var, width=5)
        similarity_spin.grid(row=1, column=1, padx=5, pady=5)

        # Add results limit spinner
        ttk.Label(filters_frame, text="Max Results:").grid(row=1, column=2, padx=5, pady=5)
        self.limit_var = tk.StringVar(value="10")
        self.limit_spin = ttk.Spinbox(filters_frame, from_=1, to=31, textvariable=self.limit_var, width=5)
        self.limit_spin.grid(row=1, column=3, padx=5, pady=5)

        # Create frame for buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, pady=5)

        # Add all action buttons
        ttk.Button(button_frame, text="Search", command=self.perform_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_filters).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="BFS Visualization", command=self.bfs_callback).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="DFS Visualization", command=self.dfs_callback).pack(side=tk.LEFT, padx=5)

    # Handles the search button click
    def perform_search(self):
        query = self.query_entry.get()
        if not query:
            return

        # Get all filter values
        author = self.author_entry.get().strip()
        filters = {
            'category': self.category_var.get() if self.category_var.get() != 'All' else None,
            'author': author if author else None,
            'min_similarity': float(self.similarity_var.get()),
            'limit': int(self.limit_var.get())
        }

        self.search_callback(query, filters)

    # Resets all filters to default values
    def clear_filters(self):
        self.query_entry.delete(0, tk.END)
        self.category_combo.current(0)
        self.author_entry.delete(0, tk.END)
        self.similarity_var.set("0.3")
        self.limit_var.set("10")


class BookRecommenderApp:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Book Recommender System")
        self.max_heap = []

        # Configure window appearance
        self.root.configure(bg='#f0f0f0')
        self.root.geometry("1200x800")

        self.create_gui()

    # Creates all GUI elements
    def create_gui(self):
        self.create_search_frame()
        self.create_notebook()
        self.create_status_bar()

    # Creates the search and filter section
    def create_search_frame(self):
        self.advanced_search = AdvancedSearchFrame(
            self.root,
            self.perform_filtered_search,
            self.perform_bfs,
            self.perform_dfs
        )
        self.advanced_search.pack(fill=tk.X, padx=10, pady=5)

    # Creates the notebook with visualization and results tabs
    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create visualization tab
        self.viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text="Heap Visualization")

        # Add canvas with scrollbar for visualization
        canvas_frame = ttk.Frame(self.viz_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="white")
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL,
                                  command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create results tab
        results_frame = ttk.Frame(self.notebook)
        self.notebook.add(results_frame, text="Search Results")

        # Add treeview for results with scrollbar
        self.tree = ttk.Treeview(results_frame, columns=("Title", "Author", "Similarity"),
                                 show="headings", height=10)

        # Configure treeview columns
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Similarity", text="Similarity")

        self.tree.column("Title", width=300)
        self.tree.column("Author", width=200)
        self.tree.column("Similarity", width=100)

        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL,
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click event for Google search
        self.tree.bind("<Double-1>", self.open_google_search)

    # Creates the status bar at bottom of window
    def create_status_bar(self):
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.root, textvariable=self.status_var,
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var.set("Ready")

    # Handles the search functionality
    def perform_filtered_search(self, query, filters):
        try:
            self.status_var.set("Searching...")
            self.root.update()

            # Get search results
            similar_books = find_similar_books(
                query,
                top_n=filters['limit'],
                min_similarity=filters['min_similarity'],
                category_filter=filters['category'],
                author_filter=filters['author']
            )

            self.max_heap = create_max_heap(similar_books)

            # Clear previous results
            self.canvas.delete("all")
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Draw new heap visualization
            canvas_width = self.canvas.winfo_width()
            draw_heap(self.canvas, self.max_heap, canvas_width // 2, 50)

            # Update results table
            for _, row in similar_books.iterrows():
                # Clean up author display
                author = row['Authors']
                author_display = author.replace('By', '') if author else 'Unknown'

                self.tree.insert("", "end", values=(
                    row['Title'],
                    author_display,
                    f"{row['similarity']:.3f}"
                ))

            self.status_var.set(f"Found {len(similar_books)} matching books")

        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

    # Performs BFS visualization
    def perform_bfs(self):
        if not self.max_heap:
            self.status_var.set("No data to visualize. Please perform a search first.")
            return

        self.canvas.delete("all")
        self.status_var.set("Performing BFS traversal...")
        draw_heap_bfs(self.canvas, self.max_heap, self.canvas.winfo_width() // 2, 50)
        self.status_var.set("BFS traversal complete")

    # Performs DFS visualization
    def perform_dfs(self):
        if not self.max_heap:
            self.status_var.set("No data to visualize. Please perform a search first.")
            return

        self.canvas.delete("all")
        self.status_var.set("Performing DFS traversal...")
        draw_heap_dfs(self.canvas, self.max_heap, self.canvas.winfo_width() // 2, 50)
        self.status_var.set("DFS traversal complete")

    # Opens Google search for selected book
    def open_google_search(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            title = self.tree.item(selected_item[0], "values")[0]
            search_url = f"https://www.google.com/search?q={title} book"
            import webbrowser
            webbrowser.open(search_url)

    # Starts the application
    def run(self):
        self.root.mainloop()


# Creates and runs the application
def main():
    app = BookRecommenderApp()
    app.run()


if __name__ == "__main__":
    main()