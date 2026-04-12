# to test the argparse better, try running it in console using:
# python .\main.py --rule, rules will be listed lower, as they are wip
# python .\main.py --rule control_mode
# c:\Users\alexx\tewibot\.venv\Scripts\Activate.ps1

# stdlib
import argparse
import copy
import logging
import os
import random
import threading
import time
from dataclasses import dataclass

# third party
import pandas as pd  # type: ignore
import pygame  # type: ignore
from pyparsing import deque  # type: ignore

# local
import config
from board_operations.board_operations import clear_lines, solidify_piece
from board_save_load_functions import save_game_results, save_game_state
from BoardRealTimeView import TetrisBoardViewer
from bruteforcing import find_best_placement
from GenerateBag import add_piece_from_bag, create_bag
from heuristic import analyze
from simulate_game_movement import simulate_move
from tetrio_parsing.calculate_attack import (
    calculate_attack_and_stats,
    count_lines_clear,
)
from utility.main_calc_time_place_piece import time_to_place_piece
from utility.pieces_index import PIECES_index
from utility.print_board import (
    debug_print,
    print_board,
    printgreen,
    printred,
    printyellow,
)

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(
        handler
    )  # resets logger cuz when you set it once, you cant change it

logging.basicConfig(
    format="%(levelname)s | %(filename)s -> %(lineno)d in %(funcName)s: %(message)s",
    level=logging.DEBUG,
)

DESIRED_QUEUE_PREVIEW_LENGTH = config.DESIRED_QUEUE_PREVIEW_LENGTH


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
    def __init__(self):
        # bot stats
        self.burst = []  # (PPS) stores 10 times piece was placed, then max-min
        self.pps = 0.0
        self.APM = 0.0
        self.APP = 0.0
        self.burst_attack = 0  # unused, stil; thinking about it
        self.total_attack = 0
        self.pieces_placed = 0
        self.calc_piece_time = [0,0,0,0,0,0,0] # how much time it takes to calculate one piece place,ment on averrage, [O,I,J,L,S,Z,T]
        self.calc_piece_time_piecenumber = [0,0,0,0,0,0,0] # how much a piece got placed
        # gamestats
        self.single = 0
        self.double = 0
        self.triple = 0
        self.tetris = 0
        self.combo = 0


