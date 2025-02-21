import pytest

from src.models import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counts() -> None:
    """Сброс статических счетчиков перед каждым тестом."""
    Category._product_count = 0
    Category.category_count = 0


@pytest.fixture
def product() -> Product:
    """Фикстура для создания тестового продукта."""
    return Product("Тестовый продукт", "Это тестовый продукт.", 9.99, 100)


@pytest.fixture
def category() -> Category:
    """Фикстура для создания тестовой категории."""
    return Category("Тестовая категория", "Это тестовая категория.")
