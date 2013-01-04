import unittest

from ..parsing import parsing
from .. import visitors
from . import expansion_test_cases as exp_cases
from . import test_util

class ExpansionTestCases(unittest.TestCase):
    '''
    This tests the visitors.Expander.visit method.
    '''

    def setUp(self):
        self.distribution_plus_cases = exp_cases.distribution_plus_cases
        self.distribution_minus_cases = exp_cases.distribution_minus_cases
        self.distribution_implicit_mult_cases = exp_cases.distribution_implicit_mult_cases
        self.distribution_division_cases = exp_cases.distribution_division_cases
        self.distribution_division_and_multiplication_cases = exp_cases.distribution_division_and_multiplication_cases
        
    @staticmethod
    def get_test_result(case):
        tree = parsing.Parser().parse(case)
        result = visitors.Expander().visit(tree).reduce()
        return repr(result)

    @staticmethod
    def get_expected_result(val):
        expected_result = parsing.Parser().parse(val)
        return repr(expected_result)

    def test_distribution_over_addition(self):
        test_util.run_through_cases(self, self.distribution_plus_cases, self.get_test_result, self.get_expected_result)

    def test_distribution_over_subtraction(self):
        test_util.run_through_cases(self, self.distribution_minus_cases, self.get_test_result, self.get_expected_result)

    def test_distribution_with_implicit_multiplication(self):
        test_util.run_through_cases(self, self.distribution_implicit_mult_cases, self.get_test_result, self.get_expected_result)

    def test_distribution_with_division(self):
        test_util.run_through_cases(self, self.distribution_division_cases, self.get_test_result, self.get_expected_result)

    def test_distribution_with_division_and_multiplication(self):
        test_util.run_through_cases(self, self.distribution_division_and_multiplication_cases, self.get_test_result, self.get_expected_result)
