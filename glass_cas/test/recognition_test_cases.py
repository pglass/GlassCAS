'''
Test cases for expression type determination.

Technically, these test recognition.recognize.visit,
but each set of test cases is intended for
a particular Expr.resolve method
'''

from ..expression_types import *

# for Constant
constant_expr_on_left_cases = [
  ("2 + 3"      , ConstantExpr(5)                     ),
  ("2 - 3"      , ConstantExpr(-1)                    ),
  ("2 * 3"      , ConstantExpr(6)                     ),
  ("2 / 3"      , ConstantExpr(2.0/3)                 ),
  ("2 ^ 3"      , ConstantExpr(8)                     ),

  ("3 + x"      , PolynomialExpr(Var("x"), degree=1)  ),
  ("3 - x"      , PolynomialExpr(Var("x"), degree=1)  ),
  ("3 * x"      , PolynomialExpr(Var("x"), degree=1)  ),

  ("3 + (x^2 + 4*x + 1)", PolynomialExpr(Var("x"), degree=2)  ),
  ("3 - (x^2 + 4*x + 1)", PolynomialExpr(Var("x"), degree=2)  ),
  ("3 * (x^2 + 4*x + 1)", PolynomialExpr(Var("x"), degree=2)  ),
#  ("2 / x"      , PolynomialExpr(Var("x"), degree=-1) ),
  (
    "3 / x",
    RationalExpr(
      PolynomialExpr(Var("x"), degree = 0),
      PolynomialExpr(Var("x"), degree = 1)
    )
  ),
  ("3 ^ x"      , ExponentialExpr(Var("x"), base=3)   ),

# I don't make these exponential because I simplify the
# base of an exponential expression, but I cannot validly
# do so with a dangling term added on.
  ("2 + 3^x"    , UnknownExpr()                       ),
  ("2 - 3^x"    , UnknownExpr()                       ),

  ("2 * 3^x"    , ExponentialExpr(Var("x"), base=3)   ),
  ("2 / 3^x"    , ExponentialExpr(Var("x"), base=3)   ),

# what should this be?
  ("2 ^ 3^x"    , UnknownExpr()                       ),

  ("(2 - 5) + 3" , ConstantExpr(0)                     ),
  ("(2 - 5) - 3" , ConstantExpr(-6)                    ),
  ("(2 - 5) * 3" , ConstantExpr(-9)                    ),
  ("(2 - 5) / 3" , ConstantExpr(-1)                    ),
  ("(2 - 5) ^ 3" , ConstantExpr(-27)                   ),
]

# for PolynomialExpr.resolve
polynomial_expr_on_left_cases = [
  ("x + 4"       , PolynomialExpr(Var("x"), degree=1)  ),
  ("x - 4"       , PolynomialExpr(Var("x"), degree=1)  ),
  ("x * 4"       , PolynomialExpr(Var("x"), degree=1)  ),
  ("x / 4"       , PolynomialExpr(Var("x"), degree=1)  ),

  ("x ^ 4"       , PolynomialExpr(Var("x"), degree=4)  ),

  ("x^5 + 2"     , PolynomialExpr(Var("x"), degree=5)  ),
  ("x^5 - 2"     , PolynomialExpr(Var("x"), degree=5)  ),
  ("x^5 * 2"     , PolynomialExpr(Var("x"), degree=5)  ),
  ("x^5 / 2"     , PolynomialExpr(Var("x"), degree=5)  ),

  ("x^5 + (2 ^ 5 - 3 + 4)"   , PolynomialExpr(Var("x"), degree=5)  ),
  ("x^5 - (2 ^ 5 - 3 + 4)"   , PolynomialExpr(Var("x"), degree=5)  ),
  ("x^5 * (2 ^ 5 - 3 + 4)"   , PolynomialExpr(Var("x"), degree=5)  ),
  ("x^5 / (2 ^ 5 - 3 + 4)"   , PolynomialExpr(Var("x"), degree=5)  ),

  ("(x^3 + x^7) + (3*x + x^2 + x^6)", PolynomialExpr(Var("x"), degree=7)),
  ("(x^3 + x^9) + (3*x + x^2 + x^6)", PolynomialExpr(Var("x"), degree=9)),

  (
    "x^7 + (1 / x^4)",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=11),
      PolynomialExpr(Var("x"), degree=4)
    )
  ),
  (
    "x^7 + (x^3 / x^4)",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=11),
      PolynomialExpr(Var("x"), degree=4)
    )
  ),

  ("x^7 + e^x" , UnknownExpr()),
]

