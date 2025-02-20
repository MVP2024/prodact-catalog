import json
import os
from typing import Any, Dict, List

from src.prodact_catalog.data_loader import load_categories
from src.prodact_catalog.logger import setup_logger

logger = setup_logger(__name__)


def main() -> List[Dict[str, Any]]:
    logger.info("Запуск функции main.")

    file_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "products.json")
    logger.debug(f"Проверка существования файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    try:
        logger.info("Попытка загрузки категорий из файла...")
        categories = load_categories(file_path)
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка при загрузке JSON: {e}")
        print("Caught JSONDecodeError")  # Отладочное сообщение
        return []

    result: List[Dict[str, Any]] = []
    if categories:
        for category in categories:
            category_info: Dict[str, Any] = {
                "name": category.name,
                "description": category.description,
                "products": [],
            }
            if category.products:
                for product in category.products:
                    product_info: Dict[str, Any] = {
                        "name": product.name,
                        "price": product.price,
                        "quantity": product.quantity,
                    }
                    category_info["products"].append(product_info)
            else:
                logger.warning(f"Категория '{category.name}' не содержит продуктов.")
                print(f"Категория '{category.name}' не содержит продуктов.")  # Отладочное сообщение

            result.append(category_info)

    output_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "output_categories.json")
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    logger.info(f"Данные успешно сохранены в {output_file_path}")
    print(f"Данные успешно сохранены в {output_file_path}")
    return result


# if __name__ == "__main__":
#     categories_data = main()
#     print(categories_data)  # закомичено, чтобы не занижал тесты))
