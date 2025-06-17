import pygame
import numpy as np
from utility.pieces import PIECES
import time
from utility.print_board import print_board
class TetrisBoardViewer:
    """
    This class is useful for visualizing the board state,
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

    def __init__(self, board, stats_obj, start_signal_list, queue_ref, game_over_signal_list, no_s_z_first_piece_signal_list): # Added new signal
        """
        Initializes the viewer window and sets up colors and board state.

        Args:
            board (list of lists): The initial 20x10 Tetris board (list of lists or numpy array).
            stats_obj (GameStats): The shared game statistics object.
            start_signal_list (list): The shared list for the start signal.
            queue_ref (list): Reference to the shared piece queue.
        """
        
        
        self.GUI_mode = True  # if false, everything will be printed on console, without GUI
        if self.GUI_mode:
            pygame.init()
            pygame.font.init() 
        self.board = np.array(board)
        self.stats = stats_obj
        self.start_signal = start_signal_list
        self.queue_ref = queue_ref
        self.game_over_signal = game_over_signal_list
        self.no_s_z_first_piece_signal = no_s_z_first_piece_signal_list 

        self.ui_start_time = pygame.time.get_ticks()

        self.colors = {
            'T': (128, 0, 128), 'I': (0, 255, 255), 'O': (255, 255, 0),
            'S': (0, 255, 0), 'Z': (255, 0, 0), 'J': (0, 0, 255),
            'L': (255, 165, 0), ' ': (0, 0, 0)
        }
        self.cell_size = 30
        self.board_width = 10 * self.cell_size
        self.side_panel_width = self.board_width
        
        window_width = self.board_width + 2 * self.side_panel_width
        self.window_height = 20 * self.cell_size
        if self.GUI_mode:
            self.screen = pygame.display.set_mode((window_width, self.window_height))
            pygame.display.set_caption("Tetris Bot")
            self.clock = pygame.time.Clock()
        if self.GUI_mode:
            try:
                self.font = pygame.font.SysFont('Arial', 24)
                self.button_font = pygame.font.SysFont('Arial', 28)
                self.input_font = pygame.font.SysFont('Arial', 22)
                self.game_over_font = pygame.font.SysFont('Arial', 72)
            except pygame.error:
                print("Arial font not found, using default Pygame font.")
                self.font = pygame.font.Font(None, 28)
                self.button_font = pygame.font.Font(None, 32)
                self.input_font = pygame.font.Font(None, 26)
                self.game_over_font = pygame.font.Font(None, 80)

        # --- Start Button properties ---
       
        self.start_button_x = 20  
        self.start_button_y = (self.window_height - 50) // 2 - 30 
        
        start_button_width = self.side_panel_width - 40
        start_button_height = 50
        self.start_button_rect = pygame.Rect(
            self.start_button_x, 
            self.start_button_y, 
            start_button_width, 
            start_button_height
        )
        self.start_button_color = (0, 150, 0)
        self.start_button_hover_color = (0, 200, 0)
        self.start_button_text_color = (255, 255, 255)
        self.button_visible = True

        # --- Queue display count input field properties ---
        self.input_label_text = "Queue items (0-9):"
        input_field_width = 40
        input_field_height = 30

        self.input_field_x = 100  
        self.input_field_y = 100 

        self.input_rect = pygame.Rect(
            self.input_field_x,
            self.input_field_y,
            input_field_width,
            input_field_height
        )
        self.input_text = ''
        self.input_active = False
        self.input_color_inactive = pygame.Color('lightskyblue3')
        self.input_color_active = pygame.Color('dodgerblue2')
        self.current_input_color = self.input_color_inactive
        self.num_queue_items_to_display = 5

        # --- Checkbox properties for "No S/Z First" ---
        self.checkbox_label_text = "No S/Z First Piece"
        self.checkbox_size = 20
        self.checkbox_x = self.side_panel_width + self.board_width + 20 
        self.checkbox_y = 50  
        self.checkbox_rect = pygame.Rect(
            self.checkbox_x,
            self.checkbox_y,
            self.checkbox_size,
            self.checkbox_size
        )
        self.checkbox_color = (200, 200, 200) 
        self.checkbox_check_color = (0, 200, 0)

        # Queue display properties
        self.queue_cell_size = 15 
        self.queue_display_area_x = self.side_panel_width + self.board_width 
        self.queue_piece_render_rows = 2 
        self.queue_piece_render_cols = 4  
        self.queue_slot_top_padding_cells = 1
        self.queue_slot_bottom_padding_cells = 1
        self.queue_slot_total_height_cells = (
            self.queue_slot_top_padding_cells +
            self.queue_piece_render_rows +
            self.queue_slot_bottom_padding_cells
        )

    def draw_start_button(self,GUI_mode):
        if self.GUI_mode:
            if not self.button_visible:
                return

            mouse_pos = pygame.mouse.get_pos()
            current_color = self.start_button_color
            if self.start_button_rect.collidepoint(mouse_pos):
                current_color = self.start_button_hover_color
            
            pygame.draw.rect(self.screen, current_color, self.start_button_rect, border_radius=8)
            text_surf = self.button_font.render("Start game", True, self.start_button_text_color)
            text_rect = text_surf.get_rect(center=self.start_button_rect.center)
            self.screen.blit(text_surf, text_rect)
        else: return

    def draw_input_field(self,GUI_mode):
        if self.GUI_mode:
            if not self.button_visible: 
                return

            label_surf = self.input_font.render(self.input_label_text, True, (200, 200, 200))
            label_rect = label_surf.get_rect(centerx=self.input_rect.centerx, bottom=self.input_rect.top - 5)
            self.screen.blit(label_surf, label_rect)

            pygame.draw.rect(self.screen, self.current_input_color, self.input_rect, 2)
            text_surface = self.input_font.render(self.input_text, True, (255, 255, 255))
            
            input_text_rect = text_surface.get_rect(center=self.input_rect.center)
            self.screen.blit(text_surface, input_text_rect)
        else: return
    def draw_checkbox(self,GUI_mode):
        if self.GUI_mode:
            if not self.button_visible: # Only show if start button is visible (i.e., game not started)
                return

            pygame.draw.rect(self.screen, self.checkbox_color, self.checkbox_rect, 2) 

            # Draw the checkmark if checked
            if self.no_s_z_first_piece_signal[0]:
                
                pygame.draw.line(self.screen, self.checkbox_check_color, 
                                (self.checkbox_rect.left + 3, self.checkbox_rect.centery),
                                (self.checkbox_rect.centerx - 2, self.checkbox_rect.bottom - 3), 3)
                pygame.draw.line(self.screen, self.checkbox_check_color,
                                (self.checkbox_rect.centerx - 2, self.checkbox_rect.bottom - 3),
                                (self.checkbox_rect.right - 3, self.checkbox_rect.top + 5), 3)
            
            
            label_surf = self.input_font.render(self.checkbox_label_text, True, (200, 200, 200))
            label_rect = label_surf.get_rect(left=self.checkbox_rect.right + 10, centery=self.checkbox_rect.centery)
            self.screen.blit(label_surf, label_rect)
        else: return
    def draw_game_stats(self,GUI_mode):
        if self.GUI_mode:
            # --- Draw Game Statistics (Left Panel) ---
            y_offset = 10
            line_height = 28 

            # PPS
            pps_text_content = f"PPS: {self.stats.pps:.3f} burst: {(len(self.stats.burst) - 1) / (max(self.stats.burst) - min(self.stats.burst)) if len(self.stats.burst) > 9 else 0:.3f}"
            pps_surface = self.font.render(pps_text_content, True, (255, 255, 255))
            self.screen.blit(pps_surface, (10, y_offset))
            y_offset += line_height

            # Timer (using UI start time, making it still going when you die, need to change that asp)
            elapsed_ui_time_seconds = (pygame.time.get_ticks() - self.ui_start_time) / 1000.0
            timer_text_content = f"UI Time: {elapsed_ui_time_seconds:.3f}s"
            timer_surface = self.font.render(timer_text_content, True, (255, 255, 255))
            self.screen.blit(timer_surface, (10, y_offset))
            y_offset += line_height * 1.5

            stats_texts = [
                f"Singles: {self.stats.single}",
                f"Doubles: {self.stats.double}",
                f"Triples: {self.stats.triple}",
                f"Tetrises: {self.stats.tetris}"
            ]
            for text_content in stats_texts:
                stat_surface = self.font.render(text_content, True, (255, 255, 255))
                self.screen.blit(stat_surface, (10, y_offset))
                y_offset += line_height

            # here would be hold piece

        else: 
            print("Game Statistics:")
            print(f"PPS: {self.stats.pps:.3f} burst: {(len(self.stats.burst) - 1) / (max(self.stats.burst) - min(self.stats.burst)) if len(self.stats.burst) > 9 else 0:.3f}")
            elapsed_ui_time_seconds = (pygame.time.get_ticks() - self.ui_start_time) / 1000.0
            print(f"UI Time: {elapsed_ui_time_seconds:.3f}s")
            print(f"Singles: {self.stats.single}")
            print(f"Doubles: {self.stats.double}")
            print(f"Triples: {self.stats.triple}")
            print(f"Tetrises: {self.stats.tetris}")
    def draw_queue_display(self,GUI_mode):
        if self.GUI_mode:
            # --- Draw Queue Display (Right Panel) ---
            if self.num_queue_items_to_display == 0: # If 0, don't draw queue pieces
                
                label_surface = self.font.render("Queue", True, (255, 255, 255))
                label_rect = label_surface.get_rect(
                    centerx=(self.queue_display_area_x + self.side_panel_width / 2),
                    top=10
                )
                self.screen.blit(label_surface, label_rect)
                return

            y_current_slot_start_px = 10 

            
            label_surface = self.font.render("Queue", True, (255, 255, 255))
            label_rect = label_surface.get_rect(
                centerx=(self.queue_display_area_x + self.side_panel_width / 2),
                top=y_current_slot_start_px
            )
            self.screen.blit(label_surface, label_rect)
            y_current_slot_start_px += label_surface.get_height() + 10  

        
            for i in range(min(self.num_queue_items_to_display, len(self.queue_ref))): 
                piece_char = self.queue_ref[i]

                if piece_char not in PIECES or 'flat' not in PIECES[piece_char]:
                    y_current_slot_start_px += self.queue_slot_total_height_cells * self.queue_cell_size
                    continue

                piece_shape = PIECES[piece_char]['flat']
                shape_actual_height_cells = len(piece_shape)
                shape_actual_width_cells = len(piece_shape[0]) if shape_actual_height_cells > 0 else 0

                display_box_width_px = self.queue_piece_render_cols * self.queue_cell_size
                display_box_start_x_px = self.queue_display_area_x + (self.side_panel_width - display_box_width_px) / 2

                piece_drawing_area_y_px = y_current_slot_start_px + (self.queue_slot_top_padding_cells * self.queue_cell_size)

                offset_x_in_box_px = (self.queue_piece_render_cols - shape_actual_width_cells) / 2 * self.queue_cell_size
                offset_y_in_box_px = (self.queue_piece_render_rows - shape_actual_height_cells) / 2 * self.queue_cell_size

                for r_idx, row_data in enumerate(piece_shape):
                    for c_idx, cell_content in enumerate(row_data):
                        if cell_content != ' ':
                            mino_color = self.colors.get(piece_char, (128, 128, 128))
                            
                            draw_x = display_box_start_x_px + offset_x_in_box_px + (c_idx * self.queue_cell_size)
                            draw_y = piece_drawing_area_y_px + offset_y_in_box_px + (r_idx * self.queue_cell_size)
                            
                            mino_rect = pygame.Rect(draw_x, draw_y, self.queue_cell_size, self.queue_cell_size)
                            pygame.draw.rect(self.screen, mino_color, mino_rect)
                            pygame.draw.rect(self.screen, (50, 50, 50), mino_rect, 1)

                y_current_slot_start_px += self.queue_slot_total_height_cells * self.queue_cell_size
        else:
            print("Queue Display:")
            if self.num_queue_items_to_display == 0:
                print("Queue: None")
                return
            
            for i in range(min(self.num_queue_items_to_display, len(self.queue_ref))):
                piece_char = self.queue_ref[i]
                if piece_char not in PIECES or 'flat' not in PIECES[piece_char]:
                    continue
                
                piece_shape = PIECES[piece_char]['flat']
                print(f"Piece {i + 1}: {piece_char} - Shape: {piece_shape}")

    def draw_tetris_board_area(self,GUI_mode):
        if self.GUI_mode:
            # --- Draw the Tetris Board (Middle Panel) ---
            for y_idx in range(20):
                for x_idx in range(10):
                    value = self.board[y_idx, x_idx]
                    color = self.colors.get(value, (200, 200, 200))
                    rect = pygame.Rect(
                        self.side_panel_width + (x_idx * self.cell_size),
                        y_idx * self.cell_size,
                        self.cell_size,
                        self.cell_size
                    )
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, (50, 50, 50), rect, 1) 
        else: return
    def draw_board(self,GUI_mode):
        if self.GUI_mode:
            t0 = time.perf_counter()
            self.screen.fill((0, 0, 0))
            if not self.start_signal[0] and not self.game_over_signal[0]: 
                self.draw_start_button(self.GUI_mode)
                self.draw_input_field(self.GUI_mode)
                self.draw_checkbox(self.GUI_mode) 
                
                for y_idx in range(20): 
                    for x_idx in range(10):
                        rect = pygame.Rect(
                            self.side_panel_width + (x_idx * self.cell_size), y_idx * self.cell_size,
                            self.cell_size, self.cell_size)
                        pygame.draw.rect(self.screen, (20, 20, 20), rect, 1)
            elif self.start_signal[0] and not self.game_over_signal[0]: 
                self.draw_game_stats(self.GUI_mode)
                self.draw_tetris_board_area(self.GUI_mode)
                self.draw_queue_display(self.GUI_mode)
            
            pygame.draw.rect(self.screen, (40, 40, 40),
                        pygame.Rect(0, 0, self.side_panel_width, self.window_height), 1)
            pygame.draw.rect(self.screen, (40, 40, 40), # game board area boarder
                        pygame.Rect(self.side_panel_width, 0, self.board_width, self.window_height), 1)
            pygame.draw.rect(self.screen, (40, 40, 40), # right panel border
                        pygame.Rect(self.side_panel_width + self.board_width, 0, 
                                    self.side_panel_width, self.window_height), 1)
                            
            if self.game_over_signal[0]: 
                if self.start_signal[0]:
                    self.draw_game_stats(self.GUI_mode)
                    self.draw_tetris_board_area(self.GUI_mode)
                    self.draw_queue_display(self.GUI_mode)

                overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
                overlay.fill((100, 100, 100, 200))  
                self.screen.blit(overlay, (0, 0))
                
                if self.start_signal[0]: 
                    game_over_text_surf = self.game_over_font.render("no more moves", True, (220, 20, 60))
                    game_over_text_rect = game_over_text_surf.get_rect(center=self.screen.get_rect().center)
                    self.screen.blit(game_over_text_surf, game_over_text_rect)
                            
            pygame.display.flip()
            t1 = time.perf_counter()
            ms = (t1 - t0) * 1000
            if ms > 100:
                print(f"draw_board: {ms:.2f} ms")
        else:
            print("Drawing Tetris Board:")
            print_board(self.board)
            print("End of board display.")
    def update_board(self, new_board_array):
        """Called by the game_loop thread to update the board data."""
        self.board = np.array(new_board_array) # ensure it's a numpy array or it no work ;( 

    def mainloop(self, GUI_mode):
        if self.GUI_mode:
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        if not self.game_over_signal[0]: 
                            self.game_over_signal[0] = True 
                            if self.start_signal[0] == False: 
                                self.start_signal[0] = True

                    if not self.game_over_signal[0]: 
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1: # left mouse button
                                if self.button_visible and self.start_button_rect.collidepoint(event.pos):
                                    print("start button clicked")
                                    if self.input_text.isdigit():
                                        num = int(self.input_text)
                                        if 0 <= num <= 9:
                                            self.num_queue_items_to_display = num
                                        else: 
                                            self.num_queue_items_to_display = 5 
                                    elif not self.input_text: # empty, use default
                                        self.num_queue_items_to_display = 5
                                    else: # nondigit, use default
                                        self.num_queue_items_to_display = 5
                                    
                                    print(f"queue items to display set to: {self.num_queue_items_to_display}")
                                    
                                    self.start_signal[0] = True # signal the game_loop in main.py
                                    self.button_visible = False # hide button after click
                                    self.input_active = False # deactivate input field
                            
                                if self.button_visible and self.input_rect.collidepoint(event.pos):
                                    self.input_active = not self.input_active
                                else:
                                    if self.button_visible: 
                                        self.input_active = False
                                self.current_input_color = self.input_color_active if self.input_active else self.input_color_inactive

                                if self.button_visible and self.checkbox_rect.collidepoint(event.pos):
                                    self.no_s_z_first_piece_signal[0] = not self.no_s_z_first_piece_signal[0]
                                    print(f"Checkbox 'No S/Z First Piece' set to: {self.no_s_z_first_piece_signal[0]}")

                        if event.type == pygame.KEYDOWN:
                            if self.input_active and self.button_visible:
                                if event.key == pygame.K_BACKSPACE:
                                    self.input_text = '' 
                                elif event.unicode.isdigit():
                                    if not self.input_text: 
                                        self.input_text = event.unicode
                
                self.draw_board(self.GUI_mode) # Draw the board and UI elements
                self.clock.tick(60) # Limit FPS 
            # works without it, but its ensuring that the signals are being cut off correctly
            if not self.game_over_signal[0]:
                self.game_over_signal[0] = True
            if not self.start_signal[0]:
                self.start_signal[0] = True

            pygame.quit()   
        else:
            running = True
            while running:
                
                    if not self.game_over_signal[0]: 
                        
                                    if self.input_text.isdigit():
                                        num = int(self.input_text)
                                        if 0 <= num <= 9:
                                            self.num_queue_items_to_display = num
                                        else: 
                                            self.num_queue_items_to_display = 5 
                                    elif not self.input_text: # empty, use default
                                        self.num_queue_items_to_display = 5
                                    else: # nondigit, use default
                                        self.num_queue_items_to_display = 5
                                    
                                    self.start_signal[0] = True # signal the game_loop in main.py
                                    self.button_visible = False # hide button after click
                                    self.input_active = False # deactivate input field
                   
                                
               
                #self.clock.tick(60) # Limit FPS 
            # works without it, but its ensuring that the signals are being cut off correctly
            if not self.game_over_signal[0]:
                self.game_over_signal[0] = True
            if not self.start_signal[0]:
                self.start_signal[0] = True

            