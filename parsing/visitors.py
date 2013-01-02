import parsing.parser_definitions
import parsing.parsing
import parsing.node
import numbers

class Visitor(object):
  ''' Defines the Visitor interface '''
  
  def __init__(self):
    pass

  def visit(self, n):
    ''' n should be a node '''
    pass


class Printer(Visitor):
  
  def __init__(self, rpn_mode = False):
    ''' 
    If rpn_mode is True, this it will print out as RPN.
      otherwise, you'll get a tree-like representation
    '''

    self.rpn_mode = rpn_mode

  def visit(self, n, depth = 0):
    ''' 
    Return a representation of the tree at node n, as a string.

    depth is used to keep track of indentation when printing as a tree.
    '''
    
    result = ''

    if not self.rpn_mode:
      result += ("  " * depth)
      result += str(n.value)
      result += "\n"

    for child in n.children:
      result += self.visit(child, depth = depth + 1)

    if self.rpn_mode:
      result += str(n.value)
      result += " "

    return result

class Reducer(Visitor):

  def __init__(self, replace_constants = False):
    self.replace_constants = replace_constants

  def visit(self, n):
    ''' 
    Computes the value of the tree at node n.

    replace_constants = True will replace constant identifiers 
    with their numeric values, e.g., 'e' becomes 2.7182818...
    replace_constants = False will leave 'e' in the tree.
    '''

    result_node = parsing.node.node(n.value)
    for child in n.children:
      result_node.children.append(self.visit(child))

    # replace a Constant object with an explicit number (int/float/complex)
    if self.replace_constants and isinstance(n.value, parsing.parser_definitions.Constant):
      result_node.value = n.value.value

    # DefinedAsOp means a variable/function is being defined -- handle elsewhere.
    # EqualsOp is an equation, which we can't yet solve.
    if (isinstance(result_node.value, parsing.parser_definitions.DefinedAsOp) or 
        isinstance(result_node.value, parsing.parser_definitions.EqualsOp)
        ): 
      return result_node

    elif isinstance(result_node.value, parsing.parser_definitions.GeneralOperator):
      # We can reduce this tree if all children were reduced to a number.
      # UserFunction objects handle symbol substitution and reduction themselves,
      #   so go ahead and call their apply method here.

      if (isinstance(result_node.value, parsing.parser_definitions.UserFunction) or 
          all(isinstance(x.value, numbers.Number) for x in result_node.children)
          ):
        reduced_value = result_node.value.apply(*[x.value for x in result_node.children])
        if reduced_value != None:
          result_node.value = reduced_value
          result_node.children.clear()

    return result_node

class Replacer(Visitor):
  
  def __init__(self, symbol, expr):
    ''' 
    Instantiate this Replacer so that every occurrence of 
    symbol is replaced with expr
    '''
    self.symbol = symbol
    self.expr = expr

  def visit(self, n):

    result_node = parsing.node.node(n.value)

    if str(n.value) == str(self.symbol):
      if isinstance(self.expr, parsing.node.node):
        result_node.value = self.expr.value
        result_node.children = self.expr.children
      else:
        result_node.value = self.expr
    else:
      for child in n.children:
        result_node.children.append(self.visit(child))

    return result_node



