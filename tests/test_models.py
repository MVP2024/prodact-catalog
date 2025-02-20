from typing import Any

import pytest

from src.prodact_catalog.models import Category, Product


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
    # Создаем категорию
    category = Category("Электроника", "Описание")

    # Создаем продукт
    product = Product("Смартфон", "Описание", 1000.0, 5)

    # Добавляем продукт
    category.add_product(product)

    # Проверяем, что продукт добавлен
    assert len(category.products) == 1
    assert category.products[0] == product
    assert Category.product_count == 1


def test_add_product_multiple() -> None:
    # Создаем категорию
    category = Category("Электроника", "Описание")

    # Создаем несколько продуктов
    product1 = Product("Смартфон", "Описание", 1000.0, 5)
    product2 = Product("Планшет", "Описание", 500.0, 3)

    # Добавляем продукты
    category.add_product(product1)
    category.add_product(product2)

    # Проверяем, что продукты добавлены
    assert len(category.products) == 2
    assert Category.product_count == 2


def test_add_product_error_handling(caplog: Any) -> None:
    # Создаем категорию
    category = Category("Электроника", "Описание")

    # Создаем некорректный продукт (вызовет исключение)
    with pytest.raises(ValueError):
        category.add_product(None)  # type: ignore

    # Проверяем, что было залогировано сообщение об ошибке
    assert "Ошибка при добавлении продукта" in caplog.text

    # Проверяем, что список продуктов не изменился
    assert len(category.products) == 0
