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
            name=product_dict.get("name", ""),
            description=product_dict.get("description", ""),
            price=product_dict.get("price", 0.0),
            quantity=product_dict.get("quantity", 0),
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


class Category:
    """Класс, представляющий категорию продуктов."""

    category_count = 0
    _product_count = 0  # Приватный атрибут для подсчета продуктов

    # def __init__(self, name: str, description: str, products: Optional[List[Product]] = None):
    #     self.name = name
    #     self.description = description
    #     self._products: List[Product] = []
    #
    #     # Логируем создание категории один раз
    #     logger.info(f"Создана новая категория: {name}")
    #
    #     # Увеличиваем счетчик категорий один раз
    #     Category.category_count += 1
    #
    #     # Добавляем продукты, если они переданы
    #     if products:
    #         for product in products:
    #             self.add_product(product)
    #
    #     # Логируем количество продуктов в категории
    #     logger.debug(f"Количество продуктов в категории '{name}': {len(self._products)}")
    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None):
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

    def add_product(self, product: Product) -> None:
        # Проверяем, что передан корректный объект Product
        if product is None:
            error_msg = f"Ошибка при добавлении продукта None в категорию '{self.name}'"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            self._products.append(product)
            Category._product_count += 1

            # Логируем добавление продукта
            logger.info(f"Добавлен продукт '{product.name}' в категорию '{self.name}'")
        except Exception as e:
            # Логируем ошибку при добавлении продукта
            error_msg = f"Ошибка при добавлении продукта в категорию '{self.name}': {e}"
            logger.error(error_msg)
            raise ValueError(error_msg)

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
            Также логирует информацию о количестве продуктов.
        """
        product_count = len(self._products)
        logger.debug(f"Количество продуктов в категории '{self.name}': {product_count}")
        return product_count

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
