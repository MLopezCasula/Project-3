import tkinter as tk
from tkinter import Toplevel
import heapq
import time

# This handles hover interactions
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    # used to show the node info like the title and similarity value when hovering over
    def showtip(self, text, x, y):
        self.text = text
        if self.tip_window or not self.text:
            return

        x = x + self.widget.winfo_rootx() + 10
        y = y + self.widget.winfo_rooty() + 10

        self.tip_window = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
    # hides the node info when not hovering over it
    def hidetip(self):
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None

# Used to make the hover feature and the buttons
def CreateToolTip(widget, node, text, x, y):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text, x, y)
    def leave(event):
        toolTip.hidetip()

    widget.tag_bind(node, '<Enter>', enter)
    widget.tag_bind(node, '<Leave>', leave)

# Creates a max heap from the similar books data
def create_max_heap(similar_books):
    max_heap = []
    for _, row in similar_books.iterrows():
        heapq.heappush(max_heap, (-row['similarity'], row['Title']))
    return max_heap

# draws the heap from the search button
def draw_heap(canvas_widget, heap, x, y, index=0, level=0, max_levels=5, node_size=20, color="orange"):
    if index >= len(heap) or level >= max_levels:
        return

    similarity, title = heap[index]
    similarity = -similarity
    node_text = f"{title}\n({similarity:.2f})"

    # This Calculates spacing
    total_width = (2 ** max_levels) * node_size
    horizontal_spacing = total_width / (2 ** (level + 1))

    # Draw the node
    canvas_widget.create_oval(
        x - node_size, y - node_size, x + node_size, y + node_size,
        fill=color, outline="black", tags=f"node_{index}"
    )

    # Creates the tooltip for the node
    CreateToolTip(canvas_widget, f"node_{index}", node_text, x, y)

    # Creates a button for the bfs/dfs search feature and places the button with the index below the node
    node_button = tk.Button(canvas_widget, text=f"Node {index}", command=lambda idx=index: node_button_click(canvas_widget, index, heap))
    canvas_widget.create_window(x, y + node_size + 10, window=node_button)

    # Draw child nodes
    vertical_spacing = 80
    left_child_index = 2 * index + 1
    right_child_index = 2 * index + 2

    # Left child
    if left_child_index < len(heap):
        child_x = x - horizontal_spacing
        child_y = y + vertical_spacing
        canvas_widget.create_line(x, y + node_size, child_x, child_y - node_size, width=2, fill="black")
        draw_heap(canvas_widget, heap, child_x, child_y, left_child_index, level + 1, max_levels, node_size, color)

    # Right child
    if right_child_index < len(heap):
        child_x = x + horizontal_spacing
        child_y = y + vertical_spacing
        canvas_widget.create_line(x, y + node_size, child_x, child_y - node_size, width=2, fill="black")
        draw_heap(canvas_widget, heap, child_x, child_y, right_child_index, level + 1, max_levels, node_size, color)

# Button clicked feature
def node_button_click(canvas, index, heap):
    similarity, title = heap[index]
    #print(f"Node {index} clicked!")

    # receives the number of traversed nodes
    BFS_number_of_visited_nodes = bfs_search(heap, title)
    DFS_number_of_visited_nodes = dfs_search(heap, title)

    #print(f"BFS nodes visited: {BFS_number_of_visited_nodes}")
    #print(f"DFS nodes visited: {DFS_visited}")

    canvas.delete("text")
    canvas_width = canvas.winfo_width()

    # Creates space between the edge of the canvas and the shown text
    space_x = 20
    space_y = 15
    x_position = canvas_width - space_x
    y_position_bfs = space_y
    y_position_dfs = space_y + 20

    # set tag to text to delete and anchor to 'e' to move it all the way to the right
    canvas.create_text(x_position, y_position_bfs,
                        text=f"BFS nodes visited: {BFS_number_of_visited_nodes}",
                        font = ("Helvetica", 12),
                        fill="red",
                        anchor="e",
                        tags="text")
    canvas.create_text(x_position, y_position_dfs,
                        text=f"DFS nodes visited: {DFS_number_of_visited_nodes}",
                        font=("Helvetica", 12),
                        fill="yellow",
                        anchor="e",
                        tags="text")

