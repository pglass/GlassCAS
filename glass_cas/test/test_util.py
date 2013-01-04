def run_through_cases(obj, cases, in_func, out_func = lambda x: x):
    '''
    obj should be a unittest.TestCase instance.
    cases is a list of (input, output) pairs.
    in_func is the function to apply to inputs.
    out_func is the function to apply to expected values.
    '''
    for key, val in cases:
        actual = in_func(key)
        expected = out_func(val)
        obj.assertEqual(actual, expected)
