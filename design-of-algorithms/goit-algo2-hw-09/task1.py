import random
import math

# Визначення функції Сфери
def sphere_function(x):
    return sum(xi ** 2 for xi in x)

def clip(value, low, high):
    # Обмежує значення межами [low, high]
    return max(low, min(high, value))

def random_point(bounds):
    # Випадкова точка в межах простору пошуку
    return [random.uniform(low, high) for low, high in bounds]

def random_neighbor(point, bounds, step):
    # Випадковий сусід: зсув кожної координати на величину з [-step, step]
    return [
        clip(xi + random.uniform(-step, step), low, high)
        for xi, (low, high) in zip(point, bounds)
    ]

def distance(a, b):
    # Евклідова відстань між двома точками
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))

# Hill Climbing
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    current = random_point(bounds)
    current_value = func(current)
    step = max(high - low for low, high in bounds) / 10

    for _ in range(iterations):
        # Генеруємо всіх сусідів: зсув на ±step по кожній координаті
        neighbors = []
        for i, (low, high) in enumerate(bounds):
            for direction in (-1, 1):
                neighbor = current[:]
                neighbor[i] = clip(neighbor[i] + direction * step, low, high)
                neighbors.append(neighbor)

        best_neighbor = min(neighbors, key=func)
        best_value = func(best_neighbor)

        if best_value < current_value:
            improvement = current_value - best_value
            moved = distance(current, best_neighbor)
            current, current_value = best_neighbor, best_value
            if improvement < epsilon or moved < epsilon:
                break
        else:
            # Кращих сусідів немає — зменшуємо крок
            step /= 2
            if step < epsilon:
                break

    return current, current_value

# Random Local Search
def random_local_search(func, bounds, iterations=1000, epsilon=1e-6, step=0.5, restart_prob=0.05):
    current = random_point(bounds)
    current_value = func(current)

    for _ in range(iterations):
        if random.random() < restart_prob:
            candidate = random_point(bounds)
        else:
            candidate = random_neighbor(current, bounds, step)
        candidate_value = func(candidate)

        if candidate_value < current_value:
            improvement = current_value - candidate_value
            moved = distance(current, candidate)
            current, current_value = candidate, candidate_value
            if improvement < epsilon or moved < epsilon:
                break

    return current, current_value

# Simulated Annealing
def simulated_annealing(func, bounds, iterations=1000, temp=1000, cooling_rate=0.95, epsilon=1e-6):
    current = random_point(bounds)
    current_value = func(current)
    best, best_value = current[:], current_value

    initial_temp = temp
    max_step = max(high - low for low, high in bounds) / 4

    for _ in range(iterations):
        if temp < epsilon:
            break

        # Крок плавно зменшується разом із температурою:
        # спочатку широке дослідження простору, наприкінці — точне доведення
        step = max_step * (temp / initial_temp) ** 0.25
        candidate = random_neighbor(current, bounds, step)
        candidate_value = func(candidate)
        delta = candidate_value - current_value

        if delta < 0 or random.random() < math.exp(-delta / temp):
            current, current_value = candidate, candidate_value
            if current_value < best_value:
                best, best_value = current[:], current_value

        temp *= cooling_rate

    return best, best_value

if __name__ == "__main__":
    # Межі для функції
    bounds = [(-5, 5), (-5, 5)]

    # Виконання алгоритмів
    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print("Розв'язок:", hc_solution, "Значення:", hc_value)

    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print("Розв'язок:", rls_solution, "Значення:", rls_value)

    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print("Розв'язок:", sa_solution, "Значення:", sa_value)

'''
    Hill Climbing:
    Розв'язок: [0.0001551149955014708, -0.00019488358642316683] Значення: 6.204027408657724e-08

    Random Local Search:
    Розв'язок: [0.022900164566224457, 0.009602423433016094] Значення: 0.0006166240729470987

    Simulated Annealing:
    Розв'язок: [5.626094875429283e-05, 0.0019438064706536057] Значення: 3.78154888970956e-06
'''