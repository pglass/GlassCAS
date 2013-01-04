
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
        ("   (((x^2)*(x^3) + (2*x)*(x^3)) + (1)*(x^3))" +
         " - (((x^2)*(2*x) + (2*x)*(2*x)) + (1)*(2*x))" +
         " - (((x^2)*3     + (2*x)*3    ) + 3)") # we pass it through reduce, so 1*3 becomes 3
    ),
]

distribution_minus_cases = [(x[0].replace("+", "-"), x[1].replace("+", "-")) for x in distribution_plus_cases]

distribution_implicit_mult_cases = [(x[0].replace("*", ""), x[1].replace("*", "")) for x in distribution_plus_cases + distribution_minus_cases]

distribution_division_cases = [
    ("expand((a+b)/x)"          , "(a/x) + (b/x)"),
    ("expand((a+b)/(x+y))"      , "a/(x+y) + b/(x+y)"),
    ("expand((a+b+c+d)/(x+y))"   , "a/(x+y) + b/(x+y) + c/(x+y) + d/(x+y)"),

    ("expand((a-b)/x)"          , "(a/x) - (b/x)"),
    ("expand((a-b)/(x-y))"      , "a/(x-y) - b/(x-y)"),
    ("expand((a-b-c-d)/(x-y))"   , "a/(x-y) - b/(x-y) - c/(x-y) - d/(x-y)"),
]

distribution_division_and_multiplication_cases = [
    ("expand((a*(x+y))/x)"      , "((a*x)/x + (a*y)/x)"),
    ("expand(((a+b)*(x+y))/x)"  , "(((a*x)/x + (b*x)/x) + ((a*y)/x + (b*y)/x))"),
    ("expand((a+b)*(x+y)/x)"    , "(((a*x)/x + (b*x)/x) + ((a*y)/x + (b*y)/x))"),
    ("expand((a+b)*(x+y)/(c+d))"    , "(((a*x)/(c+d) + (b*x)/(c+d)) + ((a*y)/(c+d) + (b*y)/(c+d)))"),
    ("expand((a+b)*(x+y)/(c+d))"    , "(((a*x)/(c+d) + (b*x)/(c+d)) + ((a*y)/(c+d) + (b*y)/(c+d)))"),
    (
        "expand( ((a+b)*(x+y)) / ((c+d)*(u+v)))",
        ("   (a*x/((c*u+d*u)+(c*v+d*v)) + b*x/((c*u+d*u)+(c*v+d*v)))" +
         " + (a*y/((c*u+d*u)+(c*v+d*v)) + b*y/((c*u+d*u)+(c*v+d*v)))")
    ),
    (
        "expand( (a+b)*(x+y) / ((c+d)*(u+v)))",
        ("   (a*x/((c*u+d*u)+(c*v+d*v)) + b*x/((c*u+d*u)+(c*v+d*v)))" +
         " + (a*y/((c*u+d*u)+(c*v+d*v)) + b*y/((c*u+d*u)+(c*v+d*v)))")
    ),
]