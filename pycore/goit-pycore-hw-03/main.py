# Завдання 1. Створіть функцію get_days_from_today(date), яка розраховує кількість днів між заданою датою і поточною датою
from datetime import datetime

def get_days_from_today(date: str) -> int: # 2026-03-26 -> return only days ex.31
    try:
        incoming_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    today_date = datetime.today().date()
    time_delta = today_date - incoming_date
    return time_delta.days
    

print(get_days_from_today("2021-10-09"))
print(get_days_from_today("2026-10-09"))
print(get_days_from_today("2026-04-26"))
print(get_days_from_today("2026-03-26"))
# print(get_days_from_today("test-date-day"))
# print(get_days_from_today("2026/10/09"))

# ------------------------------------------------------------------------------

# Завдання 2. Щоб виграти головний приз лотереї, необхідний збіг кількох номерів на лотерейному білеті з числами, що випали випадковим чином і в певному діапазоні під час чергового тиражу. Наприклад, необхідно вгадати шість чисел від 1 до 49 чи п'ять чисел від 1 до 36 тощо.
import random

def get_numbers_ticket(min_val: int, max_val: int, quantity: int) -> list[int]: # return sorted list of unique numbers
    if (
        min_val < 1 or 
        max_val > 1000 or 
        min_val > max_val or 
        quantity > (max_val - min_val + 1)
        ):
        return []
    random_numbers = random.sample(range(min_val, max_val + 1), quantity) # The range method generates numbers between min and max + 1, use the sample method to get a unique list of numbers corresponding to quantity 
    return sorted(random_numbers)

print(get_numbers_ticket(1, 49, 6))
print(get_numbers_ticket(-1, 30, 5))
print(get_numbers_ticket(1, 150, 7))
print(get_numbers_ticket(-1, 1150, 6))
