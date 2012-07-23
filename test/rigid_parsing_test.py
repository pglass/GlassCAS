'''
Don't run this. Use GlassCAS/run_tests.py.
'''

import unittest
import test.rigid_parsing_test_cases as rp_cases
from test.test_util import run_through_cases
from parsing import rigid_parsing


class TokenizeTestCases(unittest.TestCase):
    '''
    - Test that all possible tokens are recognized properly:
        Constants
        Functions/operators
        Variables
        Parens
        Integers/Reals
        Complex numbers
    - Test that SyntaxErrors are raise for bad inputs.
    '''
    
    def setUp(self):
        self.constants_cases = rp_cases.tokenize_constants_cases
        self.functions_cases = rp_cases.tokenize_functions_cases
        self.variables_cases = rp_cases.tokenize_variables_cases
        self.parens_cases    = rp_cases.tokenize_parens_cases
        self.reals_cases     = rp_cases.tokenize_reals_cases
        self.complex_cases   = rp_cases.tokenize_complex_cases
        self.combined_cases  = rp_cases.tokenize_combined_cases
        self.user_func_cases = rp_cases.tokenize_user_functions_cases
        self.bad_input_cases = rp_cases.tokenize_bad_input_cases
        
    def test_constants(self):
        run_through_cases(self, self.constants_cases, rigid_parsing.tokenize)
        
    def test_functions(self):
        run_through_cases(self, self.functions_cases, rigid_parsing.tokenize)

    def test_variables(self):
        run_through_cases(self, self.variables_cases, rigid_parsing.tokenize)

    def test_parens(self):
        run_through_cases(self, self.parens_cases, rigid_parsing.tokenize)

    def test_reals(self):
        run_through_cases(self, self.reals_cases, rigid_parsing.tokenize)

    def test_complex_numbers(self):
        run_through_cases(self, self.complex_cases, rigid_parsing.tokenize)

    def test_combined(self):
        run_through_cases(self, self.combined_cases, rigid_parsing.tokenize)

    def test_user_functions(self):
        run_through_cases(self, self.user_func_cases, rigid_parsing.tokenize)
        
    def test_bad_inputs(self):
        for case in self.bad_input_cases:
            with self.assertRaises(SyntaxError):
                rigid_parsing.tokenize(case)
    
class RPNConversionTestCases(unittest.TestCase):
    '''
    - Test basic algorithm correctness.
    - Test that precedences are taken into account.
    - Test that parentheses change order of evalutation.
    - Test that SyntaxErrors are raised for mismatched parentheses.
    '''
    
    def setUp(self):
        self.basic_cases      = rp_cases.rpn_basic_correctness_cases
        self.precedence_cases = rp_cases.rpn_precedence_cases
        self.parens_cases     = rp_cases.rpn_parens_cases
        self.user_func_cases  = rp_cases.rpn_user_functions_cases
        self.bad_input_cases  = rp_cases.rpn_bad_input_cases
        
    def test_basic_correctness(self):
        run_through_cases(self, self.basic_cases, rigid_parsing.to_RPN)
        
    def test_precedences(self):
        run_through_cases(self, self.precedence_cases, rigid_parsing.to_RPN)
            
    def test_parens(self):
        run_through_cases(self, self.parens_cases, rigid_parsing.to_RPN)

    def test_user_functions(self):
        run_through_cases(self, self.user_func_cases, rigid_parsing.to_RPN)
        
    def test_bad_inputs(self):
        for key in self.bad_input_cases:
            with self.assertRaises(SyntaxError):
                rigid_parsing.to_RPN(key)
    
class TreeTestCases(unittest.TestCase):
    '''
    - Test that operands are put in the correct order.
    - Test that the tree reduces to the correct value.
    - Test that replacing constants with approximate values
      works and can be enabled/disabled.
    '''
    
    def setUp(self):
        self.operand_order_cases = rp_cases.tree_operand_order_cases
        self.reduce_cases        = rp_cases.tree_reduce_cases
        self.sub_constants_cases = rp_cases.tree_replace_constants_cases
        self.bad_input_cases     = rp_cases.tree_bad_input_cases
            
    def test_operand_order(self):
        get_test_result = lambda case: repr(rigid_parsing.to_tree(case))
        run_through_cases(self, self.operand_order_cases, get_test_result)
    
    def test_reduce_value(self):
        def get_test_result(case):
            tree = rigid_parsing.to_tree(case)
            tree.reduce()
            return repr(tree)
            
        run_through_cases(self, self.reduce_cases, get_test_result)
        
    def test_constant_replacement(self):
        def get_test_result(case):
            tree = rigid_parsing.to_tree(case)
            tree.reduce(replace_constants = True)
            return repr(tree)
        
        run_through_cases(self, self.sub_constants_cases, get_test_result)
    
    def test_bad_inputs(self):
        for key in self.bad_input_cases:
            with self.assertRaises(SyntaxError):
                tree = rigid_parsing.to_tree(key)
