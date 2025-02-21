import json
import os
from typing import Any, Dict, List
import unittest
from unittest.mock import patch, mock_open, MagicMock

import pytest

from src.logger import setup_logger
from src.models import Category, Product
from src.main import main
from src.data_loader import load_categories


class TestMainFunction(unittest.TestCase):
    def setUp(self):
        # Настройка логгера и сброс статических счетчиков
        self.logger = setup_logger(__name__)
        Category._product_count = 0
        Category.category_count = 0

    @patch("src.main.load_categories")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_main_valid_data(
        self, mock_exists: MagicMock, mock_file: MagicMock, mock_load_categories: MagicMock
    ) -> None:
        # Создаем тестовую категорию и продукт
        category = Category("Смартфоны", "Описание категории")
        product = Product("Тестовый смартфон", "Описание продукта", 100000.0, 5)
        category.add_product(product)
        mock_load_categories.return_value = [category]

        # Вызываем main и проверяем результат
        result = main()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Смартфоны")
        self.assertEqual(len(result[0]["products"]), 1)
        self.assertEqual(result[0]["products"][0]["name"], "Тестовый смартфон")

    @patch("src.main.load_categories")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_main_empty_categories(
        self, mock_exists: MagicMock, mock_file: MagicMock, mock_load_categories: MagicMock
    ) -> None:
        # Тест с пустым списком категорий
        mock_load_categories.return_value = []
        result = main()
        self.assertEqual(result, [])

    @patch("src.main.logger")
    @patch("os.path.exists", return_value=False)
    def test_main_file_not_found(
        self, mock_exists: MagicMock, mock_logger: MagicMock
    ) -> None:
        # Тест на отсутствие файла
        result = main()
        mock_logger.error.assert_called_once()
        self.assertEqual(result, [])

    @patch("src.main.load_categories")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_main_category_without_products(
        self, mock_exists: MagicMock, mock_file: MagicMock, mock_load_categories: MagicMock
    ) -> None:
        # Тест категории без продуктов
        category = Category("Пустая категория", "Описание")
        mock_load_categories.return_value = [category]

        result = main()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["products"], [])

    @patch("src.main.load_categories")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_main_multiple_categories_and_products(
        self, mock_exists: MagicMock, mock_file: MagicMock, mock_load_categories: MagicMock
    ) -> None:
        # Тест с несколькими категориями и продуктами
        category1 = Category("Смартфоны", "Мобильные устройства")
        product1 = Product("iPhone", "Описание", 100000.0, 5)
        product2 = Product("Samsung", "Описание", 90000.0, 7)
        category1.add_product(product1)
        category1.add_product(product2)

        category2 = Category("Ноутбуки", "Компьютерная техника")
        product3 = Product("MacBook", "Описание", 150000.0, 3)
        category2.add_product(product3)

        mock_load_categories.return_value = [category1, category2]

        result = main()
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]["products"]), 2)
        self.assertEqual(len(result[1]["products"]), 1)

    @patch("src.main.load_categories")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_main_exception_handling(
        self, mock_exists: MagicMock, mock_file: MagicMock, mock_load_categories: MagicMock
    ) -> None:
        # Тест обработки исключений при загрузке
        mock_load_categories.side_effect = Exception("Unexpected error")

        result = main()
        self.assertEqual(result, [])

    @patch("src.main.load_categories")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_main_output_file_creation(
        self, mock_exists: MagicMock, mock_file: MagicMock, mock_load_categories: MagicMock
    ) -> None:
        # Тест создания выходного файла
        category = Category("Тестовая категория", "Описание")
        product = Product("Тестовый продукт", "Описание", 1000.0, 5)
        category.add_product(product)
        mock_load_categories.return_value = [category]

        main()

        # Проверяем, что файл открыт на запись с правильной кодировкой
        mock_file.assert_called_with(
            unittest.mock.ANY, "w", encoding="utf-8"
        )
