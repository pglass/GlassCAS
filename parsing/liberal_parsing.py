'''
liberal_parsing.py - contains functions to transform some ambiguous
inputs into a non-ambiguous form(s) that rigid_parsing can handle.
'''   

from parser_definitions import *
from parser_util import get_number

def insert_implicit_mult_ops(tokens):
    '''
    This inserts IMPLICIT_MULT and '*' symbols to support implicit
    multiplication, where IMPLICIT_MULT is the implicit multiplication
    operator with precedence 3.5 (higher than +-*/ and functions
    but less than ^ and !).
    
    This implies the following evaluations for example inputs (but this
    method does not insert parens. Evaluation order comes from precedences):
        INPUT           -->  EVALUATION ORDER
        "xy+z"          -->  (x*y) + z
        "xy"            -->  x*y
        "1/xy"          -->  1/(x*y)
        "xyz!"          -->  x*y*(z!)
        "wx^yz"         -->  w*(x^y)*z
        "cosxyz"        -->  cos(x*y*z)
    And I would also like:
        "cosxy*sinyz"   -->  cos(x*y)*sin(y*z)
        "cosxysinyz"    -->  cos(x*y)*sin(y*z)
        
    In particular, in the last examples we insert '*' rather than
    IMPLICIT_MULT before functions where there is an implicit multiplication
    (otherwise "cosxysinyz" would be evaluated as cos(x*y*sin(y*z)),
    which is probably not what was intended by the user)

    This returns True if any symbols were inserted and False otherwise.
    '''
    
    start_len = len(tokens)
    
    i = 0
    while i < len(tokens) - 1:
        # check for things on the left of an implicit multiply
        if (get_number(tokens[i]) != None or 
            tokens[i] in RPARENS + VARIABLES + CONSTANTS.keys() or
            tokens[i] in POSTFIX_FUNCTION_MAP.keys()
            ):
            
            token = tokens[i+1]
            
            # check for things on the right side
            if (get_number(token) != None or
                token in LPARENS + VARIABLES + CONSTANTS.keys()
                ):
                tokens.insert(i+1, IMPLICIT_MULT)
                i += 2
            elif token in PREFIX_FUNCTION_MAP.keys():
                tokens.insert(i+1, "*")
                i += 2
            else:
                i += 1
        else:
            i += 1

    if len(tokens) - start_len > 0:
        return True
    return False

def return_length_change(func):
    '''
    Decorator for functions f(tokens, i) that returns the change in len(tokens)
    '''
    def new_function(tokens, i):
        len_before = len(tokens)
        func(tokens, i)
        return len(tokens) - len_before
    return new_function
    
@return_length_change
def transform_if_negation(tokens, i):
    '''
    Look around index i in tokens. If there is a subtraction
    symbol '-' that is really a negation, alter tokens *in place* to
    represent the negation unambiguosly.
    '''
    if not 0 <= i < len(tokens) or tokens[i] != '-':
        return
    
    # handle minus sign at the front
    if i == 0:
        if tokens[i:i+2] == ['-', '-']:
            tokens[i:i+2] = []
        else:
            tokens[i] = NEG_OP
    # handle '+-' occurrences
    elif tokens[i-1:i+1] == ["+", "-"]:
        if i-1 == 0:
            tokens[i-1:i+1] = [NEG_OP]
        else:
            tokens[i-1:i+1] = ["-"]
    # handle '--' occurrences
    elif tokens[i-1:i+1] == ["-", "-"]:
        tokens[i-1:i+1] = ["+"]
    # handle '<LHS> OP - <RHS>' occurrences
    elif (tokens[i-1] in ["*", IMPLICIT_MULT, '/', '%'] + LPARENS or
          tokens[i-1] in PREFIX_FUNCTION_MAP.keys()
          ):
        tokens[i] = NEG_OP

def apply_transformations(tokens):
    '''
    This applies all of the transformations in this module to tokens:
        1. Subtraction-negation resolution
        2. Implicit multiplication insertion
    
    (Use this after tokenization but before conversion to RPN)
    '''
    
    i = 0
    while i < len(tokens):
        k = transform_if_negation(tokens, i)
        if k != 0:
            i += k-1
        else:
            i += 1
    
    if insert_implicit_mult_ops(tokens):
        apply_transformations(tokens)
    return tokens
