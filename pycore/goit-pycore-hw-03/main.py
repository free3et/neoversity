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

# ------------------------------------------------------------------------------

# Ваш сервіс розсилок може ефективно відправляти повідомлення лише тоді, коли номери телефонів представлені у коректному форматі. Тому вам необхідна функція, яка автоматично нормалізує номери телефонів до потрібного формату, видаляючи всі зайві символи та додаючи міжнародний код країни, якщо потрібно

import re

def normalize_phone(phone_number: str) -> str:
    trimmed_phone_number = phone_number.strip() # remove leading and trailing whitespace
    pattern = r'[^0-9+]'
    cleaned_phone_number = re.sub(pattern, '', trimmed_phone_number) # remove all non-digit and non-plus characters

    if cleaned_phone_number.startswith('+'):
        return cleaned_phone_number
    if cleaned_phone_number.startswith('380'):
        return '+' + cleaned_phone_number
    return '+38' + cleaned_phone_number

raw_numbers = [
    "067\\t123 4567",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)

# ------------------------------------------------------------------------------

# Завдання 4 У межах вашої організації, ви відповідаєте за організацію привітань колег з днем народження. Щоб оптимізувати цей процес, вам потрібно створити функцію get_upcoming_birthdays, яка допоможе вам визначати, кого з колег потрібно привітати. Функція повинна повернути список всіх у кого день народження вперед на 7 днів включаючи поточний день.

from datetime import datetime, timedelta

users = [
    {'name': 'John Doe', 'birthday': '2024.04.23'},
    {'name': 'Jane Smith', 'birthday': '2024.04.29'},
    {"name": "Jane Beam", "birthday": "1995.05.01"},
    {"name": "Jill Johnson", "birthday": "1992.02.28"},
    {"name": "Jack Dan", "birthday": "1993.03.01"},
    {"name": "Jam Lowson", "birthday": "1994.10.13"},
    {"name": "John Walker", "birthday": "1995.03.01"},
    {"name": "Mick Davidson", "birthday": "1996.03.24"},
    {"name": "Jill Johnson", "birthday": "1997.04.01"},
    {"name": "Paul Collins", "birthday": "1998.03.01"},
    {"name": "Suzie Miller", "birthday": "1999.08.05"}
]

def get_upcoming_birthdays(users: list[dict]) -> list[dict]:
    upcoming_birthdays = []
    today_day = datetime.today().date() # get current date

    for user in users:
        user_birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date() # convert string birthday to date

        birthday_this_year = user_birthday.replace(year=today_day.year) # get birthday this year

        if birthday_this_year < today_day:
            birthday_this_year = birthday_this_year.replace(year=today_day.year + 1) # if birthday is in the past, set it to next year

        delta_days = (birthday_this_year - today_day).days

        if 0 <= delta_days <= 7: # if birthday is in the next 7 days, add it to the list
            congratulation_date = birthday_this_year
            if congratulation_date.weekday() == 5:
                congratulation_date = congratulation_date + timedelta(days=2) # if birthday is on a Saturday, set it to next Monday
            elif congratulation_date.weekday() == 6:
                congratulation_date = congratulation_date + timedelta(days=1) # if birthday is on a Sunday, set it to next Monday
            upcoming_birthdays.append({'name': user['name'], 'congratulation_date': congratulation_date.strftime('%Y.%m.%d')})
    return upcoming_birthdays

congrat_list = get_upcoming_birthdays(users)
print(congrat_list)