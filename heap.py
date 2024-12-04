
import tkinter as tk
from tkinter import Toplevel
import heapq
import time

# This handles hover interactions
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None

    def showtip(self, text, x, y):
        self.text = text
        if self.tipwindow or not self.text:
            return

        x = x + self.widget.winfo_rootx() + 10
        y = y + self.widget.winfo_rooty() + 10

        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
        self.tipwindow = None

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

def draw_heap(canvas, heap, x, y, index=0, level=0, max_levels=5, node_size=20, color="orange"):
    if index >= len(heap) or level >= max_levels:
        return

    similarity, title = heap[index]
    similarity = -similarity
    node_text = f"{title}\n({similarity:.2f})"

    # This Calculates spacing
    total_width = (2 ** max_levels) * node_size
    horizontal_spacing = total_width / (2 ** (level + 1))

    # Draw the node
    canvas.create_oval(
        x - node_size, y - node_size, x + node_size, y + node_size,
        fill=color, outline="black", tags=f"node_{index}"
    )

    # Create the tooltip for the node
    CreateToolTip(canvas, f"node_{index}", node_text, x, y)

    # Draw child nodes
    vertical_spacing = 80
    left_child_index = 2 * index + 1
    right_child_index = 2 * index + 2

    # Left child
    if left_child_index < len(heap):
        child_x = x - horizontal_spacing
        child_y = y + vertical_spacing
        canvas.create_line(x, y + node_size, child_x, child_y - node_size, width=2, fill="black")
        draw_heap(canvas, heap, child_x, child_y, left_child_index, level + 1, max_levels, node_size, color)

    # Right child
    if right_child_index < len(heap):
        child_x = x + horizontal_spacing
        child_y = y + vertical_spacing
        canvas.create_line(x, y + node_size, child_x, child_y - node_size, width=2, fill="black")
        draw_heap(canvas, heap, child_x, child_y, right_child_index, level + 1, max_levels, node_size, color)

def draw_heap_bfs(canvas, heap, x, y, delay=500, max_levels=5, node_size=20):
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
        canvas.create_oval(
            node_x - node_size, node_y - node_size, node_x + node_size, node_y + node_size,
            fill="red", outline="black", tags=f"node_{index}"
        )

        # Calculate child positions
        horizontal_spacing = node_spacing / (2 ** (level + 1))
        vertical_spacing = 80
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2

        # Left child
        if left_child_index < len(heap):
            child_x = node_x - horizontal_spacing
            child_y = node_y + vertical_spacing
            queue.append((child_x, child_y, left_child_index, level + 1))
            canvas.create_line(node_x, node_y + node_size, child_x, child_y - node_size, width=2)

        # Right child
        if right_child_index < len(heap):
            child_x = node_x + horizontal_spacing
            child_y = node_y + vertical_spacing
            queue.append((child_x, child_y, right_child_index, level + 1))
            canvas.create_line(node_x, node_y + node_size, child_x, child_y - node_size, width=2)

        canvas.update()
        time.sleep(delay / 1000)

def draw_heap_dfs(canvas, heap, x, y, delay=500, index=0, level=0, max_levels=5, node_size=20):
    if index >= len(heap) or level >= max_levels:
        return

    similarity, title = heap[index]
    similarity = -similarity
    node_text = f"{title}\n({similarity:.2f})"

    # Draw the current node
    canvas.create_oval(
        x - node_size, y - node_size, x + node_size, y + node_size,
        fill="yellow", outline="black", tags=f"node_{index}"
    )
    canvas.update()
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
        canvas.create_line(x, y + node_size, child_x, child_y - node_size, width=2)
        draw_heap_dfs(canvas, heap, child_x, child_y, delay, left_child_index, level + 1, max_levels, node_size)

    # Traverse right 
    if right_child_index < len(heap):
        child_x = x + horizontal_spacing
        child_y = y + vertical_spacing
        canvas.create_line(x, y + node_size, child_x, child_y - node_size, width=2)
        draw_heap_dfs(canvas, heap, child_x, child_y, delay, right_child_index, level + 1, max_levels, node_size)
