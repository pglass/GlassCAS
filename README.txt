This is (going to be) a computer algebra system.

This has been tested under Python 3:
    >>> sys.version
    '3.3.0 (default, Dec  4 2012, 05:53:31) \n[GCC 4.6.3]'
    
demo_calculator.py is a calculator to demonstrate current capabilities:
    '^' is used for exponentiation
    '%' is used for modulus
    'j' is used for the imaginary unit (matches Python's complex type)
    'e' is Euler's number
    'pi' is pi
  An '@' is inserted for every implicit multiplication:
    >> 3x
    @
      3
      x
  There's a single global symbol table for function definitions.
  To define functions, use brackets and ':=':
    >> f[x] := 3x + 4
    >> g[x,y,z] := x + y + z
  To call functions, use parentheses:
    >> f(3)
    13
    >> g(1,2,3)
    6
    >> g(f(1), f(2), f(3))
    30

And you can run demo_calculator.py with the '--types' flag to see type recognition:
    >> 1/x
    Expression has type:  RationalExpr[ConstantExpr[1], PolynomialExpr[Var[x], degree=1]]
    Reduced expression has type: RationalExpr[ConstantExpr[1], PolynomialExpr[Var[x], degree=1]]
    ...

    >> (x^2 + 3x + 4) * (x^5 + 4x^3 + 1)
    Expression has type:  PolynomialExpr[Var[x], degree=7]
    Reduced expression has type: PolynomialExpr[Var[x], degree=7]
    ...

