'''
parser_definitions.py
'''

import cmath, math

WHITESPACE_CHARS = list("\t\n\x0b\x0c\r ")
LPARENS = list("(")
RPARENS = list(")")

REAL_NUMBER_CHARS = list("0123456789.")
NUMBER_CHARS = REAL_NUMBER_CHARS + ["j"] # Use 'j' as sqrt(-1)

CONSTANTS = {
    'e' : cmath.e,
    'pi': cmath.pi
}

# Define valid single-letter variables
# (notice that constants and variables cannot overlap)
VARIABLES = list("abcd" + "fghi" + "klmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

# operator to represent implicit multiplication
IMPLICIT_MULT = "@"

# negation operator (different than subtraction)
NEG_OP = '`'

PREFIX_FUNCTION_MAP = {
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

INFIX_FUNCTIONS = [
    "+", 
    "-", 
    "*",
    IMPLICIT_MULT,
    "/", 
    "^", # exponentiation
    "%", # modulus
    "=", # equation operator (treating this as a function simplifies parsing)  
]

POSTFIX_FUNCTION_MAP = {
    '!'         : math.factorial,
}

ALL_FUNCTIONS = (PREFIX_FUNCTION_MAP.keys() +
                 INFIX_FUNCTIONS +
                 POSTFIX_FUNCTION_MAP.keys())

# Define operator precedences.
PRECEDENCE = {
    '=' : 0,
    '+' : 1,
    '-' : 1,
    '*' : 2,
    '/' : 2,
    '%' : 2,
    IMPLICIT_MULT : 3.5,
    '^' : 4,
    '!' : 5
}
PRECEDENCE.update((f, 3) for f in PREFIX_FUNCTION_MAP.keys())
               
# Define number of operands for operators and functions
NUM_OPERANDS = {}
NUM_OPERANDS.update((f, 2) for f in INFIX_FUNCTIONS)
NUM_OPERANDS.update((f, 1) for f in PREFIX_FUNCTION_MAP.keys())
NUM_OPERANDS.update((f, 1) for f in POSTFIX_FUNCTION_MAP.keys())

# Define associativiy for operators and functions:
#   If '+' is left associative, then 1 + 2 + 3 
#   parses to (1 + 2) + 3. If '+' is right
#   associative then 1 + 2 + 3 parses to 1 + (2 + 3).
LEFT  = -1
RIGHT = 1
ASSOCIATIVITY = {}
ASSOCIATIVITY.update((f, LEFT) for f in INFIX_FUNCTIONS)
ASSOCIATIVITY.update((f, LEFT) for f in POSTFIX_FUNCTION_MAP.keys())
ASSOCIATIVITY.update((f, RIGHT) for f in PREFIX_FUNCTION_MAP.keys())
ASSOCIATIVITY['^'] = RIGHT
ASSOCIATIVITY['='] = LEFT