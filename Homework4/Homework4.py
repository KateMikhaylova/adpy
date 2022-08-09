from itertools import chain


class FlatIterator:
    '''
    Class for iterable object list of lists

    Attributes:

    nested_list: list
        list of lists to be iterated
    cursor: int
        index for iteration in list of list
    inner_cursor: int
        index for iteration in inner lists

    Methods:

    __init__(nested_list)
    __iter__
    __next__
    '''

    def __init__(self, nested_list: list):
        '''
        Sets attribute nested_list for object FlatIterator
        :param nested_list: list, list of lists
        '''
        self.nested_list = nested_list

    def __iter__(self):
        '''
        Sets initial cursor and inner_cursor attributes for object FlatIterator
        :return: object FlatIterator
        '''
        self.cursor = 0
        self.inner_cursor = -1
        return self

    def __next__(self):
        '''
        Rewrites dunder method __next__ in order to flatten list of lists.
        First, objects from first inner list are returned one after another, then
        objects from second inner list and so on until all inner elements are returned
        :return: objects from inner lists
        '''
        self.inner_cursor += 1
        if self.inner_cursor >= len(self.nested_list[self.cursor]):
            self.cursor += 1
            self.inner_cursor = 0
        if self.cursor >= len(self.nested_list):
            raise StopIteration
        return self.nested_list[self.cursor][self.inner_cursor]


def flat_generator(nested_list: list):
    '''
    Returns generator by flattening of list of lists.
    First, objects from first inner list are yielded one after another,
    then objects from second inner list and so on until all inner elements are yielded
    :param nested_list: list of lists
    :return: generator object
    '''
    outer_index = 0
    inner_index = 0
    while True:
        yield nested_list[outer_index][inner_index]
        inner_index += 1
        if inner_index >= len(nested_list[outer_index]):
            outer_index += 1
            inner_index = 0
        if outer_index >= len(nested_list):
            break


def flatter(nested_list: list) -> list:
    '''
    Auxiliary function, flattens multiply nested list
    :param nested_list: multiply nested list
    :return: list with no lists in it
    '''
    present = False
    for element in nested_list:
        if isinstance(element, list):
            present = True
            break
    if not present:
        return nested_list
    else:
        new_list = list(chain.from_iterable(nested_list))
        return flatter(new_list)


class SuperFlatIterator:
    '''
    Class for iterable object multiply nested list

    Attributes:

    nested_list: list
        multiply nested list to be iterated
    flatted_list: list
        flatted multiply nested list
    cursor: int
        index for iteration

    Methods:

    __init__(nested_list)
    __iter__
    __next__
    '''

    def __init__(self, nested_list: list):
        '''
        Sets attributes nested_list and flatted_list for object FlatIterator
        :param nested_list: list, multiply nested list
        '''
        self.nested_list = nested_list
        self.flatted_list = flatter(nested_list)

    def __iter__(self):
        '''
        Sets initial cursor attribute for object SuperFlatIterator
        :return: object SuperFlatIterator
        '''
        self.cursor = 0
        return self

    def __next__(self):
        '''
        Rewrites dunder method __next__ in order to iterate multiply nested list.
        :return: next result of iteration
        '''
        if self.cursor >= len(self.flatted_list):
            raise StopIteration
        self.cursor += 1
        return self.flatted_list[self.cursor - 1]


def super_flat_generator(very_nested_list: list):
    '''
    Returns generator by flattening of multiply nested list.
    Yields object if it is not list otherwise calls itself recursively.
    :param: very_nested_list: multiply nested list
    :return: generator object
    '''
    for inner in very_nested_list:
        if isinstance(inner, list):
            yield from super_flat_generator(inner)
        else:
            yield inner


if __name__ == '__main__':

    print('\nЗадание 1, итератор списка списков\n')

    nested_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None],
    ]

    for item in FlatIterator(nested_list):
        print(item)

    flat_list = [item for item in FlatIterator(nested_list)]
    print(flat_list)

    print('\nЗадание 2, генератор списка списков\n')

    nested_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f'],
        [1, 2, None]
    ]

    for item in flat_generator(nested_list):
        print(item)

    super_nested_list = [
                         'a', ['b', 'c'],
                         ['d', [['e']], 'f', ['g', ['h', ['i']]]],
                         [['j'], 'k'], 'l',
                         ['m', ['n', ['o', ['p'], 'q'], 'r'], 's'],
                         [['t', 'u'], [['v'], 'w']],
                         ['x', [['y']]],
                         [[['z']]]
                         ]

    print('\nЗадание 3, итератор списка с любым уровнем вложенности\n')

    for element in SuperFlatIterator(super_nested_list):
        print(element)

    print('\nЗадание 4, генератор списка с любым уровнем вложенности\n')

    for element in super_flat_generator(super_nested_list):
        print(element)
