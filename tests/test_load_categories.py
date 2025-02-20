import json
from unittest.mock import MagicMock, mock_open, patch

from src.prodact_catalog.data_loader import load_categories


class TestLoadCategories:
    def test_load_categories_empty_list(self) -> None:
        # Тест на пустой список
        with patch("builtins.open", mock_open(read_data="[]")):
            categories = load_categories("dummy_path.json")
            assert len(categories) == 0

    def test_load_categories_missing_required_fields(self) -> None:
        # Тест на категории с отсутствующими обязательными полями
        invalid_data = [
            {"description": "Без имени"},  # Отсутствует name
            {"name": 123},  # Некорректный тип name
            {"name": "Категория", "description": 456},  # Некорректный тип description
        ]

        with patch("builtins.open", mock_open(read_data=json.dumps(invalid_data))):
            categories = load_categories("dummy_path.json")
            assert len(categories) == 0

    def test_load_categories_invalid_product_data(self) -> None:
        # Тест на категории с некорректными данными продуктов
        mixed_data = [
            {
                "name": "Электроника",
                "description": "Электронные устройства",
                "products": [
                    {"name": "Смартфон"},  # Отсутствуют обязательные поля
                    {"name": "Ноутбук", "price": "Дорого", "quantity": "Много"},  # Некорректные типы
                ],
            }
        ]

        with patch("builtins.open", mock_open(read_data=json.dumps(mixed_data))):
            categories = load_categories("dummy_path.json")
            assert len(categories) == 0

    def test_load_categories_partial_valid_data(self) -> None:
        # Тест на частично корректные данные
        mixed_data = [
            {
                "name": "Электроника",
                "description": "Электронные устройства",
                "products": [
                    {"name": "Смартфон", "price": 500.0, "quantity": 10, "description": "Новая модель"},
                    {"name": "Ноутбук"},  # Некорректный продукт
                ],
            }
        ]

        with patch("builtins.open", mock_open(read_data=json.dumps(mixed_data))):
            categories = load_categories("dummy_path.json")
            assert len(categories) == 1
            assert len(categories[0].products) == 1
            assert categories[0].products[0].name == "Смартфон"

    def test_load_categories_non_list_data(self) -> None:
        # Тест на данные, не являющиеся списком
        invalid_data = {"key": "value"}

        with patch("builtins.open", mock_open(read_data=json.dumps(invalid_data))):
            categories = load_categories("dummy_path.json")
            assert len(categories) == 0


class TestLoadCategoriesExceptions:
    def test_file_not_found_error(self) -> None:
        # Тест на обработку FileNotFoundError
        with patch("builtins.open", side_effect=FileNotFoundError()):
            result = load_categories("nonexistent_file.json")
            # Проверяем, что возвращается пустой список
            assert len(result) == 0

    def test_json_decode_error(self) -> None:
        # Тест на обработку JSONDecodeError
        with patch("builtins.open", MagicMock()):
            # Имитируем JSONDecodeError при json.load()
            with patch("json.load", side_effect=json.JSONDecodeError("Test error", "", 0)):
                result = load_categories("test.json")
                # Проверяем, что возвращается пустой список
                assert len(result) == 0

    def test_value_error_in_json_loading(self) -> None:
        # Тест на обработку ValueError при загрузке JSON
        with patch("builtins.open", MagicMock()):
            # Имитируем ValueError
            with patch("json.load", side_effect=ValueError("Invalid JSON")):
                result = load_categories("test.json")
                # Проверяем, что возвращается пустой список
                assert len(result) == 0

    def test_unexpected_exception_in_category_processing(self) -> None:
        # Тест на обработку неожиданного исключения при обработке категории
        test_data = [
            {
                "name": "Тестовая категория",
                "description": "Описание",
                "products": [{"name": "Тестовый продукт", "price": 100.0, "quantity": 10}],
            }
        ]

        # Имитируем неожиданное исключение при создании категории
        with (
            patch("builtins.open"),
            patch("json.load", return_value=test_data),
            patch("src.prodact_catalog.data_loader.Category", side_effect=Exception("Unexpected error")),
        ):
            result = load_categories("test.json")
            # Проверяем, что возвращается пустой список
            assert len(result) == 0

    def test_logging_of_errors(self) -> None:
        # Тест на корректность логирования ошибок
        with (
            patch("src.prodact_catalog.data_loader.logger") as mock_logger,
            patch("builtins.open", side_effect=FileNotFoundError()),
        ):
            file_path = "nonexistent_file.json"
            load_categories(file_path)
            # Проверяем, что вызван метод error с правильным сообщением
            mock_logger.error.assert_called_once_with(f"Файл не найден: {file_path}")
