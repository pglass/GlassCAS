'''
rigid_parsing.py -- parse an infix expression to a tree.

This happens in steps:
  1. Tokenize
  2. Convert to tree:
        a. Convert to postfix/RPN
        b. Construct a tree from the RPN

This module also includes the node class which is used
to construct the tree (probably should be move to its own module)

The module is 'rigid' in that every operator, variable, constant
and function identifier has to be unique.
'''

from parsing.parser_definitions import *
from parsing.parser_util import *

def tokenize(expr):
    '''
    Split expr into a list of tokens, where all tokens are left as strings.
    
    A token is something in PREFIX_FUNCTION_MAP, INFIX_FUNTIONS.
    POSTFIX_FUNCTION_MAP, VARIABLES, or CONSTANTS, or a token
    can be a (positive) number.
    
    Raises a SyntaxError if:
        1. An undefined symbol is encountered
        2. There's a misformatted/invalid number
    '''
    
    expr = remove_whitespace(expr)
    result = []
    
    i = 0
    while i < len(expr):
        token = None
        
        if expr[i] in NUMBER_CHARS:
            token = read_complex_number(expr, i)
        if token == None:
            token = get_from_list(expr, i, PREFIX_FUNCTION_MAP.keys())
        if token == None:
            token = get_from_list(expr, i, INFIX_FUNCTIONS)
        if token == None:
            token = get_from_list(expr, i, POSTFIX_FUNCTION_MAP.keys())
        if token == None:
            token = get_from_list(expr, i, CONSTANTS)
        if token == None and expr[i] in VARIABLES + LPARENS + RPARENS:
            token = expr[i]
        if token == None:
            raise SyntaxError("Unknown/invalid symbol " + repr(expr[i]))
                
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
        if get_number(token) != None or token in VARIABLES + list(CONSTANTS.keys()):
            output.append(token)
        elif token in ALL_FUNCTIONS:
            while len(stack) > 0 and stack[-1] in ALL_FUNCTIONS:
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
            if len(stack) > 0 and stack[-1] in PREFIX_FUNCTION_MAP.keys():
                output.append(stack.pop())
                
    while len(stack) > 0:
        if stack[-1] in LPARENS + RPARENS:
            raise SyntaxError("Mismatched parentheses")
        output.append(stack.pop())
            
    return output 

