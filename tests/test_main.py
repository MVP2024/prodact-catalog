import json
import unittest
from unittest.mock import mock_open, patch

from src.prodact_catalog.models import Category, Product
from src.prodact_catalog.views import main


class TestMainFunction(unittest.TestCase):

    @patch("src.prodact_catalog.views.load_categories")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            [
                {
                    "name": "Смартфоны",
                    "description": "Смартфоны, как средство не только коммуникации.",
                    "products": [
                        {
                            "name": "Samsung Galaxy C23 Ultra",
                            "description": "256GB, Серый цвет, 200MP камера",
                            "price": 180000.0,
                            "quantity": 5,
                        }
                    ],
                }
            ]
        ),
    )
    def test_main_valid_data(self, mock_file, mock_load_categories):
        category = Category("Смартфоны", "Смартфоны, как средство не только коммуникации.")
        product = Product("Samsung Galaxy C23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
        category.add_product(product)

        mock_load_categories.return_value = [category]

        result = main()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Смартфоны")
        self.assertEqual(len(result[0]["products"]), 1)

    @patch("src.prodact_catalog.views.load_categories")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    def test_main_empty_data(self, mock_file, mock_load_categories):
        mock_load_categories.return_value = []
        result = main()
        self.assertEqual(result, [])

    @patch("src.prodact_catalog.views.logger")
    def test_main_file_not_found(self, mock_logger):
        with patch("os.path.exists", return_value=False):
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
    def test_main_no_products(self, mock_file, mock_load_categories):
        category = Category("Смартфоны", "Смартфоны, как средство не только коммуникации.")
        mock_load_categories.return_value = [category]

        result = main()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["products"], [])


if __name__ == "__main__":
    unittest.main()
