import asyncio
import argparse
import pathlib
import shutil
import logging

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

parser = argparse.ArgumentParser(
    description="Асинхронне сортування файлів"
)

parser.add_argument("source")
parser.add_argument("output")
args = parser.parse_args()
source = args.source
output = args.output

source_path = pathlib.Path(source)
output_path = pathlib.Path(output)

async def copy_file(file_path, output_path):
    try:
        extension = file_path.suffix[1:].lower()

        folder = output_path / extension

        folder.mkdir(parents=True, exist_ok=True)
        destination = folder / file_path.name

        await asyncio.to_thread(shutil.copy2, file_path, destination)
    except Exception as error:
        logging.error(
            "Не вдалося скопіювати файл %s: %s",
            file_path,
            error
        )

async def read_folder(source_path, output_path):
    if not source_path.is_dir():
        logging.error("Вихідна папка не існує: %s", source_path)
        return

    def find_files():
        files = []

        # знаходимо всі об'єкти у вихідній папці та підпапках
        for file_path in source_path.rglob("*"):
            if file_path.is_file():
                files.append(file_path)

        return files

    
    files = await asyncio.to_thread(find_files)
    tasks = []

    for file_path in files:
        task = copy_file(file_path, output_path)
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(read_folder(source_path, output_path))
