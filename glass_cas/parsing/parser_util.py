from .parser_definitions import *
import string

def remove_whitespace(expr):
    return "".join(e for e in expr if e not in string.whitespace)

def read_complex_number(expr, start):
    '''
    Return the number string in expression that begins at index start
    (it assumes a number string exists there).

    A complex number is one of the following forms:
        <real_number>
        <real_number>j
        j<real_number>
    '''

    if expr[start] == 'j' and start + 1 < len(expr):
        return read_real_number(expr, start + 1) + 'j'
    elif expr[start] == 'j':
        return 'j'

    real_num = read_real_number(expr, start)
    if (start + len(real_num) < len(expr) and
        expr[start + len(real_num)] == 'j'
        ):
        return real_num + 'j'
    else:
        return real_num

def read_real_number(expr, start):
    '''
    Return the positive real number string in expression that begins at index
    start. The number string may be an integer or real number.

    Raises a SyntaxError if a float has too many decimal points,
    or if the number consists of only decimal points.
    '''

    token = ''
    i = start

    found_decimal_point = False
    while i < len(expr) and expr[i] in REAL_NUMBER_CHARS:
        if found_decimal_point and expr[i] == '.':
            raise SyntaxError("Too many decimal points: " + expr[start:i+1])
        elif expr[i] == '.':
            found_decimal_point = True

        token += expr[i]
        i += 1
    if token == '.':
        raise SyntaxError("Dangling decimal point: " +
            expr[max(0, start - 2) : min(len(expr), start + 2)])
    return token

def read_function(expr, start):

    token = expr[start]

    i = start + 1
    if i < len(expr) and expr[i] == '[':
        while i < len(expr) and expr[i] != ']':
            token += expr[i]
            i += 1
        if i < len(expr) and expr[i] == ']':
            token += expr[i]
            return token
        else:
            raise SyntaxError("Unclosed function arguments: " +
                expr[max(0, start - 2) : min(len(expr), start + 2)])

    return None

def get_number(value):
    '''
    Return a complex, float, or int if value is or represents an
    instance of one of those types. Otherwise, return None.
    '''

    if value.__class__ in [int, float, complex]:
        return value

    try:
        return int(value)
    except:
        pass

    try:
        return float(value)
    except:
        pass

    try:
        return complex(value)
    except:
        pass

    return None

def get_from_list(expr, start, value_list):
    '''
    Return an identifier beginning at index start, where the identifier
    is something in value_list. Returns None if no such identifier is found.

    This is used in tokenize to grab functions and constants.
    '''

    token = ''
    i, j = start, start

    while j < len(expr) and expr[i:j+1] in [f[:j+1 - i] for f in value_list]:
        token = expr[i:j+1]
        if token in value_list: # in case of "pipi" or "cossin"
            return token

        j += 1

    return None

def get_user_function(expr):
    if not expr:
        return None
    name = expr[0]
    operands = []

    if name not in string.ascii_letters:
        return None
    if expr[1] != '[':
        return None

    i = 2
    while i < len(expr) and expr[i] != ']':
        if expr[i] in string.ascii_letters:
            operands.append(Var(expr[i]))
            i += 1
        elif expr[i] == ',':
            i += 1
        else:
            return None

    return UserFunction(name, operands)
