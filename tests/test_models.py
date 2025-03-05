from typing import Any, Dict
from unittest.mock import patch

import pytest

from src.models import (
    BaseContainer,
    BaseProduct,
    Category,
    CategoryIterator,
    LawnGrass,
    Order,
    PrintInfoMixin,
    Product,
    Smartphone, ProductZeroQuantityError,
)


def test_product_price_setter_with_same_price() -> None:
    """Тест установки той же самой цены."""
    product = Product("Тестовый продукт", "Описание", 100.0, 10)

    with (
        patch("builtins.input", return_value="n"),
        patch("builtins.print"),
        patch("src.models.logger.info") as mock_logger_info,
    ):
        # Не вызывает логирование при установке той же цены
        product.price = 100.0

        # Проверяем, что не было логирования об обновлении цены
        mock_logger_info.assert_not_called()
        assert product.price == 100.0


def test_product_add_method_with_none_product() -> None:
    """Тест сложения с None."""
    product = Product("Смартфон", "Описание", 1000.0, 5)

    with pytest.raises(TypeError, match="Операция сложения невозможна с None"):
        product + None  # type: ignore


def test_category_duplicate_product_list_property() -> None:
    """Проверка, что второй декоратор product_list не влияет на работу первого."""
    category = Category("Электроника", "Описание")
    product1 = Product("Смартфон", "Описание", 1000.0, 5)
    product2 = Product("Планшет", "Описание", 500.0, 3)

    category.add_product(product1)
    category.add_product(product2)

    # Используем первый декоратор product_list
    first_list = category.product_list

    expected_list = "Смартфон, 1000.0 руб. Остаток: 5 шт.\nПланшет, 500.0 руб. Остаток: 3 шт."
    assert first_list == expected_list


def test_price_setter_with_zero_price() -> None:
    """Тест установки нулевой цены."""
    product = Product("Тестовый продукт", "Описание", 100.0, 10)

    with (
        patch("builtins.input", return_value="n"),
        patch("builtins.print"),
        patch("src.models.logger.error") as mock_logger_error,
    ):
        product.price = 0.0

        mock_logger_error.assert_called_once_with("Цена не должна быть нулевая или отрицательная")
        assert product.price == 100.0


def test_price_setter_with_negative_price() -> None:
    """Тест установки отрицательной цены."""
    product = Product("Тестовый продукт", "Описание", 100.0, 10)

    with (
        patch("builtins.input", return_value="n"),
        patch("builtins.print"),
        patch("src.models.logger.error") as mock_logger_error,
    ):
        product.price = -50.0

        mock_logger_error.assert_called_once_with("Цена не должна быть нулевая или отрицательная")
        assert product.price == 100.0


def test_price_setter_with_lower_price_cancellation() -> None:
    """Тест отмены понижения цены пользователем."""
    product = Product("Тестовый продукт", "Описание", 100.0, 10)

    with (
        patch("builtins.input", return_value="n"),  # Пользователь отказывается от понижения
        patch("builtins.print") as mock_print,
        patch("src.models.logger.info") as mock_logger_info,
    ):
        product.price = 50.0  # Попытка понизить цену

        # Проверяем, что цена не изменилась
        assert product.price == 100.0

        # Проверяем вызов print с сообщением об отмене
        mock_print.assert_called_once_with("Понижение цены отменено.")

        # Проверяем логирование отмены с текущей ценой
        mock_logger_info.assert_called_once_with("Понижение цены отменено. Текущая цена: 100.0")


def test_create_product_with_none_list() -> None:
    """Тест создания продукта со списком None."""
    product_dict = {"name": "Планшет", "description": "Новый планшет", "price": 500.0, "quantity": 10}

    result = Product.create_product(product_dict, None)

    assert result.name == "Планшет"
    assert result.description == "Новый планшет"
    assert result.price == 500.0
    assert result.quantity == 10


def test_create_product_with_existing_product() -> None:
    """Тест обновления существующего продукта."""
    existing_products = [Product("Смартфон", "Описание", 1000.0, 5)]
    new_product_dict = {"name": "Смартфон", "description": "Новое описание", "price": 1200.0, "quantity": 3}

    result = Product.create_product(new_product_dict, existing_products)

    assert result.name == "Смартфон"
    assert result.price == 1200.0
    assert result.quantity == 8


def test_category_str_method_with_no_products() -> None:
    """Проверка строкового представления категории без продуктов."""
    category = Category("Пустая категория", "Описание")

    assert str(category) == "Пустая категория, количество товаров: 0 шт."


def test_category_product_count_with_no_products() -> None:
    """Проверка подсчета количества продуктов в пустой категории."""
    category = Category("Пустая категория", "Описание")

    assert category.product_count == 0


def test_category_product_list_with_no_products() -> None:
    """Проверка списка продуктов в пустой категории."""
    category = Category("Пустая категория", "Описание")

    assert category.product_list == "В категории нет товаров"


