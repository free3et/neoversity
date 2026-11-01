
import psycopg2

# Встановлюємо підключення до бази даних
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="task_manager",
    user="postgres",
    password=input("Введіть пароль PostgreSQL: ")
)

print("Підключення успішне!")

# Створюємо курсор
cursor = connection.cursor()

# Виконуємо SQL-запит
cursor.execute("SELECT current_database();")

# Отримуємо результат
result = cursor.fetchone()

print(result)

cursor.close()
connection.close()