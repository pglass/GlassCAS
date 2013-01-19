'''
run_tests.py
'''

from glass_cas.test.parsing_test import (
    TokenizeTestCases,
    RPNConversionTestCases,
    TreeTestCases,
    InsertImplicitMultOpsTestCases,
    TransformIfNegationTestCases,
    ApplyTransformationsTestCases
)

from glass_cas.test.recognition_test import (
    RecognitionTestCases
)

from glass_cas.test.expansion_test import (
    ExpansionTestCases,
    FlatteningTestCases,
    UnflatteningTestCases,
)

from glass_cas.test.simplification_test import (
    SimplificationTestCases
)

if __name__ == '__main__':
    import unittest

    unittest.main()