def test_product_str_method() -> None:
    """Тест строкового представления продукта."""
    product = Product("Тестовый продукт", "Описание", 100.0, 10)
    assert str(product) == "Тестовый продукт, 100.0 руб. Остаток: 10 шт."


def test_product_repr_method() -> None:
    """Тест представления продукта для отладки."""
    product = Product("Тестовый продукт", "Описание", 100.0, 10)
    assert repr(product) == "Тестовый продукт, 100.0 руб. Остаток: 10 шт."


def test_product_add_method_total_value() -> None:
    """Тест метода сложения продуктов для расчета общей стоимости."""
    product1 = Product("Продукт 1", "Описание", 50.0, 5)
    product2 = Product("Продукт 2", "Описание", 100.0, 3)
    assert product1 + product2 == 550.0  # 50 * 5 + 100 * 3


def test_create_product_with_zero_quantity():
    """Тест создания продукта с нулевым количеством."""
    product = Product("Продукт", "Описание", 100.0, 0, allow_zero=True)

    assert product.name == "Продукт"
    assert product.quantity == 0


def test_category_iterator_empty_no_exception() -> None:
    """Тест, что итерация по пустой категории не вызывает исключений."""
    category = Category("Пустая категория", "Описание")
    iterator = iter(category)

    with pytest.raises(StopIteration):
        next(iterator)


def test_add_method_type_error_message() -> None:
    """Проверка сообщения об ошибке при некорректном типе в операции сложения."""
    product = Product("Смартфон", "Описание", 1000.0, 5)

    with pytest.raises(TypeError) as excinfo:
        product + "Некорректный тип"  # type: ignore

    assert "Нельзя складывать товары разных типов" in str(excinfo.value)


def test_category_iterator_multiple_iterations() -> None:
    """Проверка, что итератор корректно работает при многократных итерациях."""
    category = Category("Электроника", "Описание")
    product1 = Product("Смартфон", "Описание", 1000.0, 5)
    product2 = Product("Планшет", "Описание", 500.0, 3)

    category.add_product(product1)
    category.add_product(product2)

    # Первая итерация
    first_iteration = list(category)
    assert len(first_iteration) == 2

    # Вторая итерация
    second_iteration = list(category)
    assert len(second_iteration) == 2

    # Проверяем, что результаты идентичны
    assert first_iteration == second_iteration
    assert first_iteration[0] == product1
    assert first_iteration[1] == product2


def test_get_total_product_count_multiple_categories() -> None:
    """Проверка подсчета общего количества продуктов в нескольких категориях."""
    Category._product_count = 0

    category1 = Category("Электроника", "Описание")
    category2 = Category("Одежда", "Описание")

    product1 = Product("Смартфон", "Описание", 1000.0, 5)
    product2 = Product("Планшет", "Описание", 500.0, 3)
    product3 = Product("Футболка", "Описание", 200.0, 10)

    category1.add_product(product1)
    category1.add_product(product2)
    category2.add_product(product3)

    assert Category.get_total_product_count() == 3


def test_product_initialization(product: Product) -> None:
    assert isinstance(product.name, str)
    assert isinstance(product.description, str)
    assert isinstance(product.price, float)
    assert isinstance(product.quantity, int)
    assert product.name == "Тестовый продукт"
    assert product.description == "Это тестовый продукт."
    assert product.price == 9.99
    assert product.quantity == 100


def test_category_initialization_logging() -> None:
    """Тест логирования при инициализации категории с продуктами."""
    with patch("src.models.logger.debug") as mock_logger_debug:
        products = [Product("Смартфон", "Описание", 1000.0, 5), Product("Планшет", "Описание", 500.0, 3)]
        Category("Электроника", "Описание", products)

        # Проверяем вызовы debug с количеством продуктов и их именами
        assert mock_logger_debug.call_count == 3
        mock_logger_debug.assert_any_call(f"Попытка добавить {len(products)} продуктов в категорию Электроника")
        mock_logger_debug.assert_any_call(f"Добавляю продукт: {products[0].name}")
        mock_logger_debug.assert_any_call(f"Добавляю продукт: {products[1].name}")


def test_category_initialization_with_empty_products_list() -> None:
    """Тест инициализации категории с пустым списком продуктов."""
    with patch("src.models.logger.debug") as mock_logger_debug:
        Category("Электроника", "Описание", [])

        # Проверяем, что debug не вызывался
        mock_logger_debug.assert_not_called()


def test_category_initialization_with_none_products() -> None:
    """Тест инициализации категории без продуктов."""
    with patch("src.models.logger.debug") as mock_logger_debug:
        Category("Электроника", "Описание")

        # Проверяем, что debug не вызывался
        mock_logger_debug.assert_not_called()


