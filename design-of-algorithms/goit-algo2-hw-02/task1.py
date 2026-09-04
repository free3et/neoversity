from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує порядок друку моделей.
    Моделі:
    - сортуються за пріоритетом (де 1 — найвищий пріоритет, 2 — середній, 3 — низький);
    - об'єднуються у групи для одночасного друку;
    - група не може перевищувати max_volume або max_items;
    - час групи = максимальний час друку серед її моделей.
    """

    printer = PrinterConstraints(
        max_volume=constraints["max_volume"],
        max_items=constraints["max_items"]
    )

    # Перетворюємо словники у dataclass
    jobs = [
        PrintJob(
            id=job["id"],
            volume=job["volume"],
            priority=job["priority"],
            print_time=job["print_time"]
        )
        for job in print_jobs
    ]

    valid_jobs = []

    # Перевірка правильності та можливості друку
    for job in jobs:
        if job.volume <= 0 or job.print_time <= 0:
            print(f"Завдання {job.id} має некоректні дані")
            continue

        if job.priority not in (1, 2, 3):
            print(f"Завдання {job.id} має некоректний пріоритет")
            continue

        if job.volume > printer.max_volume:
            print(
                f"Модель {job.id} перевищує максимальний об'єм принтера і не буде надрукована"
            )
            continue

        valid_jobs.append(job) # Додаємо завдання до списку завдань, які можна надрукувати

    def get_priority(job):
        return job.priority

    valid_jobs.sort(key=get_priority)

    groups = []
    current_group = []
    current_volume = 0.0

    for job in valid_jobs:
        # Перевіряємо, чи можна додати модель до поточної групи
        can_add_job_to_group = (
            len(current_group) < printer.max_items
            and current_volume + job.volume <= printer.max_volume
        )

        if can_add_job_to_group:
            current_group.append(job)
            current_volume += job.volume
        else:
            # Завершуємо поточну групу і додаємо її до списку груп
            if current_group:
                groups.append(current_group)

            # Створюємо нову групу і додаємо туди поточну модель
            current_group = [job]
            current_volume = job.volume

    # Додаємо останню групу
    if current_group:
        groups.append(current_group)

    # Формуємо порядок друку та рахуємо загальний час
    print_order = []
    total_time = 0

    for group in groups:
        print_order.extend(job.id for job in group)

        # Час одночасного друку групи —
        # максимальний час серед моделей
        group_time = max(job.print_time for job in group)
        total_time += group_time

    return {
        "print_order": print_order,
        "total_time": total_time
    }


# Тестування
def test_printing_optimization():

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    # Тест 1: однаковий пріоритет
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: різні пріоритети
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
    ]

    # Тест 3: обмеження об'єму та кількості
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
