import unittest
from unittest.mock import patch
from main import delete_book

class TestDeleteBook(unittest.TestCase):
    @patch("builtins.input", side_effect=["1"])
    @patch("main.save_library")
    def test_delete_exst_book(self, mock_save, mock_input):
        library = {
            1: {
                "id": 1,
                "title": "Test Book",
                "author": "Author",
                "year": "2022",
                "status": "В наличии"
            }
        }
        delete_book(library)

        # Проверка удаления книги с ID 1
        self.assertNotIn(1, library)
        mock_save.assert_called_once_with(library)


    @patch("builtins.input", side_effect=["2"]) 
    @patch("builtins.print") 
    def test_delete_non_exst_book(self, mock_print, mock_input):
        library = {
            1: {
                "id": 1,
                "title": "Test Book",
                "author": "Author",
                "year": "2022",
                "status": "В наличии"
            }
        }
        
        delete_book(library)  # Пытаемся удалить книгу с ID 2, которой нет в библиотеке
        # Проверяем, что книга с ID 2 не была удалена
        self.assertIn(1, library)
        # Проверяем, что выводилось правильное сообщение
        mock_print.assert_called_once_with("Книга с ID 2 не существует.")
        
        