def test_add_product_success() -> None:
    Category._product_count = 0
    category = Category("Электроника", "Описание")
    product = Product("Смартфон", "Описание", 1000.0, 5)
    category.add_product(product)

    assert len(category.products) == 1
    assert category.products[0] == product
    assert Category.get_total_product_count() == 1


def test_add_product_multiple() -> None:
    Category._product_count = 0
    category = Category("Электроника", "Описание")
    product1 = Product("Смартфон", "Описание", 1000.0, 5)
    product2 = Product("Планшет", "Описание", 500.0, 3)

    category.add_product(product1)
    category.add_product(product2)

    assert len(category.products) == 2
    assert Category.get_total_product_count() == 2


def test_add_product_with_string(caplog: Any) -> None:
    """
    Тест добавления строки вместо продукта в категорию.
    """
    category = Category("Электроника", "Описание")

    # Пытаемся добавить строку
    category.add_product("Некорректный продукт")

    # Проверяем, что было выведено предупреждение
    assert "Попытка добавить строку вместо продукта" in caplog.text

    # Проверяем, что количество продуктов в категории не изменилось
    assert len(category.products) == 0


def test_product_new_method_full_data() -> None:
    """Тест создания продукта с полными данными."""
    product_dict = {"name": "Смартфон", "description": "Новый смартфон", "price": 50000.0, "quantity": 10}

    product = Product.new_product(product_dict)

    assert product.name == "Смартфон"
    assert product.description == "Новый смартфон"
    assert product.price == 50000.0
    assert product.quantity == 10


def test_product_new_method_partial_data() -> None:
    """Тест создания продукта с частичными данными."""
    product_dict = {"name": "Планшет", "price": 30000.0}

    product = Product.new_product(product_dict)

    assert product.name == "Планшет"
    assert product.description == ""
    assert product.price == 30000.0
    assert product.quantity == 0


def test_product_new_method_empty_data() -> None:
    """Тест создания продукта с пустым словарем."""
    product_dict: Dict[str, Any] = {}

    product = Product.new_product(product_dict)

    assert product.name == ""
    assert product.description == ""
    assert product.price == 0.0
    assert product.quantity == 0


def test_product_new_method_invalid_types() -> None:
    """Тест создания продукта с некорректными типами данных."""
    product_dict = {"name": 123, "description": 456, "price": "expensive", "quantity": "много"}

    product = Product.new_product(product_dict)

    # Проверяем, что некорректные входные данные преобразованы в корректные значения по умолчанию
    assert str(product.name) == "123"  # Преобразование числа в строку
    assert str(product.description) == "456"  # Преобразование числа в строку
    assert product.price == 0.0  # Некорректная цена заменена на 0.0
    assert product.quantity == 0  # Некорректное количество заменено на 0

    # Дополнительно проверяем, что продукт создан с allow_zero=True
    try:
        # Попытка создания продукта с нулевым количеством не должна вызывать исключение
        Product("Тестовый продукт", "Описание", 100.0, 0, allow_zero=True)
    except ValueError:
        pytest.fail("Создание продукта с нулевым количеством должно быть разрешено")


def test_product_new_method_with_mixed_none_and_valid_values() -> None:
    """Тест создания продукта со смешанными значениями None и валидными."""
    product_dict = {"name": None, "description": "Описание", "price": 100.0, "quantity": None}

    product = Product.new_product(product_dict)

    assert product.name == ""
    assert product.description == "Описание"
    assert product.price == 100.0
    assert product.quantity == 0


def test_product_new_method_with_partial_none_values() -> None:
    """Тест создания продукта с частично None значениями."""
    product_dict = {"name": "Продукт", "description": None, "price": None, "quantity": 5}

    product = Product.new_product(product_dict)

    assert product.name == "Продукт"
    assert product.description == ""
    assert product.price == 0.0
    assert product.quantity == 5


def test_category_iterator_empty_iteration() -> None:
    """Тест итерации по пустой категории."""
    category = Category("Пустая категория", "Описание")

    # Проверяем, что итерация по пустой категории не вызывает ошибок
    iteration_count = 0
    for _ in category:
        iteration_count += 1

    assert iteration_count == 0


def test_add_method_with_zero_quantity_products() -> None:
    """Проверка метода сложения продуктов с нулевым количеством."""
    product1 = Product("Продукт 1", "Описание", 50.0, 0, allow_zero=True)
    product2 = Product("Продукт 2", "Описание", 100.0, 0, allow_zero=True)

    total_value = product1 + product2

    assert total_value == 0.0



