'''
parser_definitions.py

This defines a number of classes to represent operators, constants, 
variables, and user-defined functions

This also contains dictionaries that map string tokens to classes:
    OP_CLASS_DICT for operators/predefined functions, and
    CONST_CLASS_DICT for constants
'''

import cmath, math

REAL_NUMBER_CHARS = list('0123456789.')
NUMBER_CHARS = REAL_NUMBER_CHARS + ['j'] # Use 'j' as sqrt(-1)

# operator to represent implicit multiplication
IMPLICIT_MULT = '@'

# negation operator (different than subtraction)
NEG_OP = '`'

# Left and right associativity constants
LEFT  = -1
RIGHT = 1

class GeneralOperator(object):
    ''' Base class and interface for all operator objects '''
    
    def __init__(self, name=None, precedence=None, associativity=None, num_operands=None):
        self.name = name
        self.precedence = precedence
        self.associativity = associativity
        self.num_operands = num_operands
    
    def __str__(self):
        return str(self.name)
        
    def __repr__(self):
        return repr(self.name)
        
    def __eq__(self, other):
        try:
            return str(self) == str(other)
        except:
            return False
    
    def __len__(self):
        return len(self.name)
    
    def check_operands(self, *operands):
        if len(operands) < self.num_operands:
            raise SyntaxError("Too few operands for %s" % self.name)
        
    def apply(self, *operands):
        ''' Apply this operator to the given operands and return the result '''
        raise NotImplementedError(
            "apply() should be overridden in subclasses of GeneralOperator"
        )

########################################
# INFIX FUNCTIONS/OPERATORS
########################################
class InfixOp(GeneralOperator):
    def __init__(self, name=None, precedence=None, associativity=None):
        super().__init__(name=name, precedence=precedence, associativity=associativity, num_operands=2)
    
class PlusOp(InfixOp):
    def __init__(self):
        super().__init__('+', precedence=1, associativity=LEFT)
        
    def apply(self, *operands):
        self.check_operands(*operands)
        return sum(operands)
    
class SubOp(InfixOp):
    def __init__(self):
        super().__init__('-', precedence=1, associativity=LEFT)
        
    def apply(self, *operands):
        self.check_operands(*operands)
        return operands[0] - sum(operands[1:])
        
class TimesOp(InfixOp):
    def __init__(self):
        super().__init__('*', precedence=2, associativity=LEFT)
        
    def apply(self, *operands):
        self.check_operands(*operands)
        prod = 1
        for e in operands:
            prod *= e
        return prod

class ImplicitMultOp(InfixOp):
    def __init__(self):
        super().__init__(IMPLICIT_MULT, precedence=3.5, associativity=LEFT)
    
    def apply(self, *operands):
        self.check_operands(*operands)
        prod = 1
        for e in operands:
            prod *= e
        return prod
        
class DivideOp(InfixOp):
    def __init__(self):
        super().__init__('/', precedence=2, associativity=LEFT)
    
    def apply(self, *operands):
        self.check_operands(*operands)
        quotient = operands[0]
        for e in operands[1:]:
            quotient /= e
        return quotient
    
class ModulusOp(InfixOp):
    def __init__(self):
        super().__init__('%', precedence=2, associativity=LEFT)
    
    def apply(self, *operands):
        self.check_operands(*operands)
        result = operands[0]
        for e in operands[1:]:
            result %= e
        return result
        
class ExponentOp(InfixOp):
    def __init__(self):
        super().__init__('^', precedence=4, associativity=RIGHT)
        
    def apply(self, *operands):
        result = operands[-1]
        for e in reversed(operands[:-1]):
            result = e ** result
        return result
        
class EqualsOp(InfixOp):
    
    def __init__(self):
        super().__init__('=', precedence=0, associativity=LEFT)
        
    def apply(self, *operands):
        raise NotImplementedError(
            "apply() is not applicable for %s" % self.name
        )

class DefinedAsOp(InfixOp):
    def __init__(self):
        super().__init__(':=', precedence=0, associativity=LEFT)
        
    def apply(self, *operands):
        raise NotImplementedError(
            "apply() is not applicable for %s" % self.name
        )
        
