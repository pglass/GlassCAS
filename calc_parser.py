####################################################
# Parse an infix expression to a tree.
#   1. Tokenize
#   2. Convert to postfix/RPN
#   3. Construct tree from RPN
# Once we have the tree we can (hopefully) more 
#   easily accomplish more advanced stuff.
#   
# TODO: 
#   [x] Generalize node to have any number of children
#   [x] Implicit multiplication
#   [ ] Support negative numbers/variables
#   [ ] Complex numbers
#   [ ] Functions with arbitrary numbers of operators
#   [ ] Equations
#   [ ] More rigorous testing of current functions
#       - Ensure errors on invalid inputs (ln, sqrt)
#        (do this in the compute function)
#
# Goals:
#   [ ] Algebra
#       - Trig identities
#       - Other useful identities
#   [ ] Equation solving
#   [ ] Sequences, Limits, Series
#   [ ] Derivatives/Integrals
#   [ ] Differential Equations
#
####################################################

import math

WHITESPACE_CHARS = ['\t', '\n', '\x0b', '\x0c', '\r', ' ']
LPARENS = ['(', '[']
RPARENS = [')', ']']
OPERATORS = ['+', '-', '*', '/', '^', '%', '!']
FUNCTIONS = {'cos' : math.cos, 'sin' : math.sin, 'tan' : math.tan,
            'ceil' : math.ceil, 'floor' : math.floor,
            'ln' : math.log, 'log' : math.log10, 'sqrt' : math.sqrt,
            'nroot' : lambda a, b: b ** (1.0/a)}

CONSTANTS = {'e' : math.e, 'pi': math.pi}
                  
NUMBER_CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]

