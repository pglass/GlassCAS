'''
Test cases for methods in rigid_parsing

-- Note: Symbol objects compare using their string representation.
         That is, "'cos' == CosOp()" and "PlusOp() in ['+']" should
         both give true. So the *outputs* of tests can use either
         strings ['+', 'cos'] or operator objects [PlusOp(), CosOp()]
         for checking equality (if that is sufficient for the test case).
         However, you still have to be particular about the inputs.
'''

from parsing.parser_definitions import *
import string

#
# rigid_parsing.tokenize test cases
#
tokenize_constants_cases = [
    ("e"     , ["e"]                 ),
    ("pi"    , ["pi"]                ),
    ("eee"   , ["e", "e", "e"]       ),
    ("pipipi", ["pi", "pi", "pi"]    ),
    ("epiepi", ["e", "pi", "e", "pi"]),
]

tokenize_functions_cases = [
    ("".join(map(str, OP_CLASS_DICT.keys())) , list(OP_CLASS_DICT.keys())),
    (" ".join(map(str, OP_CLASS_DICT.keys())), list(OP_CLASS_DICT.keys())),
    
    ("cos"         , ["cos"]                     ),
    ("cossin"      , ["cos", "sin"]              ),
    ("cossincossin", ["cos", "sin", "cos", "sin"]),
    ("-cos+"       , ["-", "cos", "+"]           ),
]

tokenize_variables_cases = [
    ("x"   , ["x"]               ),
    ("xx"  , ["x", "x"]          ),
    ("xxxx", ["x", "x", "x", "x"]),
    ("xy"  , ["x", "y"]          ),
    ("aqxz", ["a", "q", "x", "z"]),
    ("ywpb", ["y", "w", "p", "b"]),
]

tokenize_parens_cases = [
    ("("     , ["("]                         ),
    (")"     , [")"]                         ),
    ("()"    , ["(", ")"]                    ),
    ("())(()", ["(", ")", ")", "(", "(", ")"]),
]

tokenize_reals_cases = [
    ("0"                    , [0]                    ),
    (".0"                   , [0.0]                  ),
    ("0.0"                  , [0.0]                  ),
    (".1"                   , [0.1]                  ),
    ("1."                   , [1.0]                  ),
    ("1.0"                  , [1.0]                  ),
    ("1.1"                  , [1.1]                  ),
    ("9876543210"           , [9876543210]           ),
    ("9876543210."          , [9876543210.0]         ),
    ("9876543210.0"         , [9876543210.0]         ),
    (".0123456789"          , [0.0123456789]         ),
    ("0.0123456789"         , [0.0123456789]         ),
    ("9876543210.0123456789", [9876543210.0123456789]),
]

tokenize_complex_cases = [
    ("j"                     , [1j]                    ),
    ("1j"                    , [1j]                    ),
    ("j1"                    , [1j]                    ),
    ("9876543210j"           , [9876543210j]           ),
    ("j9876543210"           , [9876543210j]           ),
    ("1.1j"                  , [1.1j]                  ),
    ("j1.1"                  , [1.1j]                  ),
    (".1j"                   , [.1j]                   ),
    ("j.1"                   , [.1j]                   ),
    ("9876543210.0123456789j", [9876543210.0123456789j]),
    ("j9876543210.0123456789", [9876543210.0123456789j]),
    ("jj"                    , [1j, 1j]                ),
    ("23.45jj67.89"          , [23.45j, 67.89j]        ),
    ("1+4j"                  , [1, "+", 4j]            ),
]

tokenize_combined_cases = [
    ("1+2"                 , [1, "+", 2]                                ),
    ("123+456"             , [123, "+", 456]                            ),
    ("(4+5)*5"             , ["(", 4, "+", 5, ")", "*", 5]              ),
    ("(4+5j)*5j"           , ["(", 4, "+", 5j, ")", "*", 5j]            ),
    ("(123+456)*789"       , ["(", 123, "+", 456, ")", "*", 789]        ),
    ("  (  1.2 + 555.99)  ", ["(", 1.2, "+", 555.99, ")"]               ),
    (" .323 + .7 + 0.7"    , [.323, "+", .7, "+", 0.7]                  ),
    ("cos"                 , ["cos"]                                    ),
    ("coscos"              , ["cos", "cos"]                             ),
    ("co"                  , ["c", "o"]                                 ),
    ("cosin"               , ["cos", "i", "n"]                          ),
    ("x*sin(x)"            , ["x", "*", "sin", "(", "x", ")"]           ),
    ("c*cos(s)"            , ["c", "*", "cos", "(", "s", ")"]           ),
    ("pi * e / cos(e)"     , ["pi", "*", "e", "/", "cos", "(", "e", ")"]),
    
    (
        "(234+567)*(123+456)", 
        ["(", 234, "+", 567, ")", "*", "(", 123, "+", 456, ")"]
    ),
    (
        "coscos(1.1+3)*cos(5)", 
        ["cos", "cos", "(", 1.1, "+", 3, ")", "*", "cos", "(", 5, ")"]
    ),
]

