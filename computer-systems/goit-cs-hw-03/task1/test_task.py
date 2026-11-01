
import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="task_manager",
    user="postgres",
    password=input("Введіть пароль PostgreSQL: ")
)

cursor = connection.cursor()

# Отримуємо ID першого користувача
cursor.execute("SELECT id FROM users LIMIT 1;")
user_id = cursor.fetchone()[0]

# Отримуємо ID статусу new
cursor.execute(
    "SELECT id FROM status WHERE name = %s;",
    ("in progress",)
)
status_id = cursor.fetchone()[0]

# Створюємо завдання
cursor.execute(
    """
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES (%s, %s, %s, %s)
    RETURNING id;
    """,
    (
        "Створити базу даних",
        "Створити базу даних задач",
        status_id,
        user_id
    )
)

task_id = cursor.fetchone()[0]

connection.commit()

print(f"Завдання успішно створено! ID: {task_id}")

cursor.close()
connection.close()
