import config
import random
import pandas as pd
import os
from utility.print_board import print_board

def save_game_results(uneven_loss, holes_punishment, height_diff_punishment, 
                      attack_bonus, game_stats, seed, game_number):
        filepath = "bruteforcer_stats.xlsx"
        
        lines_cleared = game_stats.single + game_stats.double + game_stats.triple + game_stats.tetris
        
        new_data = {
            "game_number": [game_number],
            "uneven_loss": [uneven_loss],
            "holes_punishment": [holes_punishment],
            "height_diff_punishment": [height_diff_punishment],
            "attack_bonus": [attack_bonus],
            "lines_cleared": [lines_cleared],
            "total_attack": [game_stats.total_attack],
            "pieces_placed": [game_stats.pieces_placed if hasattr(game_stats, 'pieces_placed') else 0],
            "seed": [seed],
            "attack_per_line": [game_stats.total_attack / max(1, lines_cleared)]
        }
        
        new_df = pd.DataFrame(new_data)
        
        if os.path.exists(filepath):
            existing_df = pd.read_excel(filepath)
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            updated_df = new_df
        
        updated_df.to_excel(filepath, index=False)
        
        return len(updated_df)

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