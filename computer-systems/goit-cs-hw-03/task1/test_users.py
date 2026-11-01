
import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="task_manager",
    user="postgres",
    password=input("Введіть пароль PostgreSQL: ")
)

cursor = connection.cursor()

# Отримуємо ID та імена користувачів
cursor.execute(
    "SELECT id, fullname FROM users;"
)

users = cursor.fetchall()

user_ids = [user[0] for user in users]

print("ID користувачів:", user_ids)

print("Наші користувачі:")

for user in users:
    print(user)

cursor.close()
connection.close()
