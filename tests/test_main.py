import json
import unittest
from typing import Any
from unittest.mock import mock_open, patch

from src.prodact_catalog.logger import setup_logger
from src.prodact_catalog.models import Category, Product
from src.prodact_catalog.views import main

logger = setup_logger(__name__)


class TestMainFunction(unittest.TestCase):

    @patch("src.prodact_catalog.views.load_categories")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_main_valid_data(self, mock_exists: Any, mock_file: Any, mock_load_categories: Any) -> None:
        category = Category("Смартфоны", "Смартфоны, как средство не только коммуникации.")
        product = Product("Samsung Galaxy C23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
        category.add_product(product)

        mock_load_categories.return_value = [category]

        result = main()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Смартфоны")
        self.assertEqual(len(result[0]["products"]), 1)

    # Остальные методы остаются без изменений...

    @patch("src.prodact_catalog.views.load_categories")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    @patch("os.path.exists", return_value=True)
    def test_main_empty_data(self, mock_exists: Any, mock_file: Any, mock_load_categories: Any) -> None:
        mock_load_categories.return_value = []
        result = main()
        self.assertEqual(result, [])

    @patch("src.prodact_catalog.views.logger")
    @patch("os.path.exists", return_value=False)
    def test_main_file_not_found(self, mock_exists: Any, mock_logger: Any) -> None:
        result = main()
        mock_logger.error.assert_called_once()
        self.assertEqual(result, [])

    @patch("src.prodact_catalog.views.load_categories")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            [{"name": "Смартфоны", "description": "Смартфоны, как средство не только коммуникации.", "products": []}]
        ),
    )
    @patch("os.path.exists", return_value=True)
    def test_main_no_products(self, mock_exists: Any, mock_file: Any, mock_load_categories: Any) -> None:
        category = Category("Смартфоны", "Смартфоны, как средство не только коммуникации.")
        mock_load_categories.return_value = [category]

        result = main()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["products"], [])

    @patch("src.prodact_catalog.views.logger")
    def test_main_json_decode_error_logging(self, mock_logger: Any) -> None:
        # Тест на логирование JSONDecodeError
        with (
            patch("builtins.open", new_callable=mock_open),
            patch("os.path.exists", return_value=True),
            patch("src.prodact_catalog.views.load_categories", side_effect=json.JSONDecodeError("Test error", "", 0)),
        ):
            result = main()

            # Проверяем, что ошибка залогирована
            mock_logger.error.assert_called_once()
            # Проверяем, что возвращается пустой список
            self.assertEqual(result, [])
            # Проверяем текст сообщения об ошибке
            error_message = mock_logger.error.call_args[0][0]
            self.assertIn("Ошибка при загрузке JSON", error_message)

    @patch("builtins.print")
    @patch("src.prodact_catalog.views.load_categories")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_main_print_output(
        self, mock_exists: Any, mock_file: Any, mock_load_categories: Any, mock_print: Any
    ) -> None:
        # Тест на вывод данных при запуске скрипта напрямую
        # Создаем тестовую категорию
        category = Category("Тестовая категория", "Описание")
        product = Product("Тестовый продукт", "", 100.0, 5)
        category.add_product(product)
        mock_load_categories.return_value = [category]

        # Вызываем main() как будто скрипт запущен напрямую
        with patch("__main__.__name__", "__main__"):
            main()

        # Проверяем, что print был вызван с данными
        self.assertTrue(mock_print.called)
        # Проверяем, что последний вызов print содержит данные о категориях
        last_call_args = mock_print.call_args[0][0]
        self.assertIsNotNone(last_call_args)

    @patch("builtins.print")
    @patch("src.prodact_catalog.views.load_categories")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_main_output_file_creation(
        self, mock_exists: Any, mock_file: Any, mock_load_categories: Any, mock_print: Any
    ) -> None:
        # Создаем тестовую категорию
        category = Category("Тестовая категория", "Описание")
        product = Product("Тестовый продукт", "", 100.0, 5)
        category.add_product(product)
        mock_load_categories.return_value = [category]

        # Вызываем main()
        result = main()

        # Проверяем, что файл был открыт на запись
        mock_file.assert_called_with(unittest.mock.ANY, "w", encoding="utf-8")

        # Проверяем содержимое результата
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Тестовая категория")
        self.assertEqual(len(result[0]["products"]), 1)
