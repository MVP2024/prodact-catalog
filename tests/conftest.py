import pytest

from src.prodact_catalog.models import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counts():
    # Сброс статических переменных перед каждым тестом
    Category.total_categories = 0
    Category.total_products = 0


@pytest.fixture
def product():
    return Product("Тестовый продукт", "Это тестовый продукт.", 9.99, 100)


@pytest.fixture
def category():
    return Category("Тестовая категория", "Это тестовая категория.")
