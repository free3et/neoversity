import timeit
from boer_mur import boyer_moore_search
from knut_morris_pratt import kmp_search
from rabin_karp import rabin_karp_search

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print("Файл не знайдено, будь ласка перевірте шлях до файлу!")
        return None

article1 = read_file("article1.txt")
article2 = read_file("article2.txt")
repeats = 100

print("--- article 1, існуючий підрядок ---")
print("boyer_moore_search >>>", timeit.timeit(lambda: boyer_moore_search(article1, "стандартна бібліотека"), number=repeats))
print("kmp_search >>>", timeit.timeit(lambda: kmp_search(article1, "стандартна бібліотека"), number=repeats))
print("rabin_karp_search >>>", timeit.timeit(lambda: rabin_karp_search(article1, "стандартна бібліотека"), number=repeats))
print("--------------------------------")

print("--- article 1, вигаданий підрядок ---")
print("boyer_moore_search >>>", timeit.timeit(lambda: boyer_moore_search(article1, "вигаданий підрядок xyz"), number=repeats))
print("kmp_search >>>", timeit.timeit(lambda: kmp_search(article1, "вигаданий підрядок xyz"), number=repeats))
print("rabin_karp_search >>>", timeit.timeit(lambda: rabin_karp_search(article1, "вигаданий підрядок xyz"), number=repeats))
print("--------------------------------")

print("--- article 2, існуючий підрядок ---")
print("boyer_moore_search >>>", timeit.timeit(lambda: boyer_moore_search(article2, "досягнення поставленої мети"), number=repeats))
print("kmp_search >>>", timeit.timeit(lambda: kmp_search(article2, "досягнення поставленої мети"), number=repeats))
print("rabin_karp_search >>>", timeit.timeit(lambda: rabin_karp_search(article2, "досягнення поставленої мети"), number=repeats))
print("--------------------------------")

print("--- article 2, вигаданий підрядок ---")
print("boyer_moore_search >>>", timeit.timeit(lambda: boyer_moore_search(article2, "неіснуючий рядок qwerty"), number=repeats))
print("kmp_search >>>", timeit.timeit(lambda: kmp_search(article2, "неіснуючий рядок qwerty"), number=repeats))
print("rabin_karp_search >>>", timeit.timeit(lambda: rabin_karp_search(article2, "неіснуючий рядок qwerty"), number=repeats))
print("--------------------------------")
