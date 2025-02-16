from typing import List

class Product:
    """Класс, представляющий продукт."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Инициализирует продукт с заданными атрибутами.

        Args:
            name (str): Название продукта.
            description (str): Описание продукта.
            price (float): Цена продукта.
            quantity (int): Количество продукта в наличии.
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

class Category:
    """Класс, представляющий категорию продуктов."""

    total_categories = 0
    total_products = 0

    def __init__(self, name: str, description: str):
        """Инициализирует категорию с заданными атрибутами.

        Args:
            name (str): Название категории.
            description (str): Описание категории.
        """
        self.name = name
        self.description = description
        self.products: List[Product] = []
        Category.total_categories += 1

    def add_product(self, product: Product):
        """Добавляет продукт в категорию и увеличивает общее количество товаров.

        Args:
            product (Product): Продукт, который нужно добавить.
        """
        self.products.append(product)
        Category.total_products += 1
