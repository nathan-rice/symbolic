from decorator import decorator
import ast

test_string = """
x = 4
x += 1
x2 = [x]
x2[0].bit_length()
"""

method_nodes = {
"__add__": ast.Add,
    #And
    #Assert
    #Assign
    "__getattribute__": ast.Attribute,
    #AugAssign
    #AugLoad
    #AugStore
    #BinOp
    "__and__": ast.BitAnd,
    "__or__": ast.BitOr,
    "__xor__": ast.BitXor,
    #BoolOp
    #Break
    "__call__": ast.Call,
    #ClassDef
    "__cmp__": ast.Compare,
    #Continue
    #Del
    #Delete
    #Dict
    #DictComp
    "__div__": ast.Div,
    #Ellipsis
    "__eq__": ast.Eq,
    #ExceptHandler
    #Exec
    #Expr
    #Expression
    #ExtSlice
    "__floordiv__": ast.FloorDiv,
    #For
    #FunctionDef
    #GeneratorExp
    #Global
    "__gt__": ast.Gt,
    "__ge__": ast.GtE,
    #If
    #IfExp
    #Import
    #ImportFrom
    "__contains__": ast.In,
    "__index__": ast.Index,
    #Interactive
    "__inv__": ast.Invert,
    #Is
    #IsNot
    "__lshift__": ast.LShift,
    #Lambda
    #List
    #ListComp
    #Load
    "__lt__": ast.Lt,
    "__le__": ast.LtE,
    "__mod__": ast.Mod,
    #Module
    "__mul__": ast.Mult,
    #Name
    #NodeTransformer
    #NodeVisitor
    #Not
    "__ne__": ast.NotEq,
    #NotIn
    #Num
    #Or
    #Param
    #Pass
    "__pow__": ast.Pow,
    #Print
    #PyCF_ONLY_AST
    "__rshift__": ast.RShift,
    #Raise
    "__repr__": ast.Repr,
    #Return
    #Set
    #SetComp
    #Slice
    #Store
    "__str__": ast.Str,
    "__sub__": ast.Sub,
    #Subscript
    #Suite
    #TryExcept
    #TryFinally
    #Tuple
    "__pos__": ast.UAdd,
    "__neg__": ast.USub,
    #UnaryOp
    #While
    #With
    #Yield
}

@decorator
def builds_ast(f, *args, **kwargs):
    self = f.im_self
    name = f.__name__
    object.__setattr__(f.im_self, f.im_func.__name__)
    


class SymbolicMeta(type):
    """
    """

class Symbol(object):
    """
    Base class for Proxy objects.
    """

    def __init__(self, iterable=tuple(), parent=None):
        pass
    
    def __iter__(self):
        pass

    def __nonzero__(self):
        pass

    def __str__(self):
        pass
    
    def __repr__(self):
        pass
    
    def __unicode__(self):
        pass

    def __reversed__(self):
        pass

    def __getattribute__(self, item):
        pass

    def __hash__(self):
        pass

    def __invert__(self):
        pass

    def __index__(self):
        pass

    def __neg__(self):
        pass

    def __pos__(self):
        pass

    def __abs__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass

    def __getattr__(self, attr):
        pass

    def __reversed__(self):
        pass

    def __getitem__(self, item):
        pass

    def __hash__(self):
        pass

    def __invert__(self):
        pass

    def __index__(self):
        pass

    def __neg__(self):
        pass

    def __pos__(self):
        pass

    def __abs__(self):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __floordiv__(self, other):
        pass

    def __mod__(self, other):
        pass

    def __divmod__(self, other):
        pass

    def __pow__(self, other, modulo=None):
        pass

    def __lshift__(self, other):
        pass

    def __rshift__(self, other):
        pass

    def __div__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __radd__(self, other):
        return lambda: other + self.f

    def __rand__(self, other):
        return lambda: other & self.f

    def __rdiv__(self, other):
        return lambda: other / self.f

    def __rdivmod__(self, other):
        return lambda: divmod(other, self.f)

    def __rfloordiv__(self, other):
        return lambda: other // self

    def __rlshift__(self, other):
        return lambda:other << self

    def __rmod__(self, other):
        return lambda:other % self

    def __rmul__(self, other):
        return lambda: other * self

    def __ror__(self, other):
        return lambda: other | self

    def __rpow__(self, other):
        return lambda: pow(other, self)

    def __rrshift__(self, other):
        return lambda: other >> self

    def __rsub__(self, other):
        return lambda: other - self

    def __rtruediv__(self, other):
        return lambda: self.__rtruediv__(other)

    def __rxor__(self, other):
        return lambda: other ^ self

    def __contains__(self, item):
        return lambda: item in self.f

    def __eq__(self, other):
        return lambda: self.f == other

    def __ne__(self, other):
        return lambda: self.f != other

    def __le__(self, other):
        return lambda: self.f <= other

    def __lt__(self, other):
        return lambda: self.f < other

    def __gt__(self, other):
        return lambda: self.f > other

    def __ge__(self, other):
        return lambda: self.f >= other

    def __cmp__(self, other):
        return lambda: cmp(self.f, other)

    def __and__(self, other):
        return lambda: self.f & other

    def __xor__(self, other):
        return lambda: self.f ^ other

    def __or__(self, other):
        return lambda: self.f | other

    def __iand__(self, other):
        return lambda: self.f.__iand__(other)

    def __ixor__(self, other):
        return lambda: self.f.__ixor__(other)

    def __ior__(self, other):
        return lambda: self.f.__ior__(other)

    def __iadd__(self, other):
        return lambda: self.f.__iadd__(other)

    def __isub__(self, other):
        return lambda: self.f.__isub__(other)

    def __imul__(self, other):
        return lambda: self.f.__imul__(other)

    def __idiv__(self, other):
        return lambda: self.f.__idiv__(other)

    def __itruediv__(self, other):
        return lambda: self.f.__itruediv__(other)

    def __ifloordiv__(self, other):
        return lambda: self.f.__ifloordiv__(other)

    def __imod__(self, other):
        return lambda: self.f.__imod__(other)

    def __ipow__(self, other, modulo=None):
        return lambda: self.f.__ipow__(other, modulo)

    def __ilshift__(self, other):
        return lambda: self.f.__ilshift__(other)

    def __irshift__(self, other):
        return lambda: self.f.__irshift__(other)