def test_category_product_list_edge_cases() -> None:
    """Проверка краевых случаев списка продуктов."""
    # Продукты с одинаковыми характеристиками
    category = Category("Электроника", "Описание")
    product1 = Product("Смартфон", "Описание", 1000.0, 5)
    product2 = Product("Смартфон", "Описание", 1000.0, 3)
    category.add_product(product1)
    category.add_product(product2)

    expected_list = "Смартфон, 1000.0 руб. Остаток: 5 шт.\nСмартфон, 1000.0 руб. Остаток: 3 шт."
    assert category.product_list == expected_list

    # Продукты с разными ценами
    different_price_category = Category("Электроника", "Описание")
    product3 = Product("Смартфон", "Описание", 1000.0, 5)
    product4 = Product("Смартфон", "Описание", 1500.0, 3)
    different_price_category.add_product(product3)
    different_price_category.add_product(product4)

    expected_different_prices = "Смартфон, 1000.0 руб. Остаток: 5 шт.\nСмартфон, 1500.0 руб. Остаток: 3 шт."
    assert different_price_category.product_list == expected_different_prices


def test_smartphone_initialization() -> None:
    """Тест инициализации смартфона с полными данными."""
    smartphone = Smartphone(
        name="iPhone 13",
        description="Новый смартфон",
        price=1000.0,
        quantity=5,
        efficiency=0.9,
        model="Pro Max",
        memory=256,
        color="Silver",
    )

    assert smartphone.name == "iPhone 13"
    assert smartphone.description == "Новый смартфон"
    assert smartphone.price == 1000.0
    assert smartphone.quantity == 5
    assert smartphone.efficiency == 0.9
    assert smartphone.model == "Pro Max"
    assert smartphone.memory == 256
    assert smartphone.color == "Silver"


def test_smartphone_add_method() -> None:
    """Тест метода сложения для смартфонов."""
    smartphone1 = Smartphone(
        name="iPhone 13",
        description="Смартфон 1",
        price=1000.0,
        quantity=5,
        efficiency=0.9,
        model="Pro Max",
        memory=256,
        color="Silver",
    )
    smartphone2 = Smartphone(
        name="Samsung Galaxy",
        description="Смартфон 2",
        price=800.0,
        quantity=3,
        efficiency=0.8,
        model="S21",
        memory=128,
        color="Black",
    )

    total_value = smartphone1 + smartphone2
    expected_value = 1000.0 * 5 * 0.9 + 800.0 * 3 * 0.8
    assert total_value == expected_value


def test_smartphone_str_method() -> None:
    """Тест строкового представления смартфона."""
    smartphone = Smartphone(
        name="iPhone 13",
        description="Новый смартфон",
        price=1000.0,
        quantity=5,
        efficiency=0.9,
        model="Pro Max",
        memory=256,
        color="Silver",
    )

    assert str(smartphone) == "iPhone 13, 1000.0 руб. Остаток: 5 шт."


def test_smartphone_repr_method() -> None:
    """Тест представления смартфона для отладки."""
    smartphone = Smartphone(
        name="iPhone 13",
        description="Новый смартфон",
        price=1000.0,
        quantity=5,
        efficiency=0.9,
        model="Pro Max",
        memory=256,
        color="Silver",
    )

    assert repr(smartphone) == "iPhone 13, 1000.0 руб. Остаток: 5 шт."


def test_lawn_grass_initialization() -> None:
    """Тест инициализации газонной травы с полными данными."""
    lawn_grass = LawnGrass(
        name="Газонная трава 'Западлютик'",
        description="Ароматная трава",
        price=500.0,
        quantity=10,
        country="Россия",
        germination_period="7-10 дней",
        color="Зеленый",
    )

    assert lawn_grass.name == "Газонная трава 'Западлютик'"
    assert lawn_grass.description == "Ароматная трава"
    assert lawn_grass.price == 500.0
    assert lawn_grass.quantity == 10
    assert lawn_grass.country == "Россия"
    assert lawn_grass.germination_period == "7-10 дней"
    assert lawn_grass.color == "Зеленый"


def test_lawn_grass_add_method() -> None:
    """Тест метода сложения для газонной травы."""
    lawn_grass1 = LawnGrass(
        name="Газонная трава 'Батька'",
        description="Быстрорастущая трава 1",
        price=500.0,
        quantity=10,
        country="Беларусь",
        germination_period="7-10 дней",
        color="Зеленый",
    )
    lawn_grass2 = LawnGrass(
        name="Газонная трава Премиум",
        description="Быстрорастущая трава 2",
        price=600.0,
        quantity=5,
        country="Беларусь",
        germination_period="5-7 дней",
        color="Темно-зеленый",
    )

    total_value = lawn_grass1 + lawn_grass2
    expected_value = 500.0 * 10 + 600.0 * 5
    assert total_value == expected_value


def test_lawn_grass_str_method() -> None:
    """Тест строкового представления газонной травы."""
    lawn_grass = LawnGrass(
        name="Газонная трава для России",
        description="Быстрорастущая трава",
        price=500.0,
        quantity=10,
        country="Россия",
        germination_period="5-10 дней",
        color="Зеленый",
    )

    assert str(lawn_grass) == "Газонная трава для России, 500.0 руб. Остаток: 10 шт."


