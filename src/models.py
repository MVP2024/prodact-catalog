import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

# Добавляем настройку логгера
logger = logging.getLogger(__name__)


class PrintInfoMixin:
    """
    Миксин для вывода информации о создании объекта.

    #__repr__ #множественное_наследование #миксины
    """

    def __init__(self, *args, **kwargs):
        """
        Метод инициализации с выводом информации о создаваемом объекте.

        Args:
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы.
        """
        print(f"Создан объект класса {self.__class__.__name__}")
        print(f"Параметры инициализации: {args}")

        # Вызываем метод инициализации родительского класса
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        """
        Расширенный метод repr для вывода полной информации об объекте.

        Returns:
            str: Строковое представление объекта с подробной информацией.
        """
        # Получаем стандартное строковое представление
        base_repr = super().__repr__()

        # Добавляем дополнительную информацию о классе
        return f"Объект класса {self.__class__.__name__}: {base_repr}"


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для всех продуктов.

    #ABC #abstractmethod
    """

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Абстрактный метод инициализации продукта.

        Args:
            name (str): Название продукта.
            description (str): Описание продукта.
            price (float): Цена продукта.
            quantity (int): Количество продукта.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Абстрактный метод строкового представления продукта.

        Returns:
            str: Строковое представление продукта.
        """
        pass

    @abstractmethod
    def __add__(self, other: 'BaseProduct') -> float:
        """
        Абстрактный метод сложения продуктов.

        Args:
            other (BaseProduct): Второй продукт для сложения.

        Returns:
            float: Результат сложения продуктов.
        """
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        """
        Абстрактное свойство для получения цены продукта.

        Returns:
            float: Цена продукта.
        """
        pass


class Product(PrintInfoMixin, BaseProduct):
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
        # Порядок важен: сначала миксин, потом BaseProduct
        super().__init__(name, description, price, quantity)

        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

        logger.info(f"Создан продукт: {name}")

    # Свойства и сеттеры
    @property
    def price(self) -> float:
        """Геттер для цены."""
        logger.debug(f"Получение цены для продукта '{self.name}'. " f"Текущая цена: {self._price}")
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

        # Если цена не изменилась, не выполняем никаких действий
        if value == self._price:
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
        logger.info(f"Цена обновлена до {value}")

    # Магические методы представления
    def __str__(self) -> str:
        """
        Строковое представление продукта.

        Returns:
            str: Строка с информацией о продукте в формате
            "Название продукта, цена руб. Остаток: количество шт."
        """
        str_representation = f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

        logger.debug(
            f"Сформирована строка str для продукта: '{self.name}'. " f"Полное представление: {str_representation}"
        )

        return str_representation

    def __repr__(self) -> str:
        """
        Создает строковое представление продукта.

        Возвращает подробную информацию о продукте в формате:
        "Название, цена руб. Остаток: количество шт."

        Returns:
            str: Строка с информацией о продукте
        """
        repr_string = f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

        logger.debug(f"Сформирована строка repr для продукта: '{self.name}'. " f"Полное представление: {repr_string}")

        return repr_string

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
        if other is None:
            error_msg = "Операция сложения невозможна с None"
            logger.error(error_msg)
            raise TypeError(error_msg)

        if not isinstance(other, Product):
            error_msg = f"Нельзя складывать товары разных типов: '{type(self).__name__}' и '{type(other).__name__}'"
            logger.error(error_msg)
            raise TypeError(error_msg)

        total_value = self.price * self.quantity + other.price * other.quantity
        logger.info(f"Выполнено сложение товаров: {self.name} и {other.name}. Общая стоимость: {total_value}")

        return total_value

    # Классовые методы создания продуктов
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
            name=(str(product_dict.get("name", "")) if product_dict.get("name") is not None else ""),
            description=(
                str(product_dict.get("description", "")) if product_dict.get("description") is not None else ""
            ),
            price=(
                float(product_dict.get("price", 0.0)) if isinstance(product_dict.get("price"), (int, float)) else 0.0
            ),
            quantity=(
                int(product_dict.get("quantity", 0)) if isinstance(product_dict.get("quantity"), (int, float)) else 0
            ),
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
        logger.debug(
            f"Инициализация итератора для категории '{category.name}'. "
            f"Общее количество продуктов: {len(category.products)}"
        )
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
            logger.debug(
                f"Итерация в категории '{self._category.name}'. "
                f"Возвращен продукт: {product.name}. "
                f"Текущий индекс: {self._index}"
            )

            return product

        logger.debug(f"Итерация в категории '{self._category.name}' завершена. " "Достигнут конец списка продуктов.")

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
    def add_product(self, product: Optional[Union[Product, str]] = None) -> None:
        # Проверка на None
        if product is None:
            error_msg = f"Ошибка при добавлении продукта в категорию '{self.name}'"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Если передана строка, можно добавить дополнительную логику
        if isinstance(product, str):
            logger.warning(f"Попытка добавить строку вместо продукта: {product}")
            return

        # Проверка на тип Product
        if not isinstance(product, Product):
            error_msg = f"В категорию можно добавлять только продукты. Получен объект типа: {type(product).__name__}"
            logger.error(error_msg)
            raise TypeError(error_msg)

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
        logger.debug(
            f"Создан итератор для категории '{self.name}'." f"Количество продуктов для итерации: {len(self._products)}"
        )

        return CategoryIterator(self)

    def __str__(self) -> str:
        """
        Строковое представление категории.

        Returns:
            str: Строка с информацией о категории в формате
            "Название категории, количество товаров: X шт."
        """
        total_quantity = sum(product.quantity for product in self._products)
        result = f"{self.name}, количество товаров: {total_quantity} шт."

        logger.debug(
            f"Сформирована строка представления категории '{self.name}'." f"Общее количество товаров: {total_quantity}"
        )

        return result

    # Свойства
    @property
    def products(self) -> List[Product]:
        """
        Геттер для получения копии списка продуктов.

        Returns:
            List[Product]: Копия списка продуктов.
        """
        logger.debug(
            f"Получен список продуктов для категории '{self.name}'. Количество продуктов: {len(self._products)}"
        )
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
            logger.debug(f"Категория '{self.name}' не содержит продуктов")
            return "В категории нет товаров"

        product_descriptions = [
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт." for product in self._products
        ]
        logger.debug(
            f"Сформирован список продуктов для категории '{self.name}'. Количество продуктов: {len(self._products)}"
        )

        return "\n".join(product_descriptions)

    # Классовые методы
    @classmethod
    def get_total_product_count(cls) -> int:
        """
        Класс-метод для получения общего количества продуктов во всех категориях.

        Returns:
            int: Общее количество продуктов.
        """
        logger.debug(f"Получен общий счетчик продуктов: {cls._product_count}")
        return cls._product_count


