keywords = ["Гаррі", "Геґрід", "вокзал"]

files = [
    "text/harry_potter.txt",
    "text/harry_potter2.txt",
    "text/harry_potter3.txt",
]

def search_in_file(file_path, keywords):
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results.append(keyword)                 
            return results
    except FileNotFoundError:
        print('Файл не знайдено, будь ласка перевірте шлях до файлу!')
        return None
    except PermissionError:
        print(f"Немає доступу до файлу: {file_path}")
        return None

    except OSError as error:
        print(f"Помилка читання файлу: {error}")
        return None

def process_files(files, keywords):
    results = {}

    for keyword in keywords:
        results[keyword] = []

    for file_path in files:

        found_keywords = search_in_file(file_path, keywords)

        if found_keywords is not None:
            for keyword in found_keywords:
                results[keyword].append(file_path)

    return results