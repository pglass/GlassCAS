import unittest

from ..parsing import parsing
from .. import visitors
from . import recognition_test_cases as rt_cases
from . import test_util

class RecognitionTestCases(unittest.TestCase):
    '''
    This tests the visitors.Recognizer.visit method.
    '''
    def setUp(self):
        self.constant_expr_on_left_cases    = rt_cases.constant_expr_on_left_cases
        self.polynomial_expr_on_left_cases  = rt_cases.polynomial_expr_on_left_cases
        self.rational_expr_on_left_cases    = rt_cases.rational_expr_on_left_cases
        self.exponential_expr_on_left_cases = rt_cases.exponential_expr_on_left_cases
        self.equation_expr_cases            = rt_cases.equation_expr_cases

    @staticmethod
    def get_test_result(case):
        parser = parsing.Parser()
        tree = parser.parse(case)
        return visitors.Recognizer().visit(tree)

    def test_constant_expr_on_left(self):
        test_util.run_through_cases(self, self.constant_expr_on_left_cases, self.get_test_result)

    def test_polynomial_expr_on_left(self):
        test_util.run_through_cases(self, self.polynomial_expr_on_left_cases, self.get_test_result)

    def test_rational_expr_on_left(self):
        test_util.run_through_cases(self, self.rational_expr_on_left_cases, self.get_test_result)

    def test_exponential_expr_on_left(self):
        test_util.run_through_cases(self, self.exponential_expr_on_left_cases, self.get_test_result)

    def test_equation_expr(self):
        test_util.run_through_cases(self, self.equation_expr_cases, self.get_test_result)
