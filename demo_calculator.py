'''
demo_calculator.py -- A simple calculator.

See parser_definitions.py for supported functions, operators, and constants.
'''

import sys, argparse, traceback

from glass_cas.parsing import parsing

from glass_cas import visitors

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-v", "--verbose",
        help="verbose mode", 
        action="store_true")
    arg_parser.add_argument("-t", "--tracebacks",
        help="turn on full tracebacks", 
        action="store_true")
    arg_parser.add_argument("-d", "--dump_table",
        help="print out the symbol table after each input",
        action="store_true")
    arg_parser.add_argument("--tree",
        help="print a tree representation for each input (in addition to an infix representation)",
        action="store_true")
    arg_parser.add_argument("--normalize",
        help="show the normalized form of the tree",
        action="store_true")
    arg_parser.add_argument("--types",
        help="show expression types",
        action="store_true")
    arg_parser.add_argument("--no_replace_constants",
        help="do not replace constants (e, pi) with approximate values",
        action="store_true")

    ARGS = arg_parser.parse_args()
    parser = parsing.Parser()
    while True:
        uin = input('>> ')
        if len(uin) > 2 and uin in 'qqqqqqqq':
            break

        # break apart each step of parsing/evaluation for debug purposes
        tokens, fixed_input, rpn, = None, None, None,
        tree, reduced_tree = None, None
        try:
            tokens = parser.tokenize(uin)
            fixed_input = parsing.apply_transformations(list(tokens))
            rpn = parser.to_rpn(fixed_input)
            tree = parser.to_tree(rpn)

            if ARGS.types:
                tree.assign_types()
                print("Expression has type:", tree.expr_type)

            reduced_tree = tree.copy(recursive = True).reduce(not ARGS.no_replace_constants)

            if ARGS.types:
                reduced_tree.assign_types()
                print("Reduced expression has type:", reduced_tree.expr_type)

            parser.update_symbol_table(reduced_tree)

            if ARGS.normalize:
                norm = tree.copy(recursive = True)
                if ARGS.types:
                    norm.assign_types()

                norm = norm.accept(visitors.Normalizer())
                print("Normalized expression:", norm)
                if ARGS.types:
                    print("  Normalized expression has type:", norm.expr_type)

            if not ARGS.verbose:
                if ARGS.tree:
                    print(reduced_tree.__str__(mode = 'tree'))
                print(reduced_tree)
        except (SyntaxError, ZeroDivisionError, ValueError, TypeError) as error:
            if ARGS.tracebacks:
                traceback.print_tb(error.__traceback__)
            print(error)
        finally:
            if ARGS.verbose:
                if tokens != None:
                    print("Tokens:", list(map(str, tokens)))
                if fixed_input != None:
                    print("Fixed input:", list(map(str, fixed_input)))
                if rpn != None:
                    print("RPN:", rpn)
                if tree != None:
                    print("Syntax tree:")
                    if ARGS.tree:
                        print(tree.__str__(mode = 'tree'))
                    print(str(tree))
                if reduced_tree != None:
                    print("Reduced tree:")
                    if ARGS.tree:
                        print(reduced_tree.__str__(mode = 'tree'))
                    print(reduced_tree)
            if ARGS.dump_table:
                print("Defined Symbols:")
                for k, v in parser.symbol_table.items():
                    print("  ", k, ":", repr(v))