VARIABLES = ["a", "b", "c", "d", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

# Define operator precedences.
# (Determines order of operations in the absence of parentheses)
PRECEDENCE = { '+' : 0, '-' : 0, 
               '*' : 1, '/' : 1, '%' : 1, 
               '^' : 4, '!' : 5}
PRECEDENCE.update((f, 3) for f in FUNCTIONS)
               
# Define number of operands for operators and functions
NUM_OPERANDS = {}
NUM_OPERANDS.update((f, 2) for f in OPERATORS)
NUM_OPERANDS.update((f, 1) for f in FUNCTIONS)
NUM_OPERANDS['!'] = 1
NUM_OPERANDS['nroot'] = 2

# Define associativiy for operators and functions:
#   If '+' is left associative, then 1 + 2 + 3 
#       parses to (1 + 2) + 3. If '+' is right
#       associative then 1 + 2 + 3 parses
#       to 1 + (2 + 3).
LEFT  = -1
NON   = 0
RIGHT = 1
ASSOCIATIVITY = {}
ASSOCIATIVITY.update((f, LEFT) for f in OPERATORS)
ASSOCIATIVITY.update((f, RIGHT) for f in FUNCTIONS)
ASSOCIATIVITY['^'] = RIGHT
                  
def remove_whitespace(expr):
    return "".join(e for e in expr if e not in WHITESPACE_CHARS)

def extract_number(expr, start):
    ''' 
    Grab the number in expression that begins at index start 
    (assuming a number exists there)
    
    This returns a string, not an int or float object.
    
    Raises a SyntaxError if a float has too many decimal points,
    or if the number consists of only decimal points 
    '''
    
    token = expr[start]
    i = start + 1
    
    found_decimal_point = (token == '.')
    while i < len(expr) and expr[i] in NUMBER_CHARS:
        if found_decimal_point and expr[i] == '.':
            raise SyntaxError("Too many decimal points: " + expr[start:])
        elif expr[i] == '.':
            found_decimal_point = True
            
        token += expr[i]
        i += 1
    if token == '.':
        raise SyntaxError("Dangling decimal point: " + 
                  expr[max(0, start - 2) : min(len(expr), start + 2)])
    return token

def get_from_list(expr, start, value_list):
    '''
    Return an identifier beginning at index start,
    where the identifier is something in value_list.
    Returns None if no such identifier is found.
    
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

def insert_times_symbols(tokens):
    '''
    This is called at the end of the tokenize method, and is
    key to supporting implicit multiplication. It only 
    inserts multiplications symbols into the list if a rule
    applies.
   
    We're given a list of tokens for some expression (produced 
    in the tokenize method) and we want to insert multiplication 
    symbols so that parsing works as follows (examples):
        4x     --> 4 * x
        x4     --> x * 4
        4!5    --> 4! * 5
        4xy    --> 4 * x * y
        4pi    --> 4 * pi
        4cos5  --> 4 * cos(5)
        4(3)   --> 4 * (3)
        (3)4   --> (3) * 4
        cos5x  --> cos(5*x)
        cos5*x --> cos(5) * x
        sin5xy*5cos5xy --> sin(5*x*y) * 5cos(5*x*y)
    
    This implies a few rules. Let C be any constant, V be any variable, 
    and N be a number:
        1. {C,V,N}{C,V,N} --> {C,V,N}*{C,V,N}
        2. {C,V,N}(  -->  {C,V,N}*(
           ){C,V,N}  -->  )*{C,V,N}
        3. If F is a unary function:
            {C,V,N} F() --> {C,V,N} * F()
            F(){C,V,N}  --> F() * {C,V,N}
            F{C,V,N}...{C,V,N} --> F({C,V,N} * ... * {C,V,N})
        4. If F is a postfix unary operator (like factorial):
            ()F {C,V,N} --> ()F * {C,V,N}
        5. -{C,V,N,F} --> (-1 * {C,V,N,F})
    
    '''
    
    i = 0
    while i < len(tokens) - 1:
        if (get_number(tokens[i]) or 
            tokens[i] in RPARENS + VARIABLES + CONSTANTS.keys() or
            tokens[i] in OPERATORS and NUM_OPERANDS[tokens[i]] == 1):
            
            token = tokens[i+1]
            if (get_number(token) or
                token in LPARENS + VARIABLES + CONSTANTS.keys() or
                token in FUNCTIONS.keys() and NUM_OPERANDS[token] == 1):
                
                tokens.insert(i+1, "*")
                i += 2
            else:
                i += 1
        elif tokens[i] in FUNCTIONS.keys() and NUM_OPERANDS[tokens[i]] == 1:
            i, n = i+1, i+1
            
            while n < len(tokens) and (get_number(tokens[n]) or 
                    tokens[n] in VARIABLES + CONSTANTS.keys()):
                n += 1
            if n - i > 1:
                tokens[i:n] = ["("] + insert_times_symbols(tokens[i:n]) + [")"]
            i = n
        # elif tokens[i] == '-':
            # if get_number(tokens[i+1]):
                # tokens[i] = "".join(tokens[i:i+2])
                # tokens.pop(i+1)
                # i += 1
            # elif i == 0:
                # tokens[:1] = ['-1', '*']
                # i += 2
            # elif tokens[i-1] == "+":
                # tokens.pop(i-1)
                # i += 1
            # elif tokens[i-1] == "-":
                # tokens.pop(i)
                # tokens.pop(i-1)
            # elif not get_number(tokens[i+1]):
                # tokens[i-1: i+1] = ["-1", "*"]
                
                
        else:
            i += 1
    return tokens
    
def tokenize(expr):
    '''
    Split expr into a list of tokens, wehre 
    all tokens are left as strings.
    
    A token is something in OPERATORS, FUNCTIONS,
    VARIABLES, CONSTANTS, or a positive number.
    
    Raises a SyntaxError if:
    1. An undefined symbol is encountered, like '$' or '@'
    2. There's a misformatted/invalid number, like '555.232.21'
    '''
    
    expr = remove_whitespace(expr)
    result = []
    
    i = 0
    while i < len(expr):
        token = expr[i]
        
        if token in NUMBER_CHARS:
            token = extract_number(expr, i)
        elif token in [f[0] for f in FUNCTIONS]:            
            token = get_from_list(expr, i, FUNCTIONS)
            
            # if not a function, we may have a constant or a variable
            if token == None:
                if expr[i] in [c[0] for c in CONSTANTS]:
                    token = get_from_list(expr, i, CONSTANTS)
                elif expr[i] in VARIABLES:
                    token = expr[i]
                
            if token == None:
                raise SyntaxError("Unknown/invalid symbol " + `token`)  
        elif token in [c[0] for c in CONSTANTS]:
            token = get_from_list(expr, i, CONSTANTS)
        
            if token == None and expr[i] in VARIABLES:
                token = expr[i]
            elif token == None:
                raise SyntaxError("Unknown/invalid symbol " + `expr[i]`)
        elif token in LPARENS + RPARENS + OPERATORS:
            pass
        elif token in VARIABLES:
            pass
        else:
            raise SyntaxError("Unknown/invalid symbol " + `token`)
                
        result.append(token)
        i += len(token)
        
    return insert_times_symbols(result)
   
def get_number(value):
    ''' 
    Return a float or long if value is or represents a number.
    Otherwise, return None.
    '''
    
    if value.__class__ in [int, float, long]:
        return value
    
    try:
        return long(value)
    except ValueError:
        pass
    
    try:
        return float(value)
    except ValueError:
        pass
        
    return None
 
def to_RPN(expr):
    ''' 
    Convert an infix expression to an RPN expression
    using Dijsktra's Shunting-yard algorithm.
    
    This will raise any SyntaxError raised in the tokenization step,
    and will raise an additional SyntaxError for mismatched parentheses.
    '''
    
    tokens = tokenize(expr)
    output = []
    stack = []
    
    for token in tokens:
        if get_number(token) or token in VARIABLES or token in CONSTANTS:
            output.append(token)
        elif token in OPERATORS + FUNCTIONS.keys():
            while len(stack) > 0 and stack[-1] in OPERATORS + FUNCTIONS.keys():
                if (ASSOCIATIVITY[token] == LEFT and
                        PRECEDENCE[token] <= PRECEDENCE[stack[-1]]):
                    output.append(stack.pop())
                        
                elif (ASSOCIATIVITY[token] == RIGHT and 
                        PRECEDENCE[token] < PRECEDENCE[stack[-1]]):
                    output.append(stack.pop())
                else:  
                    break
            stack.append(token)
        elif token in LPARENS:
            stack.append(token)
        elif token in RPARENS:
            while len(stack) > 0 and stack[-1] not in LPARENS:
                output.append(stack.pop())
            
            if len(stack) == 0 or stack[-1] not in LPARENS:
                raise SyntaxError("Mismatched parentheses")
            
            if len(stack) > 0:
                stack.pop()
            if len(stack) > 0 and stack[-1] in FUNCTIONS:
                output.append(stack.pop())
                
    while len(stack) > 0:
        if stack[-1] in LPARENS + RPARENS:
            raise SyntaxError("Mismatched parentheses")
        output.append(stack.pop())
            
    return output 

def compute(function, operands):
    '''
    Apply the function to operands and return the result.
    
    Raises SyntaxErrors for unknown functions, and for too few operands.
    Raises ValueErrors if the operand is of the wrong type.
    '''

    if function not in OPERATORS + FUNCTIONS.keys():
        raise SyntaxError("Unkown function " + function)
    if NUM_OPERANDS[function] < len(operands):
        raise SyntaxError("Only " + str(NUM_OPERANDS[function]) + " operands for " + str(function))
    
    if function in FUNCTIONS:
        f = FUNCTIONS[function]
        if NUM_OPERANDS[function] == 1:
            return f(operands[0])
        elif NUM_OPERANDS[function] == 2:
            return f(operands[0], operands[1])
    
    if function == '+':
        return operands[0] + operands[1]
    if function == '-':
        return operands[0] - operands[1]
    if function == '*':
        return operands[0] * operands[1]
    if function == '/':
        return float(operands[0]) / operands[1]
    if function == '%':
        return operands[0] % operands[1]
    if function == '^':
        return operands[0] ** operands[1]
    if function == '!':
        if operands[0].__class__ == float:
            raise ValueError("Factorial requires an integer")
            
        return math.factorial(operands[0])
 
class node:
    
    def __init__(self, value = None):
        self.value = get_number(value)
        if self.value == None:
            self.value = value
        self.children = []
        
    def __str__(self):
        ''' 
        Returns a string representation of the tree structure 
        '''
        result = ''
                
        result += str(self.value)
        result += "\n"
        
        for child in reversed(self.children):
            for line in str(child).split("\n"):
                result += "  " + line + "\n"
        return result[:-1]
        
    def reduce(self, replace_constants = False):
        ''' 
        Calculates and replaces all obvious constant expressions.
        
        replace_constants = True will replace constant identifiers 
        with their numeric values, e.g., 'e' becomes 2.7182818...
        replace_constants = False will leave 'e' in the tree.
        '''
        operands = []
        for child in self.children:
            child.reduce(replace_constants)
            operands.append(child)

        if replace_constants and self.value in CONSTANTS.keys():
            self.value = CONSTANTS[self.value]
         
        if self.value in OPERATORS + FUNCTIONS.keys():
            if operands and all(get_number(x.value) for x in operands):    
                self.value = compute(self.value, [x.value for x in operands])
                for c in operands:
                    self.children.remove(c)
        

def to_tree(expr):
    ''' 
    Parse expr to a tree. This returns the root node of the tree.
    
    First, expr is converted to postfix/RPN using to_RPN. This detects 
    most poorly formatted inputs (SyntaxError), and takes care of order 
    of operations and parenthetical nesting issues.
    
    Then conversion to a tree only requires knowing the number of operands
    for each operator:
        - Pass over the RPN expression. 
        - Push numbers to a stack as we encounter them. 
        - When we see a function/operator, we will have just pushed
          its operands to the stack. Pop off the required number of
          operands and form a tree with the operator as the root and
          operands as leaves. Push this tree onto the stack.
    By the end, the stack should have only one node, which is the root of
    the tree representing the expression.

    In addition to SyntaxErrors raised by to_RPN, this may
    raise additional SyntaxErrors if there are not enough operands
    for an operator/function, or 
    '''
    rpn_expr = [node(i) for i in to_RPN(expr)]
    
    stack = []
    while len(rpn_expr) > 0:
        token = rpn_expr.pop(0)
        
        if get_number(token.value) or str(token.value) in VARIABLES + CONSTANTS.keys():
            stack.append(token)
        elif token.value in OPERATORS + FUNCTIONS.keys():
            if len(stack) < NUM_OPERANDS[token.value]:
                raise SyntaxError("Not enough operands for " + `token.value`)
            
            if NUM_OPERANDS[token.value] == 1:    
                token.children.append(stack.pop())
            elif NUM_OPERANDS[token.value] == 2:
                r, l = stack.pop(), stack.pop()
                token.children.append(l)
                token.children.append(r)
            stack.append(token)
            
    if len(stack) != 1:
        raise SyntaxError("RPN-to-tree conversion failed.")

    return stack.pop()
           
if __name__ == '__main__':
    import sys
    
    replace_constants = False
    if len(sys.argv) > 1:
        replace_constants = True
    
    while True:
        uin = raw_input('>>')
        if uin in 'xxxxxxxx':
            break
        try:
            tmp = to_tree(uin)
            print tmp
            tmp.reduce(replace_constants)
            print tmp
        except (ZeroDivisionError, SyntaxError, ValueError), se:
            print "error:", se
            # raise se
        