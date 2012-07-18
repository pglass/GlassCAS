'''
parser_util.py

Used in rigid_parsing.py and liberal_parsing.py
'''

from parsing.parser_definitions import *

def remove_whitespace(expr):
    return "".join(e for e in expr if e not in WHITESPACE_CHARS)

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
        
def get_number(value):
    ''' 
    Return a complex, float, or int if value is or represents an
    instance of one of those types. Otherwise, return None.
    '''
    
    if value.__class__ in [int, float, complex]:
        return value
    
    try:
        return int(value)
    except ValueError:
        pass
    
    try:
        return float(value)
    except ValueError:
        pass
        
    try:
        return complex(value)
    except ValueError:
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

