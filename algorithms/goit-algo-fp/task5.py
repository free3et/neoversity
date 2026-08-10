import colorsys
import uuid

import heapq
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.stack.pop()

    def is_empty(self):
        return not self.stack

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, title="Binary tree"):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=3000, node_color=colors)
    plt.show()


def build_heap_tree(heap):
    if not heap:
        return None

    nodes = [Node(val) for val in heap]

    for i in range(len(heap)):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(heap):
            nodes[i].left = nodes[left]
        if right < len(heap):
            nodes[i].right = nodes[right]

    return nodes[0]


def generate_color(step, total_steps):
    factor = step / max(total_steps - 1, 1)
    hue = 0.75 - 0.25 * factor # фіолетовий -> блакитний
    saturation = 0.60 + 0.15 * factor
    value = 0.88 + 0.12 * factor
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


def dfs_visualize(root, total_steps):
    visited = set()
    step = 0
    stack = Stack()
    stack.push(root)

    while not stack.is_empty():
        current = stack.pop()
        if current is None or current in visited:
            continue

        visited.add(current)
        current.color = generate_color(step, total_steps)
        step += 1

        if current.right:
            stack.push(current.right)
        if current.left:
            stack.push(current.left)


def bfs_visualize(root, total_steps):
    visited = set()
    step = 0
    queue = deque([root])

    while queue:
        current = queue.popleft()
        if current is None or current in visited:
            continue

        visited.add(current)
        current.color = generate_color(step, total_steps)
        step += 1

        if current.left:
            queue.append(current.left)
        if current.right:
            queue.append(current.right)


def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)


if __name__ == "__main__":
    heap_list = [1, 3, 5, 7, 9, 2, 4, 34, 10, 6, 11]
    heapq.heapify(heap_list)
    heap_tree_root = build_heap_tree(heap_list)
    total_steps = count_nodes(heap_tree_root)

    dfs_visualize(heap_tree_root, total_steps)
    draw_tree(heap_tree_root, title="DFS обхід")

    bfs_visualize(heap_tree_root, total_steps)
    draw_tree(heap_tree_root, title="BFS обхід")
