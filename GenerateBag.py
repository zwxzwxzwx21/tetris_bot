import random

TETROMINOES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']

def create_bag(bag_size=15, no_s_z_first_piece=True):
    """
    Create and shuffle a new bag of tetrominoes of given size.
    If no_s_z_first_piece is True, ensures the first piece is not S or Z.
    """
    bag = []
    while len(bag) < bag_size:
        bag.extend(TETROMINOES)
    bag = bag[:bag_size]
    random.shuffle(bag)
    if no_s_z_first_piece and bag and bag[0] in ('S', 'Z'):
        # Find first non-S/Z piece and swap with first
        for i, piece in enumerate(bag):
            if piece not in ('S', 'Z'):
                bag[0], bag[i] = bag[i], bag[0]
                break
    return bag

def add_piece_from_bag(queue, bag, min_bag_size=4, bag_size=7, num_pieces=1, no_s_z_first_piece=True):
    """
    Pops num_pieces from the bag and adds them to the queue.
    If the bag has less than min_bag_size pieces, creates a new one.
    Returns the updated queue and bag.
    """
    while len(bag) < min_bag_size + num_pieces:
        bag.extend(create_bag(bag_size, no_s_z_first_piece=no_s_z_first_piece))
    for _ in range(num_pieces):
        piece = bag.pop()
        queue.append(piece)
    return queue, bag