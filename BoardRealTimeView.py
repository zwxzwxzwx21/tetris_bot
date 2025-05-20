import pygame
import numpy as np


class TetrisBoardViewer:
    """
    A simple Pygame-based viewer for displaying a Tetris board in real time.
    This class is useful for visualizing the board state during AI simulations,
    debugging, or as a front-end for a Tetris bot.

    Usage:
        viewer = TetrisBoardViewer(board)
        viewer.update_board(new_board)  # Call this whenever the board changes
        viewer.mainloop()               # Keeps the window open and responsive

    Typical use case:
        - Use in a separate thread or as part of your main loop to visualize the board.
        - Call update_board() after every move or board update.
        - Call mainloop() to keep the window open (blocks until closed).
    """

    def __init__(self, board,stats_obj):
        """
        Initializes the viewer window and sets up colors and board state.

        Args:
            board (list of lists): The initial 20x10 Tetris board (list of lists or numpy array).
        """
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 10)
        self.board = np.array(board)  # Store the board as a numpy array for easy access
        self.stats = stats_obj
        self.start_time = pygame.time.get_ticks()  # Initialize the timer
        # Define colors for each piece type (RGB tuples)
        self.colors = {
            'T': (128, 0, 128),    # purple
            'I': (0, 255, 255),    # cyan
            'O': (255, 255, 0),    # yellow
            'S': (0, 255, 0),      # green
            'Z': (255, 0, 0),      # red
            'J': (0, 0, 255),      # blue
            'L': (255, 165, 0),    # orange
            ' ': (0, 0, 0)         # black (empty cell)
        }
        self.cell_size = 30
        
        # Each section (left panel, board, right panel) has the same width
        self.board_width = 10 * self.cell_size  # Width of actual Tetris board (10 cells)
        self.side_panel_width = self.board_width  # Same width as the board
        
        # Total window width is now 3x the board width (left panel + board + right panel)
        window_width = self.board_width + 2 * self.side_panel_width
        window_height = 20 * self.cell_size
        
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Tetris Board Viewer")
        self.clock = pygame.time.Clock()

        try:
            self.font = pygame.font.SysFont('Arial',30)
        except pygame.error:
            print("Font not found, using default font.")
            self.font = pygame.font.Font(None, 10)

        # test timer
        self.timer = pygame.time.get_ticks()

        self.draw_board()  # Draw the initial board

    def draw_board(self):
        """
        Draws the current board state to the Pygame window.
        Board is in the middle with equal space on both sides.
        """
        self.screen.fill((0, 0, 0))  # Fill background with black
        
        pps_text = f"PPS: {self.stats.pps:.2f}"
        pps_surface = self.font.render(pps_text, True, (255, 255, 255))
        ppr_rect = pps_surface.get_rect(topleft=(10,10))
        self.screen.blit(pps_surface, ppr_rect)  # Draw the text in the top left corner

        # Time elapsed since start (small issue that its updated every hard drop, not every frame)
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0
        timer_text = f"Time: {elapsed_time:.2f}s"
        timer_surface = self.font.render(timer_text, True, (255, 255, 255))
        timer_rect = timer_surface.get_rect(topleft=(10,self.cell_size*10 - 10))
        self.screen.blit(timer_surface, timer_rect)  # Draw the timer in the bottom left corner

        # easy clears counts (singles, doubles, triples, tetrises)
        single_line_clears_text = f"Singles: {self.stats.single}"
        single_line_clears_surface = self.font.render(single_line_clears_text, True, (255, 255, 255))
        single_line_clears_rect = single_line_clears_surface.get_rect(topleft=(10,self.cell_size*3 - 10))
        self.screen.blit(single_line_clears_surface, single_line_clears_rect)  # Draw the text in the top right corner

        double_line_clears_text = f"Doubles: {self.stats.double}"
        double_line_clears_surface = self.font.render(double_line_clears_text, True, (255, 255, 255))
        double_line_clears_rect = double_line_clears_surface.get_rect(topleft=(10,self.cell_size*4 - 10))
        self.screen.blit(double_line_clears_surface, double_line_clears_rect)  # Draw the text in the top right corner
        
        triple_line_clears_text = f"Triples: {self.stats.triple}"
        triple_line_clears_surface = self.font.render(triple_line_clears_text, True, (255, 255, 255))
        triple_line_clears_rect = triple_line_clears_surface.get_rect(topleft=(10,self.cell_size*5 - 10))
        self.screen.blit(triple_line_clears_surface, triple_line_clears_rect)  # Draw the text in the top right corner
        
        tetris_line_clears_text = f"Tetrises: {self.stats.tetris}"
        tetris_line_clears_surface = self.font.render(tetris_line_clears_text, True, (255, 255, 255))
        tetris_line_clears_rect = tetris_line_clears_surface.get_rect(topleft=(10,self.cell_size*6 - 10))
        self.screen.blit(tetris_line_clears_surface, tetris_line_clears_rect)  # Draw the text in the top right corner
        # Draw the Tetris board, positioned in the middle
        for y in range(20):
            for x in range(10):
                value = self.board[y, x]
                color = self.colors.get(value, (200, 200, 200))  # Default to gray if unknown
                rect = pygame.Rect(
                    self.side_panel_width + (x * self.cell_size),  # Shift by left panel width
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, color, rect)  # Draw filled cell
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)  # Draw cell border
        
        # Draw subtle borders to show the three sections
        pygame.draw.rect(self.screen, (40, 40, 40),
                       pygame.Rect(0, 0, self.side_panel_width, 20 * self.cell_size), 1)
        pygame.draw.rect(self.screen, (40, 40, 40),
                       pygame.Rect(self.side_panel_width + self.board_width, 0, 
                                  self.side_panel_width, 20 * self.cell_size), 1)
                         
        pygame.display.flip()  # Update the display

    def update_board(self, new_board):
        """
        Updates the board state and redraws it.

        Args:
            new_board (list of lists): The new board state to display.
        """
        self.board = np.array(new_board)
        self.draw_board()
        
        # Handle window events (like closing the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        self.clock.tick(60)  # Limit to 60 frames per second

    def mainloop(self):
        """
        Keeps the Pygame window open and responsive.
        Call this at the end of your program if you want the window to stay open.
        Blocks until the user closes the window.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.clock.tick(60)
        pygame.quit()