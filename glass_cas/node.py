from . import visitors
import numbers

class node(object):

    def __init__(self, v = None):
        '''
        If v is a node, then this copies the tree rooted at v.
        Otherwise this constructs a new node value v and no children.

        By default, n.expr_type is None. To assign the types for n and all
            children you must explicitly call n.assign_types().
        '''
        # copy constructor
        if isinstance(v, node):
            self.value = v.value
            self.children = [node(i) for i in v.children]
        # ordinary constructor
        else:
            self.value = v
            self.children = []

        self.expr_type = None

    def accept(self, visitor):
        return visitor.visit(self)

    def assign_types(self):
        self.accept(visitors.Recognizer(assign_types = True))

    def copy(self, value = None, recursive = True):
        '''
        This allows us to use node instances to create new nodes
        without actually importing the node class elsewhere.

        If value is not None, recursive has no effect.
        Otherwise, if recursive is False the result node has no children.

        If n is a node, and X is anything:
            n.copy()
                <==> node(n)
            n.copy(recursive = False)
                <==> node(n.value)
            n.copy(value = X)
                <==> node(X)

        This does not copy the expr_type. You must call assign_types() afterward.
        '''

        if value != None:
            return node(value)
        elif not recursive:
            return node(self.value)
        
        return node(self)
       
    def __repr__(self):
        '''
        Return a string representation of this tree in RPN.
        '''

        # this is is used for evaluating test results. Best not to touch.

        return self.accept(visitors.Printer(mode = visitors.Printer.POSTFIX_MODE))

    def __str__(self, mode = visitors.Printer.INFIX_MODE):
        '''
        Produce a string representation of this tree's structure.

        mode is a string that corresponds to a static member of visitors.Printer:
            mode == "prefix" produces an unparenthesized prefix representation
            mode == "postfix" produces an unparenthesized postfix representation
            mode == "infix" produces a fully parenthesized infix representation
            mode == "tree" produces a multiline tree-like representation, with 
                children indented according to their depth.
        '''

        return self.accept(visitors.Printer(mode = mode))

    def reduce(self, replace_constants = False):
        '''
        Computes and returns the value of this tree.
        This does not alter this tree at all.

        replace_constants = True will replace Constant objects with an
          approximate numeric values, e.g., E() becomes 2.7182818...
        replace_constants = False will leave E() in the tree.
        '''

        return self.accept(visitors.Reducer(replace_constants = replace_constants))

    def replace(self, symbol, expr):
        '''
        Replace all occurrences of symbol with expr.
        '''

        return self.accept(visitors.Replacer(symbol, expr))
