from BTrees.OOBTree import OOBTree
import timeit

# Створення OOBTree
tree = OOBTree()
items_dict = {}

def get_items_info(path: str) -> list[dict]:
    try:
        items_info = []
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line == "ID,Name,Category,Price":
                    continue
                try: 
                    id, name, category, price = line.split(',')
                    items_info.append({
                    "id": id,
                    "name": name,
                    "category": category,
                    "price": float(price),
                })
                except ValueError:
                    print(f"Некоректний рядок: {line}")
                    continue    
            return items_info
    except FileNotFoundError:
        print('Файл не знайдено, будь ласка перевірте шлях до файлу!')

data_info = get_items_info("generated_items_data.csv")

# Додавання товарів до OOBTree
def add_item_to_tree(tree, item):
    tree[(item['price'], item['id'])] = item
    return tree

for item in data_info:
    add_item_to_tree(tree, item)

# Додавання товарів до dict
def add_item_to_dict(dict, item):
    dict[item['id']] = item
    return dict

for item in data_info:
    add_item_to_dict(items_dict, item)

# Діапазонний запит для OOBTree
def range_query_tree(tree, min_price, max_price):
    return list(tree.items((min_price,), (max_price + 1e-9,))) # 1e-9 - для того щоб включити максимальну ціну в діапазон

# Діапазонний запит для dict
def range_query_dict(dict, min_price, max_price):
    result = []
    for item in dict.values():
        if min_price <= item['price'] <= max_price:
            result.append(item)
    return result

time_tree = timeit.timeit(lambda: range_query_tree(tree, 100, 200), number=100)
time_dict = timeit.timeit(lambda: range_query_dict(items_dict, 100, 200), number=100)
print(f"Total range_query time for OOBTree: {time_tree:.6f} seconds")
print(f"Total range_query time for Dict: {time_dict:.6f} seconds")

# Вивід результатів
# Total range_query time for OOBTree: 0.048395 seconds
# Total range_query time for Dict: 0.325042 seconds
# Тобто OOBTree показав кращий результат за рахунок відсортованої структури даних