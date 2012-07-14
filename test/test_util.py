def run_through_cases(obj, cases, func):
    '''
    obj should be a unittest.TestCase instance.
    cases is a list of pairs (input, output).
    func gives the output.
    '''
    for key, val in cases:
        actual = func(key)
        obj.assertEquals(actual, val)
