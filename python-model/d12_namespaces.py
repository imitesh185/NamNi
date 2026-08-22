"""
Drill 1.2 - Namespaces: the name -> object mapping
==================================================

Companion code. Run this file for the environment probe, then import the
individual pieces in a bare REPL as the drills call for them.

Marked [CPython] where the behaviour is implementation, not language.
"""

import dis
import sys


SOME_GLOBAL = 42


# --------------------------------------------------------------------------
# D1 / D2 - is a namespace really just a mapping?
# --------------------------------------------------------------------------

def module_level_probe():
    """At module level, locals() and globals() are the SAME object."""
    return locals() is globals()


def names_bound_to(obj, namespace=None):
    """Every name in the namespace currently referring to this exact object.
    Uses `is`, not `==` - we are asking about references, not values."""
    ns = globals() if namespace is None else namespace
    return sorted(k for k, v in ns.items() if v is obj)


# --------------------------------------------------------------------------
# D3 - function locals are not a dict you can write to.
# PEP 667 (3.13+) made locals() return an independent snapshot each call.
# --------------------------------------------------------------------------

def locals_is_a_snapshot():
    a = 1
    snap = locals()
    b = 2
    return snap, locals()


def try_to_write_through_locals():
    a = 1
    locals()['a'] = 999
    return a


# --------------------------------------------------------------------------
# D4 - [CPython] why the two lookups above behave differently.
# --------------------------------------------------------------------------

def compare_bytecode():
    def uses_local():
        v = 1
        return v

    def uses_global():
        return SOME_GLOBAL

    print("--- local name access ---")
    dis.dis(uses_local)
    print("--- global name access ---")
    dis.dis(uses_global)


# --------------------------------------------------------------------------
# D6 - a class body is a namespace, but NOT an enclosing scope.
# --------------------------------------------------------------------------

class ClassBodyScope:
    y = 1

    def bare_name(self):
        return y

    def via_self(self):
        return self.y


# --------------------------------------------------------------------------
# D7 - the except-as name is unbound when the block exits.
# --------------------------------------------------------------------------

def err_survives_the_block():
    try:
        1 / 0
    except ZeroDivisionError as err:
        pass
    return "err" in locals()


if __name__ == "__main__":
    print("python                       :", sys.version.split()[0])
    print("module locals() is globals()  :", module_level_probe())
    print("globals() is a", type(globals()).__name__)
