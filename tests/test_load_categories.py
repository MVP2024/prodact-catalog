import json
from unittest.mock import MagicMock, mock_open, patch

from src.data_loader import load_categories


class TestLoadCategories:
    def test_load_categories_empty_list(self) -> None:
        with patch("builtins.open", mock_open(read_data="[]")):
            categories = load_categories("dummy_path.json")
            assert len(categories) == 0

    def test_load_categories_missing_required_fields(self) -> None:
        invalid_data = [
            {"description": "Без имени"},  # Отсутствует name
            {"name": 123},  # Некорректный тип name
            {"name": "Категория", "description": 456},  # Некорректный тип description
        ]

        with patch("builtins.open", mock_open(read_data=json.dumps(invalid_data))):
            categories = load_categories("dummy_path.json")
            assert len(categories) == 0

    def test_load_categories_invalid_product_data(self) -> None:
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
        invalid_data = {"key": "value"}

        with patch("builtins.open", mock_open(read_data=json.dumps(invalid_data))):
            categories = load_categories("dummy_path.json")
            assert len(categories) == 0

    def test_load_categories_with_optional_product_description(self) -> None:
        data = [
            {
                "name": "Электроника",
                "description": "Электронные устройства",
                "products": [
                    {"name": "Смартфон", "price": 500.0, "quantity": 10},  # Без описания
                ],
            }
        ]

        with patch("builtins.open", mock_open(read_data=json.dumps(data))):
            categories = load_categories("dummy_path.json")
            assert len(categories) == 1
            assert categories[0].products[0].description == ""

    def test_load_categories_multiple_valid_categories(self) -> None:
        data = [
            {
                "name": "Электроника",
                "description": "Электронные устройства",
                "products": [
                    {"name": "Смартфон", "price": 500.0, "quantity": 10},
                ],
            },
            {
                "name": "Одежда",
                "description": "Модная одежда",
                "products": [
                    {"name": "Футболка", "price": 100.0, "quantity": 20},
                ],
            },
        ]

        with patch("builtins.open", mock_open(read_data=json.dumps(data))):
            categories = load_categories("dummy_path.json")
            assert len(categories) == 2
            assert categories[0].name == "Электроника"
            assert categories[1].name == "Одежда"


class TestLoadCategoriesExceptions:
    def test_file_not_found_error(self) -> None:
        with patch("builtins.open", side_effect=FileNotFoundError()):
            result = load_categories("nonexistent_file.json")
            assert len(result) == 0

    def test_json_decode_error(self) -> None:
        with patch("builtins.open", MagicMock()):
            with patch("json.load", side_effect=json.JSONDecodeError("Test error", "", 0)):
                result = load_categories("test.json")
                assert len(result) == 0

    def test_value_error_in_json_loading(self) -> None:
        with patch("builtins.open", MagicMock()):
            with patch("json.load", side_effect=ValueError("Invalid JSON")):
                result = load_categories("test.json")
                assert len(result) == 0

    def test_unexpected_exception_in_category_processing(self) -> None:
        test_data = [
            {
                "name": "Тестовая категория",
                "description": "Описание",
                "products": [{"name": "Тестовый продукт", "price": 100.0, "quantity": 10}],
            }
        ]

        with (
            patch("builtins.open"),
            patch("json.load", return_value=test_data),
            patch("src.data_loader.Category", side_effect=Exception("Unexpected error")),
        ):
            result = load_categories("test.json")
            assert len(result) == 0

    def test_logging_of_errors(self) -> None:
        with (
            patch("src.data_loader.logger") as mock_logger,
            patch("builtins.open", side_effect=FileNotFoundError()),
        ):
            file_path = "nonexistent_file.json"
            load_categories(file_path)
            mock_logger.error.assert_called_once_with(f"Файл не найден: {file_path}")

    def test_unexpected_global_exception(self) -> None:
        with (
            patch("builtins.open", mock_open(read_data=json.dumps([]))),
            patch("json.load", side_effect=Exception("Unexpected global error")),
            patch("src.data_loader.logger") as mock_logger,
        ):
            result = load_categories("test.json")
            assert len(result) == 0
            mock_logger.error.assert_called_once_with("Неожиданная ошибка при загрузке файла: Unexpected global error")
