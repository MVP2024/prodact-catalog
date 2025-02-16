import unittest
from unittest.mock import mock_open, patch
from src.prodact_catalog.data_loader import load_categories
from src.prodact_catalog.models import Product, Category

class TestLoadCategories(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='[{"name": "Category1", "description": "Description1", "products": [{"name": "Product1", "description": "Description1", "price": 10.0, "quantity": 5}]}]')
    def test_load_categories_success(self, mock_file):
        categories = load_categories("dummy_path.json")
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0].name, "Category1")
        self.assertEqual(len(categories[0].products), 1)
        self.assertEqual(categories[0].products[0].name, "Product1")

    @patch("builtins.open", new_callable=mock_open)
    def test_load_categories_file_not_found(self, mock_file):
        mock_file.side_effect = FileNotFoundError
        categories = load_categories("dummy_path.json")
        self.assertEqual(categories, [])

    @patch("builtins.open", new_callable=mock_open, read_data='not a json')
    def test_load_categories_json_decode_error(self, mock_file):
        categories = load_categories("dummy_path.json")
        self.assertEqual(categories, [])
