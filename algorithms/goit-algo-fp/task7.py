'''
Завдання 7. Використання методу Монте-Карло

Необхідно написати програму на Python, яка імітує велику кількість кидків кубиків, обчислює суми чисел, які випадають на кубиках, і визначає ймовірність кожної можливої суми.

Створіть симуляцію, де два кубики кидаються велику кількість разів. Для кожного кидка визначте суму чисел, які випали на обох кубиках. Підрахуйте, скільки разів кожна можлива сума (від 2 до 12) з’являється у процесі симуляції. Використовуючи ці дані, обчисліть імовірність кожної суми.

На основі проведених імітацій створіть таблицю або графік, який відображає ймовірності кожної суми, виявлені за допомогою методу Монте-Карло.

Таблиця ймовірностей сум при киданні двох кубиків виглядає наступним чином.

Сума	Імовірність
2	2.78% (1/36)
3	5.56% (2/36)
4	8.33% (3/36)
5	11.11% (4/36)
6	13.89% (5/36)
7	16.67% (6/36)
8	13.89% (5/36)
9	11.11% (4/36)
10	8.33% (3/36)
11	5.56% (2/36)
12	2.78% (1/36)

Порівняйте отримані за допомогою методу Монте-Карло результати з аналітичними розрахунками, наведеними в таблиці вище.'''

from collections import defaultdict
import random
import matplotlib.pyplot as plt


def simulate_dice_rolls(num_rolls):
    counts = defaultdict(int)
    for i in range(num_rolls):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        counts[dice1 + dice2] += 1
    
    print(f"\nRolls: {num_rolls}")
    print(f"{'Sum':>4} | {'MC':>7} | {'Theory':>8}")
    for dice in range(2, 13):
        mc = counts[dice] / num_rolls
        print(f"{dice:>4} | {mc*100:6.2f}% | {ANALYTICAL[dice]*100:6.2f}%")
    return {s: counts[s] / num_rolls for s in range(2, 13)}

def plot_probabilities(probabilities):
    sums = list(probabilities.keys())
    probs = list(probabilities.values())
    
    # Створення графіка
    plt.bar(sums, probs, tick_label=sums)
    plt.xlabel('Сума чисел на кубиках')
    plt.ylabel('Ймовірність')
    plt.title(f"Ймовірність сум двох кубиків (кидків: {num_rolls})")
    
    # Додавання відсотків випадання на графік
    for i, prob in enumerate(probs):
        plt.text(sums[i], prob, f"{prob*100:.2f}%", ha='center')
    
    plt.show()

ANALYTICAL = {2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36,
              7: 6/36, 8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36}

if __name__ == "__main__":
    for num_rolls in [100, 1000, 10000, 100000]:
        # Симуляція кидків і обчислення ймовірностей
        probabilities = simulate_dice_rolls(num_rolls)

        # Відображення ймовірностей на графіку
        plot_probabilities(probabilities)