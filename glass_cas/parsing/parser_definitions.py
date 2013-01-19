'''
parser_definitions.py

This defines a number of classes to represent operators, constants,
variables, and user-defined functions

This also contains dictionaries that map string tokens to classes:
    OP_CLASS_DICT for operators/predefined functions, and
    CONST_CLASS_DICT for constants

    These dicts are particularly important. They define what nodes
    are produced by the parser. e.g. If you wanted a bunch
    of aliases for the same function, just add the following mappings
    to OP_CLASS_DICT:
      'derivative'    : DerivativeOp,
      'derive'        : DerivativeOp,
      'differentiate' : DerivativeOp,
      'diff'          : DerivativeOp,
      'D'             : DerivativeOp,

    NOTE: There may be issues having operator strings within other operator
    strings. For example, the following should work fine:
      '/' : DivideOp,
      'd/dx' : DeriviativeOp,
    At least until you define variables 'd' and 'dx', and want to divide d by dx.
    Then what happens is undefined, but the parser will do the same thing every time.
    I believe the following will cause similar problems:
      'd'    : SomethingOp,
      'dx'   : SomethingElseOp,
      '/'    : DivideOp,
      'd/dx' : DeriviativeOp,
'''

import cmath, math

REAL_NUMBER_CHARS = list('0123456789.')
NUMBER_CHARS = REAL_NUMBER_CHARS + ['j'] # Use 'j' as sqrt(-1)

# operator to represent implicit multiplication
IMPLICIT_MULT = '@'

# negation operator (different than subtraction)
NEG_OP = '`'

# argument separator
ARG_DELIM = ','

# Left and right associativity constants
LEFT  = -1
RIGHT = 1

class GeneralOperator(object):
    ''' Base class and interface for all operator objects '''

    def __init__(self, name=None, precedence=None, commutative=False, 
                 associativity=None, num_operands=None):
        self.name = name
        self.precedence = precedence
        self.associativity = associativity
        self.commutative = commutative
        self.num_operands = num_operands

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__class__.__name__ + '()'

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
    def __init__(self, name=None, precedence=None, commutative=False, associativity=None):
        super().__init__(
            name=name, 
            precedence=precedence, 
            commutative=commutative, 
            associativity=associativity, 
            num_operands=2
        )

class PlusOp(InfixOp):
    def __init__(self):
        super().__init__('+', precedence=1, commutative=True, associativity=LEFT)

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
        super().__init__('*', precedence=2, commutative=True, associativity=LEFT)

    def apply(self, *operands):
        self.check_operands(*operands)
        prod = 1
        for e in operands:
            prod *= e
        return prod

class ImplicitMultOp(TimesOp):
    '''
    ImplicitMultOp extends TimesOp, since we usually treat it the same.
    '''
    def __init__(self):
        super().__init__()
        self.name = IMPLICIT_MULT
        self.precedence = 3.5

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
        self.check_operands(*operands)
        result = operands[-1]
        for e in reversed(operands[:-1]):
            result = e ** result
        return result

class EqualsOp(InfixOp):
    def __init__(self):
        super().__init__('=', precedence=0, commutative=True, associativity=LEFT)

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

# a couple of classes for testing
class PrecZeroPostfixOp(PostfixOp):
    def __init__(self):
        super().__init__(name='Post(0)', precedence=0, associativity=LEFT, num_operands=1)
class PrecThreePostfixOp(PostfixOp):
    def __init__(self):
        super().__init__(name='Post(3)', precedence=3, associativity=LEFT, num_operands=1)

class FactorialOp(PostfixOp):
    def __init__(self):
        super().__init__(name='!', precedence=5, associativity=LEFT, num_operands=1)

    def apply(self, *operands):
        self.check_operands(*operands)
        return math.factorial(operands[0])

########################################
# PREFIX FUNCTIONS/OPERATORS
########################################
class PrefixOp(GeneralOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# a couple of classes for testing
class PrecZeroPrefixOp(PrefixOp):
    def __init__(self):
        super().__init__("Prefix(0)", precedence=0, associativity=RIGHT, num_operands=1)
class PrecFivePrefixOp(PrefixOp):
    def __init__(self):
        super().__init__("Prefix(5)", precedence=5, associativity=RIGHT, num_operands=1)

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

class ExpandOp(PrefixOp):
    def __init__(self):
        super().__init__('expand', precedence=1, associativity=RIGHT, num_operands=1)

    def apply(self, *operands):
        # TODO: I don't like this import here.
        # this is to avoid circular imports since visitors imports parser_definitions
        # Solutions?
        #   -- maybe move these apply methods somewhere else, like to their own module
        #   -- make a node.expand method that uses Expander; call node.expand here
        #   -- rethink the organization/architecture of the whole program
        #   -- or, leave the import here
        from ..visitors import Expander

        self.check_operands(*operands)
        result = Expander().visit(operands[0])
        return result

class SimplifyOp(PrefixOp):
    def __init__(self):
        super().__init__('simplify', precedence=1, associativity=RIGHT, num_operands=1)

    def apply(self, *operands):
        # TODO: I don't like this import here (same as with expand)
        from ..visitors import Simplifier

        self.check_operands(*operands)
        result = Simplifier().visit(operands[0])
        return result

########################################
# USER-DEFINED FUNCTION/OPERATOR
########################################
class UserFunction(PrefixOp):
    ''' Represent f[v1, v2, ..., vn] = <expression> '''
    def __init__(self, name, operand_list=[], value=None):
        super().__init__(
            name=name,
            precedence=3,
            associativity=RIGHT,
            num_operands=len(operand_list)
        )

        self.operand_list = operand_list
        self.value = value

    def __str__(self):
        result = str(self.name)
        result += '['
        for e in self.operand_list[:-1]:
            result += str(e) + ','

        try:
            result += str(self.operand_list[-1])
        except IndexError:
            pass
        result += ']'

        return result

    def __repr__(self):
        return "UserFunction(%s = %s)" % (self, self.value)

    def __eq__(self, other):
        return str(self) == str(other)

    def check_operands(self, *operands):
        if len(self.operand_list) < len(operands):
            raise SyntaxError("Too few operands for %s" % self.name)
        if len(self.operand_list) > len(operands):
            raise SyntaxError("Not enough operands for %s" % self.name)


    def apply(self, *operands):
        # print("applying %s%s" % (self.name, operands))
        if self.value != None:
            self.check_operands(*operands)

            # node.replace works for a single (symbol, value) pair and
            # produces a copy of the tree for each substitution, which is
            # both inefficient and ugly to write.
            if len(operands) > 0:
                result = self.value.replace(self.operand_list[0], operands[0])
                for symbol, value in zip(self.operand_list[1:], operands[1:]):
                    result = result.replace(symbol, value)
                return result.reduce()
            else:
                # cannot return the same instance of this function's body
                return self.value.copy(recursive = True)
        return None

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
        return "%s(%s = %r)" % (self.__class__.__name__, self.name, self.value)

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
        return "%s(%s = %s)" % (self.__class__.__name__, self.name, self.value)

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
    'expand': ExpandOp,
    'simplify' : SimplifyOp,
}
