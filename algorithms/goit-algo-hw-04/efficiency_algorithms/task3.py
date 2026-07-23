import random
import timeit

from insertion_sort import insertion_sort
from merge_sort import merge_sort
from tim_sort import tim_sort

ARRAY_SIZE = 1000
numbers = [random.randint(1, 1_000_000) for _ in range(ARRAY_SIZE)]

for repeats in [100, 1_000, 10_000]:
    print(f"--- array size={ARRAY_SIZE}, repeats={repeats} ---")
    print('insertion_sort >>>', timeit.timeit(lambda: insertion_sort(numbers.copy()), number=repeats))
    print('merge_sort >>>', timeit.timeit(lambda: merge_sort(numbers.copy()), number=repeats))
    print('tim_sort >>>', timeit.timeit(lambda: tim_sort(numbers.copy()), number=repeats))
    print('sorted (built-in Timsort) >>>', timeit.timeit(lambda: sorted(numbers.copy()), number=repeats))
    print('--------------------------------')