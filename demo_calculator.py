'''
demo_calculator.py -- A simple calculator.

See parser_definitions.py for supported functions, operators, and constants.
'''

import sys, argparse, traceback
import parsing.rigid_parsing as rigid_parsing
import parsing.liberal_parsing as liberal_parsing
            
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
        uin = input('>>')
        if len(uin) > 1 and uin in 'xxxxxxxx':
            break
        
        tokens, fixed_input, rpn, = None, None, None,
        tree, reduced_tree = None, None
        try:
            tokens = rigid_parsing.tokenize(uin)
            fixed_input = liberal_parsing.apply_transformations(list(tokens))
            rpn = rigid_parsing.to_RPN(fixed_input)
            tree = rigid_parsing.to_tree(rpn)

            reduced_tree = rigid_parsing.node(tree)
            reduced_tree.reduce(ARGS.replace_constants)
            if not ARGS.verbose:
                print(reduced_tree)
        except (SyntaxError, ZeroDivisionError, ValueError, TypeError) as error:
            print(error)
        finally:
            if ARGS.verbose:
                print("Tokens:", tokens)
                print("Fixed input:", fixed_input)
                print("RPN:", rpn)
                print("Tree:")
                print(tree)
                print("Reduce:")
                print(reduced_tree)
                
