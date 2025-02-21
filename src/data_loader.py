import json
import logging
from typing import List

from .models import Category, Product

logger = logging.getLogger(__name__)


def load_categories(file_path: str) -> List[Category]:
    logger.info(f"Начало загрузки категорий из файла: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        logger.debug(f"Загружено {len(data)} записей из файла")

        categories = []
        for category_data in data:
            try:
                category = Category(name=category_data["name"], description=category_data["description"])

                for product_data in category_data.get("products", []):
                    try:
                        product = Product(
                            name=product_data["name"],
                            description=product_data.get("description", ""),
                            price=float(product_data["price"]),
                            quantity=int(product_data["quantity"]),
                        )
                        category.add_product(product)
                    except (KeyError, ValueError) as e:
                        logger.warning(f"Ошибка при создании продукта: {e}")

                if category.products:
                    categories.append(category)
                    logger.info(f"Добавлена категория: {category.name}")
                else:
                    logger.warning(f"Категория {category.name} не содержит продуктов")

            except (KeyError, ValueError) as e:
                logger.error(f"Ошибка при обработке категории: {e}")

        logger.info(f"Загружено {len(categories)} категорий")
        return categories

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при загрузке файла: {e}")
        return []
