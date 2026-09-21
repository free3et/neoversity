import random
import time

class Node:
    def __init__(self, key, value):
        self.data = (key, value)
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, key, value):
        new_node = Node(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        return new_node

    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = None
        node.next = None

    def move_to_front(self, node):
        if node != self.head:
            self.remove(node)
            node.next = self.head
            self.head.prev = node
            self.head = node

    def remove_last(self):
        if self.tail:
            last = self.tail
            self.remove(last)
            return last
        return None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.list = DoublyLinkedList()

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.list.move_to_front(node)
            return node.data[1]
        return -1

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.data = (key, value)
            self.list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last:
                    del self.cache[last.data[0]]
            new_node = self.list.push(key, value)
            self.cache[key] = new_node

def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:        # ~3% запитів — Update
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:                                 # ~97% — Range
            if random.random() < p_hot:       # 95% — «гарячі» діапазони
                left, right = random.choice(hot)
            else:                             # 5% — випадкові діапазони
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    return queries

# повертає суму без кешування
def range_sum_no_cache(array, left, right):
    return sum(array[left:right+1])

# повертає суму з кешуванням
def range_sum_with_cache(array, left, right, cache):
    key = (left, right)
    result = cache.get(key)

    if result == -1:
        result = sum(array[left:right+1])
        cache.put(key, result)

    return result

# оновлює елемент без кешування
def update_no_cache(array, index, value):
    array[index] = value

def update_with_cache(array, index, value, cache):
    array[index] = value

    for key in list(cache.cache.keys()):
        left, right = key

        if left <= index <= right:
            node = cache.cache.pop(key)
            cache.list.remove(node)

N = 100000
Q = 50000

array = [random.randint(1, 100) for _ in range(N)]
queries = make_queries(N, Q)

array1 = array.copy()

start = time.perf_counter()

for query in queries:
    if query[0] == "Range": # 
        _, left, right = query
        range_sum_no_cache(array1, left, right)

    else:
        _, index, value = query
        update_no_cache(array1, index, value)

time_no_cache = time.perf_counter() - start

array2 = array.copy()
cache = LRUCache(1000)

start = time.perf_counter()

for query in queries:
    if query[0] == "Range": # Range(L, R) — обчислити суму елементів array[L : R + 1].
        _, left, right = query
        range_sum_with_cache(array2, left, right, cache)

    else:
        _, index, value = query
        update_with_cache(array2, index, value, cache)

time_with_cache = time.perf_counter() - start

print(f"Без кешу : {time_no_cache:.4f} с")
print(f"LRU-кеш  : {time_with_cache:.4f} с")

print(f"Прискорення: ×{time_no_cache / time_with_cache:.6f}")