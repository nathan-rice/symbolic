from decorator import decorator
import ast
import types
from inspect import getcallargs
from dispatch import DispatchDict
from itertools import chain

def sym_getattr(sym, attr_name, *default):
    try:
        return object.__getattribute__(sym, attr_name)
    except AttributeError:
        if len(default) > 0:
            return default[0]
        else:
            raise

def compile_sym(symbol):
    prior = object.__getattribute__(symbol, "prior")
    module = [object.__getattribute__(s, "ast") for s in prior]
    parent = object.__getattribute__(symbol, "parent")
    results = object.__getattribute__(symbol, "ast")
    if module:
        mode = 'exec'
        if parent:
            module.append(ast.Expr(results))
        results = ast.Module(module)
    else:
        mode = 'eval'
        results = ast.Expression(results)
    try:
        return compile(ast.fix_missing_locations(results), '<string>', mode)
    except TypeError as err:
        print ast.dump(object.__getattribute__(symbol, 'ast'))
        raise

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

def ast_attr(ctx):
    def _ast_attr(self, item):
        return ast.Attribute(
            ast_self_node(self),
            item,
            ctx()
        )
    return _ast_attr

def ast_assign(self, item, value):
    return ast.Assign(
        [
            ast.Attribute(
                ast_self_node(self),
                item,
                ast.Store()
            )
        ],
        ast_obj_nodes(value)
    )


ast_op_nodes = {
    "__add__": binary_op(ast.Add),
    "__iadd__": aug_assign(ast.Add),
    "__getattribute__": ast_attr(ast.Load),
    "__and__": binary_op(ast.BitAnd),
    "__iand__": aug_assign(ast.BitAnd),
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
    "__setitem__": subscript,
    "__pos__": unary_op(ast.UAdd),
    "__neg__": unary_op(ast.USub),
    "__invert__": unary_op(ast.Invert),
    "__setattr__": ast_assign
}

ast_stmt_nodes = {
    "__iadd__",
    "__isub__",
    "__imul__",
    "__idiv__",
    "__ifloordiv__",
    "__idivmod__",
    "__ipow__",
    "__imod__",
    "__iand__",
    "__ior__",
    "__ixor__",
    "__ilshift__",
    "__irshift__",
    "__setattr__"
}

def copy_chainable(obj, **kwargs):
    args = kwargs.pop("args", object.__getattribute__(obj, "args"))
    state = kwargs.pop("state", object.__getattribute__(obj, "state"))
    operation = kwargs.pop("operation", object.__getattribute__(obj, "operation"))
    parent = kwargs.pop("parent", object.__getattribute__(obj, "parent"))
    name = kwargs.pop("name", object.__getattribute__(obj, "name"))
    prior = kwargs.pop("prior", object.__getattribute__(obj, "prior"))
    return type(obj)(state, parent, prior, name, operation, args)


@decorator
def chainable(f, *args, **kwargs):
    bound_args = getcallargs(f, *args, **kwargs)
    self = bound_args["self"]
    state = f(**bound_args)
    prior = object.__getattribute__(self, "prior")
    all_sym = filter(lambda x: x != "self" and isinstance(bound_args[x], Symbol), bound_args)
    chainable_args = chain.from_iterable(sym_getattr(bound_args[i], "prior") for i in all_sym)
    if chainable_args:
        prior += tuple(chainable_args) # Will be empty if no other
    name = object.__getattribute__(self, "name")
    type_self = type(self)
    results = type_self(state, self, prior)
    object.__setattr__(results, "operation", f.__name__)
    object.__setattr__(results, "args", bound_args)
    # If the operation was a statement we need to add the result to previous
    # and start a new chain.
    if f.__name__ in ast_stmt_nodes:
        prior += (results,)
        results = type_self(prior=prior, name=name)
    return results

@decorator
def pseudochainable(f, *args, **kwargs):
    """
    This takes a non-chainable statement on a Symbol and emulates chainable
    behavior by inserting nodes between this node and its parent, then
    updating the state of the current node to appear as if it were the result
    of a chained call.
    
    A visual representation may be somewhat clearer.  Letters represent
    node identity and numbers represent temporal location:
    
    Before:  (A 0) -> (B 1)
    After: (A 0) -> (C 1) -> (D 2) -> (B 3)
    
    Node C represents a copy of node B in the before state.  Node D represents
    the statement operation, which is not chainable.  Node B now represents the
    start of a new expression, with a prior expression tuple of (*D's priors, D). 
    """
    # First lets collect all the required values
    bound_args = getcallargs(f, *args, **kwargs)
    self = bound_args["self"]
    # We need to make a copy of this node and insert it between this node
    # and its parent.
    old_self = copy_chainable(self)
    # We then need to create the statement terminating node
    terminator = copy_chainable(self, state=f(**bound_args), parent=old_self, operation=f.__name__, args=bound_args)
    # Finally we need to update the current chainable to indicate that it
    # is now an empty node (save name and priors).
    prior = sym_getattr(terminator, "prior") + (terminator,)
    object.__setattr__(self, "operation", None)
    object.__setattr__(self, "args", None)
    object.__setattr__(self, "state", None)
    object.__setattr__(self, "parent", None)
    object.__setattr__(self, "prior", prior)
    # Name should already be set properly, so that is it!
    # Note that this is a pointless return as this decorator is
    # only used for statement terminating methods...
    return self



class Symbol(object):
    """
    Base class for Proxy objects.
    """

#    def __str__(self):
#        pass
#    
    def __repr__(self):
        return ast.dump(object.__getattribute__(self, "ast"))

    @property
    def ast(self):
        parent = object.__getattribute__(self, "parent")
        if parent is None:
            return ast.Name(object.__getattribute__(self, "name"), ast.Load())
        else:
            node_func = ast_op_nodes.get(
                object.__getattribute__(self, "operation"),
                None
            )
            if node_func:
                args = object.__getattribute__(self, "args")
                return node_func(**args)
            else:
                return ast.Name(object.__getattribute__(self, "name"), ast.Load())

    def __init__(self, state=None, parent=None, prior=None, name=None, operation=None, args=None):
        """By default, children should get attributes from their parents."""
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "parent", parent)
        object.__setattr__(self, "prior", prior or sym_getattr(parent, "prior", tuple()))
        object.__setattr__(self, "name", name or sym_getattr(parent, "name", "symbol"))
        object.__setattr__(self, "operation", operation or sym_getattr(parent, "operation", None))
        object.__setattr__(self, "args", args or sym_getattr(parent, "args", None))

    @chainable
    def __getattribute__(self, item):
        return lambda: object.__getattribute__(self, item)

    @pseudochainable
    def __setattr__(self, item, value):
        return lambda: object.__setattr__(self, item, value)

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

    @chainable
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
    def __ipow__(self, other):
        return lambda: object.__getattribute__(self, "state").__ipow__(other)

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
    Symbol: lambda x: object.__getattribute__(x, "ast"),
    tuple: lambda x: ast.Tuple([ast_obj_nodes(y) for y in x], ast.Load())
})