tokenize_user_functions_cases = [
    ('f[x]'          , ['f[x]']                                 ),
    ('g[x,y]'        , ['g[x,y]']                               ),
    ('h[x,y,]'       , ['h[x,y]']                               ),
    ('i[a,b,c,d,e,f]', ['i[a,b,c,d,e,f]']                       ),
    ('a[abcdef]'     , ['a[a,b,c,d,e,f]']                       ),
    ('f[x]'          , [UserFunction('f', [Var('x')])]          ),
    ('f[x,y]'        , [UserFunction('f', [Var('x'), Var('y')])]),
    
]

tokenize_bad_input_cases = [
    ".",
    "..",
    ".1.",
    ".12345678.",
    "1.."
    "1..2",
    "123..456",
    "23.45.67",
    "\\",
    "#",
    "123.#",
    "+.",
    ".+",
    'f[',
    '[x,y,z]',
    'f[x,y,',
]

#
# rigid_parsing.to_RPN test cases
#
rpn_basic_correctness_cases = [
    (list(map(Var, string.ascii_letters)), list(map(Var, string.ascii_letters))),
    
    ([1,2,3,4,5,6,7,8,9,0], [1,2,3,4,5,6,7,8,9,0]),
    ([3j, EqualsOp(), 4]  , [3j, 4, EqualsOp()]  ),
    ([3j, PlusOp(), 4]    , [3j, 4, PlusOp()]    ),
    ([3j, SubOp(), 4]     , [3j, 4, SubOp()]     ),
    ([3j, TimesOp(), 4]   , [3j, 4, TimesOp()]   ),
    ([3j, DivideOp(), 4]  , [3j, 4, DivideOp()]  ),
    ([3j, ModulusOp(), 4] , [3j, 4, ModulusOp()] ),
    ([3j, ExponentOp(), 4], [3j, 4, ExponentOp()]),
    
    (
        [Var('x'), EqualsOp(), Var('y'), EqualsOp(), Var('z')],
        [Var('x'), Var('y'), EqualsOp(), Var('z'), EqualsOp()]
    ),
    (
        [Var('x'), PlusOp(), Var('y'), PlusOp(), Var('z')],
        [Var('x'), Var('y'), PlusOp(), Var('z'), PlusOp()]
    ),
    (
        [Var('x'), SubOp(), Var('y'), SubOp(), Var('z')],
        [Var('x'), Var('y'), SubOp(), Var('z'), SubOp()]
    ),
    (
        [Var('x'), TimesOp(), Var('y'), TimesOp(), Var('z')],
        [Var('x'), Var('y'), TimesOp(), Var('z'), TimesOp()]
    ),
    (
        [Var('x'), DivideOp(), Var('y'), DivideOp(), Var('z')], 
        [Var('x'), Var('y'), DivideOp(), Var('z'), DivideOp()]
    ),
    (
        [Var('x'), ModulusOp(), Var('y'), ModulusOp(), Var('z')],
        [Var('x'), Var('y'), ModulusOp(), Var('z'), ModulusOp()]
    ),
    (
        [Var('x'), ExponentOp(), Var('y'), ExponentOp(), Var('z')], 
        [Var('x'), Var('y'), Var('z'), ExponentOp(), ExponentOp()]
    ),
    
    ([CosOp(), 3]                  , [3, CosOp()]                  ),
    ([3, FactorialOp()]            , [3, FactorialOp()]            ),
    ([CosOp(), CosOp(), CosOp(), 3], [3, CosOp(), CosOp(), CosOp()]),
    (
        [3, FactorialOp(), FactorialOp(), FactorialOp()], 
        [3, FactorialOp(), FactorialOp(), FactorialOp()]
    ),
]
    
