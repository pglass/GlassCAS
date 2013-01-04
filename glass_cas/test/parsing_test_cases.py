'''
Test cases for methods in parsing

-- Note: Symbol objects compare using their string representation.
         That is, "'cos' == CosOp()" and "PlusOp() in ['+']" should
         both give true. So the *outputs* of tests can use either
         strings ['+', 'cos'] or operator objects [PlusOp(), CosOp()]
         for checking equality (if that is sufficient for the test case).
         However, you still have to be particular about the input types.
'''

from ..parsing.parser_definitions import *
from ..node import node
import string

#
# Parser.tokenize test cases
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

tokenize_arg_delimiter_cases = [
    (ARG_DELIM    , [ARG_DELIM]),
    (ARG_DELIM * 4, [ARG_DELIM, ARG_DELIM, ARG_DELIM, ARG_DELIM]),
    (
        '3{0}x{0}5.5{0}'.format(ARG_DELIM),
        [3, ARG_DELIM, Var('x'), ARG_DELIM, 5.5, ARG_DELIM]),
    (
        '3{0}xy{0}f[a{0}b]'.format(ARG_DELIM),
        [3, ARG_DELIM, Var('x'), Var('y'), ARG_DELIM, UserFunction('f', [Var('a'), Var('b')])]
    ),
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
# Parser.to_rpn test cases
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
    (
        [Var('x'), ExponentOp(), NegationOp(), Pi()],
        [Var('x'), Pi(), NegationOp(), ExponentOp()]
    ),

    # factorial is highest precedence
    (
        [4, PlusOp(), 5, FactorialOp()],
        [4, 5, FactorialOp(), PlusOp()]
    ),
    (
        [4, ExponentOp(), 5, FactorialOp()],
        [4, 5, FactorialOp(), ExponentOp()]
    ),
    (
        [TanOp(), Var('x'), FactorialOp()],
        [Var('x'), FactorialOp(), TanOp()]
    ),
]

rpn_prefix_cases = [
    # check that order is correct
    (
        [CosOp(), SinOp(), TanOp(), 4],
        [4, TanOp(), SinOp(), CosOp()]
    ),
    (
        [PrecFivePrefixOp(), SinOp(), PrecZeroPrefixOp(), 4],
        [4, PrecZeroPrefixOp(), SinOp(), PrecFivePrefixOp()]
    ),
    (
        [PrecFivePrefixOp(), PrecZeroPrefixOp(), SinOp(), 4],
        [4, SinOp(), PrecZeroPrefixOp(), PrecFivePrefixOp()]
    ),
    # make sure prefix and infix precedences are respected
    (
        [4, PlusOp(), CosOp(), 5],
        [4, 5, CosOp(), PlusOp()]
    ),
    (
        [4, ExponentOp(), CosOp(), 5],
        [4, 5, CosOp(), ExponentOp()]
    ),
    (
        [4, PlusOp(), PrecZeroPrefixOp(), 5],
        [4, 5, PrecZeroPrefixOp(), PlusOp()]
    ),
    (
        [4, PlusOp(), PrecFivePrefixOp(), 5],
        [4, 5, PrecFivePrefixOp(), PlusOp()]
    ),
    (
        [CosOp(), 4, PlusOp(), PrecFivePrefixOp(), 5],
        [4, CosOp(), 5, PrecFivePrefixOp(), PlusOp()]
    ),
    (
        [PrecZeroPrefixOp(), 4, PlusOp(), PrecFivePrefixOp(), 5],
        [4, 5, PrecFivePrefixOp(), PlusOp(), PrecZeroPrefixOp()]
    ),
]

