'''
parser_defintions.py -- contains definitions parsing modules
'''

import cmath
import math

WHITESPACE_CHARS = list("\t\n\x0b\x0c\r ")
LPARENS = list("([")
RPARENS = list(")]")

REAL_NUMBER_CHARS = list("0123456789.")
NUMBER_CHARS = REAL_NUMBER_CHARS + ["j"] # Use 'j' as sqrt(-1)

# Define valid single-letter variables
VARIABLES = list("abcdefghiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

CONSTANTS = {
    'e' : cmath.e,
    'pi': cmath.pi
}

OPERATORS = [
    "+", 
    "-", 
    "*", 
    "/", 
    "^", # exponentiation
    "%", # modulus
    "!", # factorial
    "=",
]

# negation operator (this is treated as a function)
NEG_OP = '`'

FUNCTIONS = {
    'cos'       : cmath.cos,
    'sin'       : cmath.sin,
    'tan'       : cmath.tan,
    'ceil'      : math.ceil,
    'floor'     : math.floor,
    'ln'        : cmath.log,
    'log'       : cmath.log10,
    'sqrt'      : cmath.sqrt,
    NEG_OP      : lambda x: -x,
}

# Define precedences.
PRECEDENCE = {
    '=' : 0,
    '+' : 1, '-' : 1,
    '*' : 2, '/' : 2, '%' : 2,
    '^' : 4,
    '!' : 5
}
PRECEDENCE.update((f, 3) for f in FUNCTIONS)
               
# Define number of operands for operators and functions
NUM_OPERANDS = {}
NUM_OPERANDS.update((f, 2) for f in OPERATORS)
NUM_OPERANDS.update((f, 1) for f in FUNCTIONS)
NUM_OPERANDS['!'] = 1

# Define associativiy for operators and functions:
#   If '+' is left associative, then 1 + 2 + 3 
#   parses to (1 + 2) + 3. If '+' is right
#   associative then 1 + 2 + 3 parses to 1 + (2 + 3).
LEFT  = -1
RIGHT = 1
ASSOCIATIVITY = {}
ASSOCIATIVITY.update((f, LEFT) for f in OPERATORS)
ASSOCIATIVITY.update((f, RIGHT) for f in FUNCTIONS)
ASSOCIATIVITY['^'] = RIGHT
ASSOCIATIVITY['='] = LEFT