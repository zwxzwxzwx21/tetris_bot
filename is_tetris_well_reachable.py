
from board_operations.stack_checking import count_minos


def is_tetris_well_reachable(board,queue,col ,index_of_top_well , spaces_above_the_well): # dont think we need col
    blocks_to_fill_to_reach_well = count_minos(board,  index_of_top_well-spaces_above_the_well,index_of_top_well)
    board_messines = calculate_board_messiness(board, index_of_top_well-spaces_above_the_well,index_of_top_well)
    if blocks_to_fill_to_reach_well <= :
        return True