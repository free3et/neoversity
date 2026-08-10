import heapq
import matplotlib.pyplot as plt
import networkx as nx

# створення графа
GRAPH = {
    "A": {"B": 4, "C": 2},
    "B": {"A": 4, "C": 1, "D": 5},
    "C": {"A": 2, "B": 1, "D": 8, "E": 10},
    "D": {"B": 5, "C": 8, "E": 2},
    "E": {"C": 10, "D": 2},
}

# алгоритм Дейкстри
def dijkstra(graph, start):
    distances = {v: float("inf") for v in graph} 
    distances[start] = 0
    heap = [(0, start)]

    while heap:
        dist, vertex = heapq.heappop(heap) # вилучення вершини з купи
        if dist > distances[vertex]: # якщо відстань до вершини більша за відстань до сусідньої вершини
            continue

        for neighbor, weight in graph[vertex].items(): # перебір сусідніх вершин
            new_dist = dist + weight # обчислення відстані до сусідньої вершини
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

        print(distances)  # стан після кожного кроку

    return distances

if __name__ == "__main__":
    print(dijkstra(GRAPH, "A"))

    G = nx.Graph()
    for v, neighbors in GRAPH.items():
        for n, w in neighbors.items():
            if v < n:
                G.add_edge(v, n, weight=w)

    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=700, font_size=16)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"))
    plt.show()