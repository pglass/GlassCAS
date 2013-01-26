from .parsing.parser_definitions import *
from .expression_types import *
import numbers
from math import factorial

class Visitor(object):
    ''' Defines the Visitor interface '''

    def __init__(self):
        pass

    def visit(self, n):
        ''' n should be a node '''
        pass


class Printer(Visitor):
    
    PREFIX_MODE  = "prefix"
    INFIX_MODE   = "infix"
    POSTFIX_MODE = "postfix"
    TREE_MODE    = "tree" 
    BFS_MODE     = "breadth_first"

    def __init__(self, mode = TREE_MODE):
        '''
        mode determines what representation this printer produces:
            PREFIX_MODE  - produce a prefix representation with no parentheses
            INFIX_MODE   - produce a fully parenthesized infix representation
            POSTFIX_MODE - produce a postfix/rpn representatio, no parentheses
            TREE_MODE    - produces a tree with one node per line, with
                child nodes indented according to their depth.
                For "(x + 2) * (y + 3)" this will print:
                    *
                      +
                        x
                        2
                      +
                        y
                        2
            BFS_MODE - produces a string with each node's value ordered
                according to a breadth first traversal of the tree.
                For "(x - 2) * (y / 3)" this will return: '*-/x2y3'
            Each mode can be identified, respectively, by the strings:
                "prefix", "infix", "postfix", "tree"
        '''

        self.mode = mode

    def visit(self, n):
        '''
        Return a representation of the tree at node n, as a string.
        The representation 

        depth is used to keep track of indentation when printing as a tree.
        '''
        if self.mode == Printer.TREE_MODE:
            return self.visit_tree_mode(n, 0)[:-1] # strip off trailing newline
        elif self.mode == Printer.INFIX_MODE:
            return self.visit_infix_mode(n)
        elif self.mode == Printer.BFS_MODE:
            return self.visit_breadth_first_mode(n)
        else:
            return self.visit_postfix_prefix_modes(n)[:-1] # strip off trailing space

    def visit_infix_mode(self, n):
        result = ''
        
        if len(n.children) == 0:
            result += str(n.value)

        elif isinstance(n.value, PrefixOp):
            # something like 'f(x,y,z)'
            result += "%s(" % str(n.value)
            for i in range(len(n.children) - 1):
                result += "%s" % self.visit_infix_mode(n.children[i])
                result += ARG_DELIM
            result += "%s)" % self.visit_infix_mode(n.children[-1])

        elif isinstance(n.value, PostfixOp):
            # something like '(x,y,z)f'
            result += "("
            for i in range(len(n.children) - 1):
                result += "%s" % self.visit_infix_mode(n.children[i])
                result += ARG_DELIM
            result += "%s)" % self.visit_infix_mode(n.children[-1])
            result += str(n.value)

        else:
            result += "("
            for i in range(len(n.children) - 1):
                result += ("%s %s " % (self.visit_infix_mode(n.children[i]), str(n.value)))
            result += "%s" % self.visit_infix_mode(n.children[-1])
            result += ")"

        return result

    def visit_postfix_prefix_modes(self, n):
        result = ''

        if self.mode == Printer.PREFIX_MODE:
            result += str(n.value) + " "

        for child in n.children:
            result += self.visit_postfix_prefix_modes(child)

        if self.mode == Printer.POSTFIX_MODE:
            result += str(n.value) + " "

        return result

    def visit_tree_mode(self, n, depth):

        result = ("  " * depth)
        result += str(n.value)
        result += "\n"

        for child in n.children:
            result += self.visit_tree_mode(child, depth + 1)

        return result       

    def visit_breadth_first_mode(self, n):
        frontier = [n]
        result = ''

        while frontier:
            current = frontier.pop(0)
            result += str(current.value)
 
            for child in current.children:
                frontier.append(child)
        
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
        
        result_node = n.copy(recursive = False)
        for child in n.children:
            result_node.children.append(self.visit(child))

        # replace a Constant object (e, pi) with its numerical value (a float) 
        if self.replace_constants and isinstance(n.value, Constant):
            result_node.value = n.value.value

        # DefinedAsOp means a variable/function is being defined -- handle elsewhere.
        # EqualsOp is an equation, which we can't yet solve.
        if (isinstance(result_node.value, DefinedAsOp) or
            isinstance(result_node.value, EqualsOp)
            ):
            return result_node

        elif isinstance(result_node.value, UserFunction):
            # UserFunction.apply returns a *node*
            reduced_node = result_node.value.apply(*[x.value for x in result_node.children])
            if reduced_node != None:
                result_node = reduced_node

        elif isinstance(result_node.value, ExpandOp) or isinstance(result_node.value, SimplifyOp):
            return result_node.value.apply(*result_node.children)

        elif isinstance(result_node.value, GeneralOperator):
            # We can reduce the given node to a number if all children were reduced to a number.
            if all(isinstance(x.value, numbers.Number) for x in result_node.children):
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

        expr should be a node.
        '''
        self.symbol = symbol
        self.expr = expr

    def visit(self, n):
        # TODO: this needs to be tested
        # this is also pretty inefficient

        result_node = n.copy(recursive = False)

        if str(n.value) == str(self.symbol):
            result_node = n.copy(self.expr)
        else:
            for child in n.children:
                result_node.children.append(self.visit(child))

        return result_node

class Recognizer(object):
    '''
    The purpose of this class is to be able to tell you what kind of 
    expression a particular tree represents.
    
    Practicality?
      1. This will work for a lot of basic forms, which is good.
    
      2. I'm basically classifying mathematical expressions, but
         it's not always clear what the type is. Ex:
            e^x + log(x) = x^2
         It may turn out that there are no solutions to self equation,
         but we could still give it a type. Maybe:
            EquationExpr[ExpLogCombExpr[Var(x)], PolynomialExpr[Var(x), degree = 2]]
         I'm not really sure how useful the above would be, except that
         we could rule out many methods of solving the equation.
    
         But if there's no standard classification for a particular expression,
         then I probably don't know how to solve it anyway.
    
      3. Ideally, we would be allowed to find the type by manipulating
         the tree however we want, but the recognizer cannot be performance
         prohibitive.
    
    NOTES:
      -- It takes some work supporting more expression types.
         For N unique operators and M different expression types, there
         are have M*N*M ways to combine the expressions, so making a new 
         expression type involves updating the resolve method for all other 
         types. The code is mostly just hundreds of conditionals checking which 
         combination we were given.
    '''

    def __init__(self, assign_types = False):
        '''
        If assign_types is True, then this will set n.expr_type
            to the each node n's determined type.
        '''
        self.assign_types = assign_types

    def visit(self, n):
        result = UnknownExpr()
        if isinstance(n.value, EqualsOp):
            left = self.visit(n.children[0])
            right = self.visit(n.children[1])
            result = EquationExpr(left, right)
        elif isinstance(n.value, DefinedAsOp):
            result = DefinedAsExpr()
        elif isinstance(n.value, InfixOp):
            left = self.visit(n.children[0])
            right = self.visit(n.children[1])
            result = left.resolve(n.value, right)
            
        elif isinstance(n.value, NegationOp):
            child_type = self.visit(n.children[0])
            if isinstance(child_type, ConstantExpr):
                result = ConstantExpr(-child_type.value)
            else:
                # not positive this holds in all cases
                result = child_type
#            elif isinstance(child_type, PolynomialExpr):
#                result = child_type

        elif isinstance(n.value, numbers.Number):
            result = ConstantExpr(n.value)
        elif isinstance(n.value, Constant):
            result = ConstantExpr(n.value.value)
        elif isinstance(n.value, Var):
            result = PolynomialExpr(Var(n.value), 1)

        if self.assign_types:
            n.expr_type = result

        return result

class Expander(Visitor):
    
    is_plus_or_minus = lambda c: isinstance(c, PlusOp) or isinstance(c, SubOp)

    def visit(self, n):
        '''
        This works recursively as follows:
           1. Expand children first
           2. Distribute operators over addition/subtraction
           3. Expand children again if we distributed them
        It works decently, but it's slow. 
        For performance, this will reuse instances from the input
        node instead of make full copies, if possible.
        
        A better algorithm might be to first flatten the tree, 
        then expand as above, then unflatten. This will result in 
        fewer calls to distribute and map, however the entire tree
        is traversed twice for the flattening and unflattening.
        For example:
          Current method:
            Input: x * (((a+b) + c) + d)
            Distribute: x * ((a+b) + c) + x * d
            Distribute: (x * (a+b) + x*c) + x * d
            Distribute: ((x*a + x*b) + x*c) + x * d
          Flatting method:
            Input: x * (((a+b) + c) + d))
            Flatten: x * (a + b + c + d)
            Distribute: x*a + x*b + x*c + x*d
            Unflatten: (x*a + x*b) + (x*c + x*d)
            
        '''

        result = n.copy(recursive = False)
        for child in n.children:
            result.children.append(self.visit(child))

        # we assume the tree is binary at all +-*/^ nodes
        if isinstance(result.value, TimesOp):
            if Expander.is_plus_or_minus(result.children[0].value):
                if Expander.is_plus_or_minus(result.children[1].value):
                    result = self.distribute(result.children[0], result.children[1], result.value, left_distr = True)
                else:
                    result = self.distribute(result.children[1], result.children[0], result.value, left_distr = False)
                return self.visit(result)
            elif Expander.is_plus_or_minus(result.children[1].value):
                result = self.distribute(result.children[0], result.children[1], result.value, left_distr = True)
                return self.visit(result)

        elif isinstance(result.value, DivideOp):
            if Expander.is_plus_or_minus(result.children[0].value):
                result = self.distribute(result.children[1], result.children[0], result.value, left_distr = False)
                return self.visit(result)

        elif isinstance(result.value, NegationOp):
            if Expander.is_plus_or_minus(result.children[0].value):
                result = self.map(result.value, result.children[0])
                return self.visit(result)
                
        elif isinstance(result.value, ExponentOp):
            if isinstance(result.children[1].value, int) and result.children[1].value >= 0:
                if Expander.is_plus_or_minus(result.children[0].value):
                    result = self.expand_sum_to_integer_power(result)
                    return self.visit(result)

        return result

    def expand_sum_to_integer_power(self, n):
        '''
        n is a node that represents '(A + B) ^ k' where
            A and B can be any nodes and k is an integer.
        
        Use the binomial theorem to produce a node that represents
            Sum[(k choose i) * A^i * B^(k-i), i in range(0, k+1)]

        This does not make new instances of (A+B) each time we need a copy.
        '''
        
        k = n.children[1].value
        if k == 0:
            return n.copy(value = 1)

        A, B = n.children[0].children

        choose = lambda n, r: int(factorial(n)/(factorial(r) * factorial(n-r)))

        coeffs = [choose(k, i) for i in range(0, k+1)]

        result = n.copy(value = PlusOp())

        for i, c in enumerate(coeffs):
            # term represents (c * A^i * B^(k-i))
            term = n.copy(value = TimesOp())
            
            if isinstance(n.children[0].value, SubOp) and i % 2 == 1:
                # account for sign
                term.children.append(n.construct(n.copy(value = c), NegationOp()))
            elif c != 1:
                term.children.append(n.copy(value = c))
                
            if k-i == 1:
                # use 'x' instead of 'x^1'
                term.children.append(A)
            elif k-i != 0:
                # don't put anything for 'x^0'
                term.children.append(n.construct(A, ExponentOp(), n.copy(value = k-i)))

            if i == 1:
                term.children.append(B)
            elif i != 0:
                term.children.append(n.construct(B, ExponentOp(), n.copy(value = i)))
            
            if len(term.children) == 1:
                result.children.append(term.children[0])
            else:
                result.children.append(term)

        return result.accept(Unflattener())
    
    def map(self, func, B):
        '''
        Map func to each child in B.

        func is a PrefixOp or PostfixOp.
        B is any node.

        Ex:
            -(a+b) --> -a + -b
            -(a+(b+c)) --> -a + -(b+c)
        '''
        
        result = B.copy(recursive = False)
        
        for child in B.children:
            new_node = B.copy(value = func)
            new_node.children.append(child)
            result.children.append(new_node)

        return result

    def distribute(self, A, B, operator, left_distr = True):
        '''
        Distribute A to B over operator.

        B must be a node with a PlusOp or SubOp as its value.
        A can be any node.
        operator is the operator we distribute over.
            This can be TimesOp or ImplicitMultOp. We pass it in to stay consistent.
            This is also valid, in some cases, for DivideOp.

        If left_distr is True then perform a left distribution.
            Otherwise perform a right distribution. This is important
            for non-commutative types. 
        '''

        result = B.copy(recursive = False)
        
        for c in B.children:
            new_term = B.copy(value = operator)
            if left_distr:
                new_term.children.append(A)
                new_term.children.append(c)
            else:
                new_term.children.append(c)
                new_term.children.append(A)
            result.children.append(new_term)

        return result

class Flattener(Visitor):
    def visit(self, n):
        '''
        Compress sequences of additions and multiplications to be
        a single root node with many children, rather than binary
        in all cases.
        Example:
            3 + 4 + 5 + 6 normally parses to:
                +
                  +
                    +
                      3
                      4
                    5
                  6
            After flattening this becomes:
                +
                  3
                  4
                  5
                  6
        NOTES:
        When updating this method, you should also update Unflattener.visit.

        This should maintain expr_type attributes correctly. Recognizer is
        not made for use with a flattened tree, so you have to first call assign_types()
        and then flatten the tree to have expression types in the output.

        This only works for + and * because they're the only commutative operators.
        We can also do some flattening for - and / but we'd first have to
        apply some transformations:
            3-4-5 --> 3 + (-4) + (-5)
            3-(4-5) --> 3 + (-4) + 5
            3/4/5 --> 3 * (1/4) * (1/5), or 3 * (4^-1) * (5^-1)
            3/(4/5) --> 3 * (1/(4/5)), or 3 * (5/4), or 3 * (1/4) * 5
        I feel like this is beyond the scope of the Flattener though.
        '''

        result = n.copy(recursive = False)
        result.expr_type = n.expr_type
        for child in n.children:
            result.children.append(self.visit(child))

        if isinstance(result.value, InfixOp) and result.value.commutative:
            for i, child in enumerate(result.children):
                if type(child.value) == type(result.value):
                    result.children[i:i+1] = child.children

        return result

class Unflattener(Visitor):
    DEFAULT_MODE  = "default"
    BALANCED_MODE = "balanced"
    def __init__(self, mode = DEFAULT_MODE):
        '''
        This undoes the flattening done by Flattener. Since we can't
        know the structure of the original tree, we can choose the 
        structure of the output tree. The resultant tree will binary 
        at all nodes containing a commutative operator.

        Default mode treats commutative operators as left associative.
            Ex: (3+4+5+6) --> ((3+4) + 5) + 6)
        Balanced mode tries to produces a balanced tree, favoring the
            left side when there is an imbalance.
                Ex: (3+4+5+6) --> (3+4) + (5+6)
                Ex: (3+4+5+6+7) --> ((3+4) + 5) + (6+7)
            This can be useful if we want to limit the stack depth of
            subsequent operations, but only if there was significant 
            flattening done to the input tree.
        '''
        self.mode = mode

    def visit(self, n):
        # TODO? respect operator associativity
        if self.mode == Unflattener.DEFAULT_MODE: 
            result = n.copy(recursive = False)
            if isinstance(n.value, InfixOp) and n.value.commutative:
                if len(n.children) > 2:
                    new_node = n.copy(recursive = False)
                    new_node.children = n.children[:-1]
                    result.children.append(self.visit(new_node))
                    result.children.append(self.visit(n.children[-1]))
                else:
                    result.children.append(self.visit(n.children[0]))
                    result.children.append(self.visit(n.children[1]))
            else:
                for child in n.children:
                    result.children.append(self.visit(child))
            return result

        elif self.mode == Unflattener.BALANCED_MODE:
            result = n.copy(recursive = False)
            if isinstance(n.value, InfixOp) and n.value.commutative:
                if len(n.children) == 1:
                    return self.visit(n.children[0])
                elif len(n.children) > 2:
                    split = int(len(n.children)/2 + .5)
                    new_node = n.copy(recursive = False)
                    new_node.children = n.children[:split] 
                    result.children.append(self.visit(new_node))
    
                    new_node = n.copy(recursive = False)
                    new_node.children = n.children[split:] 
                    result.children.append(self.visit(new_node))
                else:
                    result.children.append(self.visit(n.children[0]))
                    result.children.append(self.visit(n.children[1]))
            else:
                for child in n.children:
                    result.children.append(self.visit(child))
            return result

class Sorter(Visitor):
    
    BY_NODE_VALUE = "by_node_value"
    BY_SUBTREE_REPR = "by_subtree_repr" 
    BY_EXPR_TYPE = "by_expr_type" 

    def __init__(self, mode = BY_NODE_VALUE):
        '''
        This will sort each node's list of children according
            to the given mode. This will produce an equivalent tree,
            so it will only sort children where the operation being
            applied is commutative.

        BY_NODE_VALUE will sort according to str(node.value).
        BY_SUBTREE_REPR will sort children according to the string 
            of the prefix representation of the subtree rooted 
            by each child node.
        BY_EXPR_TYPE will sort first by the type of expression:
                  UnknownExpr
                > ExponentialExpr
                > RationalExpr
                > PolynomialExpr
                > ConstantExpr
            Then it will also sort among members of the same type
                using certain attributes. For PolynomialExprs, it will 
                use the variable name and the degree. For ConstantExprs
                it uses a string representation of the constant value.
            Then it sorts by subtree representation. For example:
                x^2 + x + 1 --> 1 + x + x^2

        This is a useful hack for grouping similar-looking terms in 
            a flattened tree.
        '''
        self.mode = mode

    @staticmethod
    def by_node_value_key(n):
        return str(n.value)

    @staticmethod
    def by_subtree_repr_key(n):
        return n.accept(Printer(mode = Printer.BFS_MODE))

    @staticmethod
    def get_expr_sort_val(expr_type):
        if isinstance(expr_type, ExponentialExpr):
            return "05"
        elif isinstance(expr_type, RationalExpr):
            return "04"
        elif isinstance(expr_type, PolynomialExpr):
            return "03" + str(expr_type.var) + str(expr_type.degree)
        elif isinstance(expr_type, ConstantExpr):
            return "02" + str(expr_type.value)
        else:
            return "01"

    @staticmethod
    def by_expr_type_key(n):
        return Sorter.get_expr_sort_val(n.expr_type) + Sorter.by_subtree_repr_key(n)

    def visit(self, n):
        result = n.copy(recursive = True)
        if self.mode == Sorter.BY_NODE_VALUE:
            self.sort_visit(result, Sorter.by_node_value_key)
        elif self.mode == Sorter.BY_SUBTREE_REPR:
            self.sort_visit(result, Sorter.by_subtree_repr_key)
        elif self.mode == Sorter.BY_EXPR_TYPE:
            self.sort_visit(result, Sorter.by_expr_type_key)
        return result

    def sort_visit(self, n, sort_key):
        for child in n.children:
            self.sort_visit(child, sort_key)

        if isinstance(n.value, InfixOp) and n.value.commutative:
            n.children.sort(key = sort_key)

class Normalizer(Visitor):
    
    def visit(self, n):
        '''
        n is a node.

        This does the following transformations
            1. (a - b) --> a + (-1 * b)
            2. (a / b) --> (1/b) * a
            3. `x --> (-1 * x)
        
        Then it flattens the tree.
        Then it sorts the tree according to Sorter.BY_EXPR_TYPE.
        '''

        result = self.norm_visit(n)

        result.assign_types()

        result = result.accept(Flattener())
        result = result.accept(Sorter(mode = Sorter.BY_EXPR_TYPE))
        return result

    def norm_visit(self, n): 
        for i in range(len(n.children)):
            n.children[i] = self.norm_visit(n.children[i])

        result = n
        if isinstance(n.value, SubOp):
            # a - b --> a + (-1 * b)
            new_right = n.construct(n.copy(value = -1), TimesOp(), n.children[1])
            result = n.construct(n.children[0], PlusOp(), new_right)
        elif isinstance(n.value, DivideOp):
            # a/b --> (1/b) * a
            new_left = n.construct(n.copy(value = 1), DivideOp(), n.children[1])
            result = n.construct(new_left, TimesOp(), n.children[0])
        elif isinstance(n.value, NegationOp):
            # `x --> -1 * x
            result = n.construct(n.copy(value = -1), TimesOp(), n.children[0])

        return result

