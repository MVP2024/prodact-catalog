import logging

from src.data_loader import load_categories
from src.models import Category, Product

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    # Формируем путь к файлу
    file_path = r"D:\Projects\poetry\ProductCatalog\data\products.json"

    categories = load_categories(file_path)

    # Создаем несколько продуктов
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Выводим информацию о каждом продукте
    print("Информация о продуктах:")
    for product in [product1, product2, product3]:
        print(f"Название: {product.name}")
        print(f"Описание: {product.description}")
        print(f"Цена: {product.price}")
        print(f"Количество: {product.quantity}\n")

    # Создаем категорию с продуктами
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    # Проверяем свойства категории
    print(f"Название категории: {category1.name}")
    print(f"Описание категории: {category1.description}")
    print(f"Количество продуктов в категории: {len(category1.products)}")

    # Создаем вторую категорию с продуктами
    category2 = Category("Планшеты", "Планшеты, как средство для работы и развлечений", [])

    # Проверяем свойства второй категории
    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)  # Это выведет список продуктов

    print(Category.category_count)  # Статический счетчик категорий
    print(Category.product_count)  # Статический счетчик продуктов
