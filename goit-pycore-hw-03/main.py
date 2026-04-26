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
print(get_days_from_today("test-date-day"))
print(get_days_from_today("2026/10/09"))