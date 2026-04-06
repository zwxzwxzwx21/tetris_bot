from utility.print_board import printred
from utility.pieces import PIECES
from config import DESIRED_QUEUE_PREVIEW_LENGTH
from simulate_game_movement import simulate_move
from bruteforcing import find_best_placement
import pygame
import time

    #printred(best_move_str)
def main_viewer(viewer, das_state, das_delay, arr_delay, self):
    if self.weights_updated_event.is_set():
        self.weights_updated_event.clear()
        move_history_with_best_move_info = find_best_placement(
            self.board, self.queue[:DESIRED_QUEUE_PREVIEW_LENGTH], self.stats.combo, self.stats, self.held_piece
        )
        if move_history_with_best_move_info:
            move_history, best_move_str, goal_y_pos, used_hold = move_history_with_best_move_info
            best_move_str_original = best_move_str
            if self.no_calculation_mode:
                best_move_str = f"{self.queue[0]}_4_flat_0"
                goal_y_pos = 1
            else:
                best_move_str = best_move_str_original

            piece_type, x_str, rotation1,rotation2 = best_move_str.split("_")
            rotation  = rotation1 + "_" + rotation2
            x = int(x_str[1:])
            piece_type_placed = piece_type
            piece_shape = PIECES[piece_type_placed][rotation]
            viewer.set_preview(piece_type_placed, piece_shape, x, self.board,rotation,held_piece=self.held_piece,yvalue=goal_y_pos,control_mode=self.control_mode)
            viewer.update_board(self.board)

    self.held_piece = None if self.held_piece is None else self.held_piece
    change_held_piece_flag = False
    #printgreen(f"best move str: {best_move_str}")
    piece_type, x_str, rotation1,rotation2 = best_move_str.split("_")
    #printred(f"{piece_type}, {x_str}, {rotation1},{rotation2}")
    rotation  = rotation1 + "_" + rotation2
    #print(x_str)

    x = int(x_str[1:])
    piece_type_placed = self.queue[0]

    piece_shape = PIECES[piece_type_placed][rotation]
    #print(piece_type_placed, piece_shape, x,rotation)
    key_pressed  = viewer.get_key_pressed()
    key_held = viewer.get_key_held()


    left_held = key_held == pygame.K_LEFT
    right_held = key_held == pygame.K_RIGHT
    down_held = key_held == pygame.K_DOWN
    #region
    if left_held:
        das_state['left']['held_frames'] += 1
        
        if das_state['left']['held_frames'] >= das_delay:
            das_state['left']['charged'] = True
            
    else:
        das_state['left'] = {'held_frames': 0, 'arr_counter': 0, 'charged': False}

    if down_held:
        das_state['down']['held_frames'] += 1
        
        if das_state['down']['held_frames'] >= das_delay:
            das_state['down']['charged'] = True
            
    else:
        das_state['down'] = {'held_frames': 0, 'arr_counter': 0, 'charged': False}

    if right_held:
        das_state['right']['held_frames'] += 1
        if das_state['right']['held_frames'] >= das_delay:
            das_state['right']['charged'] = True
            
    else:
        das_state['right'] = {'held_frames': 0, 'arr_counter': 0, 'charged': False}

    das_move_left = False
    das_move_right = False
    das_move_down = False

    if das_state['left']['charged']:
        das_state['left']['arr_counter'] += 1
        if das_state['left']['arr_counter'] >= arr_delay:
            das_move_left = True
            das_state['left']['arr_counter'] = 0
            
    if das_state['right']['charged']:
        das_state['right']['arr_counter'] += 1
        if das_state['right']['arr_counter'] >= arr_delay:
            das_move_right = True
            das_state['right']['arr_counter'] = 0
            
    if down_held and das_state['down']['charged']:
        das_state['down']['arr_counter'] += 1
        if das_state['down']['arr_counter'] >= arr_delay:
            das_move_down = True
            das_state['down']['arr_counter'] = 0
            
    das_info = {'left': das_move_left, 'right': das_move_right, 'down': das_move_down}
    #endregion
    self.board, best_move_str, goal_y_pos, last_key, a, change_held_piece_flag, self.no_calculation_mode = simulate_move(self.board, best_move_str,goal_y_pos, key_pressed,self.held_piece, das_info, self.queue, self.no_calculation_mode, up_y_movement = True)

    if change_held_piece_flag:
        
        if self.held_piece is None:
            self.held_piece = self.queue[0]
            self.queue.pop(0)
            
        else:
            temp_hold_piece = self.held_piece
            self.held_piece = self.queue[0]
            self.queue[0] = temp_hold_piece
        change_held_piece_flag = False
    # piece_shape arg is not even used
    viewer.set_preview(piece_type_placed, piece_shape, x, self.board,rotation,held_piece=self.held_piece,yvalue=goal_y_pos,control_mode=self.control_mode)
    viewer.update_board(self.board)

    if last_key == pygame.K_SPACE:
        break_loop = True
    elif last_key == pygame.K_q:
        #printyellow(f'queue: {self.queue} current peice : {self.queue[0]}')

        move_history_with_best_move_info = find_best_placement(
            self.board, self.queue[:DESIRED_QUEUE_PREVIEW_LENGTH], self.stats.combo, self.stats, self.held_piece
        )
        
        move_history, best_move_str,goal_y_pos, used_hold = move_history_with_best_move_info
        best_move_str_original = best_move_str
        #printyellow(f'new best move: {best_move_str} at y pos {goal_y_pos}')
        #best_move_str = f"{self.queue[0]}_4_flat_0"
        if self.no_calculation_mode:
            best_move_str = f"{self.queue[0]}_4_flat_0"
            goal_y_pos = 1

        else:
            best_move_str = best_move_str_original
        #goal_y_pos = 1 if self.no_calculation_mode else goal_y_pos
        
        try:
            x = int(x_str[1:])
        except ValueError:
            x = int(x_str)
        viewer.set_preview(piece_type_placed, piece_shape, x, self.board,rotation,held_piece=self.held_piece,yvalue=goal_y_pos,control_mode=self.control_mode)
        viewer.update_board(self.board)

        
    time.sleep(0.016)

    # heuristic checks

    from heuristic import aggregate,bumpiness,blockade,tetrisSlot,check_holes2,iDependency,analyze

