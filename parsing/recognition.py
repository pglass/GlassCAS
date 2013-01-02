''' 
The purpose of self module is to provide a class Recognizer
which is able to tell you what kind of expression a particular
tree represents.

Examples...
  n represents "3 + 4"
    --> ConstantExpr
  n represents "x^3 + x^2 + x + 1"
    --> PolynomialExpr[Var(x), degree = 3]
  n represents "e^x"
    --> ExponentialExpr(Constant(e))
    or maybe:
    --> ExponentialExpr(base = e)
  n represents "x + log(x) = 1"
    --> PolyLogCombinationExpr[Var(x), isEquation = true]
    or maybe:
    --> EquationExpr[PolyLogCombinationExpr[Var(x)], ConstantExpr]
  n represents "

Practicality?
  1. This will work for a lot of basic forms, which is good.

  2. I'm basically classifying mathematical expressions, but
     it's not always clear (to me) what the type is. Ex:
        e^x + log(x) = x^2
     It may turn out that there are no solutions to self equation,
     but we could still give it a type. Maybe:
        EquationExpr[ExpLogCombExpr[Var(x)], PolynomialExpr[Var(x), degree = 2]]
     I'm not really sure how useful the above would be, except that
     we could rule out many methods of solving the equation.

     But if there's no standard classification for a particular expression,
     then I probably don't know how to solve it, anyway.

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


  -- If we can determine an expression is constant, we should
     always be able to compute its value (given the expression is valid).
     Computing these values here is dangerous though, because we 
     don't handle division by zero, etc, etc.
     
  -- I have the feeling I should store the type at every node of the tree.
'''

from parsing.node import node
from parsing.parser_definitions import *
from parsing.expression_types import *
import numbers

class Recognizer(object):

  def __init__(self):
    pass

  def visit(self, n):
    # the order of conditionals is specific here:
    #   handle EqualsOp, DefinedAsOp, then any other infix ops
    if isinstance(n.value, EqualsOp):
      left = self.visit(n.children[0])
      right = self.visit(n.children[1])
      return EquationExpr(left, right)
    elif isinstance(n.value, DefinedAsOp):
      return DefinedAsExpr()
    elif isinstance(n.value, InfixOp):
      left = self.visit(n.children[0])
      right = self.visit(n.children[1])
      return left.resolve(n.value, right)
    elif isinstance(n.value, numbers.Number):
      return ConstantExpr(n.value)
    elif isinstance(n.value, Constant):
      return ConstantExpr(n.value.value)
    elif isinstance(n.value, Var):
      return PolynomialExpr(Var(n.value), 1)
      
    return UnknownExpr()
