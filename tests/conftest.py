import pytest

from src.prodact_catalog.models import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counts() -> None:
    """Сброс статических счетчиков перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product() -> Product:
    """Фикстура для создания тестового продукта."""
    return Product("Тестовый продукт", "Это тестовый продукт.", 9.99, 100)


@pytest.fixture
def category() -> Category:
    """Фикстура для создания тестовой категории."""
    return Category("Тестовая категория", "Это тестовая категория.")
