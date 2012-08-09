'''
Don't run this. Use GlassCAS/run_tests.py.
'''

import unittest
import parsing.parsing
import test.parsing_test_cases as pt_cases
import test.test_util


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
        self.constants_cases = pt_cases.tokenize_constants_cases
        self.functions_cases = pt_cases.tokenize_functions_cases
        self.variables_cases = pt_cases.tokenize_variables_cases
        self.parens_cases    = pt_cases.tokenize_parens_cases
        self.reals_cases     = pt_cases.tokenize_reals_cases
        self.complex_cases   = pt_cases.tokenize_complex_cases
        self.combined_cases  = pt_cases.tokenize_combined_cases
        self.user_func_cases = pt_cases.tokenize_user_functions_cases
        self.arg_delim_cases = pt_cases.tokenize_arg_delimiter_cases
        self.bad_input_cases = pt_cases.tokenize_bad_input_cases
        
    @staticmethod
    def get_test_result(case):
        # do tests without worrying about the parser's symbol table
        parser = parsing.parsing.Parser()
        return parser.tokenize(case)
        
    def test_constants(self):
        test.test_util.run_through_cases(self, self.constants_cases, self.get_test_result)
        
    def test_functions(self):
        test.test_util.run_through_cases(self, self.functions_cases, self.get_test_result)

    def test_variables(self):
        test.test_util.run_through_cases(self, self.variables_cases, self.get_test_result)

    def test_parens(self):
        test.test_util.run_through_cases(self, self.parens_cases, self.get_test_result)

    def test_reals(self):
        test.test_util.run_through_cases(self, self.reals_cases, self.get_test_result)

    def test_complex_numbers(self):
        test.test_util.run_through_cases(self, self.complex_cases, self.get_test_result)
        
    def test_combined(self):
        test.test_util.run_through_cases(self, self.combined_cases, self.get_test_result)

    def test_user_functions(self):
        test.test_util.run_through_cases(self, self.user_func_cases, self.get_test_result)
    
    def test_arg_delimiter(self):
        test.test_util.run_through_cases(self, self.arg_delim_cases, self.get_test_result)
    
    def test_bad_inputs(self):
        for case in self.bad_input_cases:
            with self.assertRaises(SyntaxError):
                self.get_test_result(case)
    
class RPNConversionTestCases(unittest.TestCase):
    '''
    - Test basic algorithm correctness.
    - Test that precedences are taken into account.
    - Test that parentheses change order of evalutation.
    - Test that SyntaxErrors are raised for mismatched parentheses.
    '''
    
    def setUp(self):
        self.basic_cases      = pt_cases.rpn_basic_correctness_cases
        self.precedence_cases = pt_cases.rpn_precedence_cases
        self.prefix_cases     = pt_cases.rpn_prefix_cases
        self.postfix_cases    = pt_cases.rpn_postfix_cases
        self.parens_cases     = pt_cases.rpn_parens_cases
        self.user_func_cases  = pt_cases.rpn_user_functions_cases
        self.arg_delim_cases  = pt_cases.rpn_arg_delimiter_cases
        self.bad_input_cases  = pt_cases.rpn_bad_input_cases
        
    @staticmethod
    def get_test_result(case):
        # do tests without worrying about the parser's symbol table
        parser = parsing.parsing.Parser()
        return parser.to_rpn(case)
        
    def test_basic_correctness(self):
        test.test_util.run_through_cases(self, self.basic_cases, self.get_test_result)
        
    def test_precedences(self):
        test.test_util.run_through_cases(self, self.precedence_cases, self.get_test_result)

    def test_prefix_support(self):
        test.test_util.run_through_cases(self, self.prefix_cases, self.get_test_result)
        
    def test_postfix_support(self):
        test.test_util.run_through_cases(self, self.postfix_cases, self.get_test_result)
    
    def test_parens(self):
        test.test_util.run_through_cases(self, self.parens_cases, self.get_test_result)

    def test_user_functions(self):
        test.test_util.run_through_cases(self, self.user_func_cases, self.get_test_result)

    def test_arg_delimiters(self):
        test.test_util.run_through_cases(self, self.arg_delim_cases, self.get_test_result)
    
    def test_bad_inputs(self):
        for key in self.bad_input_cases:
            with self.assertRaises(SyntaxError):
                self.get_test_result(key)
    
