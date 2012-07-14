import unittest
import test_util
import liberal_parsing_test_cases as lp_cases
from parsing import liberal_parsing

class InsertImplicitMultOpsTestCases(unittest.TestCase):

    def setUp(self):
        self.literals_cases  = lp_cases.implicit_mult_literals_cases
        self.parens_cases    = lp_cases.implicit_mult_parens_cases
        self.functions_cases = lp_cases.implicit_mult_functions_cases
        self.combined_cases  = lp_cases.implicit_mult_combined_cases
    
    @staticmethod
    def get_test_result(tokens):
        liberal_parsing.insert_implicit_mult_ops(tokens)
        return tokens
    
    def test_literals_handling(self):
        test_util.run_through_cases(self, self.literals_cases, self.get_test_result)
    def test_parens_handling(self):
        test_util.run_through_cases(self, self.parens_cases, self.get_test_result)
    def test_functions_handling(self):
        test_util.run_through_cases(self, self.functions_cases, self.get_test_result)
    def test_combined_cases(self):
        test_util.run_through_cases(self, self.combined_cases, self.get_test_result)

class TransformIfNegationTestCases(unittest.TestCase):
    
    def setUp(self):
        self.neg_at_start_cases = lp_cases.negation_at_beginning_cases
        self.plus_neg_cases   = lp_cases.negation_plus_minus_cases
        self.minus_neg_cases  = lp_cases.negation_minus_minus_cases
        self.func_neg_cases   = lp_cases.negation_func_minus_cases
    
    @staticmethod
    def get_test_result(case):
            tokens, i = case
            len_diff = liberal_parsing.transform_if_negation(tokens, i)
            return tokens, len_diff
    
    def test_negation_at_beginning(self):
        test_util.run_through_cases(self, self.neg_at_start_cases, self.get_test_result)
    def test_plus_neg_handling(self):
        test_util.run_through_cases(self, self.plus_neg_cases, self.get_test_result)
    def test_minus_neg_handling(self):
        test_util.run_through_cases(self, self.minus_neg_cases, self.get_test_result)
    def test_func_neg_handling(self):
        test_util.run_through_cases(self, self.func_neg_cases, self.get_test_result)
        
class ApplyTransformationsTestCases(unittest.TestCase):
    
    def setUp(self):
        self.implicit_mult_cases = lp_cases.apply_implicit_mult_cases
        self.negation_cases      = lp_cases.apply_negation_cases
        self.combined_cases      = lp_cases.apply_combined_cases
    
    @staticmethod
    def get_test_result(case):
        tokens = case
        liberal_parsing.apply_transformations(tokens)
        return tokens
    
    def test_implicit_mult_support(self):
        test_util.run_through_cases(self, self.implicit_mult_cases, self.get_test_result)
    def test_negation_support(self):
        test_util.run_through_cases(self, self.negation_cases, self.get_test_result)
    def test_combined_support(self):
        test_util.run_through_cases(self, self.combined_cases, self.get_test_result)
        