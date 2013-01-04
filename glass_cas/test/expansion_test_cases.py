
distribution_plus_cases = [
    ("expand(x)"            , "x"                       ),
    ("expand(1/x)"          , "1/x"                     ),
    ("expand(1/x)"          , "1/x"                     ),
    
    ("expand(3*(x+y))"      , "(3*x) + (3*y)"           ),
    ("expand((x+y)*3)"      , "(x*3) + (y*3)"           ),
    ("expand(x*(a+b))"      , "(x*a) + (x*b)"           ),
    ("expand((a+b)*x)"      , "(a*x) + (b*x)"           ),
    ("expand(x*((a+b)+c))"  , "((x*a) + (x*b)) + x*c"   ),
    ("expand(x*(a+(b+c)))"  , "x*a + ((x*b) + (x*c))"   ),
    ("expand(((a+b)+c)*x)"  , "((a*x) + (b*x)) + c*x"   ),
    ("expand((a+(b+c))*x)"  , "a*x + ((b*x) + (c*x))"   ),

    ("expand((a+b)*(x+y))"  , "((a*x) + (b*x)) + ((a*y) + (b*y))" ),

    ("expand(x*(a+b+c))"    , "x*a + x*b + x*c"),
    ("expand((a+b+c)*x)"    , "a*x + b*x + c*x"),
    ("expand((a+b+c)*(x+y))", "(a*x + b*x + c*x) + (a*y + b*y + c*y)"),
    (
        "expand((a+b+c)*(x+y+z))", 
        "(a*x + b*x + c*x) + (a*y + b*y + c*y) + (a*z + b*z + c*z)"
    ),

    ("expand((1/x) * (a + b))", "(1/x)*a + (1/x)*b"),
    ("expand((a + b) * (1/x))", "a*(1/x) + b*(1/x)"),

    (
        "expand((x^2 + 2*x + 1) * (x^3 - 2*x - 3))",
        ("   ((x^2)*(x^3) + (2*x)*(x^3) + (1)*(x^3))" +
         " - ((x^2)*(2*x) + (2*x)*(2*x) + (1)*(2*x))" +
         " - ((x^2)*(3) + (2*x)*(3) + (1)*(3))")
    ),
]

distribution_minus_cases = [(x[0].replace("+", "-"), x[1].replace("+", "-")) for x in distribution_plus_cases]

distribution_implicit_mult_cases = [(x[0].replace("*", ""), x[1].replace("*", "")) for x in distribution_plus_cases + distribution_minus_cases]



