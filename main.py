# -*- coding: utf-8 -*-
# if someone is reading that, i may or may not have used some AI help for comments and such to make code more readable
# half of them i didnt even read but i dont remove them because fucking higlighting puts them there as it feels and it was usefull
# ^ update i have cleared some useless things up, yeah you can mby look them up in previous commits but what for
# those dont even have any working code so i wouldnt bother
# once!! so i wil lleave them, so like whateverr sorry algosith dont bother with them
# got an issue with that? better not or i will cry.

# to test the argparse better, try running it in console using:
# python .\main.py --rule, rules will be listed lower, as they are wip
import argparse  # testing it
import copy
import logging
import random
import threading
import time
import pandas as pd
import os

from tetrio_parsing.calculate_attack import count_lines_clear

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(
        handler
    )  # resets logger cuz when you set it once, you cant change it

logging.basicConfig(
    format="%(levelname)s | %(filename)s -> %(lineno)d in %(funcName)s: %(message)s",
    level=logging.DEBUG,
)
from board_operations.board_operations import clear_lines
from board_operations.checking_valid_placements import drop_piece
from BoardRealTimeView import TetrisBoardViewer
from bruteforcing import find_best_placement
from GenerateBag import add_piece_from_bag, create_bag
from tests.combo_attack_test import (
    custom_board,  # probably stupid way to do that, idk better yet
)
from utility.pieces import PIECES
from utility.print_board import print_board

if not PIECES:
    raise ImportError("PIECES dictionary could not be imported or is empty.")

DESIRED_QUEUE_PREVIEW_LENGTH = 5

from dataclasses import dataclass

@dataclass
class MoveHistory:
    board: list
    queue: list
    bag: list
    combo: int
    stats: dict
    move: str | None
    rng: object

class GameStats:
    def __init__(self,seed):
        self.burst = []  # (PPS) stores 10 times piece was placed, then max-min
        self.pps = 0.0
        self.single = 0
        self.double = 0
        self.triple = 0
        self.tetris = 0
        self.combo = 0
        self.burst_attack = 0  # unused, stil; thinking about it
        self.total_attack = 0
        self.APM = 0.0
        self.APP = 0.0
        self.seed = seed
        self.pieces_placed = 0 
