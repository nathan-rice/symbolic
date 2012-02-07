from decorator import decorator
import ast
import types
from inspect import getcallargs
from dispatch import DispatchDict

def compile_sym(symbol):
    expr = ast.Expression(object.__getattribute__(symbol, "ast"))
    fixed = ast.fix_missing_locations(expr)
    return compile(fixed, '<string>', 'eval')

def ast_self_node(symbol):
    return object.__getattribute__(symbol, "ast")

def binary_op(op):
    return lambda self, other: ast.BinOp(
        object.__getattribute__(self, "ast"),
        op(),
        ast_obj_nodes(other),
    )

def compare(op):
    return lambda self, other: ast.Compare(
        object.__getattribute__(self, "ast"),
        [op()],
        [ast_obj_nodes(other)],
    )

def aug_assign(op):
    return lambda self, other: ast.AugAssign(
        object.__getattribute__(self, "ast"),
        op(),
        ast_obj_nodes(other),
    )

def subscript(self, item):
    if isinstance(item, types.SliceType):
        index = ast.Slice(
            item.start and ast_obj_nodes(item.start),
            item.stop and ast_obj_nodes(item.stop),
            item.step and ast_obj_nodes(item.step)
        )
    else:
        index = ast.Index(ast_obj_nodes(item))
    return ast.Subscript(
        value=object.__getattribute__(self, "ast"),
        slice=index,
        ctx=ast.Load()
    )


def unary_op(op):
    return lambda self: ast.UnaryOp(op(), ast_self_node(self))

def ast_name(name, ctx=ast.Load):
    return ast.Name(id=name, ctx=ctx())

ast_obj_nodes = DispatchDict({
    int: lambda x: ast.Num(x),
    float: lambda x: ast.Num(x),
    str: lambda x: ast.Str(x)
})

ast_obj_nodes[types.SliceType] = lambda x: ast.Index(

)

ast_op_nodes = {
    "__add__": binary_op(ast.Add),
    "__iadd__": aug_assign(ast.Add),
    "__getattribute__": (
        lambda self, attr:
            ast.Attribute(
                ast_self_node(self),
                ast_name(attr),
                ast.Load()
            )
    ),
    "__setattr__": (
        lambda self, attr, value:
            ast.Attribute(
                ast_self_node(self),
                ast_name(attr, ast.Store)
            )
    ),
    #AugLoad
    #AugStore
    "__and__": binary_op(ast.BitAnd),
    "__iand__": aug_assign(ast.And),
    "__or__": binary_op(ast.BitOr),
    "__ior__": aug_assign(ast.BitOr),
    "__xor__": binary_op(ast.BitXor),
    "__ixor__": aug_assign(ast.BitXor),
    #BoolOp
    "__call__": ast.Call,
    "__cmp__": ast.Compare,
    #Del
    #Delete
    #Dict
    #DictComp
    "__div__": binary_op(ast.Div),
    "__idiv__": aug_assign(ast.Div),
    #Ellipsis
    "__eq__": compare(ast.Eq),
    #ExceptHandler
    #Exec
    #Expr
    #Expression
    #ExtSlice
    "__floordiv__": binary_op(ast.FloorDiv),
    "__ifloordiv__": aug_assign(ast.FloorDiv),
    #For
    #FunctionDef
    #GeneratorExp
    #Global
    "__gt__": compare(ast.Gt),
    "__ge__": compare(ast.GtE),
    #If
    #IfExp
    #Import
    #ImportFrom
    "__contains__": ast.In,
    "__index__": ast.Index,
    #Interactive
    "__inv__": unary_op(ast.Invert),
    #Is
    #IsNot
    "__lshift__": binary_op(ast.LShift),
    "__ilshift__": aug_assign(ast.LShift),
    #Lambda
    #List
    #ListComp
    #Load
    "__lt__": compare(ast.Lt),
    "__le__": compare(ast.LtE),
    "__mod__": binary_op(ast.Mod),
    "__imod__": aug_assign(ast.Mod),
    #Module
    "__mul__": binary_op(ast.Mult),
    "__imul__": aug_assign(ast.Mult),
    #Name
    #NodeTransformer
    #NodeVisitor
    #Not
    "__ne__": compare(ast.NotEq),
    #NotIn
    #Num
    #Or
    #Param
    #Pass
    "__pow__": binary_op(ast.Pow),
    "__ipow__": aug_assign(ast.Pow),
    #Print
    #PyCF_ONLY_AST
    "__rshift__": binary_op(ast.RShift),
    "__irshift__": aug_assign(ast.RShift),
    #Raise
    "__repr__": ast.Repr,
    #Return
    #Set
    #SetComp
    #Slice
    #Store
    "__str__": ast.Str,
    "__sub__": binary_op(ast.Sub),
    "__isub__": aug_assign(ast.Sub),
    "__getitem__": subscript,
    #Suite
    #TryExcept
    #TryFinally
    #Tuple
    "__pos__": unary_op(ast.UAdd),
    "__neg__": unary_op(ast.USub),
    "__invert__": unary_op(ast.Invert)
    #UnaryOp
    #While
    #With
    #Yield
}

