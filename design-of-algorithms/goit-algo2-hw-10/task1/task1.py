import random
import time
import matplotlib.pyplot as plt

def randomized_quick_sort(arr):
    # Якщо масив має менше двох елементів, він вже відсортований
    if len(arr) < 2:
        return arr

    # Вибираємо випадковий індекс для опорного елемента
    pivot_index = random.randint(0, len(arr) - 1)
    pivot = arr[pivot_index]

    # Розділяємо масив на частини
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # Рекурсивно сортуємо ліву і праву частини, а потім об'єднуємо
    return randomized_quick_sort(left) + middle + randomized_quick_sort(right)

def deterministic_quick_sort(arr):
    # Якщо масив має менше двох елементів, він вже відсортований
    if len(arr) < 2:
        return arr

    # Вибираємо опорний елемент за фіксованим правилом: перший, останній або середній елемент
    pivot = arr[0]

    # Розділяємо масив на частини
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # Рекурсивно сортуємо ліву і праву частини, а потім об'єднуємо
    return deterministic_quick_sort(left) + middle + deterministic_quick_sort(right)

# Розміри тестових масивів
sizes = [10_000, 50_000, 100_000, 500_000]

# Кількість повторень для кожного розміру
repetitions = 5

randomized_times = []
deterministic_times = []


for size in sizes:
    print(f"\nРозмір масиву: {size}")

    randomized_total = 0
    deterministic_total = 0

    for i in range(repetitions):
        # Створюємо випадковий масив потрібного розміру
        arr = [random.randint(1, 1_000_000) for _ in range(size)]

        # Рандомізований QuickSort
        start = time.perf_counter()
        sorted_arr_randomized = randomized_quick_sort(arr)
        randomized_time = time.perf_counter() - start

        # Детермінований QuickSort
        start = time.perf_counter()
        sorted_arr_deterministic = deterministic_quick_sort(arr)
        deterministic_time = time.perf_counter() - start

        randomized_total += randomized_time
        deterministic_total += deterministic_time

    # Обчислюємо середній час
    randomized_average = randomized_total / repetitions
    deterministic_average = deterministic_total / repetitions

    randomized_times.append(randomized_average)
    deterministic_times.append(deterministic_average)

    print(f"Рандомізований QuickSort: {randomized_average:.4f} секунд")
    print(f"Детермінований QuickSort: {deterministic_average:.4f} секунд")

# Виведення таблиці результатів
print("\n" + "=" * 65)
print("ТАБЛИЦЯ РЕЗУЛЬТАТІВ")
print("=" * 65)
print(f"{'Розмір':<15}{'Рандомізований':<25}{'Детермінований':<25}")
print("-" * 65)

for size, random_time, deterministic_time in zip(
    sizes, randomized_times, deterministic_times
):
    print(
        f"{size:<15}"
        f"{random_time:<25.4f}"
        f"{deterministic_time:<25.4f}"
    )

# Побудова графіка
plt.figure(figsize=(10, 6))

plt.plot(
    sizes,
    randomized_times,
    marker="o",
    label="Рандомізований QuickSort"
)

plt.plot(
    sizes,
    deterministic_times,
    marker="o",
    label="Детермінований QuickSort"
)

plt.xlabel("Розмір масиву")
plt.ylabel("Середній час виконання (секунди)")
plt.title("Порівняння рандомізованого та детермінованого QuickSort")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

'''
Приклад виведення в термінал виконання програми
    Розмір масиву: 10000
    Рандомізований QuickSort: 0.0087 секунд
    Детермінований QuickSort: 0.0075 секунд

    Розмір масиву: 50000
    Рандомізований QuickSort: 0.0484 секунд
    Детермінований QuickSort: 0.0449 секунд

    Розмір масиву: 100000
    Рандомізований QuickSort: 0.1033 секунд
    Детермінований QuickSort: 0.0940 секунд

    Розмір масиву: 500000
    Рандомізований QuickSort: 0.6107 секунд
    Детермінований QuickSort: 0.5583 секунд

=================================================================
ТАБЛИЦЯ РЕЗУЛЬТАТІВ
=================================================================
Розмір         Рандомізований           Детермінований           
-----------------------------------------------------------------
10000          0.0087                   0.0075                   
50000          0.0484                   0.0449                   
100000         0.1033                   0.0940                   
500000         0.6107                   0.5583          
'''