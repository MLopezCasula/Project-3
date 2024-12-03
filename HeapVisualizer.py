import pygame
import math

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


class MaxHeapVisualizer:
    def __init__(self, max_heap):
        self.max_heap = max_heap  # Directly use the provided max_heap
        self.running = True

    def draw_tree(self, nodes, screen, x, y, level=0, offset=225, max_depth=5):
        if not nodes:
            return

        # Get the current node (root of the subtree)
        value, title = nodes[0]

        # Calculate node size based on depth (decreases as we go down)
        node_radius = max(10, 30 - (level * 3))

        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Node's center
        node_center = (x, y)

        # Calculate the distance from the mouse to the center of the node
        distance = math.sqrt((mouse_x - x) ** 2 + (mouse_y - y) ** 2)

        # Draw the current node
        node_text = font.render(f"{title}", True, BLUE)
        node_width = node_text.get_width()

        # Check if the mouse is over the node (within the circle)
        if distance <= node_radius:
            # Display the node's title when hovering (above the node)
            screen.blit(node_text, (x - node_width // 2, y - node_text.get_height() - 25))

        # Draw the circle representing the node
        pygame.draw.circle(screen, RED, (x, y), node_radius)

        # Increase vertical spacing more significantly as we go deeper
        next_y = y + 60 + (level * 30)

        # If left child exists, draw it
        if 2 * level + 1 < len(nodes):
            pygame.draw.line(screen, BLACK, (x, y + node_radius), (x - offset, next_y - node_radius), 2)
            self.draw_tree(nodes[2 * level + 1:], screen, x - offset, next_y, level + 1, offset // 2, max_depth)

        # If right child exists, draw it
        if 2 * level + 2 < len(nodes):
            pygame.draw.line(screen, BLACK, (x, y + node_radius), (x + offset, next_y - node_radius), 2)
            self.draw_tree(nodes[2 * level + 2:], screen, x + offset, next_y, level + 1, offset // 2, max_depth)

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
