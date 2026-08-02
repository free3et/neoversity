class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key): # додавання нового елемента до дерева
    if root is None: # якщо дерево порожнє, то створюємо новий вузол
        return Node(key)
    else: # якщо дерево не порожнє, то додаємо новий елемент
        if key < root.val:
            root.left = insert(root.left, key) 
        else:
            root.right = insert(root.right, key) 
    return root

def find_min(root): # знаходження найменшого значення в дереві
    if root is None:
        return None 
    current = root
    while current.left is not None: # поки ліва гілка не дорівнює None, то переходимо до лівого піддерева
        current = current.left
    return current.val

def sum_of_values(root): # знаходження суми всіх значень в дереві
    if root is None:
        return 0
    return root.val + sum_of_values(root.left) + sum_of_values(root.right)

root = None # створюємо порожнє дерево
for x in [5, 3, 2, 4, 7, 6, 8]:
    root = insert(root, x)

print("Найменше значення:", find_min(root))
print("Сума всіх значень:", sum_of_values(root))

