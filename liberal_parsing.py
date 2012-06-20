'''
liberal_parsing.py - contains functions to transform some ambiguous
inputs into a non-ambiguous form(s) that rigid_parsing can handle.
'''   

from parser_definitions import *
from parser_util import get_number

def insert_times_symbols(tokens):
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
        
    In particular, in the last two examples we insert '*' rather than
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
            tokens[i] == '!'
            ):
            
            token = tokens[i+1]
            
            # check for things on the right side
            if (get_number(token) != None or
                token in LPARENS + VARIABLES + CONSTANTS.keys()):
                
                tokens.insert(i+1, IMPLICIT_MULT)
                i += 2
            elif token in FUNCTIONS.keys() and NUM_OPERANDS[token] == 1:
                tokens.insert(i+1, "*")
                i += 2
            else:
                i += 1
        else:
            i += 1

    if len(tokens) - start_len > 0:
        return True
    return False

def check_and_replace_operator(tokens, i):
    '''
    Given tokens and the index i of a symbol, if there is ambiguity concerning
    what operation the symbol represents:
        1. Determine what the symbol represents based on context and modify
           tokens to resolve the ambiguity.
           This changes the tokens list in place, and len(tokens) may change.
        2. Fail to determine what operation the symbol represents,
           and do nothing else.

    In case (1), return the index immediately after the modified section.
    In case (2), return None.
    '''
    
    # '-' may represent either negation or subtraction
    if tokens[i] == '-':
        # -R
        if i == 0 and tokens[i] == '-':
            if tokens[i:i+2] == ['-', '-']:
                tokens[i:i+2] = []
                return i
            else:
                tokens[i] = NEG_OP
                return i+1
        # L +- R --> L - R
        elif tokens[i-1:i+1] == ["+", "-"]:
            if i-1 == 0:
                tokens[i-1:i+1] = [NEG_OP]
            else:
                tokens[i-1:i+1] = ["-"]
            return i-1
        # L -- R --> L + R
        elif tokens[i-1:i+1] == ["-", "-"]:
            tokens[i-1:i+1] = ["+"]
            return i
        # L * -R, (-R), L / -R, L % -R
        elif (tokens[i-1] in ["*", IMPLICIT_MULT, '/', '%'] + LPARENS or
              tokens[i-1] in FUNCTIONS.keys()
             ):
            tokens[i] = NEG_OP
            return i+1
        elif (tokens[i-1] in ["!"] + VARIABLES + CONSTANTS.keys() or
              get_number(tokens[i-1]) != None
             ):
            return i+1
        return None
    
    return i+1

def interpret_and_correct_input(tokens):
    '''
    This performs ambiguous operator resolution and implicit multiplication
    processing before the input is converted to reverse polish notation.
    '''
    
    i = 0
    while i < len(tokens):
        k = check_and_replace_operator(tokens, i)
        if k != None:
            i = k
        else:
            i += 1
    
    if insert_times_symbols(tokens):
        interpret_and_correct_input(tokens)
    return tokens

