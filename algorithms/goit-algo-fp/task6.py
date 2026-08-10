dish_data = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}

# Greedy approach
def greedy_algorithm(items, budget):
    sorted_items = sorted(
    items.items(),
    key=lambda x: x[1]["calories"] / x[1]["cost"],
    reverse=True,
)
    total_calories = 0
    remaining_budget = budget
    chosen_items = []
    for name, data in sorted_items:
        if remaining_budget >= data["cost"]:
            remaining_budget -= data["cost"]
            total_calories += data["calories"]
            chosen_items.append(name)
    return total_calories, budget - remaining_budget, chosen_items


# Dynamic Programming approach
def dynamic_programming(items, budget):
    item_names = list(items.keys())
    item_costs = [items[item]["cost"] for item in item_names]
    item_calories = [items[item]["calories"] for item in item_names]

    # Create a DP table where rows represent up to the i-th item and columns represent budget
    dp_table = [[0 for x in range(budget + 1)] for y in range(len(dish_data) + 1)]

    # Реалізація побудови таблиці оптимального блюда по калоріям для всіх бюджетів
    for i in range(len(dish_data) + 1):
        for max_cost in range(budget + 1):
            if i == 0 or max_cost == 0:
                dp_table[i][max_cost] = 0
            elif item_costs[i - 1] <= max_cost:
                dp_table[i][max_cost] = max(item_calories[i - 1] + dp_table[i - 1][max_cost - item_costs[i - 1]], dp_table[i - 1][max_cost])
            else:
                dp_table[i][max_cost] = dp_table[i - 1][max_cost]

    # Реалізація отримання оптимального набору страв через використання обчисленої таблиці
    chosen_items = []
    current_budget = budget

    for i in range(len(dish_data), 0, -1):
        if dp_table[i][current_budget] != dp_table[i - 1][current_budget]:
            chosen_items.append(item_names[i - 1])
            current_budget -= item_costs[i - 1]

    return dp_table[len(dish_data)][budget], budget - current_budget, chosen_items

if __name__ == '__main__':
    # Execute both algorithms
    budget = 100

    greedy_result = greedy_algorithm(dish_data, budget)
    dp_result = dynamic_programming(dish_data, budget)

    print("Greedy result:", greedy_result)
    print("Dynamic programming result:", dp_result)