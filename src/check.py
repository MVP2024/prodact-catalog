import logging
import os

from src.prodact_catalog.data_loader import load_categories

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    # Формируем путь к файлу
    file_path = r"D:\Projects\poetry\ProductCatalog\data\products.json"

    # Выводим путь для отладки
    print(f"Путь к файлу: {file_path}")
    print("Текущая рабочая директория:", os.getcwd())  # Выводим текущую рабочую директорию

    categories = load_categories(file_path)

    # Выводим загруженные категории
    print("Загруженные категории:")
    for category in categories:
        print(category)
