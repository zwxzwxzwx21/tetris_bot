from utility.boxes import sequences  # Assume BOXES is a list of lists, e.g. [['i', 'o', 'o'], ...]

def find_box_in_queue(queue, boxes=sequences):
    """
    Finds the first box from boxes that appears in queue
    # i have a feeling this can be done more efficiently, however we are not gonna
    # use this one besides 40l so i dont care that much 
    """
    # i dont feel like using that at all tbh, makes no sense to me why making a bot just for 40l at all leaving cuz why not
    for box in boxes:
        box_indices = []
        q_idx = 0
        for piece in box:
            while q_idx < len(queue) and queue[q_idx] != piece:
                q_idx += 1
            if q_idx == len(queue):
                break  # This box is not present in queue
            box_indices.append(q_idx)
            q_idx += 1
        if len(box_indices) == len(box):
            # Split queue into box_queue and remaining_queue
            box_queue = [queue[i] for i in box_indices]
            remaining_queue = [queue[i] for i in range(len(queue)) if i not in box_indices]
            return remaining_queue, box_queue
    return queue, []
