import queue
import random

"""
Програма імітує приймання й обробку заявок сервісного центру:
генерує нові заявки, додає їх до черги та послідовно обробляє.
"""
# Створити чергу заявок
queue_tasks = queue.Queue()

def generate_request():
    task = {
        'id': random.randint(1, 10000),
        'description': 'Task description',
        'status': 'pending'
    }
    queue_tasks.put(task) # додаємо заявку до черги
    print(f'Task {task["id"]} added to queue!')

def process_request():
    if not queue_tasks.empty(): # якщо черга не порожня, то обробляємо заявку
        task = queue_tasks.get() # видаляємо заявку з черги
        print(f'Task {task["id"]} processed!')
    else:
        print('Queue is empty!')

def main():
    while True:
        user_input = input(
            "Do you want to add task (press a), procceed task (press p) or to exit (press q)? "
        ).strip().lower()

        if user_input == 'a':
            generate_request()
        elif user_input == 'p':
            process_request()
        elif user_input == 'q':
            print("Exiting the program.")
            break
        else:
            print("Unknown command. Please enter 'a', 'p' or 'q'.")

main()