rpn_precedence_cases = [
    # equals sign is lowest precedence
    (
        [Var('x'), PlusOp(), 5, EqualsOp(), Var('y'), SubOp(), 3], 
        [Var('x'), 5, PlusOp(), Var('y'), 3, SubOp(), EqualsOp()]
    ),
    (
        [Var('x'), TimesOp(), 5, EqualsOp(), Var('y'), ExponentOp(), 3, FactorialOp()], 
        [Var('x'), 5, TimesOp(), Var('y'), 3, FactorialOp(), ExponentOp(), EqualsOp()]
    ),

    # multiplication/division/modulus are higher than addition/subtraction
    (
        [Var('w'), PlusOp(), Var('x'), TimesOp(), Var('y')],
        [Var('w'), Var('x'), Var('y'), TimesOp(), PlusOp()]
    ),
    (
        [Var('w'), PlusOp(), Var('x'), DivideOp(), Var('y')],
        [Var('w'), Var('x'), Var('y'), DivideOp(), PlusOp()]
    ),
    (
        [Var('w'), PlusOp(), Var('x'), ModulusOp(), Var('y')], 
        [Var('w'), Var('x'), Var('y'), ModulusOp(), PlusOp()]
    ),
    (
        [Var('w'), PlusOp(), Var('x'), TimesOp(), Var('y'), PlusOp(), Var('z')], 
        [Var('w'), Var('x'), Var('y'), TimesOp(), PlusOp(), Var('z'), PlusOp()]
    ),
    (
        [Var('w'), PlusOp(), Var('x'), DivideOp(), Var('y'), PlusOp(), Var('z')],
        [Var('w'), Var('x'), Var('y'), DivideOp(), PlusOp(), Var('z'), PlusOp()]
    ),
    (
        [Var('w'), PlusOp(), Var('x'), ModulusOp(), Var('y'), PlusOp(), Var('z')], 
        [Var('w'), Var('x'), Var('y'), ModulusOp(), PlusOp(), Var('z'), PlusOp()]
    ),
    
    # functions are higher than +-*/%
    (
        [CosOp(), Var('x'), EqualsOp(), Var('y')],
        [Var('x'), CosOp(), Var('y'), EqualsOp()]
    ),
    (
        [CosOp(), Var('x'), PlusOp(), Var('y')], 
        [Var('x'), CosOp(), Var('y'), PlusOp()]
    ),
    (
        [CosOp(), Var('x'), SubOp(), Var('y')], 
        [Var('x'), CosOp(), Var('y'), SubOp()]
    ),
    (
        [CosOp(), Var('x'), TimesOp(), Var('y')], 
        [Var('x'), CosOp(), Var('y'), TimesOp()]
    ),
    (
        [CosOp(), Var('x'), DivideOp(), Var('y')], 
        [Var('x'), CosOp(), Var('y'), DivideOp()]
    ),
    (
        [CosOp(), Var('x'), ModulusOp(), Var('y')], 
        [Var('x'), CosOp(), Var('y'), ModulusOp()]
    ),
    (
        [CosOp(), Var('x'), EqualsOp(), SinOp(), Var('y')], 
        [Var('x'), CosOp(), Var('y'), SinOp(), EqualsOp()]),
    (
        [CosOp(), Var('x'), PlusOp(), SinOp(), Var('y')], 
        [Var('x'), CosOp(), Var('y'), SinOp(), PlusOp()]
    ),
    (
        [CosOp(), Var('x'), SubOp(), SinOp(), Var('y')], 
        [Var('x'), CosOp(), Var('y'), SinOp(), SubOp()]
    ),
    (
        [CosOp(), Var('x'), TimesOp(), SinOp(), Var('y')], 
        [Var('x'), CosOp(), Var('y'), SinOp(), TimesOp()]
    ),
    (
        [CosOp(), Var('x'), DivideOp(), SinOp(), Var('y')], 
        [Var('x'), CosOp(), Var('y'), SinOp(), DivideOp()]
    ),
    (
        [CosOp(), Var('x'), ModulusOp(), SinOp(), Var('y')], 
        [Var('x'), CosOp(), Var('y'), SinOp(), ModulusOp()]
    ),
    
    # exponentiation is higher than functions
    (
        [SqrtOp(), Var('x'), ExponentOp(), Var('y')],
        [Var('x'), Var('y'), ExponentOp(), SqrtOp()]
    ),
    
    # factorial is highest precedence
    (
        [TanOp(), Var('x'), FactorialOp()], 
        [Var('x'), FactorialOp(), TanOp()]
    ),
]

