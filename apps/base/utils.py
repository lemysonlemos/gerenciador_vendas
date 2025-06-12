import re


def digits(txt):
    """
    Keep only digits in txt.

    >>> digits('15-12/1985.')
    >>> '15121985'
    """
    if txt:
        return re.sub(r'\D', '', txt)
    return txt