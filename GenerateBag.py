import random

TETROMINOES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']

def create_bag(bag_size=7, no_s_z_first_piece=False, custom_bag=False):
    """
    create and shuffle a new bag of minoes of a given size
    if no_s_z_first_piece (checkbox flag) is true, attempts to avoid:
    1. s/z as the first piece.
    2. o as the first piece, followed by s/z as the second.
    """

    if custom_bag:
        return ['T', 'O', 'I', 'S', 'Z', 'J', 'L'] # edit as needed, idk how it would work with smaller, bigger bags

    if bag_size == 7: 
        bag = list(TETROMINOES)
        random.shuffle(bag)
    else: # For other bag sizes, fill by extending and truncating
        bag = []
        temp_tetrominoes_for_extension = list(TETROMINOES)
        while len(bag) < bag_size:
            random.shuffle(temp_tetrominoes_for_extension) 
            bag.extend(temp_tetrominoes_for_extension)
        bag = bag[:bag_size]

    if no_s_z_first_piece and bag: 

        # --- rule 1 avoid s/z as the first piece ---
        if bag[0] in ('S', 'Z'):
            # try to swap bag[0] with a non s z piece from the rest of the bag
            for i in range(1, len(bag)):
                if bag[i] not in ('S', 'Z'):
                    bag[0], bag[i] = bag[i], bag[0]
                    break

        # --- rule 2 avoid 'O' first, then s/z second ---
        # this check is performed after rule 1 might have altered bagp[0]
        if len(bag) > 1 and bag[0] == 'O' and bag[1] in ('S', 'Z'):
            # Try to swap bag[1] (the s/z piece) with a non-s/z piece from bag[2:]
            for i in range(2, len(bag)):
                if bag[i] not in ('S', 'Z'):
                    bag[1], bag[i] = bag[i], bag[1]
                    break

    return bag

def add_piece_from_bag(queue, bag, no_s_z_first_piece, min_bag_size=4, bag_size=7, num_pieces=1):
    """
    Pops num_pieces from the bag and adds them to the queue.
    If the bag needs refilling, creates a new one using the no_s_z_first_piece flag.
    Returns the updated queue and bag.
    """

    # condition to refill: if bag doesn't have enough for current request + maintaining min_bag_size buffer
    # alternatively: if current bag < (num_pieces + min_bag_size)
    while len(bag) < num_pieces + min_bag_size: 
        new_bag_pieces = create_bag(bag_size=bag_size, no_s_z_first_piece=no_s_z_first_piece)
        if not new_bag_pieces: 
            break
        bag.extend(new_bag_pieces)
        
    pieces_added_this_call = 0
    for _ in range(num_pieces):
        if not bag: 
            break
        piece = bag.pop(0)
        queue.append(piece)
        pieces_added_this_call += 1
        
    return queue, bag