import config
import random
from utility.print_board import print_board

def save_game_state(self,move_str,board,MoveHistoryClass):
    if config.PRINT_MODE:
        print("SAVED BOARD:")
        print_board(board)
    game_history = MoveHistoryClass(
        board = [row[:] for row in board],
        queue = list(self.queue),
        bag = list(self.bag),
        combo = self.stats.combo,
        stats = {
            "total_attack": self.stats.total_attack,
            "single": self.stats.single,
            "double": self.stats.double,
            "triple": self.stats.triple,
            "tetris": self.stats.tetris,
            "combo": self.stats.combo,
        },
        move = move_str,
        rng = random.getstate(),
    )
    if self.history_index < len(self.history) - 1:
        self.history = self.history[: self.history_index + 1]
    self.history.append(game_history)
    self.history_index += 1

def load_game_state(self, index, board):
    if config.PRINT_MODE:
        print("LOADING STATE")
        print_board(board)
    move_to_load = self.history[index]
    for a,b in enumerate(move_to_load.board):
        self.board[a][:] = b
    self.queue[:] = move_to_load.queue
    self.bag[:] = move_to_load.bag   #apparently needed lol
    self.combo = move_to_load.combo
    self.stats.total_attack = move_to_load.stats["total_attack"]
    self.stats.single = move_to_load.stats["single"]
    self.stats.double = move_to_load.stats["double"]
    self.stats.triple = move_to_load.stats["triple"]
    self.stats.tetris = move_to_load.stats["tetris"]
    self.stats.combo = move_to_load.stats["combo"]
    random.setstate(move_to_load.rng)
    self.history_index = index