class TetrisGame:
    def __init__(self, seed):
        self.board = [[" " for _ in range(10)] for _ in range(20)]
        self.queue = []
        self.bag = []
        self.stats = GameStats()

        self.history = []
        self.history_index = -1  # related to save/load
        self.pending_save = None  # the clogger
        self.seed = seed
        random.seed(self.seed)  # needed for undo redo

        self.held_piece = None  # should be string i guess
        self.weights_updated_event = threading.Event()

        # signals
        self.control_mode = [False]
        self.no_calculation_mode = False  # disables heuristic  - not done yet
        self.no_s_z_first_piece_signal = [False]
        self.custom_bag = [False]
        self.slow_mode = [False]
        self.custom_board = [False]
        self.gui_mode = [False]
        self.delay_mode = [False, -1]  # on/off , delay
        self.delay = -1

    def request_weights_recalc(self):
        self.weights_updated_event.set()

    def game_loop(self, viewer):
        actual_game_start_time = time.perf_counter()

        # queue fill
        if not self.queue:
            debug_print("queue fill", "main.py 112")
            num_to_add = DESIRED_QUEUE_PREVIEW_LENGTH - len(self.queue)
            if num_to_add > 0:
                self.queue, self.bag = add_piece_from_bag(
                    self.queue,
                    self.bag,
                    num_pieces=num_to_add,
                    no_s_z_first_piece=self.no_s_z_first_piece_signal[0],
                )
            if len(self.queue) < DESIRED_QUEUE_PREVIEW_LENGTH:
                debug_print("failed to fill queue", "main.py 120")
                return
        # we force a piece to be in hold position so calculations can be run on it,
        # and if better piece is found, that is accesible only after using hold, even if we havent used it in the game yet
        # using hold to "replace" the piece givess the same result, for example
        # imagine we have a queue S,L,J, with best placement being S, we firce L to be in held slot, we place S piece, calculate for both L and J, everything is good
        # now if the best placement is L, we simply replace the held L with S and move with comparing J and S, at least thast how i imagine it lol
        self.held_piece = self.queue[1]
        self.queue.pop(1)

        if not self.history:
            save_game_state(
                self, move_str=None, board=self.board, MoveHistoryClass=MoveHistory
            )

        # main game loop
        while True:
            if self.pending_save is not None:
                save_game_state(
                    self,
                    self.pending_save,
                    board=self.board,
                    MoveHistoryClass=MoveHistory,
                )
                self.pending_save = None

            debug_print("\n=== Current Queue ===", "main.py 137")
            debug_print(self.queue[:DESIRED_QUEUE_PREVIEW_LENGTH], "main.py 138")

            time_start = time.perf_counter()

            move_history_with_best_move_info = find_best_placement(
                self.board,
                self.queue[:DESIRED_QUEUE_PREVIEW_LENGTH],
                self.stats.combo,
                self.stats,
                self.held_piece,
            )
            
            time_to_calc_piece = time.perf_counter() - time_start
            
            self.stats.calc_piece_time, self.stats.calc_piece_time_piecenumber = time_to_place_piece(
                move_history_with_best_move_info[0][0][0], # a piece like "T", "I" etc
                self.stats.calc_piece_time,
                time_to_calc_piece,
                self.stats.calc_piece_time_piecenumber
            )
            #print(self.stats.calc_piece_time, self.stats.calc_piece_time_piecenumber)
            
            print(
                f"O piece time: {(self.stats.calc_piece_time[0]/(self.stats.calc_piece_time_piecenumber[0] if self.stats.calc_piece_time_piecenumber[0] != 0 else 1)):.5f}\
                    I piece time: {(self.stats.calc_piece_time[1]/(self.stats.calc_piece_time_piecenumber[1] if self.stats.calc_piece_time_piecenumber[1] != 0 else 1)):.5f}\
                    J piece time: {(self.stats.calc_piece_time[2]/(self.stats.calc_piece_time_piecenumber[2] if self.stats.calc_piece_time_piecenumber[2] != 0 else 1)):.5f}\
                    L piece time: {(self.stats.calc_piece_time[3]/(self.stats.calc_piece_time_piecenumber[3] if self.stats.calc_piece_time_piecenumber[3] != 0 else 1)):.5f}\
                    S piece time: {(self.stats.calc_piece_time[4]/(self.stats.calc_piece_time_piecenumber[4] if self.stats.calc_piece_time_piecenumber[4] != 0 else 1)):.5f}\
                    Z piece time: {(self.stats.calc_piece_time[5]/(self.stats.calc_piece_time_piecenumber[5] if self.stats.calc_piece_time_piecenumber[5] != 0 else 1)):.5f}\
                    T piece time: {(self.stats.calc_piece_time[6]/(self.stats.calc_piece_time_piecenumber[6] if self.stats.calc_piece_time_piecenumber[6] != 0 else 1)):.5f}")
            
            debug_print(
                f"move history from best placement: {move_history_with_best_move_info}",
                "main.py 144",
            )

            if not move_history_with_best_move_info:
                debug_print(
                    "game over, tewibot has run into a problem (laziness) and had to be put down, bye bye tewi",
                    "main.py 147",
                )
                debug_print(f"piece that failed: {self.queue[0]}", "main.py 148")
                break
            else:
                move_history, best_move_str, goal_y_pos, used_hold = (
                    move_history_with_best_move_info
                )
                best_move_str_original = best_move_str

            if self.no_calculation_mode:
                # set positions for testing gamemode
                piece_type, x_str, rotation1, rotation2 = best_move_str.split("_")
                best_move_str = f"{piece_type}_x4_flat_0"
                goal_y_pos = 1

            # needed for viewer which is created only with --rule gui
            das_delay = config.das_delay  # 0.16s before repeat starts
            arr_delay = config.arr_delay  # 0s between moves after DAS activates
            das_state = config.das_state

            break_loop = False

            while self.control_mode[0] and break_loop == False:
                # we dont really need bruteforcer to work in control_mode, only to display heuristic on given piece, so im not making it efficient
                if viewer:
                    from main_viewer import main_viewer

                    main_viewer(viewer, das_state, das_delay, arr_delay, self)
                else:
                    break

            debug_print(
                f"move history str: {move_history}, full move history: {move_history_with_best_move_info}, goal y pos: {goal_y_pos}",
                "main.py 166",
            )
            piece_type_placed = [0]
            first_move = best_move_str
            debug_print(f"first move: {first_move}", "main.py 168")
            piece_type, x_str, rotation1, rotation2 = first_move.split("_")
            rotation = rotation1 + "_" + rotation2

            if used_hold and self.held_piece is not None:
                self.queue[0], self.held_piece = self.held_piece, self.queue[0]

            x = int(x_str[1:])

            piece_type_placed = piece_type

            if viewer:
                viewer.set_preview(
                    piece_type_placed,
                    x,
                    self.board,
                    rotation,
                    held_piece=self.held_piece,
                    yvalue=goal_y_pos,
                    control_mode=self.control_mode,
                )

            board_after_drop = solidify_piece(
                copy.deepcopy(self.board),
                piece_type_placed,
                [piece_type_placed, rotation, x, goal_y_pos],
            )

            if self.slow_mode[0]:
                debug_print(board_after_drop, "main.py 170")
                decision = input(
                    f"found move: {'placeholder'} at x={x} rotation={rotation}, enter to continue...\n undo to move back, redo to redo if you have undone a move before "
                )
                if decision.lower() == "undo":
                    if self.history_index > 0:
                        self.load_game_state(self.history_index - 1, board=self.board)
                    else:
                        debug_print("no move to undo", "main.py 177")
                    continue
                elif decision.lower() == "redo":
                    if self.history_index < len(self.history) - 1:
                        self.load_game_state(self.history_index + 1, board=self.board)
                    else:
                        debug_print("no move to redo", "main.py 183")
                    continue

            elif self.delay_mode[0] == True:
                self.delay = self.delay_mode[1]

            if self.delay > 0:
                time.sleep(self.delay)

            # its never none, usually its just first rotation and leftmost X, i think it would be good to change it
            # so when there isnt a single good move found, it returns none and fucks up entire program so heuristic can be edited
            # tho im not so sure, leaving it here just because of that
            if board_after_drop is None:
                debug_print("cannot drop piece", "main.py 192")
                break

            board_after_clear, lines_cleared_count = clear_lines(board_after_drop)
            debug_print(f"lines cleared: {lines_cleared_count}", "main.py 194")
            attack, self.stats.combo = count_lines_clear(
                lines_cleared_count, self.stats.combo, board_after_clear
            )

            attack, self.stats.combo, s, d, t, q = calculate_attack_and_stats(
                lines_cleared_count, self.stats.combo, board_after_clear
            )
            self.stats.total_attack += attack
            self.stats.single += s
            self.stats.double += d
            self.stats.triple += t
            self.stats.tetris += q
            total_lines_cleared = (
                self.stats.single
                + 2 * self.stats.double
                + 3 * self.stats.triple
                + 4 * self.stats.tetris
            )

            self.board[:] = board_after_clear
            self.stats.pieces_placed += 1  # there were two of these, i removed one so idk if things are not broken cuz of that

            if viewer:
                viewer.clear_preview()
                viewer.update_board(self.board)
                viewer.update_pieces(self.stats.pieces_placed)

            debug_print(self.board, "main.py 200")

            if self.queue:
                self.queue.pop(0)  # remove the used piece

            # add one new piece to the queue
            self.queue, self.bag = add_piece_from_bag(
                self.queue,
                self.bag,
                num_pieces=1,
                no_s_z_first_piece=self.no_s_z_first_piece_signal[0],
            )

            # i think after removing board viewer it doesnt work, but i also dont print it at all so that is something i will do later
            # im making those comments and changes cuz i wanna public code soon and then i will be so much more motivated to work on it lmao
            elapsed = time.perf_counter() - actual_game_start_time

            if len(self.stats.burst) < 10:
                self.stats.burst.append(elapsed)
            else:
                self.stats.burst.pop(0)
                self.stats.burst.append(elapsed)
            debug_print(self.stats.burst, "main.py 212")
            if elapsed > 0:
                # thhat can go into calculate burst function and places in calculate attack
                self.stats.APM = (self.stats.total_attack / elapsed) * 60
                self.stats.APP = (
                    (self.stats.total_attack / self.stats.pieces_placed)
                    if self.stats.pieces_placed > 0
                    else 0
                )
                self.stats.pps = self.stats.pieces_placed / elapsed
                self.stats.burst_pps = (
                    (len(self.stats.burst) - 1)
                    / (max(self.stats.burst) - min(self.stats.burst))
                    if len(self.stats.burst) > 9
                    else 0
                )
                debug_print(
                    f"PPS: {self.stats.pps:.2f} burst: {self.stats.burst_pps / 10}",
                    "main.py 214",
                )

            self.pending_save = best_move_str

        logging.debug("game loop finished")
        return self.stats.pieces_placed


