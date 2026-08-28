def find_min_max(arr):
    if len(arr) == 1:
        return arr[0], arr[0]
    
    mid = len(arr) // 2
    left = arr[:mid]    # ліва половина масиву
    right = arr[mid:]   # права половина масиву
    left_min, left_max = find_min_max(left) # мінімум і максимум лівої половинки
    right_min, right_max = find_min_max(right) # мінімум і максимум правої половинки
    return min(left_min, right_min), max(left_max, right_max) # мінімум і максимум всього масиву

print(find_min_max([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
print(find_min_max([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]))
print(find_min_max([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))
print(find_min_max([10, 10, 10, 10, 10, 10, 10, 10, 10, 10]))
print(find_min_max([11, 222, 3, 4000, 52, 622, 77, 85, 9, 10]))
print(find_min_max([10, 99, 81, 7, 6, 15, 4, 33]))
