import pygame

CELL_SIZE = 28
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SIDE_WIDTH = 170
FPS = 60

COLOR_BG = (0, 0, 0)
COLOR_PANEL = (28, 28, 36)
COLOR_GRID = (42, 42, 54)
COLOR_TEXT = (220, 220, 230)
COLOR_BUTTON = (30, 140, 40)

PIECE_COLORS = {
    "I": (0, 255, 255),
    "J": (0, 0, 200),
    "L": (255, 140, 0),
    "O": (240, 230, 0),
    "S": (0, 200, 0),
    "Z": (200, 0, 0),
    "T": (160, 0, 160),
    " ": (24, 24, 32),
}


class TetrisBoardViewer:
    def __init__(self, board_, stats, queue, no_s_z_first_piece_signal, slow_mode, seed):
        pygame.init()
        self.surface = pygame.display.set_mode(
            (BOARD_WIDTH * CELL_SIZE + SIDE_WIDTH, BOARD_HEIGHT * CELL_SIZE)
        )
        pygame.display.set_caption("tewi bot 🐰")
        self.font = pygame.font.SysFont("orbitron", 16)
        self.clock = pygame.time.Clock()
        self.board = board_
        self.stats = stats
        self.queue = queue
        self.no_s_z_first_piece_signal = no_s_z_first_piece_signal
        self.slow_mode = slow_mode
        self.running = True
        self.draw = True
        self.start_button = True
        self.preview = None

    def update_board(self, new_board):
        self.board = new_board
        self.draw = True

    def set_preview(self, piece, shape, xpos, board_array):
        height = len(shape)
        width = len(shape[0])

        def occupied(cell):
            return cell not in (" ", 0)

        def collides(ypos):
            for h in range(height):
                for w in range(width):
                    if occupied(shape[h][w]):
                        yyy = ypos + h
                        xxx = xpos + w
                        if yyy >= BOARD_HEIGHT:
                            return True
                        if xxx < 0 or xxx >= BOARD_WIDTH:
                            return True
                        if board_array[yyy][xxx] not in (" ", 0):
                            return True
            return False

        y = 0
        while not collides(y + 1):
            y += 1
        self.preview = (piece, shape, xpos, y)
        self.draw = True

    def clear_preview(self):
        if self.preview:
            self.preview = None
            self.draw = True

    def _draw_board(self):
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                a = self.board[y][x]
                color = PIECE_COLORS.get(a, (90, 90, 100))
                xx = x * CELL_SIZE
                yy = y * CELL_SIZE
                pygame.draw.rect(self.surface, color, (xx, yy, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(
                    self.surface, COLOR_GRID, (xx, yy, CELL_SIZE, CELL_SIZE), 1
                )

        if self.preview:
            piece, shape, xpos, ypos = self.preview
            base = PIECE_COLORS.get(piece, (180, 180, 180))
            duszek = tuple(wawa // 2 for wawa in base)
            height = len(shape)
            width = len(shape[0])
            for h in range(height):
                for w in range(width):
                    if shape[h][w] not in (" ", 0):
                        xx = (xpos + w) * CELL_SIZE
                        yy = (ypos + h) * CELL_SIZE
                        pygame.draw.rect(
                            self.surface, duszek, (xx, yy, CELL_SIZE, CELL_SIZE)
                        )
                        pygame.draw.rect(
                            self.surface, base, (xx, yy, CELL_SIZE, CELL_SIZE), 1
                        )

    def _draw_panel(self):
        xpos = BOARD_WIDTH * CELL_SIZE
        pygame.draw.rect(
            self.surface, COLOR_PANEL, (xpos, 0, SIDE_WIDTH, BOARD_HEIGHT * CELL_SIZE)
        )
        y = 8

        def line(txt):
            nonlocal y
            bleh = self.font.render(txt, True, COLOR_TEXT)
            self.surface.blit(bleh, (xpos + 8, y))
            y += 18

        queue_ = list(self.queue)[:5]
        line("queue:")
        line(" ".join(queue_) if queue_ else "-")
        y += 6
        line("stats:")
        lines_total = (
            self.stats.single
            + self.stats.double
            + self.stats.triple
            + self.stats.tetris
        )
        line(f"PPS: {self.stats.pps:.2f}")
        line(f"combo: {self.stats.combo}")
        line(f"lines: {lines_total}")
        # line(f"total attack: {self.stats.total_attack}")
        line(f"APM: {self.stats.APM:.2f}")
        line(f"APP: {self.stats.APP:.2f}")
        line(f"total_attack: {self.stats.total_attack}")
        y += 6
        line("clears:")
        line(f"single: {self.stats.single}")
        line(f"double: {self.stats.double}")
        line(f"triple: {self.stats.triple}")
        line(f"tetris: {self.stats.tetris}")
        y += 6
        line("rules:")
        line(f"nosz: {self.no_s_z_first_piece_signal[0]}")
        line(f"slow mode: {self.slow_mode[0]}")
        y += 6
        line("seed:")
        line(f"{self.stats.seed}")

    def _draw(self):
        self.surface.fill(COLOR_BG)
        self._draw_board()
        self._draw_panel()
        pygame.display.flip()

    def mainloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if self.draw:
                self.draw = False
                self._draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        # buttons dont appear anymore (somehow?) and also i wanna make so you have button that just acts as pressing enter in slow mode
