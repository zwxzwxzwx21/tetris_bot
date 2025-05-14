import tkinter as tk

class TetrisBoardViewer(tk.Tk):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.colors = {
            'T': "purple",
            'I': "cyan",
            'O': "yellow",
            'S': "green",
            'Z': "red",
            'J': "blue",
            'L': "orange",
            ' ': "black"  # Puste pole
        }
        self.cell_size = 30
        self.title("Tetris Board Viewer")
        self.resizable(False, False)
        self.canvas = tk.Canvas(self, 
                              width=10*self.cell_size, 
                              height=20*self.cell_size)
        self.canvas.pack()
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for y in range(20):
            for x in range(10):
                value = self.board[y][x]
                color = self.colors.get(value, "light gray")
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, 
                                          fill=color, 
                                          outline="black",
                                          width=1)

    def update_board(self, new_board):
        self.board = [row[:] for row in new_board]  # Głęboka kopia
        self.draw_board()