from typing import Any, Dict
from unittest.mock import patch

import pytest

from src.models import Category, LawnGrass, Product, Smartphone


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


def test_create_product_with_empty_dict() -> None:
    """Тест создания продукта с пустым словарем."""
    result = Product.create_product({})
    assert result.name == ""
    assert result.description == ""
    assert result.price == 0.0
    assert result.quantity == 0


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


def test_add_product_error_handling(caplog: Any) -> None:
    category = Category("Электроника", "Описание")

    with pytest.raises(ValueError):
        category.add_product(None)

    assert "Ошибка при добавлении продукта" in caplog.text
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
    product1 = Product("Продукт 1", "Описание", 50.0, 0)
    product2 = Product("Продукт 2", "Описание", 100.0, 0)

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
