'''
liberal_parsing_tests_cases.py

Define test cases for all functions in liberal_parsing.py
'''

from parsing.parser_definitions import NEG_OP
from parsing.parser_definitions import IMPLICIT_MULT as IM_OP

#
# test cases for liberal_parsing.insert_implicit_mult_ops
#
implicit_mult_literals_cases = [
    (['4',]     , ['4']),
    (['3j',]    , ['3j']),
    (['e',]     , ['e']),
    (['x',]     , ['x']),
    
    (['4', 'x'] , ['4', IM_OP, 'x']),
    (['x', '4'] , ['x', IM_OP, '4']),
    (['4', 'pi'], ['4', IM_OP, 'pi']),
    (['pi', '4'], ['pi', IM_OP, '4']),
    
    (['e', '3j', 'x', '1.5'] , ['e', IM_OP, '3j', IM_OP, 'x', IM_OP, '1.5']),
]

implicit_mult_parens_cases = [
    (['4', '('], ['4', IM_OP, '(']),
    (['x', '('], ['x', IM_OP, '(']),
    (['e', '('], ['e', IM_OP, '(']),
    ([')', '4'], [')', IM_OP, '4']),
    ([')', 'x'], [')', IM_OP, 'x']),
    ([')', 'e'], [')', IM_OP, 'e']),
    ([')', '('], [')', IM_OP, '(']),
]

implicit_mult_functions_cases = [
    (['cos', '(']     , ['cos', '(']),
    (['4', 'cos']     , ['4', '*', 'cos']),
    (['x', 'cos']     , ['x', '*', 'cos']),
    (['pi', 'cos']    , ['pi', '*', 'cos']),
    ([')', 'cos']     , [')', '*', 'cos']),
    (['4', '!', '5']  , ['4', '!', IM_OP, '5']),
    (['5', '!', 'x']  , ['5', '!', IM_OP, 'x']),
    (['6', '!', 'e']  , ['6', '!', IM_OP, 'e']),
    (['7', '!', 'cos'], ['7', '!', '*', 'cos']),
]

implicit_mult_combined_cases = [
    (
        ['1', '/', 'x',        'y',      'cos', 'x'], 
        ['1', '/', 'x', IM_OP, 'y', '*', 'cos', 'x']
    ),
    (
        ['x',        'y', '^', 'y',        'z'],
        ['x', IM_OP, 'y', '^', 'y', IM_OP, 'z']
    ),
    (
        ['4',      'cos', '5',      'sin', '4', '!',        'pi',        'y',      'cos', 'e'] , 
        ['4', '*', 'cos', '5', '*', 'sin', '4', '!', IM_OP, 'pi', IM_OP, 'y', '*', 'cos', 'e']
    ),
    (
        ['4',      'cos', '5',        'x', '*', '5',      'sin', '4',        'pi',        'y',      'cos', 'e'], 
        ['4', '*', 'cos', '5', IM_OP, 'x', '*', '5', '*', 'sin', '4', IM_OP, 'pi', IM_OP, 'y', '*', 'cos', 'e']
    ),
    (
        ['(', '4', '+', '3', ')',        '(', '4', '+', '2', ')'],    
        ['(', '4', '+', '3', ')', IM_OP, '(', '4', '+', '2', ')']
    )
]

#
# test cases liberal_parsing.transform_if_negation
#
negation_at_beginning_cases = [
    (
        (['-'], 0),     # tokens, index-of-concern
        ([NEG_OP], 0)   # tokens, change in len(tokens)
    ),
    (   
        (['-', '1'], 0), 
        ([NEG_OP, '1'], 0)
    ),
    (
        (['-', 'x'], 0),
        ([NEG_OP, 'x'], 0)
    ),
    (
        (['-', 'pi'], 0),
        ([NEG_OP, 'pi'], 0)
    ),
    (
        (['-', 'cos'], 0),
        ([NEG_OP, 'cos'], 0)
    ),
]

negation_plus_minus_cases = [
    (
        (['+', '-'], 1),   # tokens, index-of-concern
        ([NEG_OP], -1)     # tokens, change in len(tokens)
    ),
    (
        (['+', '-', 'x'], 1),
        ([NEG_OP, 'x'], -1)
    ),
    (
        (['x', '+', '-', 'y'], 2), 
        (['x', '-', 'y'], -1)
    ),
    (
        (['e', '+', '-', 'pi'], 2),
        (['e', '-', 'pi'], -1)
    ),
    (
        (['3', '!', '+', '-', 'cos', '4j'], 3),
        (['3', '!', '-', 'cos', '4j'], -1)
    )
]

