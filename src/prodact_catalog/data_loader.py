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
            logger.info(f"Чтение данных из файла: {file_path}")
            data = json.load(file)

            if not isinstance(data, list):
                logger.warning("Загруженные данные не являются списком")
                return []

            categories = []
            for category_data in data:
                # Проверка наличия обязательных полей
                if not all(key in category_data for key in ["name", "description"]):
                    logger.warning(f"Пропуск категории: отсутствуют обязательные поля. Данные: {category_data}")
                    continue

                # Проверка типов данных
                if not isinstance(category_data["name"], str) or not isinstance(category_data["description"], str):
                    logger.warning(f"Пропуск категории: некорректный тип данных. Данные: {category_data}")
                    continue

                try:
                    # Создание категории с безопасной обработкой
                    category = Category(name=category_data["name"], description=category_data["description"])

                    # Обработка продуктов с дополнительной валидацией
                    products_data = category_data.get("products", [])
                    for product_data in products_data:
                        # Проверка наличия обязательных полей для продукта
                        if not all(key in product_data for key in ["name", "price", "quantity"]):
                            logger.warning(f"Пропуск продукта: отсутствуют обязательные поля. Данные: {product_data}")
                            continue

                        # Проверка типов данных продукта
                        try:
                            product = Product(
                                name=product_data["name"],
                                description=product_data.get("description", ""),
                                price=float(product_data["price"]),
                                quantity=int(product_data["quantity"]),
                            )
                            category.add_product(product)
                        except (ValueError, TypeError) as e:
                            logger.warning(f"Ошибка при создании продукта: {e}. Данные: {product_data}")

                    # Добавляем категорию только если есть хотя бы один корректный продукт
                    if category.products:
                        categories.append(category)
                        logger.info(f"Категория '{category.name}' успешно добавлена")
                    else:
                        logger.warning(f"Категория '{category.name}' не содержит корректных продуктов")

                except Exception as e:
                    logger.error(f"Ошибка при обработке категории: {e}")
                    continue

            logger.info(f"Успешно загружено {len(categories)} категорий")
            return categories

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Ошибка при загрузке JSON: {e}")
        return []
