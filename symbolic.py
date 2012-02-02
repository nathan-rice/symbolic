class Symbol(object):
    """
    Base class for Proxy objects.
    """

    def __init__(self, iterable=tuple(), parent=None):
        self.iterable = iterable
        self.parent = parent


    def __getattr__(self, item):
        iterable = IteratorProxy(_iterable(self), _cacheable(self))
        return type(self)((e.__getattribute__(item) for e in iterable), self)

    def __iter__(self):
        return iter(_iterable(self))

    def __nonzero__(self):
        return bool(_iterable(self))

    def __str__(self):
        return ", ".join(str(e) for e in _iterable(self))

    def __repr__(self):
        return "%s([%s])" % (type(self).__name__ , ", ".join(repr(e) for e in _iterable(self)))

    def __unicode__(self):
        return u", ".join(unicode(e) for e in _iterable(self))

    def __reversed__(self):
        return lambda: reversed(_iterable(self))

    def __getattribute__(self, item):
        pass

    def __hash__(self):
        return lambda: (hash(e) for e in _iterable(self))

    def __invert__(self):
        return lambda: (~e for e in _iterable(self))

    def __index__(self):
        return lambda: (operator.index(e) for e in _iterable(self))

    def __neg__(self):
        return lambda: (-e for e in _iterable(self))

    def __pos__(self):
        return lambda: (+e for e in _iterable(self))

    def __abs__(self):
        return lambda: (e.__abs__() for e in _iterable(self))

    def __call__(self, *args, **kwargs):
        return lambda: self.f(*args, **kwargs)

    def __getattr__(self, attr):
        return lambda: getattr(self.f, attr)

    def __reversed__(self):
        return lambda: reversed(self.f)

    def __getitem__(self, item):
        return lambda: self.f[item]

    def __hash__(self):
        return lambda: hash(self.f)

    def __invert__(self):
        return lambda:~self.f

    def __index__(self):
        return lambda: operator.index(self.f)

    def __neg__(self):
        return lambda:-self.f

    def __pos__(self):
        return lambda:+self.f

    def __abs__(self):
        return lambda: abs(self.f)

    def __add__(self, other):
        return lambda: self.f + other

    def __sub__(self, other):
        return lambda: self.f - other

    def __mul__(self, other):
        return lambda: self.f * other

    def __floordiv__(self, other):
        return lambda: self.f // other

    def __mod__(self, other):
        return lambda: self.f % other

    def __divmod__(self, other):
        return lambda: divmod(self.f, other)

    def __pow__(self, other, modulo=None):
        return lambda: pow(self.f, other, modulo)

    def __lshift__(self, other):
        return lambda: self.f << other

    def __rshift__(self, other):
        return lambda: self.f >> other

    def __div__(self, other):
        return lambda: self.f / other

    def __truediv__(self, other):
        return lambda: self.f.__truediv__(other)

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
