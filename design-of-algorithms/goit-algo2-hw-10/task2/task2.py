# Визначення класу Teacher
class Teacher:
    def __init__(self, first_name: str, last_name: str, age: int, email: str, can_teach_subjects: set[str]):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = can_teach_subjects
        self.assigned_subjects = set()

def create_schedule(subjects, teachers):
    uncovered_subjects = set(subjects)

    for teacher in teachers:
        teacher.assigned_subjects = set()

    while uncovered_subjects:
        best_teacher = None
        best_subjects = set()

        for teacher in teachers:
            available_subjects = (
                teacher.can_teach_subjects & uncovered_subjects
            )

            if len(available_subjects) > len(best_subjects):
                best_teacher = teacher
                best_subjects = available_subjects

            elif len(available_subjects) == len(best_subjects):
                if available_subjects and (
                    best_teacher is None
                    or teacher.age < best_teacher.age
                ):
                    best_teacher = teacher
                    best_subjects = available_subjects

        if best_teacher is None:
            print("Неможливо покрити всі предмети наявними викладачами.")
            return None

        best_teacher.assigned_subjects = best_subjects
        uncovered_subjects -= best_subjects

    return [
        teacher for teacher in teachers
        if teacher.assigned_subjects
    ]


if __name__ == '__main__':
    # Множина предметів
    subjects = {
        'Математика',
        'Фізика',
        'Хімія',
        'Інформатика',
        'Біологія'
    }

    # Створення списку викладачів
    teachers = [
        Teacher('Олександр', 'Іваненко', 45, 'o.ivanenko@example.com', {'Математика', 'Фізика'}),
        Teacher('Марія', 'Петренко', 38, 'm.petrenko@example.com', {'Хімія'}),
        Teacher('Сергій', 'Коваленко', 50, 's.kovalenko@example.com', {'Інформатика', 'Математика'}),
        Teacher('Наталія', 'Шевченко', 29, 'n.shevchenko@example.com', {'Біологія', 'Хімія'}),
        Teacher('Дмитро', 'Бондаренко', 35, 'd.bondarenko@example.com', {'Фізика', 'Інформатика'}),
        Teacher('Олена', 'Гриценко', 42, 'o.grytsenko@example.com', {'Біологія'})
    ]

    # Виклик функції створення розкладу
    schedule = create_schedule(subjects, teachers)

    # Виведення розкладу
    if schedule:
        print("Розклад занять:")
        for teacher in schedule:
            print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
            print(f"   Викладає предмети: {', '.join(teacher.assigned_subjects)}\n")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")

'''
Розклад занять:
Олександр Іваненко, 45 років, email: o.ivanenko@example.com
   Викладає предмети: Математика

Наталія Шевченко, 29 років, email: n.shevchenko@example.com
   Викладає предмети: Хімія, Біологія

Дмитро Бондаренко, 35 років, email: d.bondarenko@example.com
   Викладає предмети: Інформатика, Фізика
'''