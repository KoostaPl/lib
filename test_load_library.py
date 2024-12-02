import unittest
from unittest.mock import patch, mock_open
from main import load_library, save_library, add_book, delete_book, search_books, display_books, change_status

class TestLibrary(unittest.TestCase):
    # Если файл существует и содержит корректный JSON.
    @patch("builtins.open", new_callable=mock_open, read_data='{"1": {"id": 1, "title": "Test Book", "author": "Author", "year": "2022", "status": "В наличии"}}')
    def test_load_library_valid(self, mock_file):
        library = load_library()
        expected = {
            1: {
                "id": 1,
                "title": "Test Book",
                "author": "Author",
                "year": "2022",
                "status": "В наличии"
            }
        }
        self.assertEqual(library, expected)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_library_not_found(self, mock_file):
        # Проверка при отсутствии файла -> возвращение пустого словаря
        library = load_library()
        self.assertEqual(library, {})

    @patch("builtins.open", new_callable = mock_open, read_data = "invalid json")
    def test_load_library_invalid_json(self, mock_file):
        # Проверка при некорректном JSON -> возвращение пустого словаря
        library = load_library()
        self.assertEqual(library, {})


    