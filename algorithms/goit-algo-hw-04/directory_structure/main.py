import sys
from pathlib import Path
from colorama import Fore, Style
import shutil

def copy_and_sort_files(dir_path: Path, new_dir_path: Path, abs_target_path: Path):
    try: 
        for item in dir_path.iterdir():
            # Якщо підпапка або файл є нашою цільовою директорією призначення — пропуск
            if item.resolve() == abs_target_path:
                continue 
                
            if item.is_dir(): 
                copy_and_sort_files(item, new_dir_path, abs_target_path) 
            else:
                # Отримуємо розширення без крапки
                extension = item.suffix[1:].lower()
                
                # Створюємо шлях до цільової папки
                target_folder = new_dir_path / extension
                target_folder.mkdir(parents=True, exist_ok=True)
                new_path = target_folder / item.name
                
                # Копіюємо файл у підготовлене місце
                shutil.copy2(item, new_path)
                print(f"✅ Скопійовано: {Fore.GREEN}{item.name}{Style.RESET_ALL} -> {Fore.YELLOW}{extension}/{new_path.name}{Style.RESET_ALL}")

    except PermissionError: 
        print(f"{Fore.RED}❌ Немає доступу до директорії {dir_path.name}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Виникла помилка при обробці папки {dir_path.name}: {e}{Style.RESET_ALL}")

# Головний блок виконання
if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print(f"{Fore.CYAN}Використання: python script.py <шлях_до_директорії> [шлях_призначення]{Style.RESET_ALL}")
        sys.exit()

    path = Path(sys.argv[1]) 
    
    # Дозволяємо користувачу вводити свій шлях призначення або беремо "dist"
    target_arg = sys.argv[2] if len(sys.argv) > 2 else "dist"
    new_dir_path = Path(target_arg)
    abs_target_path = new_dir_path.resolve()

    if not path.exists(): 
        print(f"{Fore.RED}Директорія не знайдена{Style.RESET_ALL}")
        sys.exit()

    if not path.is_dir(): 
        print(f"{Fore.RED}Вказаний шлях не є директорією{Style.RESET_ALL}")
        sys.exit()
    
    copy_and_sort_files(path, new_dir_path, abs_target_path)
    print(f"\n{Fore.GREEN}🎉 Усі файли успішно розсортовано!{Style.RESET_ALL}")