negation_minus_minus_cases = [
    (
        (['-', '-'], 0),
        ([], -2)
    ),
    (
        (['x', '-', '-'], 2),
        (['x', '+'], -1)
    ),
    (
        (['x', '-', '-', '-', 'y'], 2),
        (['x', '+', '-', 'y'], -1)
    ),
]

negation_func_minus_cases = [
    ((['*', '-']  , 1), (['*', NEG_OP]  , 0)),
    ((['/', '-']  , 1), (['/', NEG_OP]  , 0)),
    ((['%', '-']  , 1), (['%', NEG_OP]  , 0)),
    ((['cos', '-'], 1), (['cos', NEG_OP], 0)),
    
    ((['!', '-']  , 1), (['!', '-']     , 0)),
]

#
# test cases for liberal_parsing.apply_transformations
#
apply_implicit_mult_cases = [
    (['4', 'x'] , ['4', IM_OP, 'x'] ),
    (['x', '4'] , ['x', IM_OP, '4'] ),
    (['4', 'pi'], ['4', IM_OP, 'pi']),
    (['pi', '4'], ['pi', IM_OP, '4']),

    (['e', '3j', 'x', '1.5'] , ['e', IM_OP, '3j', IM_OP, 'x', IM_OP, '1.5']),
    (
        ['cos', 'x',        'y',      'sin', 'x',        'y'],
        ['cos', 'x', IM_OP, 'y', '*', 'sin', 'x', IM_OP, 'y'],
    ),
]
apply_negation_cases = [
    (['x', '-', '3']            , ['x', '-', '3']),
    (['x', '-', '-', '3']       , ['x', '+', '3']),
    (['x', '-', '-', '-', '3']  , ['x', '-', '3']),
    
    (['x', '+', '-', '3']                       , ['x', '-', '3']),
    (['x', '+', '-', '+', '-', '3']             , ['x', '+', '3']),
    (['x', '+', '-', '-', '+', '-', '3']        , ['x', '-', '3']),
    (['x', '+', '-', '+', '-', '+', '-', '3']   , ['x', '-', '3']),
    (['x', '+', '-', '-', '-', '+', '-', '3']   , ['x', '+', '3']),

    (['x', '-', '+', '-', '3']            , ['x', '+', '3']),
    (['x', '-', '+', '-', '+', '-', '3']  , ['x', '-', '3']),
    (['x', '-', '-', '-', '+', '-', '3']  , ['x', '+', '3']),
    
    (['-', 'x']                     , [NEG_OP, 'x']),
    (['-', '-', 'x']                , ['x']),
    (['(', '-', 'x', ')']           , ['(', NEG_OP, 'x', ')']),
    (['(', '-', '-', 'x', ')']      , ['(', NEG_OP, NEG_OP, 'x', ')']),
    (['-', '(', '-', 'x', ')']      , [NEG_OP, '(', NEG_OP, 'x', ')']),
    (['cos', '-', 'x']              , ['cos', NEG_OP, 'x']),
    (['cos', '-', '-', 'x']         , ['cos', NEG_OP, NEG_OP, 'x']),
    (['cos', '(', '-', 'x', ')']    , ['cos', '(', NEG_OP, 'x', ')']),
    (
        ['cos', '(', '-', '-', 'x', ')'], 
        ['cos', '(', NEG_OP, NEG_OP, 'x', ')']),
    (
        ['x', '+', '-', 'cos', '-', '-', 'x'], 
        ['x', '-', 'cos', NEG_OP, NEG_OP, 'x']
    ),
    
    # we do not resolve multiple plus-signs in a row
    (['x', '+', '+', '3']       , ['x', '+', '+', '3']),
    (['x', '+', '+', '+', '3']  , ['x', '+', '+', '+', '3']),
    (['x', '-', '-', '+', '3']  , ['x', '+', '+', '3']),
    
    # we also do not resolve ['-', '+'] ocurrences
    (['x', '-', '+', '3']       , ['x', '-', '+', '3']),
    (['x', '+', '-', '+', '3']  , ['x', '-', '+', '3']),
]

apply_combined_cases = [
    # need more tests here
    (
        ['1', '/', '-', 'x', 'y'],
        ['1', '/', NEG_OP, 'x', IM_OP, 'y']
    ),
    (
        ['-',    'x',      'cos', '-',    '3',        'x'],
        [NEG_OP, 'x', '*', 'cos', NEG_OP, '3', IM_OP, 'x']
    ),
]
