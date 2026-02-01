import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tetrio_parsing.calculate_attack import attack_simplified

attack = attack_simplified('tetris',7)
print(attack)