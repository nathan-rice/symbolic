from decorator import decorator
import ast
import types
from inspect import getcallargs
from dispatch import DispatchDict

def compile_sym(symbol, mode='eval'):
    if mode == "exec":
        wrapper = ast.Module
    else:
        wrapper = ast.Expression
    tree = wrapper(object.__getattribute__(symbol, "ast"))
    fixed = ast.fix_missing_locations(tree)
    return compile(fixed, '<string>', mode)

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

def ast_call(*args, **kwargs):
    bound_args = getcallargs(object.__getattribute__(type(kwargs["self"]), "__call__"), *args, **kwargs)
    return ast.Call(
        ast_self_node(bound_args["self"]),
        [ast_obj_nodes(v) for v in bound_args["kwargs"]["args"]],
        [ast.keyword(k, ast_obj_nodes(v)) for (k, v) in bound_args["kwargs"]["kwargs"].items()],
        None,
        None
    )

def ast_attr(self, item, ctx=ast.Load):
    return ast.Attribute(
        ast_self_node(self),
        item,
        ctx()
    )

ast_op_nodes = {
    "__add__": binary_op(ast.Add),
    "__iadd__": aug_assign(ast.Add),
    "__getattribute__": ast_attr,
    "__and__": binary_op(ast.BitAnd),
    "__iand__": aug_assign(ast.And),
    "__or__": binary_op(ast.BitOr),
    "__ior__": aug_assign(ast.BitOr),
    "__xor__": binary_op(ast.BitXor),
    "__ixor__": aug_assign(ast.BitXor),
    "__call__": ast_call,
    "__div__": binary_op(ast.Div),
    "__idiv__": aug_assign(ast.Div),
    "__eq__": compare(ast.Eq),
    "__floordiv__": binary_op(ast.FloorDiv),
    "__ifloordiv__": aug_assign(ast.FloorDiv),
    "__gt__": compare(ast.Gt),
    "__ge__": compare(ast.GtE),
    "__inv__": unary_op(ast.Invert),
    "__lshift__": binary_op(ast.LShift),
    "__ilshift__": aug_assign(ast.LShift),
    "__lt__": compare(ast.Lt),
    "__le__": compare(ast.LtE),
    "__mod__": binary_op(ast.Mod),
    "__imod__": aug_assign(ast.Mod),
    "__mul__": binary_op(ast.Mult),
    "__imul__": aug_assign(ast.Mult),
    "__ne__": compare(ast.NotEq),
    "__pow__": binary_op(ast.Pow),
    "__ipow__": aug_assign(ast.Pow),
    "__rshift__": binary_op(ast.RShift),
    "__irshift__": aug_assign(ast.RShift),
    "__sub__": binary_op(ast.Sub),
    "__isub__": aug_assign(ast.Sub),
    "__getitem__": subscript,
    "__pos__": unary_op(ast.UAdd),
    "__neg__": unary_op(ast.USub),
    "__invert__": unary_op(ast.Invert)
}

@decorator
def chainable(f, *args, **kwargs):
    bound_args = getcallargs(f, *args, **kwargs)
    self = bound_args["self"]
    results = type(self)(f(**bound_args), self)
    object.__setattr__(results, "operation", f.__name__)
    object.__setattr__(results, "args", bound_args)
    return results


class Symbol(object):
    """
    Base class for Proxy objects.
    """


    @property
    def ast(self):
        parents = object.__getattribute__(self, "parents")
        if parents is None:
            return ast.Name(object.__getattribute__(self, "name"), ast.Load())
        else:
            node_func = ast_op_nodes[object.__getattribute__(self, "operation")]
            args = object.__getattribute__(self, "args")
            if not callable(node_func): print node_func
            return node_func(**args)

    def __init__(self, state=None, parents=None, name="symbol"):
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "parents", parents)
        object.__setattr__(self, "name", name)

    @chainable
    def __getattribute__(self, item):
        return lambda: object.__getattribute__(self, item)

    @chainable
    def __invert__(self):
        return lambda:-object.__getattribute__(self, "state")

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

ast_obj_nodes = DispatchDict()
ast_obj_nodes.update({
    int: lambda x: ast.Num(x),
    float: lambda x: ast.Num(x),
    str: lambda x: ast.Str(x),
    Symbol: lambda x: ast.Name(object.__getattribute__(x, "name"), ast.Load()),
    tuple: lambda x: ast.Tuple([ast_obj_nodes(y) for y in x], ast.Load())
})