def parse_args():
    parser = argparse.ArgumentParser(description="Test arguments/rules")
    parser.add_argument("--seed", type=int, help="override RNG seed")
    
    parser.add_argument("--max-pieces", type=int, default=99999999)

    parser.add_argument(
        "--rules",
        choices=[
            "custom_bag",
            "nosz",
            "custom_board",
            "slow",
            "gui",
            "delay",
            "seed",
            "control_mode",
        ],
        nargs="+",
        default=[],
        help="unsure what it does i guess its like, when you just ask for help, well there is none, youre left alone in the dark world",
    )
    return parser.parse_args()


def resolve_seed(args):
    if args.seed is not None:
        return args.seed
    return time.time_ns() % (2**32 - 1)


def apply_rules(game, args):
    game.no_s_z_first_piece_signal[0] = "nosz" in args.rules

    game.custom_bag[0] = "custom_bag" in args.rules
    if game.custom_bag[0]:
        game.bag = create_bag(custom_bag=True)
        debug_print(
            f"custom bag mode enabled, using custom bag \n bag={game.bag}",
            "main.py 256",
        )
        time.sleep(1)

    game.custom_board[0] = "custom_board" in args.rules
    if game.custom_board[0]:
        game.board = config.custom_board

    if "delay" in args.rules:
        game.delay_mode[0] = True
        game.delay_mode[1] = float(input("enter delay in seconds"))
    elif "slow" in args.rules:
        game.slow_mode[0] = True
        debug_print("slow mode enabled, press enter to place each piece", "main.py 262")

    game.gui_mode[0] = "gui" in args.rules
    use_gui = "gui" in args.rules

    game.control_mode[0] = "control_mode" in args.rules
    if game.control_mode[0]:
        print("control mode requires gui mode to be enabled, enabling gui mode")
        game.gui_mode[0] = True
        use_gui = True

    return use_gui