def test_lawn_grass_repr_method() -> None:
    """Тест представления газонной травы для отладки."""
    lawn_grass = LawnGrass(
        name="Газонная трава для России",
        description="Быстрорастущая трава",
        price=500.0,
        quantity=10,
        country="Россия",
        germination_period="7-10 дней",
        color="Зеленый",
    )

    assert repr(lawn_grass) == "Газонная трава для России, 500.0 руб. Остаток: 10 шт."


def test_lawn_grass_add_method_different_types() -> None:
    """Тест сложения газонной травы разных типов."""

    class CustomLawnGrass(LawnGrass):
        pass

    lawn_grass1 = LawnGrass(
        name="Газонная трава Элита",
        description="Быстрорастущая трава 1",
        price=500.0,
        quantity=10,
        country="Россия",
        germination_period="7-10 дней",
        color="Зеленый",
    )
    custom_lawn_grass = CustomLawnGrass(
        name="Рандомная трава",
        description="Рандомная трава",
        price=400.0,
        quantity=7,
        country="Россия",
        germination_period="10-14 дней",
        color="Салатовый",
    )

    with pytest.raises(TypeError, match="Нельзя складывать товары разных типов"):
        lawn_grass1 + custom_lawn_grass


def test_smartphone_add_method_different_types() -> None:
    """Тест сложения смартфонов разных типов."""

    class CustomSmartphone(Smartphone):
        pass

    smartphone1 = Smartphone(
        name="iPhone 13",
        description="Смартфон 1",
        price=1000.0,
        quantity=5,
        efficiency=0.9,
        model="Pro Max",
        memory=256,
        color="Silver",
    )
    custom_smartphone = CustomSmartphone(
        name="Custom Phone",
        description="Кастомный смартфон",
        price=800.0,
        quantity=3,
        efficiency=0.8,
        model="Custom",
        memory=128,
        color="Black",
    )

    with pytest.raises(TypeError, match="Нельзя складывать товары разных типов"):
        smartphone1 + custom_smartphone


def test_add_method_different_product_types() -> None:
    """Тест сложения продуктов разных классов."""
    smartphone = Smartphone(
        name="iPhone 13",
        description="Смартфон",
        price=1000.0,
        quantity=5,
        efficiency=0.9,
        model="Pro Max",
        memory=256,
        color="Silver",
    )
    lawn_grass = LawnGrass(
        name="Газонная трава Элита",
        description="Быстрорастущий бурьян для соседей",
        price=500.0,
        quantity=10,
        country="Россия",
        germination_period="7-10 дней",
        color="голубой",
    )

    with pytest.raises(TypeError, match="Нельзя складывать товары разных типов"):
        smartphone + lawn_grass


def test_add_method_error_message_content() -> None:
    """Проверка точного содержания сообщения об ошибке."""
    smartphone1 = Smartphone(
        name="iPhone 13",
        description="Смартфон 1",
        price=1000.0,
        quantity=5,
        efficiency=0.9,
        model="Pro Max",
        memory=256,
        color="Silver",
    )
    lawn_grass = LawnGrass(
        name="Газонная трава Скороспелка",
        description="Быстрорастущая трава",
        price=500.0,
        quantity=10,
        country="Белорусь",
        germination_period="7-10 дней",
        color="Зеленый",
    )

    with pytest.raises(TypeError) as excinfo:
        smartphone1 + lawn_grass

    assert str(excinfo.value) == "Нельзя складывать товары разных типов: 'Smartphone' и 'LawnGrass'"


def test_add_method_logging() -> None:
    """Проверка логирования при попытке сложения разных типов."""
    smartphone1 = Smartphone(
        name="iPhone 13",
        description="Смартфон 1",
        price=1000.0,
        quantity=5,
        efficiency=0.9,
        model="Pro Max",
        memory=256,
        color="Silver",
    )
    lawn_grass = LawnGrass(
        name="Газонная трава 'Финн'",
        description=" медленнорастущая трава",
        price=500.0,
        quantity=10,
        country="Россия",
        germination_period="7-10 дней",
        color="Зеленый",
    )

    with patch("src.models.logger.error") as mock_logger_error:
        with pytest.raises(TypeError):
            smartphone1 + lawn_grass

        mock_logger_error.assert_called_once_with(
            f"Нельзя складывать товары разных типов: '{type(smartphone1).__name__}' и '{type(lawn_grass).__name__}'"
        )


def test_add_product_with_none(caplog: Any) -> None:
    """
    Тест добавления None в категорию.
    """
    category = Category("Электроника", "Описание")

    with pytest.raises(ValueError) as excinfo:
        category.add_product(None)

    # Проверяем текст исключения
    assert f"Ошибка при добавлении продукта в категорию '{category.name}'" in str(excinfo.value)

    # Проверяем, что была залоггирована ошибка
    assert "Ошибка при добавлении продукта" in caplog.text

    # Проверяем, что количество продуктов в категории не изменилось
    assert len(category.products) == 0


