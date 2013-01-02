'''
expression_types.py

This module contains classes that represent mathematical expression 
metadata. That is, these can contain information about expressions
but do not need to contain the expressions themselves. This allows 
us elsewhere to classify expressions and hopefully to determine the
best way to solve the associated expression.

The essential method on all of these classes is resolve().
  If you have '<expr1> <OP> <expr2>', and you know the types
  of both expressions, then you can use expr1.resolve(OP, expr2)
  to get the type of the entire expression.
  
  The annoying thing about this is that, with N operators and M
  different types of expressions, you have M*N*M cases to handle
  in determining the type.

  How can we reduce the number of these checks, or reduce the
  amount of code we have to write?
    1. Avoid handling equivalent cases in multiple places:
       ex: A [+-*] B is often the same type as B [+-*] A.
       But be careful of non-commutative operators (-, /, ^, %)
    2. A lot of these cases don't make sense
'''

from parsing.parser_definitions import *

class Expr(object):
  
  def __repr__(self):
    return str(self)

  def __str__(self):
    return self.__class__.__name__

  def resolve(self, operator, right_type):
    raise NotImplementedError(
      "cannot call Expr.resolve(). Expr should not be instantiated."
    )

class DefinedAsExpr(Expr):
  pass

class UnknownExpr(Expr):
  
  def __init__(self, info = None):
    ''' info is some string that says why we couldn't determine the type. '''
    self.info = info


  def __str__(self):
    result = self.__class__.__name__
    if self.info:
      result += "[%s]" % self.info
    return result

  def __eq__(self, other):
    return type(self) == type(other)

  def resolve(self, operator, right_type):
    return UnknownExpr()

class EquationExpr(Expr):
  
  def __init__(self, left_type, right_type):
    ''' 
    For example, if n represents "x^2 = e^x" then construct 
    the type of n as:
      EquationExpr(PolynomialExpr(...), ExponentialExpr(...))
    '''
    
    self.left_type  = left_type
    self.right_type = right_type

  def __repr__(self):
    return str(self)

  def __str__(self):
    result = self.__class__.__name__ 
    result += "[%s, %s]" % (self.left_type, self.right_type)
    return result

  def __eq__(self, other):
    if type(self) == type(other):
      return (self.left_type == other.left_type and self.right_type == other.right_type)
    return False

class PolynomialExpr(Expr):
  
  def __init__(self, var, degree):
    '''
    var should be an instantiation of the Var class.
    degree is the degree of the polynomial
      For example, if n represents "x^4 + x^2 + 1" then n is
      an expression of type:
        PolynomialExpr(Var(x), 4)
    '''

    self.var = var
    self.degree = degree

  def resolve(self, operator, right_type):
    ''' PolynomialExpr.resolve() '''

    op_check = lambda op_type: isinstance(operator, op_type)

    if isinstance(right_type, ConstantExpr):
      if any(map(op_check, [PlusOp, SubOp, TimesOp])):
        return right_type.resolve(operator, self)
      elif op_check(DivideOp):
        return self
      elif op_check(ExponentOp):
        # not sure if I want to apply this to non-integer exponents 
        return PolynomialExpr(self.var, degree = self.degree * right_type.value)

    elif isinstance(right_type, PolynomialExpr):
      if self.var == right_type.var:
        if any(map(op_check, [PlusOp, SubOp])):
          new_degree = max(self.degree, right_type.degree)
          return PolynomialExpr(self.var, new_degree)
        elif op_check(TimesOp):
          new_degree = self.degree + right_type.degree
          return PolynomialExpr(self.var, new_degree)
        elif op_check(DivideOp):
          return RationalExpr(self, right_type)

    elif isinstance(right_type, RationalExpr):
      if any(map(op_check, [PlusOp, SubOp, TimesOp])):
        return right_type.resolve(operator, self)
      elif op_check(DivideOp):
        if self.var == right_type.var:
          # P / (T / B) = P*B / T --> top = P * B, bottom = T
          new_top_degree = self.degree + right_type.bottom_type.degree
          new_top_type = PolynomialExpr(self.var, new_top_degree)
          return RationalExpr(new_top_type, right_type.top_type)
        
    return UnknownExpr(info = "cannot determine resultant type for %s(%s, %s)" % (operator, self, right_type))

  def __repr__(self):
    return str(self)

  def __str__(self):
    result = self.__class__.__name__
    result += "[%s[%s], degree=%s]" % (self.var.__class__.__name__, self.var, self.degree)
    return result 

  def __eq__(self, other):
    if type(self) == type(other):
      return (self.var == other.var and self.degree == other.degree)
    return False

