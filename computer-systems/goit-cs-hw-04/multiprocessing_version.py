
from multiprocessing import Process, Queue
from shared import process_files, keywords, files
from time import perf_counter

def worker(file_part, keywords, queue):
    try:
        results = process_files(file_part, keywords)
        queue.put(("success", results))
    except Exception as error:
        queue.put(("error", str(error)))

if __name__ == "__main__":
    start_time = perf_counter()
    first_part = files[:len(files) // 2]
    second_part = files[len(files) // 2:]

    queue = Queue()

    process1 = Process(
        target=worker,
        args=(first_part, keywords, queue)
    )

    process2 = Process(
        target=worker,
        args=(second_part, keywords, queue)
    )

    process1.start()
    process2.start()

    result1 = queue.get()
    result2 = queue.get()

    process1.join()
    process2.join()

    final_results = {
        keyword: [] for keyword in keywords
    }

    for result in [result1, result2]:
        for keyword, paths in result.items():
            final_results[keyword].extend(paths)

    print("Результати multiprocessing:")
    print(final_results)

    queue.close()
    queue.join_thread()

    end_time = perf_counter()

    execution_time = end_time - start_time

    print(f"Час виконання: {execution_time:.4f} секунд")

'''
    Результати multiprocessing:
    {'Гаррі': ['text/harry_potter.txt', 'text/harry_potter2.txt', 'text/harry_potter3.txt'], 'Геґрід': ['text/harry_potter.txt', 'text/harry_potter2.txt', 'text/harry_potter3.txt'], 'вокзал': ['text/harry_potter3.txt']}
    Час виконання: 0.0756 секунд
'''