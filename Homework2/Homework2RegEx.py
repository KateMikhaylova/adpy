import csv
import re


def get_info_from_csv(file_name: str) -> list:
    '''
    Gets contact list from csv file
    :param file_name: name of csv file
    :return: contact list
    '''
    with open(file_name, encoding='utf8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        return contacts_list


def transpose_matrix(matrix: list) -> list:
    '''
    Transposes matrix (array, list of lists), rows turn into columns and vise versa
    :param matrix: matrix to be transposed
    :return: transposed matrix
    '''
    transposed_matrix = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
    return transposed_matrix


def standardize_phones(phone_list: list) -> None:
    '''
    Standardizes phone numbers to pattern '+7(999)999-99-99 доб.9999' using regular expressions
    :param phone_list: list of phones
    :return: None, amends initial list
    '''
    for i, phone in enumerate(phone_list):
        search_pattern = r'(\+7|8)[\s(]*(\d{3})[)\s-]*(\d{3})-*(\d{2})-*(\d{2})[\s(]*(доб\.)*\s*(\d{4})*\)*'
        replace_pattern = r'+7(\2)\3-\4-\5 \6\7'
        new_phone = re.sub(search_pattern, replace_pattern, phone)
        phone_list[i] = new_phone.strip()


def split_lastname(transposed_contact_list: list) -> None:
    '''
    Splits lastname string (if firstname and/or surname (patronym) is indicated in the same string as lastname)
    and moves firstname and/or surname (patronym) to corresponding strings
    :param transposed_contact_list: Transposed contact list matrix
    :return: None, amends initial list
    '''
    for i, lastname in enumerate(transposed_contact_list[0]):
        pattern = r'[а-яёА-ЯЁ]+'  # or pattern = r'\w+'
        splitted = (re.findall(pattern, lastname))
        if len(splitted) == 2:
            transposed_contact_list[0][i] = splitted[0]
            transposed_contact_list[1][i] = splitted[1]
        elif len(splitted) == 3:
            transposed_contact_list[0][i] = splitted[0]
            transposed_contact_list[1][i] = splitted[1]
            transposed_contact_list[2][i] = splitted[2]
        else:
            pass


def split_firstname(transposed_contact_list: list) -> None:
    '''
    Splits firstname string (if surname (patronym) is indicated in the same string as firstname)
    and moves surname (patronym) to corresponding string
    :param transposed_contact_list: Transposed contact list matrix
    :return: None, amends initial list
    '''
    for i, firstname in enumerate(transposed_contact_list[1]):
        pattern = r'[а-яёА-ЯЁ]+'  # or pattern = r'\w+'
        splitted = (re.findall(pattern, firstname))
        if len(splitted) == 2:
            transposed_contact_list[1][i] = splitted[0]
            transposed_contact_list[2][i] = splitted[1]


def join_doubled_contacts(contact_list: list) -> list:
    '''
    Finds doubled persons in contact list and joins information from several lines into one
    :param contact_list: List of lists containing persons contact information
    :return: contact list without doubled information
    '''
    final_list = list()
    final_list.append(contact_list[0])
    del (contact_list[0])
    contact_list.sort()
    final_list.append(contact_list[0])
    for person in contact_list:
        if person[0] == final_list[-1][0] and person[1] == final_list[-1][1]:
            for i, parameter in enumerate(final_list[-1]):
                if not parameter:
                    final_list[-1][i] = person[i]
        else:
            final_list.append(person)
    return final_list


def save_info_to_csv(file_name: str, contact_list: list) -> None:
    '''
    Saves contact list to csv file
    :param file_name: name of csv file
    :param contact_list: ordered contact list
    :return: None
    '''
    with open(file_name, "w", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contact_list)


if __name__ == '__main__':
    contacts_list = get_info_from_csv("phonebook_raw.csv")
    transposed_list = transpose_matrix(contacts_list)
    standardize_phones(transposed_list[5])
    split_lastname(transposed_list)
    split_firstname(transposed_list)
    contact_list = transpose_matrix(transposed_list)
    ordered_contact_list = join_doubled_contacts(contact_list)
    save_info_to_csv("phonebook.csv", ordered_contact_list)
