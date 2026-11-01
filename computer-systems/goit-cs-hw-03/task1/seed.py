import random
import psycopg2
from faker import Faker

NUMBER_STATUSES = 3
NUMBER_USERS = 10
NUMBER_TASKS = 30

fake = Faker("uk_UA")

def generate_fake_data(number_users, number_statuses, number_tasks):

    fake_statuses = ["new", "in progress", "completed"]

    fake_users = []
    fake_tasks = []

    # Генеруємо користувачів
    for _ in range(number_users):
        fullname = fake.name()
        email = fake.unique.email()

        fake_users.append((fullname, email))

    # Генеруємо завдання
    for _ in range(number_tasks):
        title = fake.sentence(nb_words=4)
        description = fake.text(max_nb_chars=200)

        status = random.choice(fake_statuses)
        user_index = random.randrange(number_users)

        fake_tasks.append(
            (title, description, status, user_index)
        )

    return fake_statuses, fake_users, fake_tasks


def insert_data_to_db(users, statuses, tasks):

    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="task_manager",
        user="postgres",
        password=input("Введіть пароль PostgreSQL: ")
    )

    try:
        with connection:
            with connection.cursor() as cursor:

                # Додаємо статуси
                # N CONFLICT (name) DO NOTHING - якщо статус уже існує, PostgreSQL не створюватиме його повторно
                for status_name in statuses:
                    cursor.execute(
                        """
                        INSERT INTO status (name)
                        VALUES (%s)
                        ON CONFLICT (name) DO NOTHING;
                        """,
                        (status_name,)
                    )

                # Отримуємо ID статусів
                cursor.execute("SELECT id, name FROM status;")

                status_ids = {
                    name: status_id
                    for status_id, name in cursor.fetchall()
                }

                # Додаємо користувачів
                user_ids = []

                for fullname, email in users:
                    cursor.execute(
                        """
                        INSERT INTO users (fullname, email)
                        VALUES (%s, %s)
                        RETURNING id;
                        """,
                        (fullname, email)
                    )
                    # беремо ID користувачів
                    user_ids.append(cursor.fetchone()[0])

                # Додаємо завдання
                for title, description, status, user_index in tasks:
                    cursor.execute(
                        """
                        INSERT INTO tasks
                        (title, description, status_id, user_id)
                        VALUES (%s, %s, %s, %s);
                        """,
                        (
                            title,
                            description,
                            status_ids[status],
                            user_ids[user_index]
                        )
                    )

        print("Дані успішно додано!")
        print(f"Користувачів: {len(users)}")
        print(f"Статусів: {len(statuses)}")
        print(f"Завдань: {len(tasks)}")

    finally:
        connection.close()

if __name__ == "__main__":

    statuses, users, tasks = generate_fake_data(
        NUMBER_USERS,
        NUMBER_STATUSES,
        NUMBER_TASKS
    )

    insert_data_to_db(users, statuses, tasks)