# test RationalExpr.resolve
rational_expr_on_left_cases = [
  (
    "(1/x)",
    RationalExpr(
      ConstantExpr(1, var = Var("x")), # ConstantExpr subclasses PolynomialExpr
      PolynomialExpr(Var("x"), degree=1)
    )
  ),
  (
    "(1/x) + 1",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=1),
      PolynomialExpr(Var("x"), degree=1)
    )
  ),
  (
    "(1/x) - 1",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=1),
      PolynomialExpr(Var("x"), degree=1)
    )
  ),
  (
    "(1/x) + (2 - 3 * 4 ^ 7)",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=1),
      PolynomialExpr(Var("x"), degree=1)
    )
  ),
  (
    "(1/x) + (2 - 3 * 4 ^ 7)",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=1),
      PolynomialExpr(Var("x"), degree=1)
    )
  ),
  (
    "(1/x) + x",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=2),
      PolynomialExpr(Var("x"), degree=1)
    )
  ),
  (
    "(1/x) - x",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=2),
      PolynomialExpr(Var("x"), degree=1)
    )
  ),

  (
    "(1/x) * x",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=1),
      PolynomialExpr(Var("x"), degree=1)
    )
  ),
  (
    "(1/x) + (x^3 + 4*x + 1)",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=4),
      PolynomialExpr(Var("x"), degree=1)
    )
  ),
  (
    "(1/x) - (x^3 + 4*x + 1)",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=4),
      PolynomialExpr(Var("x"), degree=1)
    )
  ),
  (
    "(1/x) * (x^3 + 4*x + 1)",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=3),
      PolynomialExpr(Var("x"), degree=1)
    )
  ),
  (
    "(1/x) / x",
    RationalExpr(
      ConstantExpr(1),
      PolynomialExpr(Var("x"), degree=2)
    )
  ),
  (
    "(2/x) + (2/x)",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=1),
      PolynomialExpr(Var("x"), degree=2)
    )
  ),
  (
    "(2/x) - (2/x)",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=1),
      PolynomialExpr(Var("x"), degree=2)
    )
  ),
  (
    "(2/x) * (3/x)",
    RationalExpr(
      ConstantExpr(6),
      PolynomialExpr(Var("x"), degree=2)
    )
  ),
  (
    "(2/x) / (2/x)",
    RationalExpr(
      PolynomialExpr(Var("x"), degree=1),
      PolynomialExpr(Var("x"), degree=1)
    )
  ),

  (
    "(2/x) ^ 2",
    RationalExpr(
      ConstantExpr(4),
      PolynomialExpr(Var("x"), degree=2)
    )
  ),

  ("(2/x) ^ x"        , UnknownExpr()),
  ("(2/x) ^ (2/x)"    , UnknownExpr()),
]

# test cases for ExponentialExpr.resolve
exponential_expr_on_left_cases = [
  ("(2^x)"        , ExponentialExpr(Var("x"), base=2) ),
  ("(2^x) + 2"    , UnknownExpr()                     ),
  ("(2^x) - 2"    , UnknownExpr()                     ),
  ("(2^x) * 2"    , ExponentialExpr(Var("x"), base=2) ),
  ("(2^x) / 2"    , ExponentialExpr(Var("x"), base=2) ),
  ("(2^x) ^ 2"    , ExponentialExpr(Var("x"), base=2) ),

  ("(2^x) + x"    , UnknownExpr()                     ),
  ("(2^x) - x"    , UnknownExpr()                     ),
  ("(2^x) * x"    , UnknownExpr()                     ),
  ("(2^x) / x"    , UnknownExpr()                     ),
  ("(2^x) ^ x"    , UnknownExpr()                     ),

  ("(2^x) + (3/x)", UnknownExpr()                     ),
  ("(2^x) - (3/x)", UnknownExpr()                     ),
  ("(2^x) * (3/x)", UnknownExpr()                     ),
  ("(2^x) / (3/x)", UnknownExpr()                     ),
  ("(2^x) ^ (3/x)", UnknownExpr()                     ),

  ("(2^x) + (3^x)", UnknownExpr()                     ),
  ("(2^x) - (3^x)", UnknownExpr()                     ),
  ("(2^x) * (3^x)", UnknownExpr()                     ),
  ("(2^x) / (3^x)", UnknownExpr()                     ),
  ("(2^x) ^ (3^x)", UnknownExpr()                     ),
]

equation_expr_cases = [
  (
    "x = x^2",
    EquationExpr(
      PolynomialExpr(Var("x"), degree=1),
      PolynomialExpr(Var("x"), degree=2)
    )
  ),
  (
    "3 + 4 ^ 2 - 5 = 5 ^ 2 + 1",
    EquationExpr(ConstantExpr(14), ConstantExpr(26))
  ),
  (
    "1/x = 3^x",
    EquationExpr(
      RationalExpr(ConstantExpr(1), PolynomialExpr(Var("x"), degree=1)),
      ExponentialExpr(Var("x"), base=3)
    )
  ),
  (
    "(2/x + 2^x) = ((x^2) * (e^x))",
    EquationExpr(UnknownExpr(), UnknownExpr())
  ),
  (
    "2/x + 2^x = (x^2) * (e^x)",
    EquationExpr(UnknownExpr(), UnknownExpr())
  ),

]
