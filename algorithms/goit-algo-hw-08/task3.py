import heapq

def min_cost_to_connect_cables(lengths): # знаходження мінімальних витрат на з'єднання кабелів
    if len(lengths) <= 1:
        return 0

    heap_copy = lengths[:]
    heapq.heapify(heap_copy) # створення мінімальної купи з довжин кабелів
    total_cost = 0
    
    while len(heap_copy) > 1:
        first_smallest = heapq.heappop(heap_copy)
        second_smallest = heapq.heappop(heap_copy)
        cost = first_smallest + second_smallest # вартість з'єднання двох кабелів
        total_cost += cost
        heapq.heappush(heap_copy, cost) # додавання з'єднаного кабелю до купи
    return total_cost

print(min_cost_to_connect_cables([1, 2, 3, 4, 5]))