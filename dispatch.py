import sys

if sys.version_info < (3, 0):
    iterator_next = "next"
else:
    iterator_next = "__next__"

class AbstractDispatchDict(dict):
    """
    This
    """

    def __call__(self, key, *args, **kwargs):
        """
        because AbstractDispatchDicts are callable, any nested AbstractDispatchDicts
        in values will propagate the lookup, allowing you to form dispatch trees. 
        """
        return self.__getitem__(key)(key, *args, **kwargs)

    def __getitem__(self, key):
        global iterator_next
        key_closure = self.key_closure(key)
        first_key = getattr(key_closure, iterator_next)()
        def get_target():
            for key in key_closure:
                translator = dict.get(self, key)
                if translator != None:
                    dict.__setitem__(self, first_key, translator)
                    return translator
            raise KeyError("No dispatch target found for %s" % key)
        return dict.get(self, first_key) or get_target()

    @classmethod
    def key_closure(self, key):
        return NotImplemented


class DispatchDict(AbstractDispatchDict):

    @classmethod
    def key_closure(cls, k):
        mro = isinstance(k, type) and k.__mro__ or type(k).__mro__
        for class_ in mro:
            yield class_
