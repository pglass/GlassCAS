'''
liberal_parsing_tests_cases.py

Define test cases for all functions in liberal_parsing.py
'''

from parsing.parser_definitions import *
#
# test cases for liberal_parsing.insert_implicit_mult_ops
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
# test cases liberal_parsing.transform_if_negation
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
# test cases for liberal_parsing.apply_transformations
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
