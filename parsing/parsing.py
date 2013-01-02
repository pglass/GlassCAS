'''
parsing.py

This defines a Parser class, as well as unbound methods for optionally
supporting other syntax, like implicit multiplication 
'''

from parsing.node import node
from parsing.parser_definitions import *
from parsing.parser_util import *
import numbers

class Parser(object):
    
    def __init__(self):
        self.symbol_table = {}
        
    def parse(self, input_string, update_symbol_table = False):
      '''
      This parses input_string and returns the syntax tree.

      By default, this does not update this Parser's symbol_table.
      '''
      tokens = apply_transformations(self.tokenize(input_string))
      rpn = self.to_rpn(tokens)
      tree = self.to_tree(rpn)
      if update_symbol_table:
        self.update_symbol_table(tree)
      return tree

    def tokenize(self, expr):
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
            
            # read a number
            if expr[i] in NUMBER_CHARS:
                token = read_complex_number(expr, i)
                i += len(token)
                token = get_number(token)
            # read a predefined operator/function
            if token == None:
                check = get_from_list(expr, i, OP_CLASS_DICT.keys())
                
                if check != None:
                    i += len(check)
                    if check in self.symbol_table:
                        token = self.symbol_table[check]
                    else:
                        token = OP_CLASS_DICT[check]()
            # read a constant
            if token == None:
                check = get_from_list(expr, i, CONST_CLASS_DICT.keys())
                
                if check != None:
                    i += len(check)
                    if check in self.symbol_table:
                        token = self.symbol_table[check]
                    else:
                        token = CONST_CLASS_DICT[check]()
            # read a variable or user-defined function
            if token == None and expr[i] in string.ascii_letters:
            
                # try to read 'f[x,y,...]'
                check = read_function(expr, i)
                func_obj = get_user_function(check)
                
                if check == None and func_obj == None:
                    token = self.symbol_table.get(expr[i])
                    
                    if token == None:
                        token = Var(expr[i])
                    i += 1
                # otherwise, we have function
                elif func_obj != None:
                    token = func_obj
                    i += len(check)
            # read parens or arg delimiter
            if token == None and expr[i] in ['(', ')', ARG_DELIM]:
                token = expr[i]
                i += 1
            if token == None:
                raise SyntaxError("Unknown/invalid symbol " + repr(expr[i]))
            
            result.append(token)
        
        return result
    
    def to_rpn(self, tokens):
        ''' 
        Convert the tokenized infix expression tokens to a 
        postfix/RPN expression using Dijsktra's Shunting-yard algorithm.
        
        This is adapted from http://en.wikipedia.org/wiki/Shunting-yard_algorithm
        with modifcations to support postfix and prefix operators.
        
        This will raise a SyntaxError for mismatched parentheses.
        '''
        
        output = []
        stack = []
        
        for token in tokens:
            if isinstance(token, UserFunction) and token.value == None:
                output.append(token)
            elif isinstance(token, GeneralOperator):
                while len(stack) > 0 and isinstance(stack[-1], GeneralOperator):
                    if (isinstance(token, InfixOp) and 
                            ((token.associativity == LEFT and 
                             token.precedence <= stack[-1].precedence) or 
                             token.precedence < stack[-1].precedence
                            )
                        ):
                        output.append(stack.pop())
                    elif isinstance(stack[-1], PostfixOp):
                        output.append(stack.pop())
                    elif (isinstance(token, PostfixOp) and
                        isinstance(stack[-1], InfixOp) and 
                        token.precedence < stack[-1].precedence
                        ):
                        output.append(stack.pop())
                    else:  
                        break
                stack.append(token)
            elif isinstance(token, Var) or isinstance(token, numbers.Number):
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
                if len(stack) > 0 and isinstance(stack[-1], PrefixOp):
                    output.append(stack.pop())
                    
        while len(stack) > 0:
            if stack[-1] in ['(', ')']:
                raise SyntaxError("Mismatched parentheses")
            output.append(stack.pop())
                
        return output 

    def to_tree(self, rpn_tokens):
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
        
        rpn_nodes = [node(i) for i in rpn_tokens]
        
        if len(rpn_nodes) == 0:
            return node("")
        
        stack = []
        while len(rpn_nodes) > 0:
            token = rpn_nodes.pop(0)
            
            if (isinstance(token.value, UserFunction) and 
                (token.value.value == None or token.value.num_operands == 0)
                ):
                stack.append(token)
            elif isinstance(token.value, GeneralOperator):
                if len(stack) < token.value.num_operands:
                    raise SyntaxError("Not enough operands for " + repr(token.value))
                
                tmp = []
                for i in range(token.value.num_operands):
                    tmp.append(stack.pop())
                
                tmp.reverse()
                token.children += tmp
                    
                stack.append(token)
            elif (isinstance(token.value, Var) or
                  isinstance(token.value, numbers.Number)
                  ):
                stack.append(token)
            
        if len(stack) != 1:
            # could use more sophisticated feedback here
            raise SyntaxError("RPN-to-tree conversion failed: %s" % stack)

        return stack.pop()
    
    def update_symbol_table(self, root_node):
        if isinstance(root_node.value, DefinedAsOp):
            if len(root_node.children) > 0:
                left = root_node.children[0]
                right = root_node.children[1]
                if (isinstance(left.value, UserFunction) or
                    isinstance(left.value, Var)):
                    self.symbol_table[left.value.name] = left.value
                    left.value.value = right
                else:
                    raise SyntaxError("Cannot assign to literal %s" % left.value)

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
        if (isinstance(tokens[i], numbers.Number) or 
            tokens[i] == ')' or
            isinstance(tokens[i], Var) or
            isinstance(tokens[i], Constant) or
            isinstance(tokens[i], PostfixOp)
            ):
            
            token = tokens[i+1]
            
            # check for things on the right side
            if (isinstance(token, numbers.Number) or
                token == '(' or
                isinstance(token, Var) or
                isinstance(token, Constant)
                ):
                
                tokens.insert(i+1, ImplicitMultOp())
                i += 2
            elif isinstance(token, PrefixOp):
                tokens.insert(i+1, TimesOp())
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
    Decorator intended for functions f(tokens, i) that returns the change in len(tokens)
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
    if not 0 <= i < len(tokens) or tokens[i] != SubOp():
        return
    
    # handle minus sign at the front
    if i == 0:
        if tokens[i:i+2] == [SubOp(), SubOp()]:
            tokens[i:i+2] = []
        else:
            tokens[i] = NegationOp()
    # handle '+-' occurrences
    elif tokens[i-1:i+1] == [PlusOp(), SubOp()]:
        if i-1 == 0:
            tokens[i-1:i+1] = [NegationOp()]
        else:
            tokens[i-1:i+1] = [SubOp()]
    # handle '--' occurrences
    elif tokens[i-1:i+1] == [SubOp(), SubOp()]:
        tokens[i-1:i+1] = [PlusOp()]
    # handle '<LHS> OP - <RHS>' occurrences
    elif (tokens[i-1] == '(' or
          isinstance(tokens[i-1], InfixOp) or
          isinstance(tokens[i-1], PrefixOp)
          ):
        tokens[i] = NegationOp()

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
   
