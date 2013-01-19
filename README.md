Overview
========
This is my unfinished experiment in writing a computer algebra system.

This has been tested under Python 3:

    >>> sys.version
    '3.3.0 (default, Dec  4 2012, 05:53:31) \n[GCC 4.6.3]'

demo_calculator.py is an interpreter mostly for debug purposes but also to demonstrate current capabilities.

    python3 demo_calculator.py

The language is mathematical and built on top of Python's int, float, and complex types.

    >> 3^4
    81
    >> sqrt(-1)
    1j
    >> 8 % 3
    2
    >> e
    2.718281828459045
    >> pi
    3.141592653589793
    >> 5!
    120

There's a single global symbol table for function definitions. To define functions, use brackets, `[]`, and `:=`. To call functions, use parentheses. Function calls do not always require parentheses, and whitespace has no effect on the result.

    >> f[x] := 3*x + 4
    (f[x] := ((3 * x) + 4))
    >> g[x,y,z] := x + y + z
    (g[x,y,z] := ((x + y) + z))
    >> f(3)
    13
    >> g(1,2,3)
    6
    >> f 3
    13
    >> g1,2,3
    6
    >> g(f(1), f(2), f(3))
    30

An `@` is inserted for every implicit multiplication. Additionally, each variable or function identifier can be only one letter long.

    >> 3x + 4
    ((3 @ x) + 4)
    >> wxyz
    (((w @ x) @ y) @ z)

You can expand expressions with `expand`. The output is unsimplifed, so it tends to blow up pretty quickly.

    >> expand((a+b)*(c+d))
    (((a * c) + (b * c)) + ((a * d) + (b * d)))
    >> expand((x+1)^3)
    (((((x * x) * x) + ((1 * x) * x)) + (((x * 1) * x) + ((1 * 1) * x))) + ((((x * x) * 1) + ((1 * x) * 1)) + (((x * 1) * 1) + ((1 * 1) * 1))))

Use `simplify` to group like terms together. Currently, this works for polynomial addition, subtraction, and multiplication (but not division).

    >> simplify(expand((x+1)^3))
    (((1 + (3 * x)) + (3 * (x ^ 2))) + (x ^ 3))

Run demo_calculator.py with the `--types` flag to show type recognition:

    >> 1/x
    Expression has type:  RationalExpr[ConstantExpr[1], PolynomialExpr[Var[x], degree=1]]
    Reduced expression has type: RationalExpr[ConstantExpr[1], PolynomialExpr[Var[x], degree=1]]
    ...

    >> (x^2 + 3x + 4) * (x^5 + 4x^3 + 1)
    Expression has type:  PolynomialExpr[Var[x], degree=7]
    Reduced expression has type: PolynomialExpr[Var[x], degree=7]
    ...

