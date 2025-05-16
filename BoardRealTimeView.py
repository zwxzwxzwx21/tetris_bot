import pygame
import numpy as np

class TetrisBoardViewer:
    def __init__(self, board):
        pygame.init()
        self.board = np.array(board)  
        self.colors = {
            'T': (128, 0, 128),    # purple
            'I': (0, 255, 255),    # cyan
            'O': (255, 255, 0),    # yellow
            'S': (0, 255, 0),      # green
            'Z': (255, 0, 0),      # red
            'J': (0, 0, 255),      # blue
            'L': (255, 165, 0),    # orange
            ' ': (0, 0, 0)         # black
        }
        self.cell_size = 30
        self.screen = pygame.display.set_mode((10 * self.cell_size, 20 * self.cell_size))
        pygame.display.set_caption("Tetris Board Viewer")
        self.clock = pygame.time.Clock()
        self.draw_board()

    def draw_board(self):
        self.screen.fill((0, 0, 0))
        for y in range(20):
            for x in range(10):
                value = self.board[y, x]
                color = self.colors.get(value, (200, 200, 200))  
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)  
        pygame.display.flip()

    def update_board(self, new_board):
        self.board = np.array(new_board)
        self.draw_board()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        self.clock.tick(60)  # 60 FPS limit "apparently"

    def mainloop(self):
        """Zachowujemy interfejs podobny do Tkinter"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.clock.tick(60)
        pygame.quit()