class TreeTestCases(unittest.TestCase):
    '''
    - Test that operands are put in the correct order.
    - Test that the tree reduces to the correct value.
    - Test that replacing constants with approximate values
      works and can be enabled/disabled.
    '''
    
    def setUp(self):
        self.operand_order_cases = pt_cases.tree_operand_order_cases
        self.reduce_cases        = pt_cases.tree_reduce_cases
        self.user_funcs_cases    = pt_cases.tree_reduce_user_funcs_cases
        self.sub_constants_cases = pt_cases.tree_replace_constants_cases
        self.bad_input_cases     = pt_cases.tree_bad_input_cases
    
    def test_operand_order(self):
        def get_test_result(case):
            return repr(parsing.parsing.Parser().to_tree(case))
            
        test.test_util.run_through_cases(self, self.operand_order_cases, get_test_result)
    
    def test_reduce_predefined_ops(self):
        def get_test_result(case):
            tree = parsing.parsing.Parser().to_tree(case)
            tree.reduce()
            return repr(tree)
            
        test.test_util.run_through_cases(self, self.reduce_cases, get_test_result)
    
    def test_reduce_user_funcs(self):
        def get_test_result(case):
            tree = parsing.parsing.Parser().to_tree(case)
            tree.reduce()
            return repr(tree)
            
        test.test_util.run_through_cases(self, self.user_funcs_cases, get_test_result)
        
    def test_constant_replacement(self):
        def get_test_result(case):
            tree = parsing.parsing.Parser().to_tree(case)
            tree.reduce(replace_constants = True)
            return repr(tree)
        
        test.test_util.run_through_cases(self, self.sub_constants_cases, get_test_result)
    
    def test_bad_inputs(self):
        for key in self.bad_input_cases:
            with self.assertRaises(SyntaxError):
                parsing.parsing.Parser().to_tree(key)

class InsertImplicitMultOpsTestCases(unittest.TestCase):

    def setUp(self):
        self.literals_cases  = pt_cases.implicit_mult_literals_cases
        self.parens_cases    = pt_cases.implicit_mult_parens_cases
        self.functions_cases = pt_cases.implicit_mult_functions_cases
        self.combined_cases  = pt_cases.implicit_mult_combined_cases
    
    @staticmethod
    def get_test_result(tokens):
        parsing.parsing.insert_implicit_mult_ops(tokens)
        return tokens
    
    def test_literals_handling(self):
        test.test_util.run_through_cases(self, self.literals_cases, self.get_test_result)
    def test_parens_handling(self):
        test.test_util.run_through_cases(self, self.parens_cases, self.get_test_result)
    def test_functions_handling(self):
        test.test_util.run_through_cases(self, self.functions_cases, self.get_test_result)
    def test_combined_cases(self):
        test.test_util.run_through_cases(self, self.combined_cases, self.get_test_result)

class TransformIfNegationTestCases(unittest.TestCase):
    
    def setUp(self):
        self.neg_at_start_cases = pt_cases.negation_at_beginning_cases
        self.plus_neg_cases   = pt_cases.negation_plus_minus_cases
        self.minus_neg_cases  = pt_cases.negation_minus_minus_cases
        self.func_neg_cases   = pt_cases.negation_func_minus_cases
    
    @staticmethod
    def get_test_result(case):
            tokens, i = case
            len_diff = parsing.parsing.transform_if_negation(tokens, i)
            return tokens, len_diff
    
    def test_negation_at_beginning(self):
        test.test_util.run_through_cases(self, self.neg_at_start_cases, self.get_test_result)
    def test_plus_neg_handling(self):
        test.test_util.run_through_cases(self, self.plus_neg_cases, self.get_test_result)
    def test_minus_neg_handling(self):
        test.test_util.run_through_cases(self, self.minus_neg_cases, self.get_test_result)
    def test_func_neg_handling(self):
        test.test_util.run_through_cases(self, self.func_neg_cases, self.get_test_result)
        
class ApplyTransformationsTestCases(unittest.TestCase):
    
    def setUp(self):
        self.implicit_mult_cases = pt_cases.apply_implicit_mult_cases
        self.negation_cases      = pt_cases.apply_negation_cases
        self.combined_cases      = pt_cases.apply_combined_cases
    
    @staticmethod
    def get_test_result(case):
        tokens = case
        parsing.parsing.apply_transformations(tokens)
        return tokens
    
    def test_implicit_mult_support(self):
        test.test_util.run_through_cases(self, self.implicit_mult_cases, self.get_test_result)
    def test_negation_support(self):
        test.test_util.run_through_cases(self, self.negation_cases, self.get_test_result)
    def test_combined_support(self):
        test.test_util.run_through_cases(self, self.combined_cases, self.get_test_result)
        