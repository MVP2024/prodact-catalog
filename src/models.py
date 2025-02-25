import logging
from typing import Any, Dict, List, Optional

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
        self._price = price
        self.quantity = quantity

    # Свойства и сеттеры
    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """
        Сеттер для цены с проверкой корректности значения.

        Args:
            value (float): Новое значение цены.
        """
        # Проверка на нулевую или отрицательную цену
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            logger.error("Цена не должна быть нулевая или отрицательная")
            return

        # Проверка на понижение цены
        if value < self._price:
            confirmation = (
                input(f"Вы действительно хотите понизить цену с {self._price} до {value}? (y/n): ").lower().strip()
            )

            if confirmation != "y":
                print("Понижение цены отменено.")
                logger.info(f"Понижение цены отменено. Текущая цена: {self._price}")
                return

        # Если все проверки пройдены, устанавливаем новую цену
        self._price = value
        logger.info(f"Цена обновлена до {value}")

    # Магические методы представления
    def __str__(self) -> str:
        """
        Строковое представление продукта.

        Returns:
            str: Строка с информацией о продукте в формате
            "Название продукта, цена руб. Остаток: количество шт."
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        """
        Создает строковое представление продукта.

        Возвращает подробную информацию о продукте в формате:
        "Название, цена руб. Остаток: количество шт."

        Returns:
            str: Строка с информацией о продукте
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """
        Метод сложения двух продуктов, возвращающий общую стоимость товаров на складе.

        Args:
            other (Product): Второй продукт для сложения.

        Returns:
            float: Общая стоимость товаров на складе (цена * количество).

        Raises:
            TypeError: Если аргумент не является экземпляром Product.
        """
        if not isinstance(other, Product):
            raise TypeError(f"Unsupported operand type for +: '{type(self).__name__}' and '{type(other).__name__}'")

        return self.price * self.quantity + other.price * other.quantity

    # Классовые методы создания продуктов
    @classmethod
    @classmethod
    def new_product(cls, product_dict: Dict[str, Any]) -> "Product":
        """
        Класс-метод для создания нового продукта из словаря.

        Args:
            product_dict (Dict[str, Any]): Словарь с параметрами продукта.

        Returns:
            Product: Новый объект продукта.
        """
        return cls(
            name=str(product_dict.get("name", "")) if product_dict.get("name") is not None else "",
            description=str(product_dict.get("description", "")) if product_dict.get("description") is not None else "",
            price=float(product_dict.get("price", 0.0))
                if isinstance(product_dict.get("price"), (int, float))
                else 0.0,
            quantity=int(product_dict.get("quantity", 0))
                if isinstance(product_dict.get("quantity"), (int, float))
                else 0
        )

    @classmethod
    def create_product(cls, product_dict: Dict[str, Any], product_list: Optional[List["Product"]] = None) -> "Product":
        """
        Создает новый продукт с проверкой существующих товаров.

        Args:
            product_dict (Dict[str, Any]): Словарь с параметрами продукта.
            product_list (Optional[List[Product]], optional): Список существующих продуктов.

        Returns:
            Product: Новый или обновленный объект продукта.
        """
        # Извлекаем параметры из словаря
        name = product_dict.get("name", "")
        description = product_dict.get("description", "")
        price = product_dict.get("price", 0.0)
        quantity = product_dict.get("quantity", 0)

        # Если передан список продуктов, проверяем наличие дубликатов
        if product_list:
            for existing_product in product_list:
                # Сравниваем имена без учета регистра
                if existing_product.name.lower() == name.lower():
                    # Обновляем количество
                    existing_product.quantity += quantity

                    # Выбираем максимальную цену
                    existing_product.price = max(existing_product.price, price)

                    logger.info(
                        f"Обновлен существующий продукт '{name}': "
                        f"количество {existing_product.quantity}, "
                        f"цена {existing_product.price}"
                    )

                    return existing_product

        # Если дубликат не найден, создаем новый продукт
        new_product = cls(name, description, price, quantity)
        logger.info(f"Создан новый продукт '{name}'")
        return new_product


