from typing import Any
from unittest.mock import patch

import pytest

from src.models import Category, Product


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


def test_product_new_method() -> None:
    product_dict = {"name": "Тестовый продукт", "description": "Описание", "price": 100.0, "quantity": 5}

    product = Product.new_product(product_dict)

    assert product.name == "Тестовый продукт"
    assert product.description == "Описание"
    assert product.price == 100.0
    assert product.quantity == 5


def test_product_new_method_with_missing_fields() -> None:
    product_dict: dict[str, Any] = {}

    product = Product.new_product(product_dict)

    assert product.name == ""
    assert product.description == ""
    assert product.price == 0.0
    assert product.quantity == 0


@pytest.mark.parametrize(
    "initial_price, new_price, input_response, expected_price",
    [
        (100.0, 50.0, "y", 50.0),  # Понижение цены с согласием
        (100.0, 50.0, "n", 100.0),  # Понижение цены без согласия
        (100.0, 150.0, "", 150.0),  # Повышение цены
    ],
)
def test_price_setter(initial_price: float, new_price: float, input_response: str, expected_price: float) -> None:
    product = Product("Тестовый продукт", "Описание", initial_price, 10)

    with (
        patch("builtins.input", return_value=input_response),
        patch("builtins.print"),
        patch("src.models.logger.info"),
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


def test_create_product_new() -> None:
    new_product_dict = {"name": "Планшет", "description": "Новый планшет", "price": 500.0, "quantity": 10}

    result = Product.create_product(new_product_dict)

    assert result.name == "Планшет"
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


def test_category_class_methods() -> None:
    Category._product_count = 0
    Category.category_count = 0

    category1 = Category("Электроника", "Описание")
    # category2 = Category("Одежда", "Описание")

    assert Category.category_count == 1
    assert Category.get_total_product_count() == 0

    product = Product("Смартфон", "Описание", 1000.0, 5)
    category1.add_product(product)

    assert Category.get_total_product_count() == 1


def test_category_initialization_with_products() -> None:
    product1 = Product("Смартфон", "Описание", 1000.0, 5)
    product2 = Product("Планшет", "Описание", 500.0, 3)

    category = Category("Электроника", "Описание", [product1, product2])

    assert len(category.products) == 2
    assert Category.get_total_product_count() == 2
    assert Category.category_count == 1


def test_product_create_product_case_insensitive() -> None:
    existing_products = [Product("Смартфон", "Описание", 1000.0, 5)]

    new_product_dict = {
        "name": "смартфон",  # Lowercase
        "description": "Новое описание",
        "price": 1200.0,
        "quantity": 3,
    }

    result = Product.create_product(new_product_dict, existing_products)

    assert result.name == "Смартфон"
    assert result.price == 1200.0
    assert result.quantity == 8


def test_product_count_empty_category(category: Category) -> None:
    """Проверка количества продуктов в пустой категории."""
    assert category.product_count == 0


def test_product_count_with_products(category: Category, product: Product) -> None:
    """Проверка количества продуктов в категории с добавленными продуктами."""
    category.add_product(product)
    assert category.product_count == 1