class Smartphone(Product):
    """
    Класс, представляющий смартфон.

    #наследование
    #создание_класса
    #__init__
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        """
        Инициализирует смартфон с дополнительными характеристиками.

        Args:
            name (str): Название смартфона.
            description (str): Описание смартфона.
            price (float): Цена смартфона.
            quantity (int): Количество смартфонов.
            efficiency (float): Производительность смартфона.
            model (str): Модель смартфона.
            memory (int): Объем встроенной памяти.
            color (str): Цвет смартфона.
        """
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other: Product) -> float:
        """
        Метод сложения двух смартфонов с учетом их производительности.

        Args:
            other (Product): Второй продукт для сложения.

        Returns:
            float: Общая стоимость товаров на складе с учетом производительности.

        Raises:
            TypeError: Если аргумент не является точно таким же типом.
        """
        if not (isinstance(other, Smartphone) and type(other) is type(self)):
            error_msg = f"Нельзя складывать товары разных типов: '{type(self).__name__}' и '{type(other).__name__}'"
            logger.error(error_msg)
            raise TypeError(error_msg)

        total_value = self.price * self.quantity * self.efficiency + other.price * other.quantity * other.efficiency
        logger.info(
            f"Выполнено сложение смартфонов: {self.name} и {other.name}. "
            f"Общая стоимость с учетом производительности: {total_value}"
        )

        return total_value


class LawnGrass(Product):
    """
    Класс, представляющий газонную траву.
    #наследование
    #создание_класса
    #__init__
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        """
        Инициализирует газонную траву с дополнительными характеристиками.
        Args:
            name (str): Название травы.
            description (str): Описание травы.
            price (float): Цена травы.
            quantity (int): Количество травы.
            country (str): Страна-производитель.
            germination_period (str): Срок прорастания.
            color (str): Цвет травы.
        """
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __add__(self, other: Product) -> float:
        """
        Метод сложения двух видов газонной травы.

        Args:
            other (Product): Второй продукт для сложения.

        Returns:
            float: Общая стоимость товаров на складе.

        Raises:
            TypeError: Если аргумент не является точно таким же типом.
        """
        if not (isinstance(other, LawnGrass) and type(other) is type(self)):
            error_msg = f"Нельзя складывать товары разных типов: '{type(self).__name__}' и '{type(other).__name__}'"
            logger.error(error_msg)
            raise TypeError(error_msg)

        total_value = self.price * self.quantity + other.price * other.quantity
        logger.info(
            f"Выполнено сложение газонной травы: {self.name} и {other.name}. " f"Общая стоимость: {total_value}"
        )

        return total_value