########################################
# POSTFIX FUNCTIONS/OPERATORS
########################################
class PostfixOp(GeneralOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class FactorialOp(PostfixOp):
    def __init__(self):
        super().__init__('!', precedence=5, associativity=LEFT, num_operands=1)
    
    def apply(self, *operands):
        self.check_operands(*operands)
        return math.factorial(operands[0])

########################################
# PREFIX FUNCTIONS/OPERATORS
########################################
class PrefixOp(GeneralOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NegationOp(PrefixOp):
    def __init__(self):
        super().__init__(NEG_OP, precedence=3, associativity=RIGHT, num_operands=1)
    
    def apply(self, *operands):
        self.check_operands(*operands)
        return -operands[0]
    
class SqrtOp(PrefixOp):
    def __init__(self):
        super().__init__('sqrt', precedence=3, associativity=RIGHT, num_operands=1)
        
    def apply(self, *operands):
        self.check_operands(*operands)
        return cmath.sqrt(operands[0])
        
class CosOp(PrefixOp):
    def __init__(self):
        super().__init__('cos', precedence=3, associativity=RIGHT, num_operands=1)
        
    def apply(self, *operands):
        self.check_operands(*operands)
        return cmath.cos(operands[0])        
        
class SinOp(PrefixOp):
    def __init__(self):
        super().__init__('sin', precedence=3, associativity=RIGHT, num_operands=1)
        
    def apply(self, *operands):
        self.check_operands(*operands)
        return cmath.sin(operands[0])

class TanOp(PrefixOp):
    def __init__(self):
        super().__init__('tan', precedence=3, associativity=RIGHT, num_operands=1)
        
    def apply(self, *operands):
        self.check_operands(*operands)
        return cmath.tan(operands[0])

class LogEOp(PrefixOp):
    def __init__(self):
        super().__init__('ln', precedence=3, associativity=RIGHT, num_operands=1)
    
    def apply(self, *operands):
        self.check_operands(*operands)
        return cmath.log(operands[0])

class LogTenOp(PrefixOp):
    def __init__(self):
        super().__init__('log', precedence=3, associativity=RIGHT, num_operands=1)
        
    def apply(self, *operands):
        self.check_operands(*operands)
        return cmath.log10(operands[0])

########################################
# USER-DEFINED FUNCTION/OPERATOR
########################################
class UserFunction(object):
    ''' Represent f[v1, v2, ..., vn] = <expression> '''
    def __init__(self, name, operand_list, expression=None):
        self.name = name
        self.precedence = 3
        self.associativity = RIGHT
        self.num_operands = len(operand_list)
        self.operand_list = operand_list
        self.expression = expression
    
    def __str__(self):
        result = str(self.name)
        result += '['
        for e in self.operand_list[:-1]:
            result += str(e) + ','
        result += str(self.operand_list[-1])
        result += ']'
            
        if self.expression:
            result += " = %s" % self.expression
        return result
    
    def __repr__(self):
        return str(self)
        
    def __eq__(self, other):
        return str(self) == str(other)
    
    def check_operands(*operands):
        if len(self.operand_list) < len(operands):
            raise SyntaxError("Too few operands for %s" % self.name)
    
    def apply(self, *operands):
        self.check_operands(*operands)
        print("apply %s%s" % (self.name, operands))
        
########################################
# VARIABLES/CONSTANTS
########################################
class Var(object):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __str__(self):
        return str(self.name)
    def __repr__(self):
        return "Var(%s)" % str(self)
        
    def __eq__(self, other):
        try:
            return str(self) == str(other)
        except:
            return False
    
    def __len__(self):
        return len(self.name)
            
class Constant(Var):
    def __init__(self, name, value):
        super().__init__(name, value)
    def __repr__(self):
        return "Constant(%s)" % str(self)
    
class E(Constant):
    def __init__(self):
        super().__init__('e', cmath.e)
        
class Pi(Constant):
    def __init__(self):
        super().__init__('pi', cmath.pi)
        
CONST_CLASS_DICT = {
    'e' : E,
    'pi' : Pi,
}

OP_CLASS_DICT = {
    '+'     : PlusOp,
    '-'     : SubOp,
    '*'     : TimesOp,
    IMPLICIT_MULT : ImplicitMultOp,
    '/'     : DivideOp,
    '%'     : ModulusOp,
    '^'     : ExponentOp,
    '='     : EqualsOp,
    ':='    : DefinedAsOp,
    '!'     : FactorialOp,
    NEG_OP  : NegationOp,
    'sqrt'  : SqrtOp,
    'cos'   : CosOp,
    'sin'   : SinOp,
    'tan'   : TanOp,
    'ln'    : LogEOp,
    'log'   : LogTenOp,
}