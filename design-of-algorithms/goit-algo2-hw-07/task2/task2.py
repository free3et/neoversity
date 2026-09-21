from functools import lru_cache
from time import time
import timeit
import matplotlib.pyplot as plt

class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.left_node = None
        self.right_node = None


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        """Вставка нового елемента в дерево."""
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_node(data, self.root)

    def _insert_node(self, data, current_node):
        """Рекурсивна вставка елемента у дерево."""
        if data[0] < current_node.data[0]:
            if current_node.left_node:
                self._insert_node(data, current_node.left_node)
            else:
                current_node.left_node = Node(data, current_node)
        else:
            if current_node.right_node:
                self._insert_node(data, current_node.right_node)
            else:
                current_node.right_node = Node(data, current_node)

    def find(self, n):
        """Пошук елемента в дереві із застосуванням сплайювання."""
        node = self.root
        while node is not None:
            key = node.data[0]
            if n < key:
                node = node.left_node
            elif n > key:
                node = node.right_node
            else:
                self._splay(node)
                return node.data
        return None  # Якщо елемент не знайдено.

    def _splay(self, node):
        """Реалізація сплайювання для переміщення вузла до кореня."""
        while node.parent is not None:
            if node.parent.parent is None:  # Zig ситуація
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:  # Zig-Zig
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:  # Zig-Zig
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:  # Zig-Zag
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        """Права ротація вузла."""
        left_child = node.left_node
        if left_child is None:
            return

        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child

        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        """Ліва ротація вузла."""
        right_child = node.right_node
        if right_child is None:
            return

        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child

        right_child.left_node = node
        node.parent = right_child

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

def fibonacci_splay(n, tree):
    # Перевіряємо, чи значення вже є в дереві
    result = tree.find(n)

    if result is not None:
        return result[1]

    # Базові випадки
    if n == 0:
        value = 0
    elif n == 1:
        value = 1
    else:
        value = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)

    # Зберігаємо результат у Splay Tree
    tree.insert((n, value))

    return value


if __name__ == "__main__":
    tree = SplayTree()
    n = 35
    n_values = list(range(0, 951, 50))
    time_splay = [timeit.timeit(lambda: fibonacci_splay(n, tree), number=1) for n in n_values]
    time_lru = [timeit.timeit(lambda: fibonacci_lru(n),number=1) for n in n_values]
    print(
        f"{'n':<8}"
        f"{'LRU Cache Time (s)':<25}"
        f"{'Splay Tree Time (s)':<25}"
    )

    print("-" * 55)

    for n, lru_time, splay_time in zip(
        n_values,
        time_lru,
        time_splay
    ):
        print(
            f"{n:<8}"
            f"{lru_time:<25.10f}"
            f"{splay_time:<25.10f}"
        )

      # виведення таблиці (копія з консолі)
    """
       n       LRU Cache Time (s)       Splay Tree Time (s)      
        -------------------------------------------------------
        0       0.0000005420             0.0000015411             
        50      0.0000507089             0.0000254170             
        100     0.0000046659             0.0000225829             
        150     0.0000042501             0.0000238330             
        200     0.0000047919             0.0000208749             
        250     0.0000043751             0.0000205419             
        300     0.0000050000             0.0000237499             
        350     0.0000054589             0.0000217091             
        400     0.0000046669             0.0000309590             
        450     0.0000059169             0.0000246249             
        500     0.0000044589             0.0000211659             
        550     0.0000045830             0.0000288328             
        600     0.0000046249             0.0000244158             
        650     0.0000045002             0.0000244172             
        700     0.0000097081             0.0000254582             
        750     0.0000047910             0.0000240419             
        800     0.0000045830             0.0000258330             
        850     0.0000045411             0.0000229999             
        900     0.0000058331             0.0000228342             
        950     0.0000059579             0.0000229171 
     """

    # побудова графіка
    plt.title('Порівняння часу обчислення чисел Фібоначчі з використанням LRU кешу та Splay Tree')
    plt.plot(n_values, time_splay, label='Splay Tree')
    plt.plot(n_values, time_lru, label='LRU Cache')
    plt.xlabel('n')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.show()

    # висновки
    print("Висновки:")
    print("LRU Cache є лідером на всьому діапазоні n (як для малих, так і для великих значень). Він забезпечує доступ за O(1) завдяки внутрішній хеш-таблиці CPython.")
    print("Splay Tree поступається у швидкості на всіх етапах через накладні витрати на динамічне балансування (повороти дерева _splay), збереження об'єктів Node у пам'яті, складність O(log n).")

