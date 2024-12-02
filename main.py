import json
from typing import Dict


LIBRARY_FILE = "library.json"

def load_library() -> Dict[int, Dict]:
    """
    Загружает библиотеку из файла JSON.

    :return: Словарь с данными о книгах
    """
    try:
        with open(LIBRARY_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip() # Читаем содержимое и удаляение лишних пробелов
            if content:
                library = json.loads(content)
            else:
                return {}
            return {int(book_id): book_info for book_id, book_info in library.items()} # Возвращаем ID книги цифрой
    except FileNotFoundError:
        # Если файл отсутствует, возвращаем пустую библиотеку
        print("Ошибка: файл не был найден.")
        return {}
    except json.JSONDecodeError:
        print("Ошибка: неверный формат JSON.")
        return {}
    
def save_library(library: Dict[int, Dict]) -> None:
    """
    Сохраняет библиотеку в файл JSON.

    :param library: Словарь с данными о книгах
    """
    if not library:
        print("Библиотека пуста, ничего не сохраняется.")
        return
    with open(LIBRARY_FILE, "w", encoding="utf-8") as file:
        json.dump(library, file, ensure_ascii=False, indent=4)
        
def add_book(library: Dict[int, Dict]) -> None:
    """
    Добавляет новую книгу в библиотеку.

    :param library: Словарь с данными о книгах
    """

    # Запрос пользовательских данных по добавлению книги
    title = input("Введите название книги: ").strip()
    author = input("Введите автора книги: ").strip()

    while True:
        year = input("Введите год издания книги: ").strip()
        if not year.isdigit() or int(year) <= 0:
            print("Ошибка: год должен быть положительным числом. Введите корректный год.")
        else:
            break

    if library:
        book_id = max(library.keys()) + 1  # Ищем максимальный ключ и увеличиваем его
    else:
        book_id = 1  # Если библиотека пуста, начинаем с ID = 1

    # Добавим её в библиотеку 
    library[book_id] = {
        "id": book_id,
        "title": title,
        "author": author,
        "year": year,
        "status": "В наличии" # По умолчанию новый статус
    }
    print(f"Книга '{title}' успешно добавлена.")
    save_library(library)

def delete_book(library: Dict[int, Dict]) -> None:
    """
    Удаляет книгу из библиотеки по её ID.

    :param library: Словарь с данными о книгах
    """
    try:
        book_id = int(input("Введите ID книги для последующего удаления: ").strip())

        if book_id in library:
            del library[book_id]
            print(f"Книга с ID {book_id} была успешно удалена.")
            save_library(library) # Фиксируем изменения в файле
        else:
            print(f"Книга с ID {book_id} не существует.")
    except ValueError:
        print("Ошибка: введённый ID не верный.")

def search_books(library: Dict[int, Dict]) -> None:
    """
    Ищет книги в библиотеке по названию, автору или году издания.

    :param library: Словарь с данными о книгах
    """
    search_condition = input("Введите название книги, автора книги или год издания книги для поиска: ").strip()

    # По какой категории будем искать
    found_books = []
    for book_id, book_info in library.items():
        if (
            search_condition.lower() in book_info['title'].lower() or
            search_condition.lower() in book_info['author'].lower() or
            search_condition.lower() in book_info['year']
        ):
            found_books.append(book_info)
    
    if found_books:
        print("\nНайденные книги:")
        for book in found_books:
            print(f"ID книги: {book['id']} |  Название: {book['title']} | Автор: {book['author']} | Год: {book['year']} | Статус: {book['status']}")
    else:
        print("Книги не были найдены.")

def display_books(library: Dict[int, Dict]) -> None:
    """
    Отображает все книги в библиотеке.
    
    :param library: Словарь с данными о книгах
    """
    if not library:
        print("Библиотека пуста.")
        return
    
    print("\nВсе книги из библиотеки:")
    for book in library.values():
        print(f"ID книги: {book['id']} | Название: {book['title']} | Автор: {book['author']} | Год: {book['year']} | Статус: {book['status']}")

def change_status(library: Dict[int, Dict]) -> None:
    """
    Изменяет статус книги по ID.
    
    :param library: Словарь с данными о книгах
    """
    book_id = input("Для изменения статуса книги введите её ID: ").strip()

    # Проверка, является ли ID числом
    if not book_id.isdigit():
        print("Ошибка: Некорректный ID. ID должен являться числом.")
        return
    
    book_id = int(book_id)

    if book_id in library:
        while True:
            try:
                new_status = int(input("Введите новый статус (1 - В наличии, 2 - Выдана): ").strip())
                if new_status == 1:
                    status_text = "В наличии"
                    break
                elif new_status == 2:
                    status_text = "Выдана"
                    break
                else:
                    print("Ошибка: Введите 1 для 'В наличии' или 2 для 'Выдана'.")
            except ValueError:
                print("Ошибка: Введите число 1 или 2.")
        
        #Изменение статуса книги
        library[book_id]['status'] = status_text
        print(f"Статус книги с ID {book_id} изменён на '{status_text}'.")
        save_library(library) # Фиксируем изменения в файле
    else:
        print("Ошибка: Книга с данным ID не найдена.")

def main() -> None:
    """
    Основная функция программы. 
    Отображает меню и выполняет действия пользователя.
    """
    library = load_library() # Загрузка библиотеки из json файла

    while True:
        # Вывод меню библиотеки
        print("\n\tБиблиотека")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Просмотреть все книги")
        print("5. Изменить статус книги")
        print("6. Выйти из библиотеки")

        choice = input("Выберите действие (введите номер): ").strip()

        if choice == "1":
            print("Форма добавления книги.")
            # Добавление книги
            add_book(library)
        elif choice == "2":
            print("Процесс удаления книги.")
            delete_book(library)
        elif choice == "3":
            print("Функция поиска книги (заглушка).")
            search_books(library)
        elif choice == "4":
            print("Функция просмотра всех книг (заглушка).")
            display_books(library)
        elif choice == "5":
            change_status(library)
        elif choice == "6":
            print("Выход из программы.")
            save_library(library)  # Сохраняем библиотеку перед выходом
            break
        else:
            print("Ошибка: неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()


