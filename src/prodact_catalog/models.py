import logging
from typing import List, Optional

# Добавляем настройку логгера
logger = logging.getLogger(__name__)


class Product:
    """Класс, представляющий продукт."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализирует продукт с заданными атрибутами.

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

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None):
        """
        Инициализирует категорию с заданными атрибутами.

        Args:
            name (str): Название категории.
            description (str): Описание категории.
            products (Optional[List[Product]], optional): Список продуктов. По умолчанию None.
        """
        self.name = name
        self.description = description
        self.products: List[Product] = products or []

        # Логируем создание категории
        logger.info(f"Создана новая категория: {name}")

        # Увеличиваем счетчики класса
        Category.category_count += 1
        Category.product_count += len(self.products)

        # Логируем количество продуктов в категории
        logger.debug(f"Количество продуктов в категории '{name}': {len(self.products)}")

    def add_product(self, product: Product) -> None:
        """
        Добавляет продукт в категорию.

        Args:
            product (Product): Продукт для добавления.
        """
        # Проверяем, что передан корректный объект Product
        if product is None:
            error_msg = f"Ошибка при добавлении продукта None в категорию '{self.name}'"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            self.products.append(product)
            Category.product_count += 1

            # Логируем добавление продукта
            logger.info(f"Добавлен продукт '{product.name}' в категорию '{self.name}'")
        except Exception as e:
            # Логируем ошибку при добавлении продукта
            logger.error(f"Ошибка при добавлении продукта '{product.name}' в категорию '{self.name}': {e}")
            raise
