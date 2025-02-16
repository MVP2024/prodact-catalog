from src.prodact_catalog.models import Category, Product


def test_product_initialization(product):
    assert product.name == "Тестовый продукт"
    assert product.description == "Это тестовый продукт."
    assert product.price == 9.99
    assert product.quantity == 100


def test_category_initialization(category):
    assert category.name == "Тестовая категория"
    assert category.description == "Это тестовая категория."
    assert category.products == []
    assert Category.total_categories == 1


def test_add_product_to_category(category, product):
    category.add_product(product)
    assert product in category.products
    assert Category.total_products == 1


def test_multiple_categories():
    Category("Категория 1", "Первая категория.")
    Category("Категория 2", "Вторая категория.")

    # Проверка, что количество категорий увеличилось
    assert Category.total_categories == 2


def test_add_multiple_products(category):
    product1 = Product("Продукт 1", "Описание 1", 10.0, 5)
    product2 = Product("Продукт 2", "Описание 2", 20.0, 10)

    category.add_product(product1)
    category.add_product(product2)

    assert len(category.products) == 2
    assert Category.total_products == 2