class Denormalizer(Visitor):
    
    def visit(self, n):
        '''
        n is a node.
        
        This tries to undo the transformations performed by Normalizer. 
        Namely:
            1. a + (-1 * b) --> a - b
            2. (1/b) * a --> a / b
            3. -1 * x --> `x
        It als unflattens the tree.

        '''
        result = self.denorm_visit(n)
        result = result.accept(Unflattener())
        return result

    def denorm_visit(self, n):
        result = n
        if isinstance(n.value, PlusOp) and isinstance(n.children[1].value, TimesOp) and n.children[1].children[0].value == -1:
            # a + (-1 * b) --> a - b
            result = n.construct(n.children[0], SubOp(), n.children[1].children[1])
        elif isinstance(n.value, TimesOp) and isinstance(n.children[0].value, DivideOp) and n.children[0].children[0].value == 1:
            # (1/b) * a --> a / b
            result = n.construct(n.children[1], DivideOp, n.children[0].children[1])
        elif isinstance(n.value, TimesOp) and n.children[0].value == -1:
            # -1 * x --> `x
            result = n.construct(n.children[1], NegationOp())

        for i in range(len(result.children)):
            result.children[i] = self.denorm_visit(result.children[i])

        return result

class Simplifier(Visitor):
   
    def visit(self, n):
        result = n.accept(Normalizer())
        result = self.simplify_visit(result)
        # we don't need to denormalize here. It's more of a display nicety.
        result = result.accept(Denormalizer())
        return result

    def simplify_visit(self, n):
        result = n

        # so this approach is limited. 
        # What if, for example, a RationalExpr simplifies to a PolynomialExpr or ConstantExpr?
        #   x / x --> 1
        #   x^2 / x --> x
        if isinstance(result.expr_type, ConstantExpr):
            result = n.copy(value = result.expr_type.value)
            result.expr_type = n.expr_type
            return result
        elif isinstance(result.expr_type, PolynomialExpr):
            result.children = [self.simplify_visit(x) for x in result.children]
            result = self.simplify_to_polynomial(result)
            result.expr_type = n.expr_type
            return result
        else:
            return n


    def resolve_poly_add(self, a, b):
        '''
        Called from simplify to polynomial.

        Note:
        a and b will not be a sum of terms. That is, if a.expr_type
        is a PolynomialExpr with degree d, then a represents (A ^ d)
        and not (A^d + <term> + <term> + ...). The only issue here is 
        that A could still be (1+x), for example. That is, the input 
        is not necessarily fully expanded.
        '''
        
        if type(a.expr_type) != type(b.expr_type):
            return None

        result = None
        result_type = a.expr_type.resolve(PlusOp(), b.expr_type)

        if isinstance(result_type, UnknownExpr):
            return None

        if isinstance(result_type, ConstantExpr):
            result = a.copy(value = result_type.value)
        elif isinstance(result_type, PolynomialExpr):
            # if a, b are of same variable and degree
            if a.expr_type == b.expr_type:
                if isinstance(a.value, Var) and isinstance(b.value, Var):
                    # x + x --> 2 * x
                    result = a.construct(a.copy(value = 2), TimesOp(), a)
                elif isinstance(a.value, ExponentOp) and isinstance(b.value, ExponentOp):
                    # _^d + _^d --> 2 * (_^d)
                    #
                    # so there are other cases that hit this conditional, like:
                    #   (1+x)^2 + x^2 --> 1 + 2x + x^2 + x^2 --> 1 + 2x + 2x^2
                    # But this requires an expansion, and I'd rather not expand here.
                    if a.strict_match(b):
                        result = a.construct(a.copy(value = 2), TimesOp(), a)
                elif isinstance(a.value, TimesOp):
                    if (isinstance(b.value, TimesOp) 
                        and isinstance(a.children[0].value, numbers.Number)
                        and isinstance(b.children[0].value, numbers.Number)
                        and a.children[1].strict_match(b.children[1])
                        ):
                        # (3 * _) + (2 * _) --> 5 * _
                        new_coeff = a.children[0].value + b.children[0].value
                        result = a.construct(a.copy(value = new_coeff), TimesOp(), a.children[1])
                    elif isinstance(a.children[0].value, numbers.Number) and a.children[1].strict_match(b):
                        # (3 * _) + _ --> 4 * _
                        new_coeff = a.children[0].value + 1
                        if new_coeff == 0:
                            result = a.copy(value = 0)
                            result_type = ConstantExpr(0)
                        else:
                            result = a.construct(a.copy(value = new_coeff), TimesOp(), b)
        if result != None:
            result.expr_type = result_type
        return result 

    def resolve_poly_mult(self, a, b):
        result = None
        result_type = a.expr_type.resolve(TimesOp(), b.expr_type)

        if isinstance(result_type, UnknownExpr):
            return None 
        
        if isinstance(result_type, ConstantExpr):
            result = a.copy(value = result_type.value)
        elif isinstance(a.expr_type, ConstantExpr):
            if a.expr_type.value == 0:
                # 0 * _ --> 0
                result = a.copy(value = 0)
                result_type = ConstantExpr(0)
            elif isinstance(b.value, TimesOp) and isinstance(b.children[0].value, numbers.Number):
                # a * (b * x) --> (a*b) * x
                new_coeff = TimesOp().apply(a.value, b.children[0].value)
                if new_coeff == 0:
                    result = a.copy(value = 0)
                    result_type = ConstantExpr(0)
                else:
                    result = a.construct(a.copy(value = new_coefficient), TimesOp(), b.children[1])
        elif isinstance(result_type, PolynomialExpr):
            if isinstance(a.value, Var) and isinstance(b.value, Var):
                # x * x --> x^2
                result = a.construct(a, ExponentOp(), a.copy(value = 2))
            elif isinstance(a.value, ExponentOp) and isinstance(b.value, Var):
                # _^c * _ --> _^(c + 1)
                new_exponent = a.children[1].value + 1
                result = a.construct(b, ExponentOp(), a.copy(value = new_exponent))
            elif isinstance(a.value, ExponentOp) and isinstance(b.value, ExponentOp):
                # _^c * _^d --> _^(c+d)
                if a.children[0].strict_match(b.children[0]):
                    new_exponent = a.children[1].value + b.children[1].value
                    result = a.construct(a.children[0], ExponentOp(), a.copy(value = new_exponent))

        if result != None:
            result.expr_type = result_type
        return result 
 
    def simplify_to_polynomial(self, n):

        result = n.copy(recursive = False)

        if isinstance(n.value, PlusOp) or isinstance(n.value, TimesOp):
            # handle <poly> + ... + <poly> or <poly> * ... * <poly>
            # keep in mind n is already flattened and sorted            

            result.children.append(n.children.pop(0))
            while len(n.children) > 0:
                
                a = result.children[-1]
                b = n.children.pop(0)
                
                new_node = None
                if isinstance(n.value, PlusOp):
                    new_node = self.resolve_poly_add(a, b)
                elif isinstance(n.value, TimesOp):
                    new_node = self.resolve_poly_mult(a, b)

                if new_node != None:
                    result.children[-1] = new_node
                else:
                    result.children.append(b)
        else:
            result = n.copy(recursive = True)

        if len(result.children) == 1:
            return result.children[0]

        return result

