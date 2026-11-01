import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="task_manager",
    user="postgres",
    password=input("Введіть пароль PostgreSQL: ")
)

cursor = connection.cursor()

# Отримуємо всі статуси
cursor.execute("SELECT id, name FROM status;")

statuses = cursor.fetchall()

status_ids = {
    name: status_id
    for status_id, name in statuses
}

print(status_ids)

print("Наші статуси:")

for status in statuses:
    print(status)

cursor.close()
connection.close()
