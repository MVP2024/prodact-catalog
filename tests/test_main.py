import json
import os
import unittest
from unittest.mock import mock_open, patch

from src.prodact_catalog.views import main

class TestMainFunction(unittest.TestCase):

    def setUp(self):
        # Подготовка тестовых данных
        self.test_data = [
            {
                "name": "Category1",
                "description": "Description1",
                "products": [
                    {"name": "Product1", "description": "Description of Product1", "price": 100, "quantity": 10},
                    {"name": "Product2", "description": "Description of Product2", "price": 200, "quantity": 5},
                ],
            },
            {"name": "Category2", "description": "Description2", "products": []},
        ]
        self.test_json = json.dumps(self.test_data, ensure_ascii=False, indent=4)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    @patch("src.prodact_catalog.data_loader.load_categories")
    def test_main_success(self, mock_load_categories, mock_exists, mock_file):
        # Установка возвращаемых данных для mock_load_categories
        mock_load_categories.return_value = json.loads(self.test_json)

        # Тест успешного выполнения функции
        result = main()

        # Проверка, что результат соответствует ожидаемому
        expected_result = [
            {
                "name": "Category1",
                "description": "Description1",
                "products": [
                    {"name": "Product1", "price": 100, "quantity": 10},
                    {"name": "Product2", "price": 200, "quantity": 5},
                ],
            },
            {"name": "Category2", "description": "Description2", "products": []},
        ]
        self.assertEqual(result, expected_result)

        # Проверка, что файл был открыт для записи
        output_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "output_categories.json")
        mock_file.assert_any_call(output_file_path, "w", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=False)
    @patch("os.path.join", return_value="fake_path/products.json")
    def test_main_file_not_found(self, mock_join, mock_exists, mock_file):
        # Тест случая, когда файл не найден
        with self.assertLogs('src.prodact_catalog.views.logger', level="ERROR") as log:
            result = main()

        # Проверка, что результат пуст
        self.assertEqual(result, [])

        # Проверка, что в логах есть сообщение об ошибке
        self.assertIn("Файл не найден: fake_path/products.json", log.output[0])

    @patch("builtins.open", new_callable=mock_open, read_data="invalid_json")
    @patch("os.path.join", return_value="fake_path/products.json")
    def test_main_invalid_json(self, mock_join, mock_file):
        # Тест случая, когда JSON некорректен
        with self.assertLogs('src.prodact_catalog.views.logger', level="ERROR") as log:
            result = main()

        # Проверка, что результат пуст
        self.assertEqual(result, [])

        # Проверка, что в логах есть сообщение об ошибке
        self.assertIn("Ошибка при загрузке JSON:", log.output[0])

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps([{"name": "Category1", "description": "Description1", "products": []}]),
    )
    @patch("os.path.join", return_value="fake_path/products.json")
    def test_main_empty_products(self, mock_join, mock_file):
        # Тест случая, когда категория не содержит продуктов
        result = main()

        # Проверка, что результат содержит категорию без продуктов
        expected_result = [{"name": "Category1", "description": "Description1", "products": []}]
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()