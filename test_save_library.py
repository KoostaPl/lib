import unittest
from unittest.mock import patch, mock_open
import json
from main import save_library

class TestSaveLibrary(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    def test_save_library(self, mock_file):
        library = {
            "1": {
                "id": 1,
                "title": "Test Book",
                "author": "Author",
                "year": "2022",
                "status": "В наличии"
            }
        }
        save_library(library)

        # Образуем из библиотеки json
        expected_json = json.dumps(library, ensure_ascii=False, indent=4)

        # Собираем все части данных, передаваемые в write, в одну строку
        written_data = ''.join([call[0][0] for call in mock_file().write.call_args_list])
        
        # Проверяем, что собранные данные соответствуют ожидаемому json
        self.assertEqual(written_data, expected_json)


    @patch("builtins.open", new_callable=mock_open)
    def test_save_empty_library(self, mock_file):
        # Пустая библиотека не должна ничего записывать
        with patch("builtins.print") as mock_print:
            save_library({})
            mock_print.assert_called_once_with("Библиотека пуста, ничего не сохраняется.")