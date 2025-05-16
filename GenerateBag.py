import random

TETROMINOES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']

def create_bag():
    """Create and shuffle a new 7-bag of tetrominoes."""
    bag = TETROMINOES.copy()  
    random.shuffle(bag)
    return bag

def add_piece_from_bag(queue, bag):
    """
    Pops one piece from the bag and adds it to the queue.
    If the bag is empty, creates a new one.
    Returns the updated queue and bag.
    """
    if not bag:
        bag = create_bag()
    piece = bag.pop()
    queue.append(piece)
    return queue, bag