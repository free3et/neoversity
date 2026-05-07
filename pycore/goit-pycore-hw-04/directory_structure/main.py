import sys
from pathlib import Path
from colorama import Fore, Style

def display_directory_structure(path: str, space=""):
    try:
        dir_path = Path(path)

        for item in dir_path.iterdir():
            if item.is_dir(): # якщо елемент папка
                print(f"{space}📦{Fore.YELLOW}{item.name}{Style.RESET_ALL}")
                display_directory_structure(item, space + "  ") # рекурсивно обходимо папки і додаємо відступи для наочності
            else: # якщо елемент є файлом
                print(f"{space}📄{Fore.GREEN}{item.name}{Style.RESET_ALL}")
    except FileNotFoundError: # якщо директорія не знайдена
        print(f"{Fore.RED}Директорія не знайдена{Style.RESET_ALL}")
    except PermissionError: # якщо немає доступу до директорії
        print(f"{Fore.RED}Немає доступу до директорії{Style.RESET_ALL}")

if len(sys.argv) < 2: # перевірка наявності аргументу командного рядка
    print("Вкажіть шлях до директорії!")
    sys.exit()

path = Path(sys.argv[1]) # отримуємо шлях до директорії

if not path.exists(): # якщо директорія не існує
    print(f"{Fore.RED}Директорія не знайдена{Style.RESET_ALL}")
    sys.exit()

if not path.is_dir(): # якщо шлях не є директорією
    print(f"{Fore.RED}Вказаний шлях не є директорією{Style.RESET_ALL}")
    sys.exit()
print(f"{Fore.YELLOW}📦 {path.name}{Style.RESET_ALL}") # виведення кореневої директорії

display_directory_structure(path) # викликаємо функцію для виведення структури директорії