@decorator
def chainable(f, *args, **kwargs):
    bound_args = getcallargs(f, *args, **kwargs)
    self = bound_args["self"]
    results = type(self)(f(**bound_args), self)
    object.__setattr__(results, "operation", f.__name__)
    object.__setattr__(results, "args", bound_args)
    return results


class SymbolicMeta(type):
    """
    """


class Symbol(object):
    """
    Base class for Proxy objects.
    """


    @property
    def ast(self):
        parent = object.__getattribute__(self, "parent")
        if parent is None:
            return ast.Name(object.__getattribute__(self, "name"), ast.Load())
        else:
            node_func = ast_op_nodes[object.__getattribute__(self, "operation")]
            args = object.__getattribute__(self, "args")
            return node_func(**args)

    def __init__(self, state=None, parent=None, name="symbol"):
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "parent", parent)
        object.__setattr__(self, "name", name)

    def __iter__(self):
        return lambda: iter(object.__getattribute__(self, "state"))

    def __nonzero__(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __unicode__(self):
        pass

    @chainable
    def __getattribute__(self, item):
        return lambda: object.__getattribute__(self, item)

    def __hash__(self):
        pass

    @chainable
    def __invert__(self):
        return lambda:-object.__getattribute__(self, "state")

    def __index__(self):
        pass

    @chainable
    def __neg__(self):
        return lambda:-object.__getattribute__(self, "state")

    @chainable
    def __pos__(self):
        return lambda:+object.__getattribute__(self, "state")

    @chainable
    def __abs__(self):
        return lambda: abs(object.__getattribute__(self, "state"))

    @chainable
    def __call__(self, *args, **kwargs):
        return lambda: object.__getattribute__(self, "state")(*args, **kwargs)

    def __reversed__(self):
        return lambda: reversed(object.__getattribute__(self, "state"))

    @chainable
    def __getitem__(self, item):
        return lambda: object.__getattribute__(self, "state")[item]

    @chainable
    def __add__(self, other):
        return lambda: object.__getattribute__(self, "state") + other

    @chainable
    def __sub__(self, other):
        return lambda: object.__getattribute__(self, "state") - other

    @chainable
    def __mul__(self, other):
        return lambda: object.__getattribute__(self, "state") * other

    @chainable
    def __div__(self, other):
        return lambda: object.__getattribute__(self, "state") / other

    def __truediv__(self, other):
        return lambda: object.__getattribute__(self, "state").__truediv__(other)

    @chainable
    def __floordiv__(self, other):
        return lambda: object.__getattribute__(self, "state") // other

    @chainable
    def __mod__(self, other):
        return lambda: object.__getattribute__(self, "state") % other

    def __divmod__(self, other):
        pass

    @chainable
    def __pow__(self, other):
        return lambda: pow(object.__getattribute__(self, "state"))

    @chainable
    def __lshift__(self, other):
        return lambda: object.__getattribute__(self, "state") << other

    @chainable
    def __rshift__(self, other):
        return lambda: object.__getattribute__(self, "state") >> other

    @chainable
    def __radd__(self, other):
        return lambda: other + object.__getattribute__(self, "state")

    @chainable
    def __rand__(self, other):
        return lambda: other & object.__getattribute__(self, "state")

    @chainable
    def __rdiv__(self, other):
        return lambda: other / object.__getattribute__(self, "state")

    @chainable
    def __rdivmod__(self, other):
        return lambda: divmod(other, object.__getattribute__(self, "state"))

    @chainable
    def __rfloordiv__(self, other):
        return lambda: other // object.__getattribute__(self, "state")

    @chainable
    def __rlshift__(self, other):
        return lambda: other << object.__getattribute__(self, "state")

    @chainable
    def __rmod__(self, other):
        return lambda: other % object.__getattribute__(self, "state")

    @chainable
    def __rmul__(self, other):
        return lambda: other * object.__getattribute__(self, "state")

    @chainable
    def __ror__(self, other):
        return lambda: other | object.__getattribute__(self, "state")

    @chainable
    def __rpow__(self, other):
        return lambda: pow(other, object.__getattribute__(self, "state"))

    @chainable
    def __rrshift__(self, other):
        return lambda: other >> object.__getattribute__(self, "state")

    @chainable
    def __rsub__(self, other):
        return lambda: other - object.__getattribute__(self, "state")

    @chainable
    def __rtruediv__(self, other):
        return lambda: object.__getattribute__(self, "state").__rtruediv__(other)

    @chainable
    def __rxor__(self, other):
        return lambda: other ^ object.__getattribute__(self, "state")

    @chainable
    def __contains__(self, item):
        return lambda: item in object.__getattribute__(self, "state")

    @chainable
    def __eq__(self, other):
        return lambda: object.__getattribute__(self, "state") == other

    @chainable
    def __ne__(self, other):
        return lambda: object.__getattribute__(self, "state") != other

    @chainable
    def __le__(self, other):
        return lambda: object.__getattribute__(self, "state") <= other

    @chainable
    def __lt__(self, other):
        return lambda: object.__getattribute__(self, "state") < other

    @chainable
    def __gt__(self, other):
        return lambda: object.__getattribute__(self, "state") > other

    @chainable
    def __ge__(self, other):
        return lambda: object.__getattribute__(self, "state") >= other

    @chainable
    def __cmp__(self, other):
        return lambda: cmp(object.__getattribute__(self, "state"), other)

    @chainable
    def __and__(self, other):
        return lambda: object.__getattribute__(self, "state") & other

    @chainable
    def __xor__(self, other):
        return lambda: object.__getattribute__(self, "state") ^ other

    @chainable
    def __or__(self, other):
        return lambda: object.__getattribute__(self, "state") | other

    @chainable
    def __iand__(self, other):
        return lambda: object.__getattribute__(self, "state").__iand__(other)

    @chainable
    def __ixor__(self, other):
        return lambda: object.__getattribute__(self, "state").__ixor__(other)

    @chainable
    def __ior__(self, other):
        return lambda: object.__getattribute__(self, "state").__ior__(other)

    @chainable
    def __iadd__(self, other):
        return lambda: object.__getattribute__(self, "state").__iadd__(other)

    @chainable
    def __isub__(self, other):
        return lambda: object.__getattribute__(self, "state").__isub__(other)

    @chainable
    def __imul__(self, other):
        return lambda: object.__getattribute__(self, "state").__imul__(other)

    @chainable
    def __idiv__(self, other):
        return lambda: object.__getattribute__(self, "state").__idiv__(other)

    @chainable
    def __itruediv__(self, other):
        return lambda: object.__getattribute__(self, "state").__itruediv__(other)

    @chainable
    def __ifloordiv__(self, other):
        return lambda: object.__getattribute__(self, "state").__ifloordiv__(other)

    @chainable
    def __imod__(self, other):
        return lambda: object.__getattribute__(self, "state").__imod__(other)

    @chainable
    def __ipow__(self, other, modulo=None):
        return lambda: object.__getattribute__(self, "state").__ipow__(other, modulo)

    @chainable
    def __ilshift__(self, other):
        return lambda: object.__getattribute__(self, "state").__ilshift__(other)

    @chainable
    def __irshift__(self, other):
        return lambda: object.__getattribute__(self, "state").__irshift__(other)


if __name__ == "__main__":
    foo = Symbol(1) + 1
    bar = object.__getattribute__(foo, "state")
    print bar()