# BFS search
def bfs_search(heap, target):
    queue = heap[:]
    visited_count = 0
    while queue:
        similarity, title = queue.pop(0)
        visited_count += 1
        if title == target:
            return visited_count
    return visited_count

# DFS search
def dfs_search(heap, target):
    visited_count = 0
    stack = [(0, 0)]
    visited_indices = set()

    # Stack for DFS
    while stack:
        index, level = stack.pop()
        if index >= len(heap):
            continue

        if index not in visited_indices:
            visited_indices.add(index)
            visited_count += 1

            similarity, title = heap[index]
            if title == target:
                return visited_count

            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

            # Was going the wrong way so I just switched it
            if right_child_index < len(heap):
                stack.append((right_child_index, level + 1))
            if left_child_index < len(heap):
                stack.append((left_child_index, level + 1))

    return visited_count

# draws the heap in bfs traversal order
def draw_heap_bfs(canvas_widget, heap, x, y, delay=500, max_levels=5, node_size=20):
    queue = [(x, y, 0, 0)]
    node_spacing = (2 ** max_levels) * node_size

    while queue:
        node_x, node_y, index, level = queue.pop(0)
        if index >= len(heap) or level >= max_levels:
            continue

        similarity, title = heap[index]
        similarity = -similarity
        node_text = f"{title}\n({similarity:.2f})"

        # Draw the node
        canvas_widget.create_oval(
            node_x - node_size, node_y - node_size, node_x + node_size, node_y + node_size,
            fill="red", outline="black", tags=f"node_{index}"
        )

        # Calculates child positions
        horizontal_spacing = node_spacing / (2 ** (level + 1))
        vertical_spacing = 80
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2

        # Left child
        if left_child_index < len(heap):
            child_x = node_x - horizontal_spacing
            child_y = node_y + vertical_spacing
            queue.append((child_x, child_y, left_child_index, level + 1))
            canvas_widget.create_line(node_x, node_y + node_size, child_x, child_y - node_size, width=2)

        # Right child
        if right_child_index < len(heap):
            child_x = node_x + horizontal_spacing
            child_y = node_y + vertical_spacing
            queue.append((child_x, child_y, right_child_index, level + 1))
            canvas_widget.create_line(node_x, node_y + node_size, child_x, child_y - node_size, width=2)

        canvas_widget.update()
        time.sleep(delay / 1000)

#draws the heap in dfs traversal order
def draw_heap_dfs(canvas_widget, heap, x, y, delay=500, index=0, level=0, max_levels=5, node_size=20):
    if index >= len(heap) or level >= max_levels:
        return

    similarity, title = heap[index]
    similarity = -similarity
    node_text = f"{title}\n({similarity:.2f})"

    # Draw the current node
    canvas_widget.create_oval(
        x - node_size, y - node_size, x + node_size, y + node_size,
        fill="yellow", outline="black", tags=f"node_{index}"
    )
    canvas_widget.update()
    time.sleep(delay / 1000)

    # Calculate child positions
    node_spacing = (2 ** max_levels) * node_size
    horizontal_spacing = node_spacing / (2 ** (level + 1))
    vertical_spacing = 80
    left_child_index = 2 * index + 1
    right_child_index = 2 * index + 2

    # Traverse left
    if left_child_index < len(heap):
        child_x = x - horizontal_spacing
        child_y = y + vertical_spacing
        canvas_widget.create_line(x, y + node_size, child_x, child_y - node_size, width=2)
        draw_heap_dfs(canvas_widget, heap, child_x, child_y, delay, left_child_index, level + 1, max_levels, node_size)

    # Traverse right
    if right_child_index < len(heap):
        child_x = x + horizontal_spacing
        child_y = y + vertical_spacing
        canvas_widget.create_line(x, y + node_size, child_x, child_y - node_size, width=2)
        draw_heap_dfs(canvas_widget, heap, child_x, child_y, delay, right_child_index, level + 1, max_levels, node_size)
