'''
liberal_parsing.py - contains functions to transform 
some ambiguous inputs into a non-ambiguous form(s) 
that rigid_parsing.py can handle.

There is 1 transformations this module can do right now:
  1. Insert times symbols to support implicit negation.
     See insert_times_symbol.
'''   

from parser_definitions import *
from rigid_parsing import get_number

def insert_times_symbols(tokens):
    '''
    Insert times symbols to support implicit multiplication.
    (After thinking about this more, I think I want implicit 
    multiplication to have precedence about 3.5: higher than 
    functions and +-*/% but less than ^ and !. It does not 
    currently work like that though.)
   
    I want this to work as follows (examples):
        4x     --> 4 * x
        4!5    --> 4! * 5
        4xy    --> 4 * x * y
        4pi    --> 4 * pi
        4cos5  --> 4 * cos(5)
        4(3)   --> 4 * (3)
        (3)4   --> (3) * 4
        cos5x  --> cos(5*x)
        cos5*x --> cos(5) * x
        xyz!   --> x*y*z!
        sin5xy*5cos5xy --> sin(5*x*y) * 5cos(5*x*y)
    
    This implies a few rules. Let C be any constant, V be any variable, 
    and N be a number, so that {C,V,N} represents one of those three:
        1. {C,V,N,')'}{C,V,N,'('} --> {C,V,N,')'}*{C,V,N,'('}
        2. If F is a function:
            {C,V,N,')'} F()     --> {C,V,N,')'} * F()
            F(){C,V,N}          --> F() * {C,V,N}
            F{C,V,N}...{C,V,N}  --> F({C,V,N} * ... * {C,V,N})
        3. If F is factorial:
            ()F {C,V,N} --> ()F * {C,V,N}
    Notice that rule 2 will insert parentheses around function arguments.
    '''
    
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
                token in LPARENS + VARIABLES + CONSTANTS.keys() or
                token in FUNCTIONS.keys() and NUM_OPERANDS[token] == 1
                ):
                
                tokens.insert(i+1, "*")
                i += 2
            else:
                i += 1
        elif tokens[i] in FUNCTIONS.keys() and NUM_OPERANDS[tokens[i]] == 1:
            i, n = i+1, i+1
            
            while n < len(tokens) and (get_number(tokens[n]) != None or 
                    tokens[n] in VARIABLES + CONSTANTS.keys()):
                n += 1
            if n > i:
                tokens[i:n] = ["("] + insert_times_symbols(tokens[i:n]) + [")"]
            i = n
                
        else:
            i += 1
    return tokens

