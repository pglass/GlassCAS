import parsing.visitors
import numbers

class node(object):
    
    def __init__(self, v = None):
        # copy constructor
        if isinstance(v, node):
            self.value = v.value
            self.children = [node(i) for i in v.children]
        # ordinary constructor
        else:
            self.value = v
            self.children = []

    def accept(self, visitor):
      return visitor.visit(self)
    
    def __repr__(self):
        '''
        Return a string representation of this tree in RPN.
        '''

        # this is is used for evaluating test results. Best not to touch.

        result = self.accept(parsing.visitors.Printer(rpn_mode = True))
        return result[:-1] # strip off trailing newline

    def __str__(self):
        '''
        Produce a string representation of this tree's structure.
        '''
        
        result = self.accept(parsing.visitors.Printer(rpn_mode = False))
        return result[:-1]  # strip off trailing newline

    def reduce(self, replace_constants = False):
      ''' 
      Computes and returns the value of this tree.
      This does not alter this tree at all.
      
      replace_constants = True will replace Constant objects with an 
        approximate numeric values, e.g., E() becomes 2.7182818...
      replace_constants = False will leave E() in the tree.
      '''
      
      return self.accept(parsing.visitors.Reducer(replace_constants = replace_constants))
    
    def replace(self, symbol, expr):
      '''
      Replace all occurrences of symbol with expr.
      '''

      return self.accept(parsing.visitors.Replacer(symbol, expr))
