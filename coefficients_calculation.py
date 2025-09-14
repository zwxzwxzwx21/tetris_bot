import os 
import pandas as pd

def save_game_stats(uneven_loss, holes_punishment, height_diff_punishment, 
                   attack_bonus, lines_cleared, total_attack, seed):
    
    filepath = "bruteforcer_stats.xlsx"
    
    new_data = {
        "uneven_loss": [uneven_loss],
        "holes_punishment": [holes_punishment],
        "height_diff_punishment": [height_diff_punishment],
        "attack_bonus": [attack_bonus],
        "lines_cleared": [lines_cleared],
        "total_attack": [total_attack],
        "seed": [seed],
        "attack_per_line": [total_attack / max(1, lines_cleared)]  
    }
    
    new_df = pd.DataFrame(new_data)
    
    if os.path.exists(filepath):
        existing_df = pd.read_excel(filepath)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df
    
    updated_df.to_excel(filepath, index=False)
    print(f"Stats saved to {filepath}, row #{len(updated_df)}")
    
    return len(updated_df)
