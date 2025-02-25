from typing import Any
from unittest.mock import patch

import pytest

from src.models import Category, Product


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


def test_category_initialization(category: Category) -> None:
    assert isinstance(category.name, str)
    assert isinstance(category.description, str)
    assert isinstance(category.products, list)
    assert category.name == "Тестовая категория"
    assert category.description == "Это тестовая категория."
    assert category.products == []


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
        category.add_product(None)  # type: ignore

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
    assert product.quantity == 0  # Некорректное количество заменено на 0


@pytest.mark.parametrize(
    "initial_price, new_price, expected_price",
    [
        (100.0, 0.01, 100.0),  # Попытка установить минимальную положительную цену
        (100.0, -0.01, 100.0),  # Попытка установить отрицательную цену
    ]
)
def test_price_setter_boundary_values(
    initial_price: float,
    new_price: float,
    expected_price: float
) -> None:
    product = Product("Тестовый продукт", "Описание", initial_price, 10)

    with (
        patch("builtins.input", return_value="n"),
        patch("builtins.print"),
        patch("src.models.logger.error"),
    ):
        product.price = new_price
        assert product.price == expected_price



def test_price_setter_negative_price() -> None:
    product = Product("Тестовый продукт", "Описание", 100.0, 10)

    with patch("builtins.print"), patch("src.models.logger.error") as mock_logger_error:

        product.price = -50.0

        mock_logger_error.assert_called_once_with("Цена не должна быть нулевая или отрицательная")
        assert product.price == 100.0


def test_price_setter_zero_price() -> None:
    product = Product("Тестовый продукт", "Описание", 100.0, 10)

    with patch("builtins.print"), patch("src.models.logger.error") as mock_logger_error:

        product.price = 0.0

        mock_logger_error.assert_called_once_with("Цена не должна быть нулевая или отрицательная")
        assert product.price == 100.0


def test_create_product_duplicate() -> None:
    existing_products = [Product("Смартфон", "Описание", 1000.0, 5)]

    new_product_dict = {"name": "Смартфон", "description": "Новое описание", "price": 1200.0, "quantity": 3}

    result = Product.create_product(new_product_dict, existing_products)

    assert result.name == "Смартфон"
    assert result.price == 1200.0
    assert result.quantity == 8


def test_create_product_empty_list() -> None:
    """Тест создания продукта с пустым списком существующих продуктов."""
    new_product_dict = {"name": "Планшет", "description": "Новый планшет", "price": 500.0, "quantity": 10}

    result = Product.create_product(new_product_dict, [])

    assert result.name == "Планшет"
    assert result.description == "Новый планшет"
    assert result.price == 500.0
    assert result.quantity == 10


def test_category_product_list_empty() -> None:
    category = Category("Тестовая категория", "Описание")
    assert category.product_list == "В категории нет товаров"


def test_category_product_list_with_products() -> None:
    category = Category("Электроника", "Описание")
    product1 = Product("Смартфон", "Описание", 1000.0, 5)
    product2 = Product("Планшет", "Описание", 500.0, 3)

    category.add_product(product1)
    category.add_product(product2)

    expected_list = "Смартфон, 1000.0 руб. Остаток: 5 шт.\nПланшет, 500.0 руб. Остаток: 3 шт."
    assert category.product_list == expected_list


def test_category_str_method_empty() -> None:
    """Проверка строкового представления пустой категории."""
    category = Category("Пустая категория", "Описание")
    expected_str = "Пустая категория, количество товаров: 0 шт."
    assert str(category) == expected_str


def test_category_str_method_with_products() -> None:
    """Проверка строкового представления категории с несколькими продуктами."""
    category = Category("Электроника", "Описание")
    product1 = Product("Смартфон", "Описание", 1000.0, 5)
    product2 = Product("Планшет", "Описание", 500.0, 3)

    category.add_product(product1)
    category.add_product(product2)

    expected_str = "Электроника, количество товаров: 8 шт."
    assert str(category) == expected_str


def test_category_iterator_empty() -> None:
    """Тест итерации по пустой категории."""
    category = Category("Пустая категория", "Описание")

    # Проверяем, что итерация по пустой категории не вызывает ошибок
    for _ in category:
        pytest.fail("Итерация по пустой категории не должна содержать элементов")


def test_category_iterator_with_products() -> None:
    """Тест итерации по категории с продуктами."""
    category = Category("Электроника", "Описание")
    product1 = Product("Смартфон", "Описание", 1000.0, 5)
    product2 = Product("Планшет", "Описание", 500.0, 3)

    category.add_product(product1)
    category.add_product(product2)

    # Собираем продукты через итерацию
    iterated_products = list(category)

    # Проверяем корректность итерации
    assert len(iterated_products) == 2
    assert iterated_products[0] == product1
    assert iterated_products[1] == product2


def test_category_iterator_multiple_iterations() -> None:
    """Тест многократной итерации по категории."""
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


def test_category_iterator_with_next() -> None:
    """Тест использования next() с итератором категории."""
    category = Category("Электроника", "Описание")
    product1 = Product("Смартфон", "Описание", 1000.0, 5)
    product2 = Product("Планшет", "Описание", 500.0, 3)

    category.add_product(product1)
    category.add_product(product2)

    # Создаем итератор
    iterator = iter(category)

    # Проверяем первый элемент
    assert next(iterator) == product1

    # Проверяем второй элемент
    assert next(iterator) == product2

    # Проверяем исключение при попытке получить следующий элемент
    with pytest.raises(StopIteration):
        next(iterator)


def test_category_iterator_partial_iteration() -> None:
    """Тест частичной итерации по категории."""
    category = Category("Электроника", "Описание")
    product1 = Product("Смартфон", "Описание", 1000.0, 5)
    product2 = Product("Планшет", "Описание", 500.0, 3)

    category.add_product(product1)
    category.add_product(product2)

    iterator = iter(category)

    # Проверяем первый элемент
    assert next(iterator) == product1

    # Проверяем, что итератор не исчерпан
    assert len(list(iterator)) == 1
