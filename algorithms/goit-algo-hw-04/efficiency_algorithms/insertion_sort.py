# insertion sort
def insertion_sort(lst, left=0, right=None):
    if right is None:
        right = len(lst) - 1

    for cur_idx in range(left + 1, right + 1):
        key = lst[cur_idx]
        prev_idx = cur_idx - 1
        while prev_idx >= left and key < lst[prev_idx]:
            lst[prev_idx + 1] = lst[prev_idx]
            prev_idx -= 1
        lst[prev_idx + 1] = key
    return lst