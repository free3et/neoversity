import uuid
import matplotlib.pyplot as plt
import networkx as nx

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # Додатковий аргумент для зберігання кольору вузла.
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор для кожного вузла.


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)  # Використання id та збереження значення вузла.
        if node.left:
            graph.add_edge(node.id, node.left.id)  # Додавання ребра між вузлами.
            l = x - 1 / 2 ** layer  # Обчислення координати x для лівого вузла.
            pos[node.left.id] = (l, y - 1)  # Додавання координат для лівого вузла.
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)  # Рекурсивне додавання ребер для лівого вузла.
        if node.right:
            graph.add_edge(node.id, node.right.id)  # Додавання ребра між вузлами.
            r = x + 1 / 2 ** layer  # Обчислення координати x для правого вузла.
            pos[node.right.id] = (r, y - 1)  # Додавання координат для правого вузла.
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)  # Рекурсивне додавання ребер для правого вузла.
    return graph


def draw_tree(tree_root):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}  # Значення вузла для міток.

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()

def build_heap_tree(heap):
    # З масиву купи будує дерево Node
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

    return nodes[0]  # корінь

# Відображення дерева.
heap = [0, 4, 1, 5, 10, 3]
root = build_heap_tree(heap)
draw_tree(root)
