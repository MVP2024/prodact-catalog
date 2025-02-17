import json
import logging
from typing import List

from .models import Category, Product

logger = logging.getLogger(__name__)


def load_categories(file_path: str) -> List[Category]:
    """
    Загружает данные о категориях и продуктах из JSON-файла.
    """
    logger.debug(f"Попытка загрузить категории из файла: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            logger.info(f"Чтение данных из файла: {file_path}")  # Логируем чтение файла
            data = json.load(file)

            if not isinstance(data, list):
                logger.warning("Загруженные данные не являются списком. Возвращается пустой список.")
                print("Загруженные данные не являются списком. Возвращается пустой список.")  # Отладочное сообщение
                return []

            categories = []
            for category_data in data:
                try:
                    logger.info(f"Обработка категории: {category_data['name']}")  # Логируем обработку категории
                    category = Category(category_data["name"], category_data["description"])
                    for product_data in category_data.get("products", []):
                        product = Product(
                            product_data["name"],
                            product_data.get("description", ""),
                            product_data["price"],
                            product_data["quantity"],
                        )
                        category.add_product(product)
                    categories.append(category)
                    logger.info(
                        f"Категория '{category.name}' успешно добавлена."
                    )  # Логируем успешное добавление категории
                except KeyError as e:
                    logger.error(f"Ошибка при обработке категории: {e}. Данные: {category_data}")
                    print(f"Ошибка при обработке категории: {e}. Данные: {category_data}")  # Отладочное сообщение
                    continue

            logger.info(f"Успешно загружено {len(categories)} категорий.")
            print(f"Успешно загружено {len(categories)} категорий.")  # Отладочное сообщение
            return categories

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        print(f"Файл не найден: {file_path}")  # Отладочное сообщение
        return []
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Ошибка при загрузке JSON: {e}")
        print(f"Ошибка при загрузке JSON: {e}")  # Отладочное сообщение
        return []
