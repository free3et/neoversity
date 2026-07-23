from insertion_sort import insertion_sort
from merge_sort import merge_sort
from merge_sort import merge

minRUN = 32

# merge two sorted lists in place
def merge_in_place(arr, left, mid, right):
    left_part = arr[left:mid + 1]
    right_part = arr[mid + 1:right + 1]
    merged = merge(left_part, right_part)

    for idx, value in enumerate(merged):
        arr[left + idx] = value

# Calculate minimum run length
def calc_min_run(n):
    r = 0
    while n >= minRUN:
        if n % 2:  # if n is odd, set r to 1
            r = 1
        n //= 2
    return n + r

def tim_sort(arr):
    n = len(arr)
    min_run = calc_min_run(n)
    
    # Step 1: Sort individual sub-arrays of size min_run
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1) # end of the sub-array
        insertion_sort(arr, start, end) # sort the sub-array
        
    # Step 2: Merge sorted runs together
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            
            if mid < right:
                merge_in_place(arr, left, mid, right)

        size *= 2

    return arr