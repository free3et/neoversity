
from faker import Faker
import random

# Створюємо об'єкт Faker
fake = Faker("uk_UA")

NUMBER_USERS = 10
NUMBER_TASKS = 30

fake_statuses = [
    "new",
    "in progress",
    "completed"
]

fake_users = []
fake_tasks = []

# генеруємо 10 юзерів
for _ in range(NUMBER_USERS):
    fullname = fake.name()
    email = fake.unique.email()
    title = fake.sentence()
    description = fake.text()

    fake_users.append((fullname, email, title, description))

print(fake_users)

# генеруємо 30 задач
for _ in range(NUMBER_TASKS):

    title = fake.sentence(nb_words=4)
    description = fake.text(max_nb_chars=200)

    status = random.choice(fake_statuses)

    fake_tasks.append((title, description, status))

print(fake_tasks)