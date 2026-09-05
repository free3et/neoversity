import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# 1. Створюємо граф
G = nx.DiGraph()

# Додаємо ребра з пропускною здатністю
edges = [
    (0, 2, 25),  # Термінал 1 -> Склад 1	25
    (0, 3, 20),  # Термінал 1 -> Склад 2	20
    (0, 4, 15),  # Термінал 1 -> Склад 3	15
    (1, 4, 15),  # Термінал 2 -> Склад 3	15
    (1, 5, 30),  # Термінал 2 -> Склад 4	30
    (1, 3, 10),  # Термінал 2 -> Склад 2	10
    (2, 6, 15),  # Склад 1 -> Магазин 1	15
    (2, 7, 10),  # Склад 1 -> Магазин 2	10
    (2, 8, 20),  # Склад 1 -> Магазин 3	20
    (3, 9, 15),  # Склад 2 -> Магазин 4	15
    (3, 10, 10),  # Склад 2 -> Магазин 5	10
    (3, 11, 25),  # Склад 2 -> Магазин 6	25
    (4, 12, 20),  # Склад 3 -> Магазин 7	20
    (4, 13, 15),  # Склад 3 -> Магазин 8	15
    (4, 14, 10),  # Склад 3 -> Магазин 9	10
    (5, 15, 20),  # Склад 4 -> Магазин 10	20
    (5, 16, 10),  # Склад 4 -> Магазин 11	10
    (5, 17, 15),  # Склад 4 -> Магазин 12	15
    (5, 18, 5),  # Склад 4 -> Магазин 13	5
    (5, 19, 10),  # Склад 4 -> Магазин 14	10
]

# Додаємо всі ребра до графа
G.add_weighted_edges_from(edges)

# Позиції для малювання графа
# Формула: для n вузлів у колонці, індекс i від 0 до n-1:
# y = (n - 1) / 2 - i
pos = {
    # Термінали (x = 0)
    0: (0, (2 - 1) / 2 - 0),   # Термінал 1 (n = 2) отримуємо y = 0.5
    1: (0, (2 - 1) / 2 - 1),  # Термінал 2 (n = 2) отримуємо y = -0.5

    # Склади (x = 2)
    2: (2, (4 - 1) / 2 - 0),   # Склад 1 (n = 4) отримуємо y = 1.5
    3: (2, (4 - 1) / 2 - 1),   # Склад 2 (n = 4) отримуємо y = 0.5
    4: (2, (4 - 1) / 2 - 2),   # Склад 3 (n = 4) отримуємо y = -0.5
    5: (2, (4 - 1) / 2 - 3),   # Склад 4 (n = 4) отримуємо y = -1.5

    # Магазини (x = 4), n = 14
    6:  (4, (14 - 1) / 2 - 0),   # 6.5   Магазин 1
    7:  (4, (14 - 1) / 2 - 1),   # 5.5   Магазин 2
    8:  (4, (14 - 1) / 2 - 2),   # 4.5   Магазин 3
    9:  (4, (14 - 1) / 2 - 3),   # 3.5   Магазин 4
    10: (4, (14 - 1) / 2 - 4),   # 2.5   Магазин 5
    11: (4, (14 - 1) / 2 - 5),   # 1.5   Магазин 6
    12: (4, (14 - 1) / 2 - 6),   # 0.5   Магазин 7
    13: (4, (14 - 1) / 2 - 7),   # -0.5   Магазин 8
    14: (4, (14 - 1) / 2 - 8),   # -1.5   Магазин 9
    15: (4, (14 - 1) / 2 - 9),   # -2.5   Магазин 10
    16: (4, (14 - 1) / 2 - 10),  # -3.5   Магазин 11
    17: (4, (14 - 1) / 2 - 11),  # -4.5   Магазин 12
    18: (4, (14 - 1) / 2 - 12),  # -5.5   Магазин 13
    19: (4, (14 - 1) / 2 - 13),  # -6.5  Магазин 14
}

# Малюємо граф
plt.figure(figsize=(10, 8))
nx.draw(G, pos, with_labels=True, node_size=2600, node_color="skyblue", font_size=12, font_weight="bold", arrows=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Відображаємо граф
# plt.show()

# 2.Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()
        
        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor] > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    
    return False

# 3. Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]  # Ініціалізуємо матрицю потоку нулем
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float('Inf')
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(path_flow, capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node
        
        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node
        
        # Збільшуємо максимальний потік
        max_flow += path_flow

    return max_flow, flow_matrix

# 4. Матриця пропускної здатності:
# 0–1 термінали, 2–5 склади, 6–19 магазини,
# 20 — суперджерело S, 21 — суперсток T
NUM_NETWORK_NODES = 20
SOURCE = 20  # суперджерело S
SINK = 21    # суперсток T
N = NUM_NETWORK_NODES + 2  # 22×22

capacity_matrix = [[0] * N for _ in range(N)]

# 5. Ребра логістичної мережі
for u, v, cap in edges:
    capacity_matrix[u][v] = cap

# 6. S → ТЕРМІНАЛИ: ємність = сума виходів термінала
terminal_out = {0: 0, 1: 0}
for u, v, cap in edges:
    if u in terminal_out:
        terminal_out[u] += cap

capacity_matrix[SOURCE][0] = terminal_out[0]  # S → Термінал 1 (25+20+15=60)
capacity_matrix[SOURCE][1] = terminal_out[1]  # S → Термінал 2 (15+30+10=55)

# 7. МАГАЗИНИ → T: ємність = сума входів у магазин
store_in = {store: 0 for store in range(6, 20)}
for u, v, cap in edges:
    if v in store_in:
        store_in[v] += cap

for store, cap in store_in.items():
    capacity_matrix[store][SINK] = cap

max_flow, flow_matrix = edmonds_karp(capacity_matrix, SOURCE, SINK)
print(f"Максимальний потік усієї мережі: {max_flow}")

# 8. Термінали та склади
terminals = [0, 1]
warehouses = [2, 3, 4, 5]
stores = list(range(6, 20))

# 9. СКЛАДИ → МАГАЗИНИ: список магазинів, куди він везе
warehouse_to_stores = {w: [] for w in warehouses}
for u, v, _ in edges:
    if u in warehouse_to_stores:
        warehouse_to_stores[u].append(v)

print("\nТермінал\tМагазин\t\tФактичний Потік")
for terminal in terminals:
    for warehouse in warehouses:
        flow_to_wh = flow_matrix[terminal][warehouse]
        if flow_to_wh <= 0:
            continue

        # скільки всього зайшло на склад від усіх терміналів
        total_in = sum(flow_matrix[t][warehouse] for t in terminals)
        if total_in == 0:
            continue

        share = flow_to_wh / total_in  # частка цього термінала

        for store in warehouse_to_stores[warehouse]:
            store_flow = flow_matrix[warehouse][store]
            actual = store_flow * share
            print(
                f"Термінал {terminal + 1}\t"
                f"Магазин {store - 5}\t"
                f"{actual:.0f}"
            )
