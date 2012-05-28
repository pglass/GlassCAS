import unittest
import calc_parser, calc_parser_test_cases

import sys

# Invoke with any argument to get printing feedback
DEBUG_ON = False
if len(sys.argv) > 1:
    DEBUG_ON = True
    print "Debugging is on"
    sys.argv = sys.argv[:1]

class ParserTest(unittest.TestCase):
    
    def setUp(self):
        self.tokenize_pass      = calc_parser_test_cases.tokenize_pass
        self.tokenize_fail      = calc_parser_test_cases.tokenize_fail
        
        self.insert_times_symbols_pass = calc_parser_test_cases.insert_times_symbols_pass
        
        self.to_RPN_tests       = calc_parser_test_cases.to_RPN_tests
        
        self.to_tree_pass       = calc_parser_test_cases.to_tree_pass
        self.to_tree_fail       = calc_parser_test_cases.to_tree_fail

        self.reduce_tests       = calc_parser_test_cases.reduce_tests
        self.reduce_replace_constants_pass = calc_parser_test_cases.reduce_replace_constants_pass

    def test_insert_times_symbols(self):
        for key, val in self.insert_times_symbols_pass.iteritems():
            # print key, val
            actual = calc_parser.insert_times_symbols(list(key))
            if actual != val:
                if DEBUG_ON:
                    print key
                    print "  ", val
                    print "  ", actual
                    
            self.assertEquals(actual, val)        

    def test_tokenize(self):
        for key, val in self.tokenize_pass.iteritems():
            actual = calc_parser.tokenize(key)
            if DEBUG_ON and actual != val:
                print "Failed", key, val, actual
            self.assertEquals(actual, val)
        
        for bad in self.tokenize_fail:            
            try:
                self.assertRaises(SyntaxError, calc_parser.tokenize, bad)
            except AssertionError, ae:
                if DEBUG_ON:
                    print "Failed", `bad`
                raise ae
                
    def test_to_RPN(self):
        for key, val in self.to_RPN_tests.iteritems():
            actual = calc_parser.to_RPN(key)
            if DEBUG_ON and actual != val:
                print "Failed"
                print key, val, actual
            self.assertEquals(actual, val)
            
    def test_to_tree(self):
        for key, val in self.to_tree_pass.iteritems():
            tree_form = str(calc_parser.to_tree(key))
            if DEBUG_ON and tree_form != val:
                print "Failed", `key`
                print val
                print tree_form
            self.assertEquals(tree_form, val)
        
        for bad in self.to_tree_fail:
            try:
                with self.assertRaises(SyntaxError) as se:
                    calc_parser.to_tree(bad)
            except AssertionError, ae:
                if DEBUG_ON:
                    print "Failed", `bad`

    def test_reduce(self):
        for key, val in self.reduce_tests.iteritems():
            t = calc_parser.to_tree(key)
            t.reduce()
            result = str(t)
            if result != val:
                print "{0}\n{1}\n{1}\n".format(key, val, result)
            self.assertEquals(result, val)
            
        for key, val in self.reduce_replace_constants_pass.iteritems():
            t = calc_parser.to_tree(key)
            t.reduce(replace_constants = True)
            result = str(t)
            if result != val:
                print "{0}\n{1}\n{1}\n".format(key, val, result)
            self.assertEquals(result, val)
        
if __name__ == '__main__':
    unittest.main()
        