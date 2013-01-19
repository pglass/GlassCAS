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
        self.distribution_negation_cases = exp_cases.distribution_negation_cases
        self.expand_integer_power_cases = exp_cases.expand_integer_power_cases
        
    @staticmethod
    def get_test_result(case):
        # each case parses to have an ExpandOp as the root
        tree = parsing.Parser().parse(case)
        result = tree.value.apply(*tree.children)
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

    def test_distribution_with_negation(self):
        test_util.run_through_cases(self, self.distribution_negation_cases, self.get_test_result, self.get_expected_result)

    def test_expand_integer_powers(self):
        test_util.run_through_cases(self, self.expand_integer_power_cases, self.get_test_result, self.get_expected_result)

class FlatteningTestCases(unittest.TestCase):

    def setUp(self):
        self.flatten_addition_cases = exp_cases.flatten_addition_cases
        self.flatten_multiplication_cases = exp_cases.flatten_multiplication_cases
        self.flatten_add_and_mult_cases = exp_cases.flatten_add_and_mult_cases

    @staticmethod
    def get_test_result(case):
        tree = parsing.Parser().parse(case)
        result = tree.accept(visitors.Flattener())
        return repr(result)

    def test_flatten_additions(self):
        test_util.run_through_cases(self, self.flatten_addition_cases, self.get_test_result)
    
    def test_flatten_multiplications(self):
        test_util.run_through_cases(self, self.flatten_multiplication_cases, self.get_test_result)
    
    def test_flatten_additions_and_multiplications(self):
        test_util.run_through_cases(self, self.flatten_add_and_mult_cases, self.get_test_result)

class UnflatteningTestCases(unittest.TestCase):
    def setUp(self):
        self.default_unflatten_addition_cases = exp_cases.default_unflatten_addition_cases
        self.default_unflatten_multiplication_cases = exp_cases.default_unflatten_multiplication_cases
        self.default_unflatten_add_and_mult_cases = exp_cases.default_unflatten_add_and_mult_cases
        
        self.balanced_unflatten_addition_cases = exp_cases.balanced_unflatten_addition_cases
        self.balanced_unflatten_multiplication_cases = exp_cases.balanced_unflatten_multiplication_cases
        self.balanced_unflatten_add_and_mult_cases = exp_cases.balanced_unflatten_add_and_mult_cases

    @staticmethod
    def get_default_mode_test_result(case):
        tree = parsing.Parser().parse(case)
        flattened_tree = tree.accept(visitors.Flattener())
        result = flattened_tree.accept(visitors.Unflattener(mode = visitors.Unflattener.DEFAULT_MODE))
        return repr(result)

    @staticmethod
    def get_balanced_mode_test_result(case):
        tree = parsing.Parser().parse(case)
        flattened_tree = tree.accept(visitors.Flattener())
        result = flattened_tree.accept(visitors.Unflattener(mode = visitors.Unflattener.BALANCED_MODE))
        return repr(result)

    def test_default_unflatten_additions(self):
        test_util.run_through_cases(self, self.default_unflatten_addition_cases, self.get_default_mode_test_result)
    
    def test_default_unflatten_multiplications(self):
        test_util.run_through_cases(self, self.default_unflatten_multiplication_cases, self.get_default_mode_test_result)

    def test_default_unflatten_add_and_mults(self):
        test_util.run_through_cases(self, self.default_unflatten_add_and_mult_cases, self.get_default_mode_test_result)

    def test_balanced_unflatten_additions(self):
        test_util.run_through_cases(self, self.balanced_unflatten_addition_cases, self.get_balanced_mode_test_result)
    
    def test_balanced_unflatten_multiplications(self):
        test_util.run_through_cases(self, self.balanced_unflatten_multiplication_cases, self.get_balanced_mode_test_result)

    def test_balanced_unflatten_add_and_mults(self):
        test_util.run_through_cases(self, self.balanced_unflatten_add_and_mult_cases, self.get_balanced_mode_test_result)


