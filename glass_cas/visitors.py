from .parsing.parser_definitions import *
from .expression_types import *
import numbers

class Visitor(object):
    ''' Defines the Visitor interface '''

    def __init__(self):
        pass

    def visit(self, n):
        ''' n should be a node '''
        pass


class Printer(Visitor):

    def __init__(self, rpn_mode = False):
        '''
        If rpn_mode is True, this it will print out as RPN.
          otherwise, you'll get a tree-like representation
        '''

        self.rpn_mode = rpn_mode

    def visit(self, n, depth = 0):
        '''
        Return a representation of the tree at node n, as a string.

        depth is used to keep track of indentation when printing as a tree.
        '''

        result = ''

        if not self.rpn_mode:
            result += ("  " * depth)
            result += str(n.value)
            result += "\n"

        for child in n.children:
            result += self.visit(child, depth = depth + 1)

        if self.rpn_mode:
            result += str(n.value)
            result += " "

        return result

class Reducer(Visitor):

    def __init__(self, replace_constants = False):
        self.replace_constants = replace_constants

    def visit(self, n):
        '''
        Computes the value of the tree at node n.

        replace_constants = True will replace constant identifiers
        with their numeric values, e.g., 'e' becomes 2.7182818...
        replace_constants = False will leave 'e' in the tree.
        '''
        
        result_node = n.copy(recursive = False)
        for child in n.children:
            result_node.children.append(self.visit(child))

        # replace a Constant object with an explicit number (int/float/complex)
        if self.replace_constants and isinstance(n.value, Constant):
            result_node.value = n.value.value

        # DefinedAsOp means a variable/function is being defined -- handle elsewhere.
        # EqualsOp is an equation, which we can't yet solve.
        if (isinstance(result_node.value, DefinedAsOp) or
            isinstance(result_node.value, EqualsOp)
            ):
            return result_node

        elif isinstance(result_node.value, UserFunction):
            # UserFunction.apply returns a *node*, even if it evaluates to a number
            reduced_node = result_node.value.apply(*[x.value for x in result_node.children])
            if reduced_node != None:
                result_node = reduced_node

        elif isinstance(result_node.value, ExpandOp):
            return result_node.value.apply(*result_node.children)
        elif isinstance(result_node.value, GeneralOperator):
            # We can reduce this tree if all children were reduced to a number.
            if all(isinstance(x.value, numbers.Number) for x in result_node.children):
                reduced_value = result_node.value.apply(*[x.value for x in result_node.children])
                if reduced_value != None:
                    result_node.value = reduced_value
                    result_node.children.clear()


        return result_node

class Replacer(Visitor):

    def __init__(self, symbol, expr):
        '''
        Instantiate this Replacer so that every occurrence of
        symbol is replaced with expr

        expr should be a node.
        '''
        self.symbol = symbol
        self.expr = expr

    def visit(self, n):
        # TODO: this needs to be tested

        result_node = n.copy(recursive = False)

        if str(n.value) == str(self.symbol):
            result_node = n.copy(self.expr)
        else:
            for child in n.children:
                result_node.children.append(self.visit(child))

        return result_node