rpn_postfix_cases = [
    # check that order is correct
    (
        [4, PrecZeroPostfixOp(), PrecThreePostfixOp(), PrecZeroPostfixOp()],
        [4, PrecZeroPostfixOp(), PrecThreePostfixOp(), PrecZeroPostfixOp()],
    ),
    (
        [4, PrecZeroPostfixOp(), PrecThreePostfixOp(), FactorialOp()],
        [4, PrecZeroPostfixOp(), PrecThreePostfixOp(), FactorialOp()],
    ),
    (
        [4, PrecThreePostfixOp(), FactorialOp(), PrecZeroPostfixOp()],
        [4, PrecThreePostfixOp(), FactorialOp(), PrecZeroPostfixOp()],
    ),
    # make sure postfix and infix precedences are respected
    (
        [4, PlusOp(), 5, PrecZeroPostfixOp()],
        [4, 5, PlusOp(), PrecZeroPostfixOp()],
    ),
    (
        [4, PlusOp(), 5, PrecThreePostfixOp()],
        [4, 5, PrecThreePostfixOp(), PlusOp()],
    ),
    (
        [4, PlusOp(), 5, PrecThreePostfixOp(), PrecZeroPostfixOp()],
        [4, 5, PrecThreePostfixOp(), PlusOp(), PrecZeroPostfixOp()],
    ),
    (
        [4, PlusOp(), 5, PrecZeroPostfixOp(), PrecThreePostfixOp()],
        [4, 5, PlusOp(), PrecZeroPostfixOp(), PrecThreePostfixOp()],
    ),
    (
        [4, PrecThreePostfixOp(), PlusOp(), 5, PrecZeroPostfixOp(), PrecThreePostfixOp()],
        [4, PrecThreePostfixOp(), 5, PlusOp(), PrecZeroPostfixOp(), PrecThreePostfixOp()],
    ),
    (
        [4, PlusOp(), 5, PrecZeroPostfixOp(), PlusOp(), 6, PrecThreePostfixOp()],
        [4, 5, PlusOp(), PrecZeroPostfixOp(), 6, PrecThreePostfixOp(), PlusOp()]
    ),
    (
        [4, PlusOp(), 5, PrecThreePostfixOp(), PlusOp(), 6, PrecZeroPostfixOp()],
        [4, 5, PrecThreePostfixOp(), PlusOp(), 6, PlusOp(), PrecZeroPostfixOp()]
    ),
    (
        [4, PlusOp(), 5, PrecThreePostfixOp(), PlusOp(), 6, PrecThreePostfixOp()],
        [4, 5, PrecThreePostfixOp(), PlusOp(), 6, PrecThreePostfixOp(), PlusOp()]
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
    (
        [1, EqualsOp(), '(', 2, ')', TimesOp(), '(', 3, ')'],
        [1, 2, 3, TimesOp(), EqualsOp()]
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

rpn_arg_delimiter_cases = [
    ([ARG_DELIM, ARG_DELIM, ARG_DELIM]          , []),
    ([3, ARG_DELIM, 4, ARG_DELIM, 5]            , [3, 4, 5]),
    (
        [UserFunction('f', [Var('x'), Var('y'), Var('z')], 5), '(', 4, ARG_DELIM, 5, ARG_DELIM, 6, ')'],
        [4, 5, 6, UserFunction('f', [Var('x'), Var('y'), Var('z')], 5)]
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
# Parser.to_tree test cases
#
# These go in as tokens in RPN. The result is checked using repr(node).
#
tree_operand_order_cases = [
    ([1]                           , '1'       ),
    ([1.2]                         , '1.2'     ),
    ([3j]                          , '3j'      ),
    ([3j, 1.2, PlusOp()]           , '3j 1.2 +'),
    ([Var('x')]                    , 'x'       ),
    ([Var('x'), Var('y'), PlusOp()], 'x y +'   ),

    ([Var('x'), Var('y'), PlusOp(), Var('z'), TimesOp()], 'x y + z *'),

    ([UserFunction('f', [], node(5))]                                         , 'f[]'),
    ([3, UserFunction('f', [Var('x')], node(5))]                              , '3 f[x]'),
    ([Var('x'), UserFunction('f', [Var('x')], node(5))]                       , 'x f[x]'),
    ([3, 4, UserFunction('f', [Var('x'), Var('y')], node(5))]                     , '3 4 f[x,y]'),
    ([3, 4, 5, UserFunction('f', [Var('x'), Var('y'), Var('z')], node(5))]      , '3 4 5 f[x,y,z]'),
]

tree_bad_input_cases = [
    [PlusOp()]                                         ,
    [Var('x'), PlusOp()]                               ,
    [Var('x'), PlusOp(), Var('y'), TimesOp()]          ,
    [Var('x'), PlusOp(), Var('y'), Var('z'), TimesOp()],
]

#
# node.reduce test cases
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

tree_reduce_user_funcs_cases = [
    # no arguments
    ([UserFunction('f', [], node(5))]                                 , '5'),
    ([UserFunction('f', [], node(5))]                                 , '5'),
    ([UserFunction('f', [], node(Var('x')))]                          , 'x'),

    # single argument
    ([3, UserFunction('f', [Var('x')], node(5))]                      , '5'),
    ([3, UserFunction('f', [Var('x')], node(Var('x')))]               , '3'),
    ([Var('y'), UserFunction('f', [Var('x')], node(5))]               , '5'),
    ([Var('y'), UserFunction('f', [Var('x')], node(Var('x')))]        , 'y'),

    # multiple arguments
    ([5, Var('z'), UserFunction('f', [Var('x'), Var('y')], node(Var('x')))]        , '5'),
    ([5, Var('z'), UserFunction('f', [Var('x'), Var('y')], node(Var('y')))]        , 'z'),

    ([2, 5, Var('y'), UserFunction('f', [Var('x'), Var('y'), Var('z')], node(5))]  , '5'),
]

tree_replace_constants_cases = [
    ([Pi(), CosOp()], '(-1-0j)'),
    ([E(), LogEOp()], '(1+0j)' ),
]

#
# test cases for parsing.insert_implicit_mult_ops
#
implicit_mult_literals_cases = [
    ([4]       , [4]       ),
    ([3j]      , [3j]      ),
    ([E()]     , [E()]     ),
    ([Var('x')], [Var('x')]),

    ([4, Var('x')], [4, ImplicitMultOp(), Var('x')]),
    ([Var('x'), 4], [Var('x'), ImplicitMultOp(), 4]),
    ([4, Pi()]    , [4, ImplicitMultOp(), Pi()]    ),
    ([Pi(), 4]    , [Pi(), ImplicitMultOp(), 4]    ),

    (
        [E(), 3j, Var('x'), 1.5],
        [E(), ImplicitMultOp(), 3j, ImplicitMultOp(), Var('x'), ImplicitMultOp(), 1.5]
    ),
]

implicit_mult_parens_cases = [
    ([4, '(']       , [4, ImplicitMultOp(), '(']       ),
    ([Var('x'), '('], [Var('x'), ImplicitMultOp(), '(']),
    ([E(), '(']     , [E(), ImplicitMultOp(), '(']     ),
    ([')', 4]       , [')', ImplicitMultOp(), 4]       ),
    ([')', Var('x')], [')', ImplicitMultOp(), Var('x')]),
    ([')', E()]     , [')', ImplicitMultOp(), E()]     ),
    ([')', '(']     , [')', ImplicitMultOp(), '(']     ),
]

implicit_mult_functions_cases = [
    ([CosOp(), '(']              , [CosOp(), '(']                                ),
    ([4, CosOp()]                , [4, TimesOp(), CosOp()]                       ),
    ([Var('x'), CosOp()]         , [Var('x'), TimesOp(), CosOp()]                ),
    ([Pi(), CosOp()]             , [Pi(), TimesOp(), CosOp()]                    ),
    ([')', CosOp()]              , [')', TimesOp(), CosOp()]                     ),
    ([4, FactorialOp(), 5]       , [4, FactorialOp(), ImplicitMultOp(), 5]       ),
    ([5, FactorialOp(), Var('x')], [5, FactorialOp(), ImplicitMultOp(), Var('x')]),
    ([6, FactorialOp(), E()]     , [6, FactorialOp(), ImplicitMultOp(), E()]     ),
    ([7, FactorialOp(), CosOp()] , [7, FactorialOp(), TimesOp(), CosOp()]        ),
]

implicit_mult_combined_cases = [
    (
        [1, DivideOp(), Var('x'),                   Var('y'),            CosOp(), Var('x')],
        [1, DivideOp(), Var('x'), ImplicitMultOp(), Var('y'), TimesOp(), CosOp(), Var('x')]
    ),
    (
        [Var('x'),                   Var('y'), ExponentOp(), Var('y'),                   Var('z')],
        [Var('x'), ImplicitMultOp(), Var('y'), ExponentOp(), Var('y'), ImplicitMultOp(), Var('z')]
    ),
    (
        [4, CosOp(), 5, SinOp(), 4, FactorialOp(), Pi(), Var('y'), CosOp(), E()],
        [4, TimesOp(), CosOp(), 5, TimesOp(), SinOp(), 4, FactorialOp(),
            ImplicitMultOp(), Pi(), ImplicitMultOp(), Var('y'), TimesOp(), CosOp(), E()]
    ),
    (
        [4, CosOp(), 5, Var('x'), TimesOp(), 5, SinOp(), 4, Pi(), Var('y'), CosOp(), E()],
        [4, TimesOp(), CosOp(), 5, ImplicitMultOp(), Var('x'), TimesOp(), 5, TimesOp(),
            SinOp(), 4, ImplicitMultOp(), Pi(), ImplicitMultOp(), Var('y'), TimesOp(), CosOp(), E()]
    ),
    (
        ['(', 4, PlusOp(), 3, ')',                   '(', 4, PlusOp(), 2, ')'],
        ['(', 4, PlusOp(), 3, ')', ImplicitMultOp(), '(', 4, PlusOp(), 2, ')']
    )
]

#
# test cases parsing.transform_if_negation
#
negation_at_beginning_cases = [
    (
        ([SubOp()], 0),     # tokens, index-of-concern
        ([NegationOp()], 0)   # tokens, change in len(tokens)
    ),
    (
        ([SubOp(), 1], 0),
        ([NegationOp(), 1], 0)
    ),
    (
        ([SubOp(), Var('x')], 0),
        ([NegationOp(), Var('x')], 0)
    ),
    (
        ([SubOp(), Pi()], 0),
        ([NegationOp(), Pi()], 0)
    ),
    (
        ([SubOp(), CosOp()], 0),
        ([NegationOp(), CosOp()], 0)
    ),
]

negation_plus_minus_cases = [
    (
        ([PlusOp(), SubOp()], 1),   # tokens, index-of-concern
        ([NegationOp()], -1)        # tokens, change in len(tokens)
    ),
    (
        ([PlusOp(), SubOp(), Var('x')], 1),
        ([NegationOp(), Var('x')], -1)
    ),
    (
        ([Var('x'), PlusOp(), SubOp(), Var('y')], 2),
        ([Var('x'), SubOp(), Var('y')], -1)
    ),
    (
        ([E(), PlusOp(), SubOp(), Pi()], 2),
        ([E(), SubOp(), Pi()], -1)
    ),
    (
        ([3, FactorialOp(), PlusOp(), SubOp(), CosOp(), 4j], 3),
        ([3, FactorialOp(), SubOp(), CosOp(), 4j], -1)
    )
]

negation_minus_minus_cases = [
    (([SubOp(), SubOp()], 0)          , ([], -2)                  ),
    (([Var('x'), SubOp(), SubOp()], 2), ([Var('x'), PlusOp()], -1)),
    (
        ([Var('x'), SubOp(), SubOp(), SubOp(), Var('y')], 2),
        ([Var('x'), PlusOp(), SubOp(), Var('y')], -1)
    ),
]

negation_func_minus_cases = [
    (([TimesOp(), SubOp()]    , 1), ([TimesOp(), NegationOp()]  , 0)),
    (([DivideOp(), SubOp()]   , 1), ([DivideOp(), NegationOp()] , 0)),
    (([ModulusOp(), SubOp()]  , 1), ([ModulusOp(), NegationOp()], 0)),
    (([CosOp(), SubOp()]      , 1), ([CosOp(), NegationOp()]    , 0)),
    (([FactorialOp(), SubOp()], 1), ([FactorialOp(), SubOp()]   , 0)),
]

#
# test cases for parsing.apply_transformations
#
apply_implicit_mult_cases = [
    ([4, Var('x')], [4, ImplicitMultOp(), Var('x')]),
    ([Var('x'), 4], [Var('x'), ImplicitMultOp(), 4]),
    ([4, Pi()]    , [4, ImplicitMultOp(), Pi()]    ),
    ([Pi(), 4]    , [Pi(), ImplicitMultOp(), 4]    ),
    (
        [E(), 3j, Var('x'), 1.5],
        [E(), ImplicitMultOp(), 3j, ImplicitMultOp(), Var('x'), ImplicitMultOp(), 1.5]
    ),
    (
        [CosOp(), Var('x'), Var('y'), SinOp(), Var('x'), Var('y')],
        [CosOp(), Var('x'), ImplicitMultOp(), Var('y'), TimesOp(),
            SinOp(), Var('x'), ImplicitMultOp(), Var('y')],
    ),
]

apply_negation_cases = [
    ([Var('x'), SubOp(), 3]                  , [Var('x'), SubOp(), 3] ),
    ([Var('x'), SubOp(), SubOp(), 3]         , [Var('x'), PlusOp(), 3]),
    ([Var('x'), SubOp(), SubOp(), SubOp(), 3], [Var('x'), SubOp(), 3] ),

    ([Var('x'), PlusOp(), SubOp(), 3]                                      , [Var('x'), SubOp(), 3] ),
    ([Var('x'), PlusOp(), SubOp(), PlusOp(), SubOp(), 3]                   , [Var('x'), PlusOp(), 3]),
    ([Var('x'), PlusOp(), SubOp(), SubOp(), PlusOp(), SubOp(), 3]          , [Var('x'), SubOp(), 3] ),
    ([Var('x'), PlusOp(), SubOp(), PlusOp(), SubOp(), PlusOp(), SubOp(), 3], [Var('x'), SubOp(), 3] ),
    ([Var('x'), PlusOp(), SubOp(), SubOp(), SubOp(), PlusOp(), SubOp(), 3] , [Var('x'), PlusOp(), 3]),

    ([Var('x'), SubOp(), PlusOp(), SubOp(), 3]                   , [Var('x'), PlusOp(), 3]),
    ([Var('x'), SubOp(), PlusOp(), SubOp(), PlusOp(), SubOp(), 3], [Var('x'), SubOp(), 3] ),
    ([Var('x'), SubOp(), SubOp(), SubOp(), PlusOp(), SubOp(), 3] , [Var('x'), PlusOp(), 3]),

    ([SubOp(), Var('x')]                   , [NegationOp(), Var('x')]                        ),
    ([SubOp(), SubOp(), Var('x')]          , [Var('x')]                                      ),
    (['(', SubOp(), Var('x'), ')']         , ['(', NegationOp(), Var('x'), ')']              ),
    (['(', SubOp(), SubOp(), Var('x'), ')'], ['(', NegationOp(), NegationOp(), Var('x'), ')']),
    ([SubOp(), '(', SubOp(), Var('x'), ')'], [NegationOp(), '(', NegationOp(), Var('x'), ')']),
    ([CosOp(), SubOp(), Var('x')]          , [CosOp(), NegationOp(), Var('x')]               ),
    ([CosOp(), SubOp(), SubOp(), Var('x')] , [CosOp(), NegationOp(), NegationOp(), Var('x')] ),
    ([CosOp(), '(', SubOp(), Var('x'), ')'], [CosOp(), '(', NegationOp(), Var('x'), ')']     ),
    (
        [CosOp(), '(', SubOp(), SubOp(), Var('x'), ')'],
        [CosOp(), '(', NegationOp(), NegationOp(), Var('x'), ')']),
    (
        [Var('x'), PlusOp(), SubOp(), CosOp(), SubOp(), SubOp(), Var('x')],
        [Var('x'), SubOp(), CosOp(), NegationOp(), NegationOp(), Var('x')]
    ),

    # we do not resolve multiple plus-signs in a row
    ([Var('x'), PlusOp(), PlusOp(), 3]          , [Var('x'), PlusOp(), PlusOp(), 3]          ),
    ([Var('x'), PlusOp(), PlusOp(), PlusOp(), 3], [Var('x'), PlusOp(), PlusOp(), PlusOp(), 3]),
    ([Var('x'), SubOp(), SubOp(), PlusOp(), 3]  , [Var('x'), PlusOp(), PlusOp(), 3]          ),

    # we also do not resolve '-+' ocurrences
    ([Var('x'), SubOp(), PlusOp(), 3]       , [Var('x'), SubOp(), PlusOp(), 3]),
    ([Var('x'), PlusOp(), SubOp(), PlusOp(), 3]  , [Var('x'), SubOp(), PlusOp(), 3]),
]

apply_combined_cases = [
    # need more tests here
    (
        [1, DivideOp(), SubOp(),      Var('x'),                   Var('y')],
        [1, DivideOp(), NegationOp(), Var('x'), ImplicitMultOp(), Var('y')]
    ),
    (
        [SubOp(),      Var('x'),            CosOp(), SubOp(),      3,                   Var('x')],
        [NegationOp(), Var('x'), TimesOp(), CosOp(), NegationOp(), 3, ImplicitMultOp(), Var('x')]
    ),
]