def to_RPN_debug(tokens):
    ''' 
    Convert the tokenized infix expression tokens to an RPN expression
    using Dijsktra's Shunting-yard algorithm. 
    
    This will raise a SyntaxError for mismatched parentheses.
    '''
    
    output = []
    stack = []
    
    for token in tokens:
        print("\nSEE {0}".format(token))
        if get_number(token) != None or token in VARIABLES + CONSTANTS.keys():
            print("push {0} to output".format(token))
            output.append(token)
        elif token in ALL_FUNCTIONS:
            print("push operators/functions from stack to output")
            while len(stack) > 0 and stack[-1] in ALL_FUNCTIONS:
                if (ASSOCIATIVITY[token] == LEFT and
                    PRECEDENCE[token] <= PRECEDENCE[stack[-1]]
                    ):
                    
                    tmp = stack.pop()
                    print("  push {0} to output".format(tmp))
                    output.append(tmp)
                elif (ASSOCIATIVITY[token] == RIGHT and 
                      PRECEDENCE[token] < PRECEDENCE[stack[-1]]
                      ):

                    tmp = stack.pop()
                    print("  push {0} to output".format(tmp))
                    output.append(tmp)
                else:  
                    break
            print("push {0} to stack".format(token))
            stack.append(token)
        elif token in LPARENS:
            print("push {0} to stack".format(token))
            stack.append(token)
        elif token in RPARENS:
            print("see {0}, move all not LPARENS to stack".format(token))
            while len(stack) > 0 and stack[-1] not in LPARENS:
                tmp = stack.pop()
                print("  push {0} to stack".format(token))
                output.append(tmp)
            
            if len(stack) == 0 or stack[-1] not in LPARENS:
                raise SyntaxError("Mismatched parentheses")
            
            if len(stack) > 0:
                stack.pop()
            if len(stack) > 0 and stack[-1] in PREFIX_FUNCTIONS_MAP.keys():
                output.append(stack.pop())
        print("stack: {0}".format(stack))
        print("output: {0}".format(output))
        
    print("moving all remaining on stack to output")
    while len(stack) > 0:
        if stack[-1] in LPARENS + RPARENS:
            raise SyntaxError("Mismatched parentheses")
        tmp = stack.pop()
        print("  push {0} to output".format(tmp))
        output.append(tmp)

    print("stack: {0}".format(stack))
    print("output: {0}".format(output))
            
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

    if function not in ALL_FUNCTIONS:
        raise SyntaxError("Unkown function " + function)
    
    if function in PREFIX_FUNCTION_MAP.keys():
        f = PREFIX_FUNCTION_MAP[function]
        if NUM_OPERANDS[function] == 1:
            return f(operands[0])
        elif NUM_OPERANDS[function] == 2:
            return f(operands[0], operands[1])
    
    if function == '+':
        return sum(operands)
    if function == '-':
        return operands[0] - operands[1]
    if function in ['*', IMPLICIT_MULT]:
        prod = 1
        for val in operands:
            prod *= val
        return prod
        # return reduce(lambda a, b: a * b, operands)
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

    def __repr__(self):
        '''
        Return a string representation of this tree in RPN.
        
        This is used for testing.
        '''
        
        result = ''
        
        for child in self.children:
            result += repr(child) + " "
                    
        return result + str(self.value)
          
    def __str__(self):
        '''
        Produce a string representation of this tree's structure.
        '''
        
        result = ''
                
        result += str(self.value)
        result += "\n"
        
        for child in reversed(self.children):
            for line in str(child).split("\n"):
                result += "  " + line + "\n"
        return result[:-1]
    
    def normalize(self):
        '''
        Attempt to produce a canonical form.
        '''
        
        
        if len(self.children) == 0:
            return
        
        if self.value == '-':
            assert len(self.children) == 2
            self.value = '+'
            tmp = node(NEG_OP)
            tmp.children.append(self.children[1])
            self.children[1] = tmp
            self.children.sort()
        elif self.value == '*':
            assert len(self.children) == 2
            
            other, child = self.children
            other.normalize()
            child.normalize()
            
            if len(self.children[0].children) > len(self.children[1].children):
                other, child = child, other
                
            new_children = []
            for c in child.children:
                tmp = node('*')
                tmp.children.append(other)
                tmp.children.append(c)
                tmp.children.sort()
                new_children.append(tmp)
                
            if len(new_children) > 0:
                self.value = '+'
                self.children = new_children

        for child in self.children:
            child.normalize()
        
        i = 0
        while i < len(self.children):
        # for i in xrange(len(self.children)):
            
            child = self.children[i]
            # convert `(...) to -1 * (...)
            if child.value == NEG_OP:
                new_node = node('*')
                new_node.children.append(node(-1))
                new_node.children.append(child.children[0])
                self.children[i] = new_node
            
            elif child.value == '+':
                if self.value == '+':
                    for c in child.children:
                        self.children.append(c)
                    self.children.pop(i)
                    self.children.sort()
                
            i += 1
        
        self.children.sort()
                        
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
         
        if self.value != '=' and self.value in ALL_FUNCTIONS:
            if operands and all(get_number(x.value) != None for x in operands):    
                self.value = compute(self.value, [x.value for x in operands])
                for c in operands:
                    self.children.remove(c)

    def __cmp__(self, other):
        '''
        This does a comparison based upon the string represntation
        of the trees and is needed for sorting operands to approach
        a canonical form.
        '''
        if other == None:
            return 1
        if str(self.value) == str(other.value):
            if self.value == '*':
                mine = "".join(map(str, self.children))
                his = "".join(map(str, other.children))
                if mine > his:
                    return 1
                elif mine < his:
                    return -1
                else:
                    return 0
            return 0
        if str(self.value) > str(other.value):
            return 1
        return -1
           
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
        
        if get_number(token.value) != None:
            stack.append(token)
        elif str(token.value) in VARIABLES + list(CONSTANTS.keys()):
            stack.append(token)
        elif token.value in ALL_FUNCTIONS:
  
            if len(stack) < NUM_OPERANDS[token.value]:
                raise SyntaxError("Not enough operands for " + repr(token.value))
            
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
