'''
run_tests.py
'''

from test.rigid_parsing_test import (
    TokenizeTestCases,
    RPNConversionTestCases,
    TreeTestCases
)

from test.liberal_parsing_test import (
    InsertImplicitMultOpsTestCases,
    TransformIfNegationTestCases,
    ApplyTransformationsTestCases
)

if __name__ == '__main__':
    import unittest

    unittest.main()