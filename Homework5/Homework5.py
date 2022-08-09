from datetime import datetime
from functools import wraps
import os


def logger(path):
    '''
    Decorator to choose path to save log file for logging decorator
    '''

    def _logger(old_function):
        '''
        Decorator to log any function progress
        '''

        @wraps(old_function)
        def new_function(*args, **kwargs):

            result = old_function(*args, **kwargs)
            with open(os.path.join(path, 'logging.txt'), 'a', encoding='utf8') as outfile:
                outfile.write(f'{datetime.now()} - {old_function.__name__} - {args}, {kwargs} - {result}\n')
            return result

        return new_function

    return _logger


@logger('summator')
def summator(*args, **kwargs):
    '''
    Sums all received args and kwargs. Works both with integer or strings
    :param args: any number of integers or strings
    :param kwargs: any number of integers or strings as keyword arguments
    :return: resulting sum
    '''
    result = args[0]
    for i, element in enumerate(args):
        if i == 0:
            continue
        result += element
    for v in kwargs.values():
        result += v
    return result


@logger('deductor')
def deductor(a: int, b: int) -> int:
    '''
    Deducts two integers
    :param a: depreciate
    :param b: subtrahend
    :return: difference
    '''
    return a - b


@logger('multiplier')
def multiplier(*args, **kwargs):
    '''
    Multiplies any number of integers
    :param args: any number of integers
    :param kwargs: any number of integers as keyword arguments
    :return: product
    '''
    result = 1
    for element in args:
        result *= element
    for v in kwargs.values():
        result *= v
    return result


@logger('divider')
def divider(a, b):
    '''
    Performs integer division
    :param a: dividend
    :param b: separator
    :return: quotient
    '''
    return a // b


if __name__ == '__main__':
    summator(2, 3, 4, a=8, b=-100, c=0.5)
    summator('a', 'b', 'c', d='d', e='e', f='f')
    deductor(10, 5)
    multiplier(1, 4, a=2, b=3, c=10)
    divider(7, 5)
    print(summator.__doc__)
