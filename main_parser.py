'''
Simple demonstration calculator.
'''

import sys, argparse, traceback
import rigid_parsing, liberal_parsing
            
if __name__ == '__main__':            
    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--replace_constants", 
                        help="replace constants with approximate values",
                        action="store_true")
    parser.add_argument("-v", "--verbose", 
                        help="verbose mode", 
                        action="store_true")

    ARGS = parser.parse_args()           
    while True:
        uin = raw_input('>>')
        if len(uin) > 1 and uin in 'xxxxxxxx':
            break
        
        tokens, tokens_with_multiplies, rpn, tree = None, None, None, None
        try:
            tokens = rigid_parsing.tokenize(uin)
            tokens_with_multiplies = liberal_parsing.insert_times_symbols(list(tokens))
            rpn = rigid_parsing.to_RPN(tokens_with_multiplies)
            tree = rigid_parsing.to_tree(rpn)
            reduced_tree = rigid_parsing.node(tree)
            reduced_tree.reduce(ARGS.replace_constants)
            
        except SyntaxError as se:
            print se.message
        finally:
            if ARGS.verbose:
                print "Tokens:", tokens
                print "Implicit multiplies:", tokens_with_multiplies
                print "RPN:", rpn
                print "Tree:"
                print tree
                print "Reduce:"
                print reduced_tree
            else:
                print reduced_tree
 