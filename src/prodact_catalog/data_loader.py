import json
import logging
from typing import List

from .models import Category, Product

logger = logging.getLogger(__name__)


def load_categories(file_path: str) -> List[Category]:
    """
    Загружает данные о категориях и продуктах из JSON-файла.

    :param file_path: Путь до JSON-файла.
    :return: Список объектов категорий или пустой список.
    """
    logger.debug(f"Попытка загрузить категории из файла: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if not isinstance(data, list):
                logger.warning("Загруженные данные не являются списком. Возвращается пустой список.")
                return []

            categories = []
            for category_data in data:
                try:
                    category = Category(category_data["name"], category_data["description"])
                    for product_data in category_data.get("products", []):
                        product = Product(
                            product_data["name"],
                            product_data.get("description", ""),  # Используем пустую строку по умолчанию
                            product_data["price"],
                            product_data["quantity"],
                        )
                        category.add_product(product)
                    categories.append(category)
                except KeyError as e:
                    logger.error(f"Ошибка при обработке категории: {e}. Данные: {category_data}")
                    continue  # Пропускаем некорректные категории

            logger.info(f"Успешно загружено {len(categories)} категорий.")
            return categories

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Ошибка при загрузке JSON: {e}")
        return []
