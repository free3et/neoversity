from threading import Thread, Lock
from time import perf_counter
from shared import process_files, keywords, files

start_time = perf_counter()
first_part = files[:(len(files) // 2)]
second_part = files[(len(files) // 2):]

final_results = {
    keyword: [] for keyword in keywords
}

lock = Lock()

def thread_worker(file_part, keywords, final_results, lock):
    try:
        local_results = process_files(file_part, keywords)

        with lock:
            for keyword, paths in local_results.items():
                final_results[keyword].extend(paths)

    except Exception as error:
        print(f"Помилка потоку: {error}")

thread1 = Thread(
    target=thread_worker,
    args=(first_part, keywords, final_results, lock)
)

thread2 = Thread(
    target=thread_worker,
    args=(second_part, keywords, final_results, lock)
)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Результати багатопотокового пошуку:")
print(final_results)

end_time = perf_counter()

execution_time = end_time - start_time

print(f"Час виконання: {execution_time:.4f} секунд")

'''
    Результати багатопотокового пошуку:
    {'Гаррі': ['text/harry_potter.txt', 'text/harry_potter2.txt', 'text/harry_potter3.txt'], 'Геґрід': ['text/harry_potter.txt', 'text/harry_potter2.txt', 'text/harry_potter3.txt'], 'вокзал': ['text/harry_potter3.txt']}
    Час виконання: 0.0010 секунд
'''