rpn_parens_cases = [
    (['(', ')']                       , [] ),
    (['(', 3, ')']                    , [3]),
    (['(', '(', 3, ')', ')']          , [3]),
    (['(', '(', 3, '(', ')', ')', ')'], [3]),
    
    ([3, TimesOp(), '(', Var('x'), ')']          , [3, Var('x'), TimesOp()]),
    (['(', 3, ')', TimesOp(), Var('x')]          , [3, Var('x'), TimesOp()]),
    (['(', 3, ')', TimesOp(), '(', Var('x'), ')'], [3, Var('x'), TimesOp()]),
    
    (
        ['(', 3j, PlusOp(), 4, ')', TimesOp(), '(', Var('x'), PlusOp(), Var('y'), ')'],
        [3j, 4, PlusOp(), Var('x'), Var('y'), PlusOp(), TimesOp()]
    ),
    (
        [SqrtOp(), '(', Var('x'), ')', ExponentOp(), Var('y')], 
        [Var('x'), SqrtOp(), Var('y'), ExponentOp()]
    ),
]

rpn_user_functions_cases = [
    ([UserFunction('f', [Var('x')])]          , ['f[x]']  ),
    ([UserFunction('f', [Var('x'), Var('y')])], ['f[x,y]']),
    (
        [Var('x'), PlusOp(), UserFunction('f', [Var('x'), Var('y')])], 
        ['x', 'f[x,y]', '+']
    ),
]

rpn_bad_input_cases = [
    ['(']                        ,
    [')']                        ,
    [')', '(']                   ,
    [3, TimesOp(), ')']          ,
    [3, TimesOp(), Var('x'), ')'],
    [3, TimesOp(), Var('x'), '('],
    ['(', 3, TimesOp(), Var('x')],
]

#
# rigid_parsing.to_tree test cases
#
# These go in as tokens in RPN. The tree structure is checked using `node`.
#
tree_operand_order_cases = [
    ([1]                           , '1'       ),
    ([1.2]                         , '1.2'     ),
    ([3j]                          , '3j'      ),
    ([3j, 1.2, PlusOp()]           , '3j 1.2 +'),
    ([Var('x')]                    , 'x'       ),
    ([Var('x'), Var('y'), PlusOp()], 'x y +'   ),
    
    ([Var('x'), Var('y'), PlusOp(), Var('z'), TimesOp()], 'x y + z *'),
]

tree_bad_input_cases = [
    [PlusOp()]                                         ,
    [Var('x'), PlusOp()]                               ,
    [Var('x'), PlusOp(), Var('y'), TimesOp()]          ,
    [Var('x'), PlusOp(), Var('y'), Var('z'), TimesOp()],
]

#
# rigid_parsing.node.reduce test cases
#
tree_reduce_cases = [
    ([1]       , '1'  ),
    ([1.2]     , '1.2'),
    ([3j]      , '3j' ),
    ([Var('x')], 'x'  ),
    
    ([1, 2, PlusOp()]    , '3'      ),
    ([1.1, 2.2, SubOp()] , '-1.1'   ),
    ([1j, 1j, TimesOp()] , '(-1+0j)'),
    ([5, 4, DivideOp()]  , '1.25'   ),
    ([5, 4, ModulusOp()] , '1'      ),
    ([3, 4, ExponentOp()], '81'     ),
    
    ([1, 2, PlusOp(), 3, PlusOp()]        , '6'                  ),
    ([1, 2, SubOp(), 3, SubOp()]          , '-4'                 ),
    ([1, 2, TimesOp(), 3, TimesOp()]      , '6'                  ),
    ([1, 2, DivideOp(), 3, DivideOp()]    , '0.16666666666666666'),
    ([1, 2, 3, DivideOp(), DivideOp()]    , '1.5'                ),
    ([2, 3, 2, ExponentOp(), ExponentOp()], '512'                ),
    ([2, 3, ExponentOp(), 2, ExponentOp()], '64'                 ),
    
    ([1j, 1j, PlusOp()]            , '2j'     ),
    ([3j, 2, SubOp()]              , '(-2+3j)'),
    ([Pi(), CosOp()]               , 'pi cos' ),
    ([E(), CosOp()]                , 'e cos'  ),
    ([Var('x'), Var('x'), PlusOp()], 'x x +'  ),
    ([Var('x'), Var('y'), PlusOp()], 'x y +'  ),
    
    ([2, 2j, PlusOp(), 3, 3j, PlusOp(), TimesOp()], '12j'),
]

tree_replace_constants_cases = [
    ([Pi(), CosOp()], '(-1-0j)'),
    ([E(), LogEOp()], '(1+0j)' ),
]