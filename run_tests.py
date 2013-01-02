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

from test.recognition_test import (
  RecognitionTestCases
)

if __name__ == '__main__':
    import unittest

    unittest.main()
