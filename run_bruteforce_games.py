import time 
import config
def run_bruteforce_games(params,class_,num_games=3):
    """function used to check how good heurisctic values are
    for X amount of random games,  

    Args:
        params (dict): dictionary containing heuristic parameters
        class_ (class): should be TetrisGame
        num_games (int, optional): number of games to run. Defaults to 3.

    Returns:
        float: average lines cleared per game
    """
    total_lines = 0

    for game_index in range(num_games):
        uneven_loss, holes_punishment, height_diff_punishment, attack_bonus, max_height_punishment = params["uneven_loss"], params["holes_punishment"], params["height_diff_punishment"], params["attack_bonus"], params["max_height_punishment"]
        import bruteforcing
        bruteforcing.uneven_loss = uneven_loss
        bruteforcing.holes_punishment = holes_punishment
        bruteforcing.height_diff_punishment = height_diff_punishment
        bruteforcing.attack_bonus = attack_bonus
        bruteforcing.max_height_punishment = max_height_punishment
        
        seed = time.time_ns() % (2**32 - 1)
        game = class_(seed=seed) # originally there was TetrisGame instead of class_
        
        game.stats.pieces_placed = 0
        
        game.start_signal[0] = True
        pieces = game.game_loop(None)
        if config.PRINT_MODE:
            print(f"pieces: {pieces}")

        lines_cleared= game.stats.single + game.stats.double*2 + game.stats.triple*3 + game.stats.tetris*4
        total_lines += lines_cleared
        if config.PRINT_MODE:
            print(f"lines cleared: {lines_cleared}")
    return total_lines/num_games
