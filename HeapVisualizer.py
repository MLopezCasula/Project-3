import pygame
import math
import heapq  # Import heapq for heap operations

# Initialize pygame
pygame.init()

# Set the screen dimensions and create a window
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Max Heap Visualization")

# Set font for displaying text
font = pygame.font.SysFont("Arial", 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Node:
    def __init__(self, similarity, title):
        self.similarity = similarity
        self.title = title


class MaxHeapVisualizer:
    def __init__(self, sorted_books):
        # Create a max heap from sorted_books
        self.max_heap = self.create_max_heap(sorted_books)  # Create max heap from sorted_books
        self.running = True

    def create_max_heap(self, sorted_books):
        # Convert the sorted books to a max heap (using negative similarity values for max-heap simulation)
        max_heap = []
        for similarity, title in sorted_books:
            heapq.heappush(max_heap, (-similarity, title))
        return [Node(-similarity, title) for similarity, title in max_heap]  # Convert to Node objects

    def draw_tree(self, nodes, screen, x, y, level=0, offset=225):
        if not nodes:
            return

        # Get the current node (root of the subtree)
        node = nodes[0]

        # Calculate node size based on depth (decreases as we go down)
        node_radius = max(10, 30 - (level * 3))

        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Node's center
        node_center = (x, y)

        # Calculate the distance from the mouse to the center of the node
        distance = math.sqrt((mouse_x - x) ** 2 + (mouse_y - y) ** 2)

        # Draw the current node
        node_text = font.render(f"{node.title}", True, BLUE)
        node_width = node_text.get_width()

        # Check if the mouse is over the node (within the circle)
        if distance <= node_radius:
            # Display the node's title when hovering (above the node)
            screen.blit(node_text, (x - node_width // 2, y - node_text.get_height() - 25))

        # Draw the circle representing the node
        pygame.draw.circle(screen, RED, (x, y), node_radius)

        # Increase vertical spacing more significantly as we go deeper
        next_y = y + 75 + (level * 30)

        # Calculate the index of the left and right children
        left_index = 2 * level + 1
        right_index = 2 * level + 2

        # If left child exists, draw it
        if left_index < len(nodes):
            pygame.draw.line(screen, BLACK, (x, y + node_radius), (x - offset, next_y - node_radius), 2)
            self.draw_tree(nodes[left_index:], screen, x - offset, next_y, level + 1, offset // 2)

        # If right child exists, draw it
        if right_index < len(nodes):
            pygame.draw.line(screen, BLACK, (x, y + node_radius), (x + offset, next_y - node_radius), 2)
            self.draw_tree(nodes[right_index:], screen, x + offset, next_y, level + 1, offset // 2)

    def visualize_max_heap(self):
        # Set background color
        screen.fill(WHITE)

        # Draw the heap tree
        self.draw_tree(self.max_heap, screen, screen_width // 2, 50)

        # Update the display
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Visualize the heap
            self.visualize_max_heap()

        pygame.quit()

