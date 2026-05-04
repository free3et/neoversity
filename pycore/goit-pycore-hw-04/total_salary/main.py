def total_salary(path: str) -> tuple[int, float]:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            sum_salary = 0
            count = 0
            for line in lines:
                if not line.strip():
                    continue
                try:
                    name, salary = line.split(',')
                    count += 1
                    sum_salary += int(salary.strip())
                except ValueError:
                    print(f"Некоректний рядок: {line}")
                    continue
                
            average_salary = sum_salary / count
            return sum_salary, average_salary
    except FileNotFoundError:
        print('Файл не знайдено, будь ласка перевірте шлях до файлу!')
        return (0, 0)

total, average = total_salary('salaries.csv')
print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average:.2f}")
