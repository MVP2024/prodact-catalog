import json
import os

from src.prodact_catalog.data_loader import load_categories, logger


def main() -> list:
    """
    Основная функция для загрузки категорий и продуктов из JSON-файла
    и сохранения информации о них в новый JSON-файл.

    Эта функция формирует путь к файлу JSON, загружает категории с помощью
    функции `load_categories`, а затем сохраняет информацию о каждой категории
    и ее продуктах в новый JSON-файл. Если категории не загружаются, записывается предупреждение
    в журнал.

    :return: Список категорий и продуктов.
    """
    # Укажите путь к вашему JSON-файлу
    file_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "products.json")

    try:
        categories = load_categories(file_path)
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка при загрузке JSON: {e}")
        return []

    result = []
    if categories:
        for category in categories:
            category_info = {
                "name": category.name,
                "description": category.description,
                "products": []
            }
            if category.products:
                for product in category.products:
                    product_info = {
                        "name": product.name,
                        "price": product.price,
                        "quantity": product.quantity
                    }
                    category_info["products"].append(product_info)
            else:
                logger.warning(f"Категория '{category.name}' не содержит продуктов.")  # Логируем пустую категорию

            result.append(category_info)

        # Сохранение результата в JSON-файл в корне проекта
        output_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "output_categories.json")
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        print(f"Данные успешно сохранены в {output_file_path}")
    else:
        logger.warning("Не удалось загрузить категории из файла.")

    return result


if __name__ == "__main__":
    categories_data = main()
    print(categories_data)  # Выводим возвращенные данные
