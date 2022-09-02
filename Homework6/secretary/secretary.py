import sys
from typing import List, NoReturn

documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

directories = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006'],
    '3': []
}


def find_owner(doc_number: str, documents_list: List[dict]) -> str:
    """
    Finds owner of indicated document
    :param doc_number: number of searched document
    :param documents_list: list with document dicts
    :return: Owner name if found or notice on document absence otherwise
    """

    for document in documents_list:
        if doc_number in document.values():
            return document['name']

    return 'Документ отсутствует'


def find_shelf(doc_number: str, shelves: dict) -> str:
    """
    Finds shelf where indicated document is stored
    :param doc_number: number of searched document
    :param shelves: shelves dict
    :return: str number of shelf if found or notice on document absence otherwise
    """

    for key, value in shelves.items():
        if doc_number in value:
            return key

    return 'Документ отсутствует'


def add_document(doc_type: str, doc_number: str, doc_owner: str, shelf: str,
                 documents_list: List[dict], shelves: dict) -> str:
    """
    Adds new document in document list and on indicated shelf
    :param doc_type: new document type
    :param doc_number: new document number
    :param doc_owner:  new document owner
    :param shelf: shelf to place new document
    :param documents_list: list of documents dicts
    :param shelves: dict of shelves
    :return: Document added notice if added or notice that shelf does not exist if shelf number input was incorrect
    """

    if shelf in shelves.keys():
        document = {"type": doc_type, "number": doc_number, "name": doc_owner}
        documents_list.append(document)
        shelves[shelf].append(doc_number)
        return 'Документ добавлен'

    return 'Полка не существует'


def delete_document(doc_number: str, documents_list: List[dict], shelves: dict) -> str:
    """
    Deletes document form shelf and/or document list if it is present, sends notice if absent
    :param doc_number: number of document to be deleted
    :param documents_list: list with documents dicts
    :param shelves: dict with shelves
    :return: Document deleted notice if deleted or notice that document does not exist
    """
    deleted = False

    for document in documents_list:
        if doc_number == document['number']:
            documents_list.remove(document)
            deleted = True

    for key, value in shelves.items():
        if doc_number in value:
            value.remove(doc_number)
            deleted = True

    if not deleted:
        return 'Документ отсутствует'

    return 'Документ удален'


def run(documents_list: List[dict], shelves: dict) -> NoReturn:
    """
    Runs secretary program permanently
    :param documents_list: list with documents dicts
    :param shelves: dict with shelves
    :return:
    """

    command_help = """Возможные команды:
    p – узнать имя человека по введенному номеру документа;
    s – узнать на какой полке находится документ по введенному номеру документа;
    l – получить список всех документов;
    a – добавление нового документа;
    d – удалить документ по номеру;
    h - справка по возможным командам;
    q - выход из программы."""
    print(command_help)

    while True:
        command = input("\nВведите вашу команду: ")

        if command == 'p':
            document_number = input('Введите номер документа для поиска владельца: ')
            print(find_owner(document_number, documents_list))

        elif command == 's':
            document_number = input('Введите номер документа для поиска полки: ')
            print(find_shelf(document_number, shelves))

        elif command == 'l':
            print(documents_list)

        elif command == 'a':
            document_type = input('Введите тип документа: ')
            document_number = input('Введите номер документа: ')
            document_owner = input('Введите имя владельца документа: ')
            shelf = input('На какой полке будет храниться документ: ')
            print(add_document(document_type, document_number, document_owner, shelf, documents_list, shelves))

        elif command == 'd':
            document_number = input('Введите номер документа для удаления: ')
            print(delete_document(document_number, documents_list, shelves))

        elif command == 'h':
            print(command_help)

        elif command == 'q':
            print('Осуществлен выход из программы')
            sys.exit()

        else:
            print('Такой команды не существует')


if __name__ == '__main__':
    run(documents, directories)
