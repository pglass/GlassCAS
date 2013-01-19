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
        "expand((x^2 + 2*x + 1) * (x^3 + 2*x + 3))",
        ("   (((x^2)*(x^3) + (2*x)*(x^3)) + (1)*(x^3))" +
         " + (((x^2)*(2*x) + (2*x)*(2*x)) + (1)*(2*x))" +
         " + (((x^2)*3     + (2*x)*(3)  ) + (1)*(3))")
    ),
    (
        "expand((x+y)*(x+y)*(x+y))",
        " (((x*x) * x + (y*x) * x) + ((x*y) * x + (y*y) * x))" +
        " + (((x*x) * y + (y*x) * y) + ((x*y) * y + (y*y) * y))"
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

distribution_negation_cases = [
    # Signs are resolved a bit during parsing actually, so "a + -b" turns into "a - b".
    # Put parentheses around negated terms to prevent this: "a + (-b)".
    ("expand(-(a+b))"        , "(-a) + (-b)"),
    ("expand(-((x+y)*(c+d)))", "(-(x*c) + (-(y*c))) + ((-(x*d)) + (-(y*d)))"),
    ("expand(-(x+y)*(c+d))"  , "((-x*c) + (-y*c)) + ((-x*d) + (-y*d))"),
    ("expand(-(1/x * (a+b)))", "(-((1/x)*a)) + (-((1/x)*b))"),
]

expand_integer_power_cases = [
    ("expand((x+y)^1)"          , "(x+y)"), 
    ("expand((x+y)^2)"          , "((x*x) + (y*x)) + ((x*y) + (y*y))"),
    ("expand((x-y)^2)"          , "((x*x) - (y*x)) - ((x*y) - (y*y))"),

    (
        "expand((x+y)^3)",
        # 1. (x+y)*(x+y)*(x+y)
        # 2. ((x+y)*(x+y)) * x + ((x+y) * (x+y)) * y
        #
        # 3. (((x*x) + (y*x)) + ((x*y) + (y*y))) * x
        #  + (((x*x) + (y*x)) + ((x*y) + (y*y))) * y
        #
        # 4. (((x*x) * x + (y*x) * x) + ((x*y) * x + (y*y) * x))
        #  + (((x*x) * y + (y*x) * y) + ((x*y) * y + (y*y) * y))
        # 
        " (((x*x) * x + (y*x) * x) + ((x*y) * x + (y*y) * x))" +
        " + (((x*x) * y + (y*x) * y) + ((x*y) * y + (y*y) * y))"
    ),
]

# flatten cases do not run the expected result through the parser
flatten_addition_cases = [
    ("3"            , "3"           ),
    ("3+4"          , "3 4 +"       ),
    ("3+4+5"        , "3 4 5 +"     ),
    ("3+(4+5)"      , "3 4 5 +"     ),
    ("(3+4)+5"      , "3 4 5 +"     ),
    (
        "(((3+4) + (5+6)) + (((7+8) + 9) + 10)) + 11", 
        "3 4 5 6 7 8 9 10 11 +"
    ),

    ("1/x", "1 x /"),
    ("(1/x) + (2/x)", "1 x / 2 x / +"),
    (
        "((1/x) + (2/x)) + ((3/x) + (4/x) + (5/x))",
        "1 x / 2 x / 3 x / 4 x / 5 x / +"
    ),

    ("(1+2+3+4+5) / (6+7+8+9)", "1 2 3 4 5 + 6 7 8 9 + /"),
    ("(1/(2/(3+4+5+6)))"      , "1 2 3 4 5 6 + / /"),

]

flatten_multiplication_cases = [
    (x[0].replace("+", "*"), x[1].replace("+", "*")) 
        for x in flatten_addition_cases
]

flatten_add_and_mult_cases = [
    ("((1*2*3) + (4*5*6) + (7*8*9))", "1 2 3 * 4 5 6 * 7 8 9 * +"),
    ("((1+2+3) * (4+5+6) * (7+8+9))", "1 2 3 + 4 5 6 + 7 8 9 + *"),
]

# these are run through the flattener, then through the unflattener
# in Unflattener.DEFAULT_MODE
default_unflatten_addition_cases = [
    ("3"            , "3"           ),
    ("3+4"          , "3 4 +"       ),
    ("3+4+5"        , "3 4 + 5 +"   ),
    ("3+(4+5)"      , "3 4 + 5 +"   ),
    ("(3+4)+5"      , "3 4 + 5 +"   ),
    (
        "(((3+4) + (5+6)) + (((7+8) + 9) + 10)) + 11", 
        "3 4 + 5 + 6 + 7 + 8 + 9 + 10 + 11 +"
    ),

    ("1/x", "1 x /"),
    ("(1/x) + (2/x)", "1 x / 2 x / +"),
    (
        "((1/x) + (2/x)) + ((3/x) + (4/x) + (5/x))",
        "1 x / 2 x / + 3 x / + 4 x / + 5 x / +"
    ),
]

default_unflatten_multiplication_cases = [
    (x[0].replace("+", "*"), x[1].replace("+", "*")) 
        for x in default_unflatten_addition_cases
]

default_unflatten_add_and_mult_cases = [
    (
        "((1*2*3) + (4*5*6) + (7*8*9))",
        "1 2 * 3 * 4 5 * 6 * + 7 8 * 9 * +"
    ),
    (
        "((1+2+3) * (4+5+6) * (7+8+9))",
        "1 2 + 3 + 4 5 + 6 + * 7 8 + 9 + *"
    ),
]

balanced_unflatten_addition_cases = [
    ("3"            , "3"           ),
    ("3+4"          , "3 4 +"       ),
    ("3+4+5"        , "3 4 + 5 +"   ),
    ("3+(4+5)"      , "3 4 + 5 +"   ),
    ("(3+4)+5"      , "3 4 + 5 +"   ),
    ("3+4+5+6"      , "3 4 + 5 6 + +"   ),
    ("3+4+5+6+7"    , "3 4 + 5 + 6 7 + +"   ),
    (
        "(((3+4) + (5+6)) + (((7+8) + 9) + 10)) + 11", 
        # produces (((3 + 4) + 5) + (6 + 7)) + ((8 + 9) + (10 + 11))
        "3 4 + 5 + 6 7 + + 8 9 + 10 11 + + +" 
    ),

    ("1/x"          , "1 x /"        ),
    ("(1/x) + (2/x)", "1 x / 2 x / +"),
    (
        "((1/x) + (2/x)) + ((3/x) + (4/x) + (5/x))",
        "1 x / 2 x / + 3 x / + 4 x / 5 x / + +"
    ),
]

balanced_unflatten_multiplication_cases = [
    (x[0].replace("+", "*"), x[1].replace("+", "*")) 
        for x in balanced_unflatten_addition_cases
]

balanced_unflatten_add_and_mult_cases = [
    (
        "((1*2*3) + (4*5*6) + (7*8*9))",
        "1 2 * 3 * 4 5 * 6 * + 7 8 * 9 * +"
    ),
    (
        "((1+2+3) * (4+5+6) * (7+8+9))",
        "1 2 + 3 + 4 5 + 6 + * 7 8 + 9 + *"
    ),
]
