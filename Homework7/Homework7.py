from typing import Any


class Stack:
    """
    Class for stack object, which performs FILO and LIFO principles.
    Objects may be added at the end of stack and taken from its end

    attributes:
    stack: attribute to store list of objects

    methods:
    __init__:   creates empty list in stack attribute
    is_empty:   checks whether stack is empty or not
    push:       places object at the end of the stack
    pop:        takes away object from the and of the stack and returns it
    peek:       returns last object of the stack
    size:       returns len of the stack
    """

    def __init__(self):
        """
        Places empty list to stack attribute
        """
        self.stack = []

    def is_empty(self) -> bool:
        """
        Check whether stack attribute is empty or not
        :return: True if stack is empty, otherwise False
        """
        return not self.stack

    def push(self, new_element: Any) -> None:
        """
        Appends new element to the end of the stack attribute
        :param new_element: new element to be added to stack
        :return:
        """
        self.stack.append(new_element)

    def pop(self) -> Any:
        """
        Pops last element from stack attribute. It is no longer present in stack
        :return: last element of stack
        """
        if self.stack:
            popped = self.stack.pop()
            return popped
        else:
            raise IndexError

    def peek(self) -> Any:
        """
        Returns last element of the stack. Element stays in stack
        :return: last element of stack
        """
        if not self.stack:
            return None
        return self.stack[-1]

    def size(self) -> int:
        """
        Returns len of stack attribute
        :return:
        """
        return len(self.stack)


def check_braces(task: str) -> str:
    """
    Receives str of braces, check whether it is balanced or not
    :param task: str of braces '(){}[]' an any order and quantity
    :return: 'Сбалансированно' if braces are balanced, "Несбалансированно" if not balanced,
             'Строка содержит недопустимые символы' if str contains symbols other than braces
    """

    stack = Stack()

    for element in task:

        if element not in '({[)}]':
            return 'Строка содержит недопустимые символы'

        if element in '({[':
            stack.push(element)
            continue

        if (element == ']' and stack.peek() == '[') or \
           (element == ')' and stack.peek() == '(') or \
           (element == '}' and stack.peek() == '{'):
            stack.pop()
        else:
            return "Несбалансированно"

    if not stack.size():
        return 'Сбалансированно'
    else:
        return "Несбалансированно"


if __name__ == '__main__':

    task1 = '(((([{}]))))'
    task2 = '{{[(])]}}'
    task3 = 'task3'

    print(check_braces(task1))
    print(check_braces(task2))
    print(check_braces(task3))

