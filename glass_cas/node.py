from . import visitors
import numbers

class node(object):

    def __init__(self, v = None):
        '''
        If v is a node, then this copies the tree rooted at v. This will
            copy expr_type attributes as well.
        Otherwise this constructs a new node with value v and no children.

        node.value should be some subclass of GeneralOperator, 
            a subclass of Var, or an int/float/complex number.

        By default, n.expr_type is None. To assign the types for n and all
            children you must explicitly call n.assign_types().
        '''
        # copy constructor
        if isinstance(v, node):
            self.value = v.value
            self.expr_type = v.expr_type 
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

    def copy(self, value = None, recursive = False):
        '''
        This allows us to use node instances to create new nodes
        without actually importing the node module elsewhere.
        This avoids a circular import between node.py and visitors.py.

        If value is not None, then recursive is assumed to be False. 
            The result will have no children.
        Otherwise, if recursive is True then all children will be copied.
            If recursive is False, then the result will have no children.

        If n is a node, and X is anything:
            n.copy()
                <==> node(n.value)
            n.copy(recursive = True)
                <==> node(n)
            n.copy(value = X)
                <==> node(X)
        '''

        if value != None:
            return node(value)
        elif not recursive:
            return node(self.value)
        
        return node(self)
       
    def construct(self, left_child, value, right_child = None, assign_types = False):
        '''
        Return a new node with the given value, and
            left_child and right_child as children.

        If right_child is None, then the result will have one child.
            Otherwise, the result will have two children.

        This does no other checks on the input, except for those done 
            by the node constructor when node(value) is called.

        '''
            
        result = node(value)
        result.children.append(left_child)
        if right_child != None:
            result.children.append(right_child)
        if assign_types:
            result.assign_types()
        return result

    def strict_match(self, other):
        if str(self) != str(other):
            return False
        return True

    def __repr__(self):
        ''' Return a string representation of this tree in RPN. '''

        # This is is used for evaluating test results. 
        # Be careful if you want to change it.

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
        Computes and returns the value of this node.
        This does not alter this instance at all.

        replace_constants = True will replace Constant objects with an
          approximate numeric values, e.g., E() becomes 2.7182818...
        replace_constants = False will leave E() in the tree.
        '''

        return self.accept(visitors.Reducer(replace_constants = replace_constants))

    def replace(self, symbol, expr):
        ''' Replace all occurrences of symbol with expr. '''

        return self.accept(visitors.Replacer(symbol, expr))