class CategoryIterator:
    """
    Итератор для перебора товаров в категории.

    Attributes:
        _category (Category): Категория, товары которой будут перебираться.
        _index (int): Текущий индекс при итерации.
    """

    def __init__(self, category: "Category"):
        """
        Инициализация итератора для категории.

        Args:
            category (Category): Категория, товары которой будут перебираться.
        """
        self._category = category
        self._index = 0

    def __iter__(self) -> "CategoryIterator":
        """
        Возвращает сам объект итератора.

        Returns:
            CategoryIterator: Текущий итератор.
        """
        return self

    def __next__(self) -> "Product":
        """
        Возвращает следующий товар в категории.

        Returns:
            Product: Следующий товар.

        Raises:
            StopIteration: Когда товары в категории закончились.
        """
        if self._index < len(self._category.products):
            product = self._category.products[self._index]
            self._index += 1
            return product

        raise StopIteration


class Category:
    """Класс, представляющий категорию продуктов."""

    # Статические атрибуты
    category_count = 0
    _product_count = 0

    # Магический метод инициализации
    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None):
        """
        Инициализирует категорию с заданными атрибутами.

        Args:
            name (str): Название категории.
            description (str): Описание категории.
            products (Optional[List[Product]], optional): Список продуктов в категории.
        """
        self.name = name
        self.description = description
        self._products: List[Product] = []

        logger.info(f"Создана новая категория: {name}")
        Category.category_count += 1

        if products:
            logger.debug(f"Попытка добавить {len(products)} продуктов в категорию {name}")
            for product in products:
                logger.debug(f"Добавляю продукт: {product.name}")
                self.add_product(product)

    # Методы работы с продуктами
    def add_product(self, product: Product) -> None:
        """
        Добавляет продукт в категорию.

        Args:
            product (Product): Продукт для добавления.

        Raises:
            ValueError: Если продукт None или возникла ошибка при добавлении.
        """
        if product is None:
            error_msg = f"Ошибка при добавлении продукта None в категорию '{self.name}'"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            self._products.append(product)
            Category._product_count += 1
            logger.info(f"Добавлен продукт '{product.name}' в категорию '{self.name}'")
        except Exception as e:
            error_msg = f"Ошибка при добавлении продукта в категорию '{self.name}': {e}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    # Магические методы
    def __iter__(self) -> "CategoryIterator":
        """
        Возвращает итератор для перебора товаров в категории.

        Returns:
            CategoryIterator: Итератор товаров категории.
        """
        return CategoryIterator(self)

    def __str__(self) -> str:
        """
        Строковое представление категории.

        Returns:
            str: Строка с информацией о категории в формате
            "Название категории, количество товаров: X шт."
        """
        total_quantity = sum(product.quantity for product in self._products)
        return f"{self.name}, количество товаров: {total_quantity} шт."

    # Свойства
    @property
    def products(self) -> List[Product]:
        """
        Геттер для получения копии списка продуктов.

        Returns:
            List[Product]: Копия списка продуктов.
        """
        return self._products.copy()

    @property
    def product_count(self) -> int:
        """
        Геттер для получения количества продуктов в категории.

        Returns:
            int: Количество продуктов в категории.
        """
        product_count = len(self._products)
        logger.debug(f"Количество продуктов в категории '{self.name}': {product_count}")
        return product_count

    @property
    def product_list(self) -> str:
        """
        Геттер для получения списка продуктов в виде строки.

        Returns:
            str: Строка с описанием продуктов в категории.
        """
        if not self._products:
            return "В категории нет товаров"

        product_descriptions = [
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            for product in self._products
        ]
        return "\n".join(product_descriptions)

    # Классовые методы
    @classmethod
    def get_total_product_count(cls) -> int:
        """
        Класс-метод для получения общего количества продуктов во всех категориях.

        Returns:
            int: Общее количество продуктов.
        """
        return cls._product_count

    @property
    def product_list(self) -> str:
        """
        Геттер для получения списка продуктов в виде строки.

        Returns:
            str: Строка с описанием продуктов в категории.
        """
        if not self._products:
            return "В категории нет товаров"

        product_descriptions = []
        for product in self._products:
            product_descriptions.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")

        return "\n".join(product_descriptions)