def test_category_iterator_iter_method() -> None:
    """
    Тест метода __iter__ в CategoryIterator.
    Проверяет, что метод возвращает сам объект итератора.
    """
    category = Category("Электроника", "Описание")
    product1 = Product("Смартфон", "Описание", 1000.0, 5)
    product2 = Product("Планшет", "Описание", 500.0, 3)

    category.add_product(product1)
    category.add_product(product2)

    iterator = CategoryIterator(category)

    # Проверяем, что __iter__ возвращает сам объект итератора
    assert iterator.__iter__() is iterator


def test_print_info_mixin_repr_method() -> None:
    """
    Тест метода __repr__ в PrintInfoMixin.
    Проверяет корректность формирования строки repr.
    """

    class TestProduct(PrintInfoMixin, Product):
        def __init__(self, name: str, description: str, price: float, quantity: int):
            super().__init__(name, description, price, quantity)

    product = TestProduct("Тестовый продукт", "Описание", 100.0, 10)

    # Проверяем, что repr содержит имя класса и стандартное строковое представление
    assert "Объект класса TestProduct" in repr(product)
    assert "Тестовый продукт, 100.0 руб. Остаток: 10 шт." in repr(product)


def test_base_product_price_property_implementation() -> None:
    """
    Тест корректной реализации свойства price в конкретном классе.
    """
    product = Product("Тестовый продукт", "Описание", 100.0, 10)

    # Проверяем, что свойство price работает корректно
    assert product.price == 100.0

    # Проверяем логирование при получении цены
    with patch("src.models.logger.debug") as mock_logger_debug:
        _ = product.price
        mock_logger_debug.assert_called_once_with("Получение цены для продукта 'Тестовый продукт'. "
                                                  "Текущая цена: 100.0")


def test_base_product_add_method_implementation() -> None:
    """
    Тест корректной реализации метода __add__ в конкретном классе.
    """
    product1 = Product("Продукт 1", "Описание", 50.0, 5)
    product2 = Product("Продукт 2", "Описание", 100.0, 3)

    # Проверяем, что метод __add__ работает корректно
    total_value = product1 + product2
    assert total_value == 550.0  # 50 * 5 + 100 * 3

    # Проверяем логирование при сложении
    with patch("src.models.logger.info") as mock_logger_info:
        product1 + product2
        mock_logger_info.assert_called_once_with(
            f"Выполнено сложение товаров: {product1.name} и {product2.name}. Общая стоимость: 550.0"
        )


def test_base_product_add_method_signature() -> None:
    """
    Тест сигнатуры метода __add__.
    Проверяет корректность типов аргументов и возвращаемого значения.
    """
    from typing import get_type_hints

    type_hints = get_type_hints(BaseProduct.__add__)

    assert type_hints["other"] == BaseProduct
    assert type_hints["return"] == float


def test_base_product_add_method_documentation() -> None:
    """
    Тест документации абстрактного метода __add__.
    Проверяет наличие и не пустые строки документации.
    """
    assert BaseProduct.__add__.__doc__ is not None
    assert len(BaseProduct.__add__.__doc__.strip()) > 0


def test_base_product_str_method_comprehensive() -> None:
    """
    Общий тест для абстрактного метода __str__ в BaseProduct.
    Проверяет невозможность создания экземпляра, требование реализации метода в наследниках
    и корректность его работы.
    """
    # Проверка невозможности создания экземпляра абстрактного класса
    with pytest.raises(TypeError) as excinfo:
        # Создаем анонимный подкласс без реализации абстрактных методов
        type(
            "FailedProduct",
            (BaseProduct,),
            {
                "__init__": lambda self, name, description, price, quantity: None,
                "price": property(lambda self: 0.0),
                "__add__": lambda self, other: 0.0,
            },
        )()

    # Проверяем, что сообщение об ошибке содержит нужную информацию
    assert "Can't instantiate abstract class" in str(excinfo.value)
    assert "__str__" in str(excinfo.value)

    # Проверка требования реализации метода в наследниках
    class IncompleteProduct(BaseProduct):
        def __init__(self, name: str, description: str, price: float, quantity: int):
            self.name = name
            self.description = description
            self._price = price
            self.quantity = quantity

        @property
        def price(self) -> float:
            return self._price

        def __add__(self, other: "BaseProduct") -> float:
            raise NotImplementedError("Метод __add__ не реализован")

        def __str__(self) -> str:
            return f"{self.name}, {self.price} руб."

    # Теперь создание экземпляра должно быть возможным, так как __str__ реализован
    product = IncompleteProduct("Тестовый продукт", "Описание", 100.0, 10)
    assert str(product) == "Тестовый продукт, 100.0 руб."

    # Проверка корректности работы __str__ в наследнике
    class TestProduct(BaseProduct):
        def __init__(self, name: str, description: str, price: float, quantity: int):
            self.name = name
            self.description = description
            self._price = price
            self.quantity = quantity

        @property
        def price(self) -> float:
            return self._price

        def __add__(self, other: "BaseProduct") -> float:
            raise NotImplementedError("Метод __add__ не реализован")

        def __str__(self) -> str:
            return f"{self.name}, {self.price} руб."

    test_product = TestProduct("Тестовый продукт", "Описание", 100.0, 10)
    assert isinstance(str(test_product), str)
    assert str(test_product) == "Тестовый продукт, 100.0 руб."

    # Проверка атрибутов абстрактного метода
    assert hasattr(BaseProduct, "__str__"), "BaseProduct должен иметь метод __str__"
    assert callable(getattr(BaseProduct, "__str__", None)), "__str__ должен быть методом"
    assert hasattr(BaseProduct.__str__, "__isabstractmethod__"), "__str__ должен быть абстрактным методом"


