'''
recognition.py

The purpose of self module is to provide a class Recognizer
which is able to tell you what kind of expression a particular
tree represents.

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
  -- It takes some work extending this class, even if it's all
     straightforward.

     For N unique operators and M different expression types, there
     are have M*N*M ways to combine the expressions. And the code
     is hundreds of conditionals checking which combination we were
     given.

'''

from parsing.parser_definitions import *
from parsing.expression_types import *
import numbers

class Recognizer(object):

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