def initialize_heuristics(game):

    (
        game.aggregate,
        game.clearedLines,
        game.bumpiness,
        game.blockade,
        game.tetrisSlot,
        game.iDependency,
        game.holes,
    ) = analyze(game.board, cleared_lines=0, print_values_to_viewer=True)


def run_game(game, use_gui):
    if use_gui:
        viewer = TetrisBoardViewer(
            game.board,
            game.stats,
            game.queue,
            game.no_s_z_first_piece_signal,
            game.slow_mode,
            game.seed,
            game.aggregate,
            game.clearedLines,
            game.bumpiness,
            game.blockade,
            game.tetrisSlot,
            game.iDependency,
            game.holes,
            game.stats.pieces_placed,
            game.control_mode,
            game.held_piece,
        )
        t = threading.Thread(target=game.game_loop, args=(viewer,), daemon=True)
        t.start()

        viewer.mainloop()
        viewer.running = False
    else:
        game.start_signal[0] = True
        game.game_loop(None)


def main():
    args = parse_args()

    game = TetrisGame(seed=resolve_seed(args))
    use_gui = apply_rules(game, args)
    initialize_heuristics(game)
    run_game(game, use_gui)


if __name__ == "__main__":
    main()

# IMPORTANT:
# - the game loop will stop if no valid placement is found
# - stats.pps can be used in other modules (for display in the viewer).
# - if the best piece placeemnt path is not found, things may not be handled correctly                          !!!!!!!!!
# TODO:
# - add more advanced scoring/evaluation for moves.
# - implement perfect clear solver/mode.
# - improve stack flatness/height evaluation for better bot performance.
# - improve the code working in a way that its usable on console, i look at it like this
# just make it work normally but do sth like, if there is a line clear,make it pink in console (assuming everything else is colored)
# and then next move just removes that line
