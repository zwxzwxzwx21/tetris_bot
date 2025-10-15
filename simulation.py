import bruteforcing
import random
#ill do range 0.00 to 5 with random steps 
'''heuristic_params = {
    "uneven_loss": 0.4,
    "holes_punishment": 2,
    "height_diff_punishment": 0.05,
    "attack_bonus": 1,
    "max_height_punishment": 1,
}'''
heuristic_params = {
    "uneven_loss": 1,
    "holes_punishment": 1,
    "height_diff_punishment": 1,
    "attack_bonus": 1,
    "max_height_punishment": 1,
}

def pick_neighbour(params,step_size=0.1):
    new_params = params.copy()
    for param in new_params:
        change = random.uniform(-step_size,step_size)
        new_val = new_params[param] + change
        new_val = max(0.0, min(5.0, new_val)) # thats smart isnt it lol
        new_params[param] = new_val
    return new_params

# idea: run 5/10 games and get avg value of lines cleared, after that we have our E(s)
# then we run new params and get new E(snew)
# if E(snew) <= E(s) we accept new params
# if E(snew) > E(s) we accept new params with probability P = exp(-(E(snew) - E(s)) / T)
# T starts high (100) and goes to 0 over time
# now its p much just write code for making 5-10 games and getting avg lines cleared which wont be hard 

from main import run_bruteforce_games
def E(params, games=10):
    for i in range(games):
        lines = 0

    return lines / games

T = 100
min_temp = 0.1
iteration = 0
max_iterations = 10000
params = heuristic_params.copy()
for iteration in range(max_iterations):
    T = T * (1 - (iteration + 1) / max_iterations)
    new_params = pick_neighbour(params)
    if P(E(params), E(new_params), T) >= random.uniform(0, 1):
        params = new_params


"""Let s = s0
For k = 0 through kmax (exclusive):
    T ← temperature( 1 - (k+1)/kmax )
    Pick a random neighbour, snew ← neighbour(s)
    If P(E(s), E(snew), T) ≥ random(0, 1):
        s ← snew
Output: the final state s"""