'''
rigid_parsing.py -- parse an infix expression to a tree.
This happens in 3 steps:
  1. Tokenize
  2. Convert to postfix/RPN
  3. Construct tree object from RPN

This module also includes the node class which is used to form
a tree out of the parse input.

The module is 'rigid' in that every operator, variable, constant
and function identifier has to be unique.
'''

from parser_definitions import *
from parser_util import *

def tokenize(expr):
    '''
    Split expr into a list of tokens, where all tokens are left as strings.
    
    A token is something in OPERATORS, FUNCTIONS, VARIABLES, CONSTANTS,
    or a (positive) number.
    
    Raises a SyntaxError if:
        1. An undefined symbol is encountered, like '$' or '@'
        2. There's a misformatted/invalid number, like '555.232.21'
    '''
    
    expr = remove_whitespace(expr)
    result = []
    
    i = 0
    while i < len(expr):
        token = None
        
        if expr[i] in NUMBER_CHARS:
            token = read_complex_number(expr, i)
        if token == None:
            token = get_from_list(expr, i, FUNCTIONS)
        if token == None:
            token = get_from_list(expr, i, CONSTANTS)
        if token == None and expr[i] in VARIABLES + LPARENS + RPARENS + OPERATORS:
            token = expr[i]
        
        if token == None:
            raise SyntaxError("Unknown/invalid symbol " + `expr[i]`)
                
        result.append(token)
        i += len(token)
        
    return result
 
def to_RPN(tokens):
    ''' 
    Convert the tokenized infix expression tokens to an RPN expression
    using Dijsktra's Shunting-yard algorithm.
    
    This will raise a SyntaxError for mismatched parentheses.
    '''
    
    output = []
    stack = []
    
    for token in tokens:
        if get_number(token) != None or token in VARIABLES + CONSTANTS.keys():
            output.append(token)
        elif token in OPERATORS + FUNCTIONS.keys():
            while len(stack) > 0 and stack[-1] in OPERATORS + FUNCTIONS.keys():
                if (ASSOCIATIVITY[token] == LEFT and
                    PRECEDENCE[token] <= PRECEDENCE[stack[-1]]
                   ):
                    
                    output.append(stack.pop())
                elif (ASSOCIATIVITY[token] == RIGHT and 
                      PRECEDENCE[token] < PRECEDENCE[stack[-1]]
                     ):
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
    
    Raises a SyntaxError for unknown functions, and for too few operands.
    Raises other errors if the operand is an invalid input. These bubble up
        from Python's implementations of the functions/operators, and include:
            ValueError (ex: "(-4)!")
            ZeroDivisionError (ex: "4/0")
            TypeError (ex: "floor(1+j)")
            (I need to find and list all possible error types here...)
    '''

    if function not in OPERATORS + FUNCTIONS.keys():
        raise SyntaxError("Unkown function " + function)
    
    if function in FUNCTIONS:
        f = FUNCTIONS[function]
        if NUM_OPERANDS[function] == 1:
            return f(operands[0])
        elif NUM_OPERANDS[function] == 2:
            return f(operands[0], operands[1])
    
    if function == '+':
        return reduce(lambda a, b: a + b, operands)
    if function == '-':
        return operands[0] - operands[1]
    if function in ['*', IMPLICIT_MULT]:
        return reduce(lambda a, b: a * b, operands)
    if function == '/':
        return float(operands[0]) / operands[1]
    if function == '%':
        return operands[0] % operands[1]
    if function == '^':
        return operands[0] ** operands[1]
    if function == '!':
        return math.factorial(operands[0])
 
class node(object):
    
    def __init__(self, v = None):
        # copy constructor
        if isinstance(v, node):
            self.value = v.value
            self.children = [node(i) for i in v.children]
        # ordinary constructor
        else:
            self.value = get_number(v)
            if self.value == None:
                self.value = v
            self.children = []

    def __str__(self):
        '''
        Produce a string representation of this tree's structure
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
        Computes the value of this tree.
        
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
         
        if self.value != '=' and self.value in OPERATORS + FUNCTIONS.keys():
            if operands and all(get_number(x.value) != None for x in operands):    
                self.value = compute(self.value, [x.value for x in operands])
                for c in operands:
                    self.children.remove(c)

def to_tree(rpn_expr):
    ''' 
    Parse rpn_expr to a tree where rpn_expr is some list of tokens
    in reverse polish notation, as is returned by to_RPN. This returns 
    the root node of the tree.
        
    Then conversion to a tree only requires knowing the number of operands
    for each operator:
        - Push numbers to a stack as we encounter them. 
        - When we see a function/operator, pop off the required number of
          operands and form a tree with the operator as the root and
          operands as leaves. Push this tree onto the stack.
    By the end, the stack should have only one node, which is the root of
    the tree representing the expression.

    This will raise a SyntaxError if there are not enough operands
    for an operator/function, or if it otherwise fails to parse 
    the input.
    '''
    
    
    rpn_nodes = [node(i) for i in rpn_expr]
    
    if len(rpn_nodes) == 0:
        return node("")
    
    stack = []
    while len(rpn_nodes) > 0:
        token = rpn_nodes.pop(0)
        
        if (get_number(token.value) != None or
                str(token.value) in VARIABLES + CONSTANTS.keys()):
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
 
