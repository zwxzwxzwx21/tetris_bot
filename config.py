PRINT_MODE = False
DESIRED_QUEUE_PREVIEW_LENGTH = 5
das_delay = 8  # 0.16s before repeat starts
arr_delay = 0   # 0s between moves after DAS activates

das_state = {
    'left': {'held_frames': 0, 'arr_counter': 0, 'charged': False},
    'down': {'held_frames': 0, 'arr_counter': 0, 'charged': False},
    'right': {'held_frames': 0, 'arr_counter': 0, 'charged': False}
}