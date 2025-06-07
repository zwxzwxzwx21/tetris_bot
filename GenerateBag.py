import random

TETROMINOES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']

def create_bag(bag_size=7, no_s_z_first_piece=False): # Default for flag is False
    """
    Create and shuffle a new bag of tetrominoes of a given size.
    If no_s_z_first_piece (checkbox flag) is True, attempts to avoid:
    1. S/Z as the first piece.
    2. O as the first piece, followed by S/Z as the second.
    """
    # Create and shuffle the bag
    if bag_size == 7: # Standard 7-bag (one of each piece)
        bag = list(TETROMINOES)
        random.shuffle(bag)
    else: # For other bag sizes, fill by extending and truncating
        bag = []
        temp_tetrominoes_for_extension = list(TETROMINOES)
        while len(bag) < bag_size:
            random.shuffle(temp_tetrominoes_for_extension) # Shuffle before each extension for variety
            bag.extend(temp_tetrominoes_for_extension)
        bag = bag[:bag_size]
        # Final shuffle for non-7-bags or if extended multiple times

    if no_s_z_first_piece and bag: # Checkbox is on and bag is not empty
        original_bag_for_logging = list(bag) # Keep a copy for logging if changes are made
        made_a_change_this_call = False

        # --- Rule 1: Avoid S/Z as the first piece ---
        if bag[0] in ('S', 'Z'):
            swapped_rule1 = False
            # Try to swap bag[0] with a non-S/Z piece from the rest of the bag
            for i in range(1, len(bag)):
                if bag[i] not in ('S', 'Z'):
                    bag[0], bag[i] = bag[i], bag[0] # Perform swap
                    print(f"Avoidance Rule 1: Initial S/Z '{original_bag_for_logging[0]}' at start. Swapped with '{bag[0]}'.")
                    print(f"   Original Bag: {original_bag_for_logging}")
                    print(f"   New Bag:      {bag}")
                    swapped_rule1 = True
                    made_a_change_this_call = True
                    break
            if not swapped_rule1:
                print(f"Avoidance Rule 1: S/Z '{bag[0]}' at start, but no non-S/Z piece found to swap. Bag remains: {bag}")

        # --- Rule 2: Avoid 'O' first, then 'S'/'Z' second ---
        # This check is performed *after* Rule 1 might have altered bag[0].
        if len(bag) > 1 and bag[0] == 'O' and bag[1] in ('S', 'Z'):
            problematic_second_piece = bag[1]
            swapped_rule2 = False
            # Try to swap bag[1] (the S/Z piece) with a non-S/Z piece from bag[2:]
            for i in range(2, len(bag)):
                if bag[i] not in ('S', 'Z'):
                    bag[1], bag[i] = bag[i], bag[1] # Perform swap
                    print(f"Avoidance Rule 2: 'O {problematic_second_piece}' sequence. Swapped '{problematic_second_piece}' with '{bag[1]}'.")
                    # If Rule 1 also made a change, original_bag_for_logging is from before Rule 1.
                    # For clarity, print current state before this specific swap if Rule 1 happened.
                    if made_a_change_this_call and not swapped_rule1: # This means Rule 1 didn't log its change yet for this sequence
                         print(f"   Bag before Rule 2 swap (after potential Rule 1): {original_bag_for_logging}") # This might be confusing
                    elif not made_a_change_this_call : # Rule 1 did not run or did not change
                         print(f"   Original Bag: {original_bag_for_logging}")

                    print(f"   New Bag:      {bag}")
                    swapped_rule2 = True
                    made_a_change_this_call = True # Ensure this is set
                    break
            if not swapped_rule2:
                print(f"Avoidance Rule 2: 'O {problematic_second_piece}' sequence, no non-S/Z piece from bag[2:] to swap. Bag remains: {bag}")
        
        # No need for the old "Bag after reversing" print.
        # The specific prints above will indicate if changes were made.

    return bag

def add_piece_from_bag(queue, bag, no_s_z_first_piece, min_bag_size=4, bag_size=7, num_pieces=1):
    """
    Pops num_pieces from the bag and adds them to the queue.
    If the bag needs refilling, creates a new one using the no_s_z_first_piece flag.
    Returns the updated queue and bag.
    """

    # Condition to refill: if bag doesn't have enough for current request + maintaining min_bag_size buffer
    # alternatively: if current bag < (num_pieces + min_bag_size)
    while len(bag) < num_pieces + min_bag_size: # Ensure enough for current request and buffer
        new_bag_pieces = create_bag(bag_size=bag_size, no_s_z_first_piece=no_s_z_first_piece)
        if not new_bag_pieces: # Safety break if create_bag returns empty
            break
        bag.extend(new_bag_pieces)
        
    pieces_added_this_call = 0
    for _ in range(num_pieces):
        if not bag: # Cannot pop from an empty bag
            break
        piece = bag.pop(0) # Pop from the front (FIFO for bag into queue)
        queue.append(piece)
        pieces_added_this_call += 1
        
    return queue, bag