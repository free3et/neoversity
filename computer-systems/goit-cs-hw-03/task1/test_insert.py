
import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="task_manager",
    user="postgres",
    password=input("Введіть пароль PostgreSQL: ")
)

cursor = connection.cursor()

# Додаємо користувача
cursor.execute(
    """
    INSERT INTO users (fullname, email)
    VALUES (%s, %s)
    RETURNING id;
    """,
    ("Тестовий користувач", "test_user_001@example.com")
)

# Отримуємо ID нового користувача
user_id = cursor.fetchone()[0]

# Зберігаємо зміни
connection.commit()

print(f"Користувача додано! Його ID: {user_id}")

cursor.close()
connection.close()
