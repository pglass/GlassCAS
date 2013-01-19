import unittest
from ..parsing import parsing
from .. import visitors
from . import simplification_test_cases as simp_cases
from . import test_util

class SimplificationTestCases(unittest.TestCase):
    
    def setUp(self):
        pass

    @staticmethod
    def get_test_result(case):
        tree = parsing.Parser().parse(case)
        return repr(tree.accept(visitors.Simplifier()))

    def test_constant_simplification(self):
        test_util.run_through_cases(self, simp_cases.constant_cases, self.get_test_result)

    def test_polynomial_addition_simplification(self):
        test_util.run_through_cases(self, simp_cases.polynomial_addition_cases, self.get_test_result)

    def test_polynomial_subtraction_simplification(self):
        test_util.run_through_cases(self, simp_cases.polynomial_subtraction_cases, self.get_test_result)

    def test_polynomial_multiplication_simplification(self):
        test_util.run_through_cases(self, simp_cases.polynomial_multiplication_cases, self.get_test_result)

    def test_polynomial_division_simplification(self):
        test_util.run_through_cases(self, simp_cases.polynomial_division_cases, self.get_test_result)
