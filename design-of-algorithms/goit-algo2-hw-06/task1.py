import string

from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import matplotlib.pyplot as plt
import requests


def get_text(url: str) -> str:
    # Отримання тексту з URL-адреси
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        return None


# Функція для видалення знаків пунктуації
def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word: str) -> tuple[str, int]:
    return word, 1


def shuffle_function(mapped_values: list[tuple[str, int]]) -> list[tuple[str, list[int]]]:
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values: tuple[str, list[int]]) -> tuple[str, int]:
    key, values = key_values
    return key, sum(values)


# Виконання MapReduce
def map_reduce(text: str, search_words: list[str] = None) -> dict[str, int]:
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Якщо задано список слів для пошуку, враховувати тільки ці слова
    if search_words:
        words = [word for word in words if word in search_words]

    # Паралельний Маппінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(word_counts: dict[str, int], top_n: int = 10) -> None:
    # Візуалізує топ-N найпопулярніших слів за допомогою горизонтального bar chart
    if not word_counts:
        print("Немає даних для візуалізації.")
        return

    # Сортування слів за спаданням частоти та вибір top_n
    sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:top_n]
    words, counts = zip(*reversed(sorted_words))  # Реверс для коректного відображення зверху вниз на діаграмі

    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color="skyblue", edgecolor="black")
    plt.xlabel("Частота використання", fontsize=12)
    plt.ylabel("Слова", fontsize=12)
    plt.title(f"Топ-{top_n} найпопулярніших слів у тексті", fontsize=14, fontweight="bold")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # URL-адреса для завантаження тексту (наприклад, "War and Peace" з Gutenberg)
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    
    print("Завантаження тексту...")
    text = get_text(url)

    if text:
        print("Виконання аналізу MapReduce...")
        word_frequencies = map_reduce(text)

        print(f"Всього унікальних слів знайдено: {len(word_frequencies)}")
        
        # Візуалізація Топ-10 слів
        visualize_top_words(word_frequencies, top_n=10)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")