class ConstantExpr(PolynomialExpr):
  def __init__(self, value, var = Var("_")):
    super().__init__(var, degree=0)
    self.value = value

  def resolve(self, operator, right_type):
    ''' ConstantExpr.resolve() '''
    
    op_check = lambda op_type: isinstance(operator, op_type)

    if isinstance(right_type, ConstantExpr):
      ops = [PlusOp, SubOp, TimesOp, DivideOp, ModulusOp, ExponentOp]

      if any(map(op_check, ops)):
        return ConstantExpr(operator.apply(self.value, right_type.value))
    elif isinstance(right_type, PolynomialExpr):
      if op_check(PlusOp) or op_check(SubOp) or op_check(TimesOp):
        return right_type
      elif op_check(DivideOp):
        # c / x, for example
#        return RationalExpr(PolynomialExpr(right_type.var, degree = 0), right_type)
        return RationalExpr(ConstantExpr(self.value, var = right_type.var), right_type)
      elif op_check(ExponentOp):
        if right_type.degree == 1:
          return ExponentialExpr(right_type.var, base = self.value)
    elif isinstance(right_type, RationalExpr):
      if op_check(PlusOp) or op_check(SubOp) or op_check(TimesOp):
        return right_type.resolve(operator, self)
      elif op_check(DivideOp):
        # c / (T / B) = cB / T
        new_top_type = self.resolve(TimesOp(), right_type.bottom_type)
        return RationalExpr(new_top_type, right_type.top_type)
      
    elif isinstance(right_type, ExponentialExpr):
      if any(map(op_check, [TimesOp, DivideOp])):
        return right_type

    return UnknownExpr("Cannot determine resultant type for %s(%s, %s)" % (operator, self, right_type))

  def __repr__(self):
    return str(self)

  def __str__(self):
    result = self.__class__.__name__
    result += "[%s]" % (self.value)
#    result += "[%s (Poly[%s, degree=%s])]" % (self.value, self.var, self.degree)
    return result

  def __eq__(self, other):
    if isinstance(other, ConstantExpr):
      return self.value == other.value
    if isinstance(other, PolynomialExpr):
      return (self.degree == other.degree == 0)
    return False 