class Recognizer(object):
    '''
    The purpose of this class is to be able to tell you what kind of 
    expression a particular tree represents.
    
    Practicality?
      1. This will work for a lot of basic forms, which is good.
    
      2. I'm basically classifying mathematical expressions, but
         it's not always clear what the type is. Ex:
            e^x + log(x) = x^2
         It may turn out that there are no solutions to self equation,
         but we could still give it a type. Maybe:
            EquationExpr[ExpLogCombExpr[Var(x)], PolynomialExpr[Var(x), degree = 2]]
         I'm not really sure how useful the above would be, except that
         we could rule out many methods of solving the equation.
    
         But if there's no standard classification for a particular expression,
         then I probably don't know how to solve it anyway.
    
      3. Ideally, we would be allowed to find the type by manipulating
         the tree however we want, but the recognizer cannot be performance
         prohibitive.
    
    NOTES:
      -- It takes some work supporting more expression types.
         For N unique operators and M different expression types, there
         are have M*N*M ways to combine the expressions, so making a new 
         expression type involves updating the resolve method for all other 
         types. The code is mostly just hundreds of conditionals checking which 
         combination we were given.
    '''

    def __init__(self, assign_types = False):
        '''
        If assign_types is True, then this will set n.expr_type
            to the each node n's determined type.
        '''
        self.assign_types = assign_types

    def visit(self, n):
        result = UnknownExpr()
        if isinstance(n.value, EqualsOp):
            left = self.visit(n.children[0])
            right = self.visit(n.children[1])
            result = EquationExpr(left, right)
        elif isinstance(n.value, DefinedAsOp):
            result = DefinedAsExpr()
        elif isinstance(n.value, InfixOp):
            left = self.visit(n.children[0])
            right = self.visit(n.children[1])
            result = left.resolve(n.value, right)
        elif isinstance(n.value, numbers.Number):
            result = ConstantExpr(n.value)
        elif isinstance(n.value, Constant):
            result = ConstantExpr(n.value.value)
        elif isinstance(n.value, Var):
            result = PolynomialExpr(Var(n.value), 1)

        if self.assign_types:
            n.expr_type = result

        return result

class Expander(Visitor):
    
    is_plus_or_minus = lambda c: isinstance(c, PlusOp) or isinstance(c, SubOp)

    def visit(self, n):
        # This works decently... It's slow though.
        # there's some extra copying in distribute and map.

        result = None

        # we assume the tree is binary at all +-*/^ nodes
        if isinstance(n.value, TimesOp):
            if Expander.is_plus_or_minus(n.children[0].value):
                if Expander.is_plus_or_minus(n.children[1].value):
                    result = self.distribute(n.children[0], n.children[1], n.value, left_distr = True)
                else:
                    result = self.distribute(n.children[1], n.children[0], n.value, left_distr = False)

                for i in range(len(result.children)):
                    result.children[i] = self.visit(result.children[i])
            elif Expander.is_plus_or_minus(n.children[1].value):
                result = self.distribute(n.children[0], n.children[1], n.value, left_distr = True)
            
                for i in range(len(result.children)):
                    result.children[i] = self.visit(result.children[i])
        elif isinstance(n.value, DivideOp):
            if Expander.is_plus_or_minus(n.children[0].value):
                result = self.distribute(n.children[1], n.children[0], n.value, left_distr = False)
                
                for i in range(len(result.children)):
                    result.children[i] = self.visit(result.children[i])
        elif isinstance(n.value, NegationOp):
            
            result = n.copy(recursive = False)
            for child in n.children:
                result.children.append(self.visit(child))

            if Expander.is_plus_or_minus(result.children[0].value):
                result = self.map(result.value, result.children[0])

        if result != None:
            return result
        else:
            result = n.copy(recursive = False)
            for child in n.children:
                result.children.append(self.visit(child))
            return result

    def map(self, func, B):
        '''
        Map A to each child in B.

        func is a PrefixOp or PostfixOp.
        B is any node.

        Ex:
            -(a+b) --> -a + -b
            -(a+(b+c)) --> -a + -(b+c)
        '''
        
        result = B.copy(recursive = False)
        
        for child in B.children:
            new_node = B.copy(value = func)
            new_node.children.append(child.copy())
            result.children.append(new_node)

        return result

    def distribute(self, A, B, operator, left_distr = True):
        '''
        Distribute A to B over operator.

        B must be a node with a PlusOp or SubOp as its value.
        A can be any node.
        operator is the operator we distribute over.
            This can be TimesOp or ImplicitMultOp. We pass it in to stay consistent.
            This is also valid, in some cases, for DivideOp.

        If left_distr is True then perform a left distribution.
            Otherwise perform a right distribution. This is important
            for non-commutative types. 
        '''

        result = B.copy(recursive = False)
        
        for c in B.children:
            new_term = B.copy(value = operator)
            if left_distr:
                new_term.children.append(A.copy())
                new_term.children.append(c.copy())
            else:
                new_term.children.append(c.copy())
                new_term.children.append(A.copy())
            result.children.append(new_term)

        return result
