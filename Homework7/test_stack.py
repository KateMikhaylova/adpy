import pytest
from Homework7 import Stack, check_braces
from typing import Any, Iterable

PUSH_FIXTURE = [(1, [1]),
                ('a', ['a']),
                (3.14, [3.14]),
                (None, [None]),
                ([1, 2, 3], [[1, 2, 3]])]

PUSH_MANY_FIXTURE = [([1, 2, 3], [1, 2, 3]),
                     (('a', 'b', 'c'), ['a', 'b', 'c']),
                     ([3.14, None, str], [3.14, None, str]),
                     ([[1, 2, 3], (5, 6, 7), {8: 'h', 9: 'i'}], [[1, 2, 3], (5, 6, 7), {8: 'h', 9: 'i'}])]

IS_EMPTY_FIXTURE = [([], True), ((), True), ({}, True), ([None], False), ([1, 'a'], False)]

PEEK_FIXTURE = [([], None),
                (('a', 'b', 'c'), 'c'),
                ([3.14, None, str], str),
                ([[1, 2, 3], (5, 6, 7), {8: 'h', 9: 'i'}], {8: 'h', 9: 'i'})]

POP_FIXTURE = [(('a', 'b', 'c'), 'c', ['a', 'b']),
               ([3.14, None, str], str, [3.14, None]),
               ([[1, 2, 3], (5, 6, 7), {8: 'h', 9: 'i'}], {8: 'h', 9: 'i'}, [[1, 2, 3], (5, 6, 7)])]

SIZE_FIXTURE = [([], 0),
                (('a', 'b', 'c'), 3),
                ([3.14, None], 2),
                ([[1, 2, 3], (5, 6, 7), {8: 'h', 9: 'i'}], 3)]

CHECK_BRACES_FIXTURE = [('(((([{}]))))', 'Сбалансированно'),
                        ('{{[(])]}}', "Несбалансированно"),
                        ('task3', 'Строка содержит недопустимые символы'),
                        ('((((([{}]))))', "Несбалансированно"),
                        ('(((([{}])))))', "Несбалансированно"),
                        ('([{(((([{(((([{(((([{(((([{(((([{[[()]]}]))))}]))))}]))))}]))))}]))))}])', 'Сбалансированно')]


class TestStack:

    def setup(self):
        """
        Puts Stack object to attribute s
        :return:
        """
        self.s = Stack()

    def teardown(self):
        """
        Sets attribute s to None
        :return:
        """
        self.s = None

    @pytest.mark.parametrize('element, result', PUSH_FIXTURE)
    def test_push_one(self, element: Any, result: list):
        """
        Tests push method adding one element
        :param element: any element to be added to stack
        :param result: predicted resulting stack
        :return:
        """
        self.s.push(element)
        assert self.s.stack == result

    @pytest.mark.parametrize('elements, result', PUSH_MANY_FIXTURE)
    def test_push_many(self, elements: Iterable, result: list):
        """
        Tests push method adding several elements
        :param elements: several elements in iterable to be added to stack
        :param result: predicted resulting stack
        :return:
        """
        for element in elements:
            self.s.push(element)
        assert self.s.stack == result

    @pytest.mark.parametrize('elements, result', IS_EMPTY_FIXTURE)
    def test_is_empty(self, elements: Iterable, result: bool):
        """
        Tests is_empty method of Stack class
        :param elements: elements in iterable to fill in stack
        :param result: predicted result of is_empty method
        :return:
        """
        for element in elements:
            self.s.stack.append(element)
        assert self.s.is_empty() == result

    @pytest.mark.parametrize('elements, result', PEEK_FIXTURE)
    def test_peek(self, elements: Iterable, result: Any):
        """
        Tests peek method of Stack class
        :param elements: elements in iterable to fill in stack
        :param result: predicted return of peek method
        :return:
        """
        for element in elements:
            self.s.stack.append(element)
        assert self.s.peek() == result

    @pytest.mark.parametrize('elements, result_return, result_stack', POP_FIXTURE)
    def test_pop(self, elements: Iterable, result_return: Any, result_stack: list):
        """
        Tests pop method of Stack class
        :param elements: elements in iterable to fill in stack
        :param result_return: predicted return of pop method
        :param result_stack: predicted resulting stack after pop method
        :return:
        """
        for element in elements:
            self.s.stack.append(element)
        assert self.s.pop() == result_return and self.s.stack == result_stack

    def test_pop_raise(self):
        """
        Tests raise of exception in pop method in case trying to pop from empty list
        :return:
        """
        with pytest.raises(IndexError):
            self.s.pop()

    @pytest.mark.parametrize('elements, result', SIZE_FIXTURE)
    def test_size(self, elements: Iterable, result: int):
        """
        Tests size method of Stack class
        :param elements: elements in iterable to fill in stack
        :param result: predicted len of stack
        :return:
        """
        for element in elements:
            self.s.stack.append(element)
        assert self.s.size() == result


@pytest.mark.parametrize('string, result', CHECK_BRACES_FIXTURE)
def test_check_braces(string: str, result: str):
    """
    Tests check_braces function
    :param string: string with braces
    :param result: predicted result of function
    :return:
    """
    assert check_braces(string) == result
