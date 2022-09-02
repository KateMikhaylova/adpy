import pytest

from secretary import find_shelf, find_owner, add_document, delete_document
from secretary_fixtures import FIXTURE_DELETE, FIXTURE_PERSON, FIXTURE_ADD, FIXTURE_SHELF

from itertools import chain


class TestSecretary:
    """
    Class to test proceeding of secretary script

    attributes:
    documents:          attribute to store list of documents while test runs
    shelves:            attribute to store dict of shelves while test runs

    methods:
    setup:              sets initial list of documents and dict of shelves
    teardown:           deletes list of documents and dict of shelves
    test_person_search: tests find_owner function
    test_shelf_search:  tests find_shelf function
    test_add_document:  tests add_document function
    test_delete:        tests delete_document function
    """

    def setup(self):
        """
        sets initial list of documents and dict of shelves
        :return:
        """

        self.documents = [{"type": "packing list", "number": "11-05-2018", "name": "Mary Black"},
                          {"type": "bill of lading", "number": "VLC001", "name": "John Smith"},
                          {"type": "waybill", "number": "BLMSCU7986359", "name": "Hugh Stanford"}
                          ]

        self.shelves = {'1': ['11-05-2018', 'DGN7865'],
                        '2': ['VLC001'],
                        '3': ['BLMSCU7986359']
                        }

    def teardown(self):
        """
        deletes list of documents and dict of shelves
        :return:
        """
        self.documents = None
        self.shelves = None

    @pytest.mark.parametrize('doc_number, result', FIXTURE_PERSON)
    def test_person_search(self, doc_number: str, result: str):
        """
        tests find_owner function
        :param doc_number: document number from fixture
        :param result: function predicted result from fixture
        :return:
        """
        assert find_owner(doc_number, self.documents) == result

    @pytest.mark.parametrize('doc_number, result', FIXTURE_SHELF)
    def test_shelf_search(self, doc_number: str, result: str):
        """
        tests find_shelf function
        :param doc_number:document number from fixture
        :param result: function predicted result from fixture
        :return:
        """
        assert find_shelf(doc_number, self.shelves) == result

    @pytest.mark.parametrize('doc_type, doc_number, doc_owner, shelf, result', FIXTURE_ADD)
    def test_add_document(self, doc_type: str, doc_number: str, doc_owner: str, shelf: str, result: str):
        """
        tests add_document function
        :param doc_type: document type from fixture
        :param doc_number: document number from fixture
        :param doc_owner: document owner from fixture
        :param shelf: document place shelf from fixture
        :param result: function predicted result from fixture
        :return:
        """
        if result == 'Документ добавлен':
            assert add_document(doc_type, doc_number, doc_owner, shelf, self.documents, self.shelves) == result \
                    and doc_number in self.shelves.get(shelf) \
                    and {"type": doc_type, "number": doc_number, "name": doc_owner} in self.documents
        else:
            assert add_document(doc_type, doc_number, doc_owner, shelf, self.documents, self.shelves) == result \
                   and doc_number not in list(chain.from_iterable(list(self.shelves.values()))) \
                   and {"type": doc_type, "number": doc_number, "name": doc_owner} not in self.documents

    @pytest.mark.parametrize('doc_number, result', FIXTURE_DELETE)
    def test_delete(self, doc_number: str, result: str):
        """
        tests delete_document function
        :param doc_number: document number from fixture
        :param result: function predicted result from fixture
        :return:
        """
        assert delete_document(doc_number, self.documents, self.shelves) == result \
                and doc_number not in list(chain.from_iterable(list(self.shelves.values()))) \
                and [i for i in self.documents if i['number'] == doc_number] == []
