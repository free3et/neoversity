class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int):
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        prev.next = cur.next
        cur = None

    def search_element(self, data: int) -> Node | None:
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None
    
    def reverse_list(self):
        current = self.head
        prev = None

        while current:
            next = current.next # зберігаємо наступний вузол
            current.next = prev # розвертаємо посилання (вузол тепер вказує назад)
            prev = current # зсуваємо prev вперед
            current = next # зсуваємо current вперед
        self.head = prev # prev стає колишнім останнім вузлом, тобто новою головою списку

    def get_middle(self, head):
        if head is None:
            return head

        one_step = head # рухається на 1 крок
        two_steps = head # рухається на 2 кроки

        while two_steps.next and two_steps.next.next:
            one_step = one_step.next
            two_steps = two_steps.next.next
        return one_step # повертаємо середній вузол

    def merge_sort(self, head):
        if head is None or head.next is None:
            return head

        middle = self.get_middle(head) # знаходимо середній вузол
        left = head # ліва частина списку
        right = middle.next # права частина списку
        middle.next = None 

        left = self.merge_sort(left) # сортуємо ліву частину списку
        right = self.merge_sort(right) # сортуємо праву частину списку

        return self.sorted_merge(left, right) # зливаємо ліву і праву частини списку

    def sorted_merge(self, a, b):
        result = None

        if a is None:
            return b
        if b is None:
            return a

        if a.data <= b.data:
            result = a
            result.next = self.sorted_merge(a.next, b)
        else:
            result = b
            result.next = self.sorted_merge(a, b.next)

        return result

    def merge_sorted_lists(self, list1, list2):
        return self.sorted_merge(self.merge_sort(list1.head), self.merge_sort(list2.head))

    
    def print_list(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

if __name__ == '__main__':

    first_list = LinkedList()
    second_list = LinkedList()

    # створюємо перший список
    first_list.insert_at_beginning(5)
    first_list.insert_at_beginning(10)
    first_list.insert_at_beginning(15)
    first_list.insert_at_end(20)
    first_list.insert_at_end(25)
    first_list.insert_at_beginning(59)
    first_list.insert_at_beginning(20)
    first_list.insert_at_beginning(35)
    print("Зв'язний список 1:")
    first_list.print_list()

    first_list.reverse_list()
    print("Зв'язний список 1 після реверсу:")
    first_list.print_list()

    first_list.head = first_list.merge_sort(first_list.head)
    print("Зв'язний список 1 відсортовано:")
    first_list.print_list()

    # створюємо другий список
    second_list.insert_at_end(1)
    second_list.insert_at_end(3)
    second_list.insert_at_end(5)
    second_list.insert_at_end(7)
    second_list.insert_at_end(9)

    print("Зв'язний список 2:")
    second_list.print_list()

    second_list.reverse_list()
    print("Зв'язний список 2 після реверсу:")
    second_list.print_list()

    second_list.head = second_list.merge_sort(second_list.head)
    print("Зв'язний список 2 відсортовано:")
    second_list.print_list()

    first_list.head = first_list.merge_sorted_lists(first_list, second_list)
    print("Зв'язний список 1 та 2 відсортовано та замерджено:")
    first_list.print_list()
