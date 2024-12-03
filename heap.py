import tkinter as tk
from tkinter import Toplevel
import heapq

# Handles hover interactions
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None

    def showtip(self, text, x, y):
        self.text = text
        if self.tipwindow or not self.text:
            return

        # Adjusts the position of the tooltip based on the canvas coordinates
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

# Draw the heap on a tkinter canvas
def draw_heap(canvas, heap, x, y, index=0, offset=250, level=0, node_size=30, color="lightblue"):
    if index >= len(heap):
        return

    similarity, title = heap[index]
    similarity = -similarity
    node_text = f"{title}\n({similarity:.2f})"

    # Draw the node
    node_group = canvas.create_oval(x - node_size, y - node_size, x + node_size, y + node_size,
                                    fill=color, outline="black", tags=f"node_{index}")

    # Create the tooltip for the node
    CreateToolTip(canvas, f"node_{index}", node_text, x, y)

    vertical_offset = 60

    new_offset = max(offset * 0.5 ** level, 60)
    new_node_size = max(20, node_size - 3)

    # Draw child nodes recursively with adjusted horizontal offset
    left_child_index = 2 * index + 1
    right_child_index = 2 * index + 2

    # Left child
    if left_child_index < len(heap):
        child_x = x - new_offset
        child_y = y + vertical_offset
        canvas.create_line(x, y + node_size, child_x, child_y - new_node_size, width=2)
        draw_heap(canvas, heap, child_x, child_y, left_child_index, new_offset, level + 1, new_node_size, color)

    # Right child
    if right_child_index < len(heap):
        child_x = x + new_offset
        child_y = y + vertical_offset
        canvas.create_line(x, y + node_size, child_x, child_y - new_node_size, width=2)
        draw_heap(canvas, heap, child_x, child_y, right_child_index, new_offset, level + 1, new_node_size, color)