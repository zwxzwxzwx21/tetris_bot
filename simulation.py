# idea: run 5/10 games and get avg value of lines cleared, after that we have our E(s)
# then we run new params and get new E(snew)
# if E(snew) <= E(s) we accept new params
# if E(snew) > E(s) we accept new params with probability P = exp(-(E(snew) - E(s)) / T)
# T starts high (100) and goes to 0 over time
# now its p much just write code for making 5-10 games and getting avg lines cleared which wont be hard 

import bruteforcing
import random
import math
'''heuristic_params = {
    "uneven_loss": 0.4,
    "holes_punishment": 2,
    "height_diff_punishment": 0.05,
    "attack_bonus": 1,
    "max_height_punishment": 1,
}'''
'''heuristic_params = {
    "uneven_loss": 0.978169566086124,
    "holes_punishment": 1.548520543539411,
    "height_diff_punishment": 0.19829854187486598,
    "attack_bonus": 1.199324363469116,
    "max_height_punishment": 0.6259050858276255,
}'''
heuristic_params = {
    "uneven_loss": 1.5035072207505125,
    "holes_punishment": 1.4133498342617155,
    "height_diff_punishment": 0.08169071129276936,
    "attack_bonus": 2.312996860233956,
    "max_height_punishment": 0.45217681702487916,
}
def pick_neighbour(params,step_size=0.3):
    new_params = params.copy()
    params_to_tweak = random.sample(list(new_params.keys()), k=random.randint(1, len(new_params)))
    for param in params_to_tweak:
        change = random.uniform(-step_size,step_size)
        new_val = new_params[param] + change
        new_val = max(0.0, min(10.0, new_val)) 
        new_params[param] = new_val
    #print(f"NEIGHBOUR uneven: {params["uneven_loss"]}, holes: {params["holes_punishment"]}, height diff: {params["height_diff_punishment"]}, attack: {params["attack_bonus"]}, max height: {params["max_height_punishment"]}")

    return new_params

from main import run_bruteforce_games
def E(params, games=10):
    print(f"uneven: {params["uneven_loss"]}, holes: {params["holes_punishment"]}, height diff: {params["height_diff_punishment"]}, attack: {params["attack_bonus"]}, max height: {params["max_height_punishment"]}")
    total_lines = 0
    for i in range(games):
        print(f" ===Game {i+1}=== ",)
        lines = run_bruteforce_games(params, 1) # 1 game per call
        total_lines += lines
        print(f"Game {i+1} cleared {lines} lines")
    avg_lines = total_lines / games
    print(f"Average lines cleared: {avg_lines}")
    return avg_lines

def P(E_s, E_snew, T):
    if E_snew >= E_s:  
        return 1.0
    else:  
        diff = (E_snew - E_s) / T
        if diff > 700:
            return 0.0
        return math.exp(-diff)

T = 100
min_temp = 0.5
iteration = 0
max_iterations = 500
params = heuristic_params.copy()
best_params = params.copy()
best_score = E(params)
for iteration in range(max_iterations):
    T = T * (1 - (iteration + 1) / max_iterations)    
    if T < min_temp:
        break
    new_params = pick_neighbour(params)

    E_current = E(params)
    E_new = E(new_params)
    
    if P(E_current, E_new, T) >= random.uniform(0, 1):
        params = new_params
        print(f"\n Iteration {iteration}: ACCEPTED (T={T:.2f})")
        
        if E_new > best_score:
            best_score = E_new
            best_params = new_params.copy()
            print(f"  NEW BEST: {best_score:.1f} lines!")
    else:
        print(f"\n Iteration {iteration}: rejected (T={T:.2f})")

    print("Current params: uneven", params["uneven_loss"], "holes", params["holes_punishment"], "height diff", params["height_diff_punishment"], "attack", params["attack_bonus"], "max height", params["max_height_punishment"])
    print("New params: uneven", new_params["uneven_loss"], "holes", new_params["holes_punishment"], "height diff", new_params["height_diff_punishment"], "attack", new_params["attack_bonus"], "max height", new_params["max_height_punishment"])


"""Let s = s0
For k = 0 through kmax (exclusive):
    T ← temperature( 1 - (k+1)/kmax )
    Pick a random neighbour, snew ← neighbour(s)
    If P(E(s), E(snew), T) ≥ random(0, 1):
        s ← snew
Output: the final state s"""