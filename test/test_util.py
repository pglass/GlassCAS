def run_through_cases(obj, cases, func):
    '''
    obj should be a unittest.TestCase instance.
    cases is a list of (input, output) pairs.
    func is the function to apply to inputs.
    '''
    for key, val in cases:
        actual = func(key)
        obj.assertEqual(actual, val)
