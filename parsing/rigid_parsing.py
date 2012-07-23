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
import string, numbers

def tokenize(expr):
    '''
    Split expr into a list of tokens.
    
    A token can be:
        a. A prefix, infix, or postfix function/operator
        b. A variable or constant
        c. A number (int, float, or complex)
    In cases (a) and (b), the token is an object instantiated using 
    some class in parser_defintions.py.
    
    Raises a SyntaxError if:
        1. An undefined symbol is encountered
        2. There's a misformatted/invalid number
    '''
    
    expr = remove_whitespace(expr)
    result = []
    
    i = 0
    while i < len(expr):
        token = None
        
        # Attempt to read different types of tokens 
        # and construct objects out of them.
        if expr[i] in NUMBER_CHARS:
            token = read_complex_number(expr, i)
            i += len(token)
            token = get_number(token)
        # read a function/operator
        if token == None:
            token = get_from_list(expr, i, OP_CLASS_DICT.keys())
            try:
                token = OP_CLASS_DICT[token]()
                i += len(token)
            except KeyError:
                token = None
        # read a constant
        if token == None:
            token = get_from_list(expr, i, CONST_CLASS_DICT.keys())
            try:
                token = CONST_CLASS_DICT[token]()
                i += len(token)
            except KeyError:
                token = None
        # read a variable or function
        if token == None and expr[i] in string.ascii_letters:
            # try to get a function 'f[x,y,...]'
            token = read_function(expr, i)
            func_obj = get_user_function(token)
            if func_obj != None:
                i += len(token)
                token = func_obj
            else:
                token = Var(expr[i])
                i += 1
        if token == None and expr[i] in ['(', ')']:
            token = expr[i]
            i += 1
        if token == None:
            raise SyntaxError("Unknown/invalid symbol " + repr(expr[i]))
        
        result.append(token)
        
    return result
  
def to_RPN(tokens):
    ''' 
    Convert the tokenized infix expression tokens to a 
    postfix/RPN expression using Dijsktra's Shunting-yard algorithm.
    
    This will raise a SyntaxError for mismatched parentheses.
    '''
    
    output = []
    stack = []
    
    for token in tokens:
        if isinstance(token, GeneralOperator):
            while len(stack) > 0 and isinstance(stack[-1], GeneralOperator):
                if (token.associativity == LEFT and
                    token.precedence <= stack[-1].precedence
                    ):
                    output.append(stack.pop())
                elif (token.associativity == RIGHT and 
                      token.precedence < stack[-1].precedence
                      ):
                    output.append(stack.pop())
                else:  
                    break
            stack.append(token)
        elif (isinstance(token, Constant) or
              isinstance(token, numbers.Number) or 
              isinstance(token, Var) or
              isinstance(token, UserFunction)
              ):
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while len(stack) > 0 and stack[-1] != '(':
                output.append(stack.pop())
            
            if len(stack) == 0 or stack[-1] != '(':
                raise SyntaxError("Mismatched parentheses")
            
            if len(stack) > 0:
                stack.pop()
            if len(stack) > 0 and isinstance(stack[-1], GeneralOperator):
                output.append(stack.pop())
                
    while len(stack) > 0:
        if stack[-1] in ['(', ')']:
            raise SyntaxError("Mismatched parentheses")
        output.append(stack.pop())
            
    return output 

class node(object):
    
    def __init__(self, v = None):
        # copy constructor
        if isinstance(v, node):
            self.value = v.value
            self.children = [node(i) for i in v.children]
        # ordinary constructor
        else:
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

        if replace_constants and isinstance(self.value, Constant):
            self.value = self.value.value
         
        if self.value != '=' and isinstance(self.value, GeneralOperator):
            if operands and all(isinstance(x.value, numbers.Number) for x in operands):   
                self.value = self.value.apply(*[x.value for x in operands])
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
        
        if isinstance(token.value, GeneralOperator):
            if len(stack) < token.value.num_operands:
                raise SyntaxError("Not enough operands for " + repr(token.value))
            
            if token.value.num_operands == 1:    
                token.children.append(stack.pop())
            elif token.value.num_operands == 2:
                r, l = stack.pop(), stack.pop()
                token.children.append(l)
                token.children.append(r)
            stack.append(token)
        elif (isinstance(token.value, Constant) or
              isinstance(token.value, numbers.Number) or
              isinstance(token.value, Var) or
              isinstance(token.value, UserFunction)
              ):
            stack.append(token)
            
    if len(stack) != 1:
        raise SyntaxError("RPN-to-tree conversion failed.")

    return stack.pop()

