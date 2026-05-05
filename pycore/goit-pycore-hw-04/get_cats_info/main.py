def get_cats_info(path: str) -> list[dict]:
    try:
        cats_info = []
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                try: 
                    id, name, age = line.split(',')
                    cats_info.append({
                    "id": id,
                    "name": name,
                    "age": age,
                })
                except ValueError:
                    print(f"Некоректний рядок: {line}")
                    continue    
            return cats_info
    except FileNotFoundError:
        print('Файл не знайдено, будь ласка перевірте шлях до файлу!')
        return None

cats_info = get_cats_info("cats_info.csv")
print(cats_info)