class TetrisGame:
    def __init__(self,seed):
        self.board = [[" " for _ in range(10)] for _ in range(20)]
        self.queue = []
        self.bag = []
        self.combo = 0
        self.start_signal = [False]
        self.game_over_signal = [False]
        self.no_s_z_first_piece_signal = [False]
        self.custom_bag = [False]
        self.stats = GameStats(seed=seed)
        self.slow_mode = [False]
        self.custom_board = [False]
        self.gui_mode = [False]
        self.delay_mode = [False,-1] # on/off , delay
        self.delay = -1
        self.history = []
        self.history_index = -1
        self.pending_save = None # the clogger 
        self.seed = seed
        random.seed(self.seed)

    def save_game_state(self,move_str,board):
        print("SAVED BOARD:")
        print_board(board)
        game_history = MoveHistory(
            board = [row[:] for row in board],
            queue = list(self.queue),
            bag = list(self.bag),
            combo = self.combo,
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
        

    def game_loop(self, viewer):
        # todo: this has to go, left from boardvierer, was really usefull but now its annoying
        # i will change it i swear, just give me second :3
        while not self.start_signal[0]:
            time.sleep(0.1)
            if self.game_over_signal[0]:
                return

        pieces_placed = 0
        actual_game_start_time = time.perf_counter()

        try:
            if not self.queue:
                logging.debug("queue fill")
                num_to_add = DESIRED_QUEUE_PREVIEW_LENGTH - len(self.queue)
                if num_to_add > 0:
                    self.queue, self.bag = add_piece_from_bag(
                        self.queue,
                        self.bag,
                        num_pieces=num_to_add,
                        no_s_z_first_piece=self.no_s_z_first_piece_signal[0],
                    )
                # algo youre may be reading this, those are kind of things ive asked
                # like obv it wasnt my idea, i saw that and was just, fuck it we ball
                if len(self.queue) < DESIRED_QUEUE_PREVIEW_LENGTH:
                    logging.debug("failed to fill queue")
                    return

            if not self.history:
                self.save_game_state(move_str=None, board=self.board)

            while True:
                if self.pending_save is not None:
                    self.save_game_state(self.pending_save,board=self.board)
                    self.pending_save = None

                if self.game_over_signal[0]:
                    # leftover from board viewer, useless
                    logging.debug("game loop finished by game_over_signal")
                    break

                logging.debug("\n=== Current Queue ===")
                logging.debug(self.queue[:DESIRED_QUEUE_PREVIEW_LENGTH])
                

                
                move_history_ = find_best_placement(
                    self.board, self.queue[:DESIRED_QUEUE_PREVIEW_LENGTH], self.combo, self.stats
                )
                
                

                if not move_history_:
                    logging.info("game over, tewibot has run into a problem (laziness) and had to be put down, bye bye tewi")
                    logging.debug(f"piece that failed: {self.queue[0]}")
                    self.game_over_signal[0] = True
                    break    
                
                move_history, best_move_str = move_history_            
                piece_type_placed = [0]
                first_move = move_history[0]
                piece_type, x_str, rotation = first_move.split("_")
                x = int(x_str[1:])
                piece_type_placed = self.queue[0]
                piece_shape = PIECES[piece_type_placed][rotation]

                if viewer:
                    viewer.set_preview(piece_type_placed, piece_shape, x, self.board)
 
                board_after_drop = drop_piece(piece_shape, copy.deepcopy(self.board), x)

                if self.slow_mode[0]:
                    print_board(
                        board_after_drop
                    )
                    decision = input(
                        f"found move: {piece_shape} at x={x} rotation={rotation}, enter to continue...\n undo to move back, redo to redo if you have undone a move before "
                    )
                    if decision.lower() == "undo":
                        if self.history_index > 0:
                            self.load_game_state(self.history_index - 1, board=self.board)
                        else:
                            print("no move to undo")
                        continue
                    elif decision.lower() == "redo":
                        if self.history_index < len(self.history) - 1:
                            self.load_game_state(self.history_index + 1, board=self.board)
                        else:
                            print("no move to redo")
                        continue
                elif self.delay_mode[0] == True:
                    self.delay = self.delay_mode[1]

                if self.delay > 0:
                    time.sleep(self.delay)

                # its never none, usually its just first rotation and leftmost X, i think it would be good to change it
                # so when there isnt a single good move found, it returns none and fucks up entire program so heuristic can be edited
                # tho im not so sure, leaving it here just because of that
                if board_after_drop is None:
                    # logging.debug(f"error: drop_piece failed for valid move: {best_move_str} with piece {piece_type_placed}")
                    logging.debug("cannot drop piece")
                    break

                board_after_clear, lines_cleared_count = clear_lines(board_after_drop)
                logging.debug(f"lines cleared: {lines_cleared_count}")
                attack, self.combo = count_lines_clear(
                    lines_cleared_count, self.combo, board_after_clear
                )
                self.stats.total_attack += attack
                self.stats.combo = self.combo

                if lines_cleared_count == 1:
                    self.stats.single += 1
                elif lines_cleared_count == 2:
                    self.stats.double += 1
                elif lines_cleared_count == 3:
                    self.stats.triple += 1
                elif lines_cleared_count == 4:
                    self.stats.tetris += 1

                self.board[:] = board_after_clear
                if viewer:
                    viewer.clear_preview()
                    viewer.update_board(self.board)

                print_board(self.board)

                if self.queue:
                    self.queue.pop(0)  # remove the used piece
                else:  # should never happen
                    logging.debug(
                        "error: tried to pop from empty queue after placement"
                    )
                    break

                # add one new piece to the queue
                self.queue, self.bag = add_piece_from_bag(
                    self.queue,
                    self.bag,
                    num_pieces=1,
                    no_s_z_first_piece=self.no_s_z_first_piece_signal[0],
                )

                pieces_placed += 1
                # i think after removing board viewer it doesnt work, but i also dont print it at all so that is something i will do later
                # im making those comments and changes cuz i wanna public code soon and then i will be so much more motivated to work on it lmao
                elapsed = time.perf_counter() - actual_game_start_time
                if len(self.stats.burst) < 10:
                    self.stats.burst.append(elapsed)
                else:
                    self.stats.burst.pop(0)
                    self.stats.burst.append(elapsed)
                logging.debug(self.stats.burst)
                if elapsed > 0:
                    self.stats.APM = (self.stats.total_attack / elapsed) * 60
                    self.stats.APP = (
                        (self.stats.total_attack / pieces_placed)
                        if pieces_placed > 0
                        else 0
                    )
                    self.stats.pps = pieces_placed / elapsed
                    self.stats.burst_pps = (
                        (len(self.stats.burst) - 1)
                        / (max(self.stats.burst) - min(self.stats.burst))
                        if len(self.stats.burst) > 9
                        else 0
                    )
                    logging.debug(
                        f"PPS: {self.stats.pps:.2f} burst: {self.stats.burst_pps / 10}"
                    )
                
                self.pending_save = best_move_str  
        finally:
            logging.debug("game loop finished")
            self.game_over_signal[0] = True

def save_game_results(uneven_loss, holes_punishment, height_diff_punishment, 
                      attack_bonus, game_stats, seed, game_number):
        # yea id admit most code i stole lol, tho i was doing fine before that!
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
def run_bruteforce_games(num_games=999999, max_pieces=9999999):
    
    start_time = time.time()
    
    for game_num in range(1, num_games + 1):
        uneven_loss = random.uniform(0, 30)
        holes_punishment = random.uniform(0, 100)
        height_diff_punishment = random.uniform(0, 50)
        attack_bonus = random.uniform(0, 50)
        
        import bruteforcing
        bruteforcing.uneven_loss = uneven_loss
        bruteforcing.holes_punishment = holes_punishment
        bruteforcing.height_diff_punishment = height_diff_punishment
        bruteforcing.attack_bonus = attack_bonus
        
        seed = time.time_ns() % (2**32 - 1)  # idk why that is the formula that was suggested by vscode but okay buddy you do you im counting on that!
        
        print(f"\n=== game {game_num}/{num_games} ===")
        print(f"vals: uneven={uneven_loss:.2f}, holes={holes_punishment:.2f}, "
              f"height_diff={height_diff_punishment:.2f}, attack={attack_bonus:.2f}")
        print(f"seed: {seed}")
        
        game = TetrisGame(seed=seed)
        game.stats.pieces_placed = 0
        
        game.start_signal[0] = True
        game.game_loop(None)
        
        save_game_results(
            uneven_loss, holes_punishment, height_diff_punishment, 
            attack_bonus, game.stats, seed, game_num
        )
        
        lines = game.stats.single + game.stats.double + game.stats.triple + game.stats.tetris
        
        elapsed = time.time() - start_time
        avg_time = elapsed / game_num
        remaining = avg_time * (num_games - game_num)
    
    print(f"\nall {num_games} games completed in {time.time() - start_time:.1f} seconds!!!!!")

# this one is cool im proud of it cuz i learned something new! (ik its not useful lol)
def parse_args():
    parser = argparse.ArgumentParser(description="Test arguments/rules")
    parser.add_argument("--seed", type=int, help="override RNG seed")
    parser.add_argument("--bruteforce", type=int,)
    parser.add_argument("--max-pieces", type=int, default=99999999)
    
    parser.add_argument(
        "--rules",
        choices=["custom_bag", "nosz", "custom_board", "slow", "gui", "delay","seed"],
        nargs="+",
        default=[],
        help="unsure what it does i guess its like, when you just ask for help, well there is none, youre left alone in the dark world",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    if args.bruteforce:
        run_bruteforce_games(num_games=args.bruteforce, max_pieces=args.max_pieces)
        exit(0)
    
    if args.seed is not None:
        seed = args.seed
    else:
        seed = time.time_ns() % (2**32 - 1)
    logging.debug(f"using seed {seed}")
    game = TetrisGame(seed=seed)

    game.start_signal[0] = True

    game.no_s_z_first_piece_signal[0] = "nosz" in args.rules

    game.custom_bag[0] = "custom_bag" in args.rules
    if game.custom_bag[0]:
        game.bag = create_bag(custom_bag=True)
        logging.debug(f"custom bag mode enabled, using custom bag \n bag={game.bag}")
        time.sleep(1)
    game.custom_board[0] = "custom_board" in args.rules
    if game.custom_board[0]:
        game.board = custom_board

    if "delay" in args.rules:
        game.delay_mode[0] = True
        game.delay_mode[1] = float(input("enter delay in seconds"))
    elif "slow" in args.rules:
        game.slow_mode[0] = True
        logging.debug("slow mode enabled, press enter to place each piece")

    game.gui_mode[0] = "gui" in args.rules

    use_gui = "gui" in args.rules
    if use_gui:
        viewer = TetrisBoardViewer(
            game.board,
            game.stats,
            game.queue,
            game.no_s_z_first_piece_signal,
            game.slow_mode,
            game.seed,
        )
        t = threading.Thread(target=game.game_loop, args=(viewer,), daemon=True)
        t.start()
        viewer.mainloop()
    else:
        game.start_signal[0] = True
        game.game_loop(None)

# IMPORTANT:
# - the game loop will stop if no valid placement is found
# - stats.pps can be used in other modules (for display in the viewer).
#
# TODO:
# - add more advanced scoring/evaluation for moves.
# - implement perfect clear solver/mode.
# - improve stack flatness/height evaluation for better bot performance.
# - improve the code working in a way that its usable on console, i look at it like this
# just make it work normally but do sth like, if there is a line clear,make it pink in console (assuming everything else is colored)
# and then next move just removes that line
