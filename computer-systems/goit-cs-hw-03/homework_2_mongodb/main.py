
import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

# Завантажуємо налаштування з файлу .env
load_dotenv()

# Отримуємо рядок підключення
MONGO_URI = os.getenv("MONGO_URI")

# Підключаємося до MongoDB з certifi
client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where()
)

# Отримуємо базу даних котиків
db = client["cats_db"]

# Отримуємо колекцію котиків
cats_collection = db["cats"]


# Функція додавання одного кота
def add_cat(name, age, features):
    try:
        cat = {
            "name": name,
            "age": age,
            "features": features
        }

        result = cats_collection.insert_one(cat)

        print(f"Кота {name} успішно додано!")
        print(f"ID документа: {result.inserted_id}")

    except Exception as e:
        print("Помилка додавання кота:", e)

# Функція додавання декількох котиків
def add_many_cats():
    try:
        cats = [
            {
                "name": "barsik",
                "age": 3,
                "features": [
                    "ходить в капці",
                    "дає себе гладити",
                    "рудий"
                ]
            },
            {
                "name": "murzik",
                "age": 5,
                "features": [
                    "любить спати",
                    "сірий",
                    "грається з м'ячиком"
                ]
            },
            {
                "name": "pushok",
                "age": 2,
                "features": [
                    "білий",
                    "пухнастий",
                    "любить молоко"
                ]
            }
        ]

        result = cats_collection.insert_many(cats)

        print(f"Додано котів: {len(result.inserted_ids)}")

    except Exception as e:
        print("Помилка додавання котів:", e)

# Функція виведення всіх котів
def show_all_cats():
    try:
        cats = cats_collection.find()

        print("\nСписок усіх котів:")

        for cat in cats:
            print('🐱 🐱 🐱  🐱  🐱')
            print(f"ID: {cat['_id']}")
            print(f"Ім'я: {cat['name']}")
            print(f"Вік: {cat['age']}")
            print(f"Характеристики: {', '.join(cat['features'])}")

    except Exception as e:
        print("Помилка отримання списку котів:", e)

def find_cat_by_name(catname):
    try:
        cat = cats_collection.find_one({"name": catname})
        if cat:
            print('------------------------------')
            print(f"Кота {cat['name']} знайдено!")
            print(f"ID: {cat['_id']}")
            print(f"Ім'я: {cat['name']}")
            print(f"Вік: {cat['age']}")
            print(f"Характеристики: {', '.join(cat['features'])}")
            print('------------------------------')
        else:
            print(f"Халепа! Кота {catname} не знайдено.")
    except Exception as e:
        print("Помилка отримання кота:", e)

# Функція оновлення віку кота за ім'ям
def update_cat(catname, age):
    try:
        # Шукаємо кота в базі даних
        cat = cats_collection.find_one({"name": catname})

        if cat:
            # Оновлюємо вік кота
            updated_cat = cats_collection.update_one(
                {"name": catname},
                {"$set": {"age": age}}
            )
            print(f"Вік кота {catname} успішно оновлено на {age} років!")

        else:
            print(f"Кота {catname} не знайдено.")

    except Exception as e:
        print("Помилка оновлення кота:", e)

def update_cat_features(catname, feature):
    try:
        # Шукаємо кота в базі даних
        cat = cats_collection.find_one({"name": catname})

        if cat:
            # Оновлюємо features кота
            updated_cat = cats_collection.update_one(
                {"name": catname},
                {"$push": {"features": feature}}
            )
            print(f"До features кота {catname} успішно додано {feature}!")

        else:
            print(f"Кота {catname} не знайдено.")

    except Exception as e:
        print("Помилка оновлення кота:", e)

# Функція додавання одного кота

# Функція видалення кота за ім'ям
def delete_cat(catname):
    try:
        result = cats_collection.delete_one({"name": catname})

        if result.deleted_count > 0:
            print(f"Кота {catname} успішно видалено!")
        else:
            print(f"Кота {catname} не знайдено.")

    except Exception as e:
        print("Помилка видалення кота:", e)

# Функція видалення усіх котів
def delete_all_cats():
    try:
        result = cats_collection.delete_many({})

        print(
            f"Усіх котиків видалено! "
            f"Кількість видалених записів: {result.deleted_count}. "
            f"І як з таким гріхом на душі далі жити?"
        )

    except Exception as e:
        print("Помилка видалення котів:", e)

if __name__ == "__main__":
    try:
        # Перевіряємо підключення
        client.admin.command("ping")
        print("Успішне підключення до MongoDB!")

        # Створюємо колекцію, якщо її ще немає
        if "cats" not in db.list_collection_names():
            db.create_collection("cats")

        print("Базу даних cats_db та колекцію cats підготовлено!")

        # Додаємо котиків
        # add_many_cats()

        # Виводимо всіх котів
        show_all_cats()

        # Шукаємо кота за ім'ям
        find_cat_by_name("barsik")

        update_cat("barsik", 10)

        update_cat_features("barsik", 'шкрябає диван')

        # Видаляємо Пушка
        delete_cat("pushok")

        # Рука не підніметься таке розкоментувати
        # delete_all_cats()

    except Exception as e:
        print("Помилка роботи з MongoDB:", e)

    finally:
        # Закриваємо підключення після завершення роботи
        client.close()