def test_base_product_str_method_documentation() -> None:
    """
    Тест документации абстрактного метода __str__.
    """
    assert BaseProduct.__str__.__doc__ is not None
    assert len(BaseProduct.__str__.__doc__.strip()) > 20
    assert "Returns" in BaseProduct.__str__.__doc__
    assert "str:" in BaseProduct.__str__.__doc__


def test_base_product_str_method_type_hints() -> None:
    """
    Тест сигнатуры и типов возвращаемого значения метода __str__.
    """
    from typing import get_type_hints

    type_hints = get_type_hints(BaseProduct.__str__)
    assert type_hints["return"] == str


def test_base_product_incomplete_class_methods() -> None:
    """
    Тест методов неполного класса продукта.
    """

    class IncompleteProduct(BaseProduct):
        def __init__(self, name: str, description: str, price: float, quantity: int):
            self.name = name
            self.description = description
            self._price = price
            self.quantity = quantity

        @property
        def price(self) -> float:
            return self._price

        def __add__(self, other: "BaseProduct") -> float:
            # Просто заглушка для теста
            return 0.0

        def __str__(self) -> str:
            return f"{self.name}, {self.price} руб."

    # Проверяем, что методы вызываются без ошибок
    product = IncompleteProduct("Тестовый продукт", "Описание", 100.0, 10)

    assert product.price == 100.0
    assert str(product) == "Тестовый продукт, 100.0 руб."
    assert product.__add__(product) == 0.0


def test_container_str_methods() -> None:
    """
    Тест методов __str__ в тестовых классах контейнеров.
    """

    class TestContainer1(BaseContainer):
        def __str__(self) -> str:
            return "Test Container 1"

    class TestContainer2(BaseContainer):
        def __str__(self) -> str:
            return "Test Container 2"

    container1 = TestContainer1("Контейнер 1", "Описание 1")
    container2 = TestContainer2("Контейнер 2", "Описание 2")

    assert str(container1) == "Test Container 1"
    assert str(container2) == "Test Container 2"

    # Тест успешной инициализации заказа.

    product = Product("Тестовый продукт", "Описание", 100.0, 10)
    order = Order("Тестовый заказ", "Описание заказа", product, 5)

    assert order.name == "Тестовый заказ"
    assert order.description == "Описание заказа"
    assert order.product == product
    assert order.quantity == 5
    assert product.quantity == 5  # Количество товара уменьшилось


def test_order_initialization_with_zero_quantity() -> None:
    """
    Тест инициализации заказа с нулевым количеством.
    """
    product = Product("Тестовый продукт", "Описание", 100.0, 10)

    with pytest.raises(ValueError, match="Количество товара должно быть положительным"):
        Order("Тестовый заказ", "Описание заказа", product, 0)


def test_order_initialization_with_negative_quantity() -> None:
    """
    Тест инициализации заказа с отрицательным количеством.
    """
    product = Product("Тестовый продукт", "Описание", 100.0, 10)

    with pytest.raises(ValueError, match="Количество товара должно быть положительным"):
        Order("Тестовый заказ", "Описание заказа", product, -5)


def test_order_initialization_with_insufficient_product_quantity() -> None:
    """
    Тест инициализации заказа с количеством, превышающим доступное количество товара.
    """
    product = Product("Тестовый продукт", "Описание", 100.0, 5)

    with pytest.raises(ValueError, match=r"Недостаточно товара на складе\. Запрошено: 10, доступно: 5"):
        Order("Тестовый заказ", "Описание заказа", product, 10)


def test_order_initialization_logging() -> None:
    """
    Тест логирования при создании заказа.
    """
    product = Product("Тестовый продукт", "Описание", 100.0, 10)

    with patch("src.models.logger.info") as mock_logger_info:
        Order("Тестовый заказ", "Описание заказа", product, 5)

        mock_logger_info.assert_called_once_with(f"Создан заказ: Тестовый заказ, товар: {product.name}, количество: 5")