class RationalExpr(Expr):
  '''
  A rational function is f(x) = P(x) / Q(x) for two polynomials P and Q.
  '''
  
  def __init__(self, top_type, bottom_type):
    '''
    top_type and bottom_type can be PolynomialExpr objects (so ConstantExpr is acceptable too).
      They are also allowed to be UnknownExpr objects (but all resolve() will then always
      return UnknownExpr).
    '''
    self.top_type = top_type
    self.bottom_type = bottom_type

    # we need to assign a matching variable name to any ConstantExpr objects
    # passed in (since ConstantExpr subclasses PolynomialExpr)
    if isinstance(top_type, ConstantExpr):
      if isinstance(bottom_type, ConstantExpr):
        self.top_type = ConstantExpr(top_type.value, var = Var("_"))
        self.bottom_type = ConstantExpr(bottom_type.value, var = Var("_"))
      elif isinstance(bottom_type, PolynomialExpr):
        self.top_type = ConstantExpr(top_type.value, var = bottom_type.var)
    elif isinstance(bottom_type, ConstantExpr):
      if isinstance(top_type, PolynomialExpr):
        self.bottom_type = ConstantExpr(bottom_type.value, var = top_type.var)

    if not isinstance(top_type, UnknownExpr) and not isinstance(bottom_type, UnknownExpr):
      if self.top_type.var != self.bottom_type.var:
        raise Exception("%s must be of a single variable" % self)
      self.var = top_type.var
 
  def resolve(self, operator, right_type):
    ''' RationalExpr.resolve() '''
    if isinstance(self.top_type, UnknownExpr) or isinstance(self.bottom_type, UnknownExpr):
      return UnknownExpr("cannot determine resultant type of %s(%s, %s)" % (operator, self, right_type))

    op_check = lambda op_type: isinstance(operator, op_type)

    if isinstance(right_type, ConstantExpr):
      if op_check(PlusOp) or op_check(SubOp):
        # using (T / B) [+-] c = (T [+-] cB) / B
        # since B is a polynomial, cB and B are the same types
        new_top_type = self.top_type.resolve(operator, self.bottom_type)
        return RationalExpr(new_top_type, self.bottom_type)
      elif op_check(TimesOp) or op_check(DivideOp):
        return self
      elif op_check(ExponentOp):
        # (T / B) ^ c = (T^c) / (B^c)
        new_top_type = self.top_type.resolve(operator, right_type)
        new_bottom_type = self.bottom_type.resolve(operator, right_type)
        return RationalExpr(new_top_type, new_bottom_type)
    elif isinstance(right_type, PolynomialExpr):
      if self.var == right_type.var:
        if op_check(PlusOp) or op_check(SubOp):
          # using (T / B) [+-] P = (T [+-] B*P) / B:
          #   new_top is T [+-] B*P
          new_top_type = self.top_type.resolve(operator, 
            self.bottom_type.resolve(TimesOp(), right_type)
          )
          return RationalExpr(new_top_type, self.bottom_type)
        elif op_check(TimesOp):
          # using (T / B) * P = (T * P) / B
          #   new_top is T * P
          new_top_type = self.top_type.resolve(TimesOp(), right_type)
          return RationalExpr(new_top_type, self.bottom_type)
        elif op_check(DivideOp):
          # using (T / B) / P = (T / B) * (1 / P) = (T / (B * P))
          #   new_bottom is B * P
          new_bottom_type = self.bottom_type.resolve(TimesOp(), right_type)
          return RationalExpr(self.top_type, new_bottom_type)
    elif isinstance(right_type, RationalExpr):
      if self.var == right_type.var:
        if any(map(op_check, [PlusOp, SubOp])):
          # using (T1 / B1) [+-] (T2 / B2) = (T1*B2 [+-] B1*T2) / (B1*B2)
          T1_times_B2 = self.top_type.resolve(TimesOp(), right_type.bottom_type)
          B1_times_T2 = self.bottom_type.resolve(TimesOp(), right_type.top_type)
          new_top_type = T1_times_B2.resolve(operator, B1_times_T2)

          new_bottom_type = self.bottom_type.resolve(TimesOp(), right_type.bottom_type)

          return RationalExpr(new_top_type, new_bottom_type)
        elif op_check(TimesOp):
          # using (T1/B1) * (T2/B2) = (T1*T2)/(B1*B2)
          new_top_type = self.top_type.resolve(TimesOp(), right_type.top_type)
          new_bottom_type = self.bottom_type.resolve(TimesOp(), right_type.bottom_type)
          return RationalExpr(new_top_type, new_bottom_type)
        elif op_check(DivideOp):
          # using (T1/B1) / (T2/B2) = (T1*B2) / (B1*T2)
          new_top_type = self.top_type.resolve(TimesOp(), right_type.bottom_type)
          new_bottom_type = self.bottom_type.resolve(TimesOp(), right_type.top_type)
          return RationalExpr(new_top_type, new_bottom_type)

    return UnknownExpr("cannot determine resultant type of %s(%s, %s)" % (operator, self, right_type))

  def __str__(self):
    result = self.__class__.__name__
    result += "[%s, %s]" % (self.top_type, self.bottom_type)
    return result

  def __eq__(self, other):
    ''' 
    This does not handle cases where you can factor out a term
    from the top and bottom. Ex: '(x^2) / (x^3)' is the same
    as '1 / x'. This function does not have enough information
    to do that simplification.
    '''

    if type(self) == type(other):
      return (self.top_type == other.top_type and self.bottom_type == other.bottom_type)
    return False

class ExponentialExpr(Expr):
  ''' 
  Represents a constant to the power of a variable '''
  
  def __init__(self, var, base):
    ''' 
    If n represents "2^x": ExponentialExpr(Var(x), base = 2)

    I'm not sure if we can always determine the base...
    '''
    self.var  = var
    self.base = base

  def resolve(self, operator, right_type):
    
    op_check = lambda op: isinstance(operator, op)

    if isinstance(right_type, ConstantExpr):
      if any(map(op_check, [PlusOp, SubOp])):
        return UnknownExpr(info = "Cannot determine resultant type for %s(%s, %s)" % (operator, self, right_type))
      elif any(map(op_check, [TimesOp, DivideOp])):
        # (2^x)*c and (2^x) / c are still exponential
        return ExponentialExpr(self.var, base = self.base)
      elif op_check(ExponentOp):
        return self

    return UnknownExpr()

  def __repr__(self):
    return str(self)

  def __str__(self):
    result = self.__class__.__name__
    result += "[%s[%s]" % (self.var.__class__.__name__, self.var)
    
    if self.base != None:
      result += ", base=%s" % (self.base) 

    result += "]"

    return result
  
  def __eq__(self, other):
    if type(self) == type(other):
      return (self.base == other.base and self.var == other.var)
    return True 


