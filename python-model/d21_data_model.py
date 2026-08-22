"""
Drill 2.1 - The data model: special methods as protocol hooks
=============================================================

Companion code. Import pieces in a bare REPL as the drills call for them.

The single claim under test: syntax and builtins do not "know" about your
object. They look up a named method ON THE TYPE and call it.
"""

import dis


# --------------------------------------------------------------------------
# D0 - the probe. Which hooks does this object's TYPE actually define?
# --------------------------------------------------------------------------

PROTOCOLS = {
    "repr":      ("__repr__",),
    "str":       ("__str__",),
    "format":    ("__format__",),
    "len":       ("__len__",),
    "bool":      ("__bool__",),
    "index":     ("__getitem__",),
    "contains":  ("__contains__",),
    "iter":      ("__iter__",),
    "call":      ("__call__",),
    "eq":        ("__eq__",),
    "hash":      ("__hash__",),
    "add":       ("__add__", "__radd__", "__iadd__"),
    "context":   ("__enter__", "__exit__"),
}


def protocol_map(obj):
    """Hooks defined on type(obj), ignoring anything on the instance.

    Reports the DEFINING class, so you can see what came from `object`
    for free and what you actually wrote.
    """
    t = type(obj)
    out = {}
    for label, names in PROTOCOLS.items():
        found = []
        for name in names:
            for klass in t.__mro__:
                if name in vars(klass):
                    if vars(klass)[name] is not None:
                        found.append(f"{name}<-{klass.__name__}")
                    else:
                        found.append(f"{name}=None<-{klass.__name__}")
                    break
        if found:
            out[label] = found
    return out


# --------------------------------------------------------------------------
# D1 - syntax is a method call. Make the call audible.
# --------------------------------------------------------------------------

class Loud:
    """Announces every hook the interpreter reaches for."""

    def __len__(self):
        print("  -> __len__")
        return 3

    def __getitem__(self, key):
        print(f"  -> __getitem__({key!r})")
        if isinstance(key, int) and key >= 3:
            raise IndexError(key)
        return key

    def __add__(self, other):
        print(f"  -> __add__({other!r})")
        return "added"

    def __call__(self, *args):
        print(f"  -> __call__{args}")
        return "called"


def show_bytecode():
    """No hidden magic: the opcodes name the operation, the type supplies it."""
    def ops(x, y):
        return x + y, x[0], len(x), bool(x)

    dis.dis(ops)


# --------------------------------------------------------------------------
# D2 - implicit lookup skips the instance.
# --------------------------------------------------------------------------

class Sneaky:
    def __len__(self):
        return 1


def instance_dunder_is_ignored():
    s = Sneaky()
    s.__len__ = lambda: 99
    return {
        "len(s)": len(s),
        "s.__len__()": s.__len__(),
        "type(s).__len__(s)": type(s).__len__(s),
        "in instance dict": "__len__" in vars(s),
    }


# --------------------------------------------------------------------------
# D3 - the two string protocols.
# --------------------------------------------------------------------------

class OnlyRepr:
    def __repr__(self):
        return "OnlyRepr(unambiguous)"


class OnlyStr:
    def __str__(self):
        return "OnlyStr(readable)"


class BothStrings:
    def __repr__(self):
        return "BothStrings(repr)"

    def __str__(self):
        return "BothStrings(str)"


def string_matrix(obj):
    return {
        "repr()": repr(obj),
        "str()": str(obj),
        "f'{}'": f"{obj}",
        "f'{!r}'": f"{obj!r}",
        "in a list": repr([obj]),
        "print": None,  # run print(obj) yourself and compare
    }


# --------------------------------------------------------------------------
# D4 - one method, several powers.
# --------------------------------------------------------------------------

class Countdown:
    """Defines __getitem__ and nothing else. Watch what it can already do."""

    def __init__(self, start):
        self.start = start

    def __getitem__(self, i):
        if i >= self.start:
            raise IndexError(i)
        return self.start - i


def free_powers(n=4):
    c = Countdown(n)
    first, second, *rest = c
    return {
        "for loop": [v for v in c],
        "list()": list(c),
        "in": 2 in c,
        "unpacking": (first, second, rest),
        "has __iter__": hasattr(type(c), "__iter__"),
        "has __contains__": hasattr(type(c), "__contains__"),
    }


# --------------------------------------------------------------------------
# D5 - the truthiness fallback chain.
# --------------------------------------------------------------------------

class NoHooks:
    pass


class HasLen:
    def __init__(self, n):
        self.n = n

    def __len__(self):
        return self.n


class HasBool(HasLen):
    def __bool__(self):
        return True


def truth_table():
    return {
        "NoHooks()": bool(NoHooks()),
        "HasLen(0)": bool(HasLen(0)),
        "HasLen(5)": bool(HasLen(5)),
        "HasBool(0)": bool(HasBool(0)),
    }


# --------------------------------------------------------------------------
# D6 - operators, NotImplemented, and the __eq__ / __hash__ coupling.
# --------------------------------------------------------------------------

class Money:
    def __init__(self, rupees):
        self.rupees = rupees

    def __repr__(self):
        return f"Money({self.rupees})"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.rupees == other.rupees


class HashableMoney(Money):
    def __hash__(self):
        return hash(self.rupees)


def equality_and_hash():
    a, b = Money(5), Money(5)
    result = {
        "a == b": a == b,
        "a is b": a is b,
        "a == 5": a == 5,
        "type(a).__hash__": Money.__hash__,
    }
    try:
        hash(a)
    except TypeError as exc:
        result["hash(a)"] = f"{type(exc).__name__}: {exc}"
    else:
        result["hash(a)"] = "no error"

    h = HashableMoney(5)
    result["hash(HashableMoney(5))"] = hash(h) == hash(5)
    result["set dedupes"] = len({HashableMoney(5), HashableMoney(5)})
    return result


class Reflected:
    """__radd__ only. Proves the interpreter tries the right operand second."""

    def __radd__(self, other):
        return f"radd saw {other!r}"
