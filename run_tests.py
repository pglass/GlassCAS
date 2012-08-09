'''
run_tests.py
'''

from test.parsing_test import (
    TokenizeTestCases,
    RPNConversionTestCases,
    TreeTestCases,
    InsertImplicitMultOpsTestCases,
    TransformIfNegationTestCases,
    ApplyTransformationsTestCases
    
)

if __name__ == '__main__':
    import unittest

    unittest.main()