def test_order_initialization_multiple_orders() -> None:
    """
    Тест создания нескольких заказов с одним и тем же продуктом.
    """
    product = Product("Тестовый продукт", "Описание", 100.0, 20)

    order1 = Order("Заказ 1", "Описание заказа 1", product, 5)
    order2 = Order("Заказ 2", "Описание заказа 2", product, 7)

    assert order1.quantity == 5
    assert order2.quantity == 7
    assert product.quantity == 8  # 20 - 5 - 7


# Тесты для покрытия ProductZeroQuantityError
def test_product_zero_quantity_error_validate_method_additional_cases():
    """
    Расширенный тест статического метода validate с дополнительными сценариями.
    """
    # Тест на успешную валидацию с различными положительными значениями
    test_cases = [1, 10, 100, 1000]
    for quantity in test_cases:
        assert ProductZeroQuantityError.validate("Тестовый продукт", quantity) is True


def test_product_zero_quantity_error_validate_method_print_output(capsys):
    """
    Тест вывода сообщений в методе validate.
    """
    # Тест успешной валидации
    ProductZeroQuantityError.validate("Тестовый продукт", 5)
    captured = capsys.readouterr()
    assert "Товар 'Тестовый продукт' успешно прошел валидацию" in captured.out
    assert "Обработка добавления товара завершена" in captured.out


def test_product_zero_quantity_error_validate_method_exception_handling():
    """
    Тест обработки исключений в методе validate.
    """
    # Тест на корректность обработки исключений
    with pytest.raises(ValueError, match="Количество товара 'Тестовый продукт' не может быть отрицательным"):
        ProductZeroQuantityError.validate("Тестовый продукт", -1)

    with pytest.raises(ValueError, match="Товар 'Тестовый продукт' с нулевым количеством не может быть добавлен"):
        ProductZeroQuantityError.validate("Тестовый продукт", 0)


def test_product_zero_quantity_error_custom_message():
    """
    Тест создания исключения с полностью пользовательским сообщением.
    """
    custom_message = "Извините, но товар не может быть добавлен с нулевым количеством"
    error = ProductZeroQuantityError(custom_message)

    assert str(error) == custom_message
    assert error.message == custom_message


def test_product_zero_quantity_error_type_checking():
    """
    Тест проверки типов в методе validate.
    """
    # Проверка обработки некорректных типов
    with pytest.raises(TypeError, match="Название продукта должно быть строкой"):
        ProductZeroQuantityError.validate(123, 5)

    with pytest.raises(TypeError, match="Количество должно быть целым числом"):
        ProductZeroQuantityError.validate("Продукт", "не число")

    with pytest.raises(TypeError, match="Название продукта должно быть строкой"):
        ProductZeroQuantityError.validate(None, 5)


def test_product_zero_quantity_error_message_initialization():
    """
    Тест инициализации исключения с пользовательским сообщением.
    """
    # Тест с сообщением по умолчанию
    error1 = ProductZeroQuantityError()
    assert str(error1) == "Товар с нулевым количеством не может быть добавлен"
    assert error1.message == "Товар с нулевым количеством не может быть добавлен"

    # Тест с пользовательским сообщением
    custom_message = "Специальное сообщение об ошибке"
    error2 = ProductZeroQuantityError(custom_message)
    assert str(error2) == custom_message
    assert error2.message == custom_message

def test_product_zero_quantity_error_inheritance():
    """
    Тест наследования от ValueError и проверка корректности сообщения об ошибке.
    """
    # Проверяем, что класс наследуется от ValueError
    assert issubclass(ProductZeroQuantityError, ValueError)

    # Тест создания исключения и проверка, что оно работает как ValueError
    with pytest.raises(ProductZeroQuantityError) as excinfo:
        raise ProductZeroQuantityError("Тестовое сообщение")

    assert "Тестовое сообщение" in str(excinfo.value)

def test_product_zero_quantity_error_str_method():
    """
    Тест метода __str__ для исключения.
    """
    # Проверяем, что метод __str__ возвращает корректное сообщение
    error = ProductZeroQuantityError("Особое сообщение об ошибке")
    assert str(error) == "Особое сообщение об ошибке"

def test_product_zero_quantity_error_validate_method():
    """
    Тест статического метода validate.
    """
    # Тест на успешную валидацию
    assert ProductZeroQuantityError.validate("Тестовый продукт", 5) is True

    # Тест на ошибку с отрицательным количеством
    with pytest.raises(ValueError, match="Количество товара 'Тестовый продукт' не может быть отрицательным"):
        ProductZeroQuantityError.validate("Тестовый продукт", -1)

    # Тест на ошибку с нулевым количеством
    with pytest.raises(ValueError, match="Товар 'Тестовый продукт' с нулевым количеством не может быть добавлен"):
        ProductZeroQuantityError.validate("Тестовый продукт", 0)