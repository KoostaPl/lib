import unittest
from unittest.mock import patch
from main import add_book

class TestAddBook(unittest.TestCase):
    # Добавление новой книги в пустую библиотеку
    @patch("builtins.input", side_effect=["New Book", "New Author", "2020"])
    @patch("main.save_library") 
    def test_add_book_to_empty_lib(self, mock_save, mock_input):
        library = {}
        add_book(library)  # Функция добавления книги

        # Проверка, что книга добавлена под ID 1
        self.assertIn(1, library)
        self.assertEqual(library[1]["title"], "New Book")
        self.assertEqual(library[1]["author"], "New Author")
        self.assertEqual(library[1]["year"], "2020")

        # Проверяем, что save_library была вызвана
        mock_save.assert_called_once_with(library)

    @patch("builtins.input", side_effect=["Another Book", "Another Author", "2024"])
    @patch("main.save_library")
    def test_add_book_to_non_empty_library(self, mock_save, mock_input):
        library = {
            1: {
                "id": 1,
                "title": "Existing Book",
                "author": "Existing Author",
                "year": "2022",
                "status": "В наличии"
            }
        }
        add_book(library)
        # Проверяем, что книга добавлена с ID 2
        self.assertIn(2, library)
        self.assertEqual(library[2]["title"], "Another Book")

        mock_save.assert_called_once_with(library)

