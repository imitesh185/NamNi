"""
Drill 1.3 - References, aliasing and containers
===============================================

Companion code. Import pieces in a bare REPL as the drills call for them.
"""

import copy


# --------------------------------------------------------------------------
# D1 - a container is a collection of references, not of values.
# --------------------------------------------------------------------------

def reference_map(container):
    """id() of every slot, so shared objects become visible."""
    return [(i, type(v).__name__, hex(id(v))) for i, v in enumerate(container)]


def repeated_reference():
    """[[]] * 3 does not create three lists."""
    rows = [[]] * 3
    rows[0].append("x")
    return rows


def built_properly():
    rows = [[] for _ in range(3)]
    rows[0].append("x")
    return rows


# --------------------------------------------------------------------------
# D2 - the three depths of copying.
# --------------------------------------------------------------------------

def copy_depths():
    original = [[1, 2], [3, 4]]
    return {
        "alias": original,
        "slice": original[:],
        "list()": list(original),
        "copy.copy": copy.copy(original),
        "copy.deepcopy": copy.deepcopy(original),
        "_original": original,
    }


# --------------------------------------------------------------------------
# D3 - argument passing needs no new rule.
# --------------------------------------------------------------------------

def rebind_vs_mutate(seq):
    seq.append("mutated")
    seq = ["rebound"]
    seq.append("invisible")
    return seq


def leaky_default(item, bucket=[]):
    bucket.append(item)
    return bucket


def safe_default(item, bucket=None):
    bucket = [] if bucket is None else bucket
    bucket.append(item)
    return bucket


# --------------------------------------------------------------------------
# D4 - the += paradox. Raises TypeError AND mutates. Both.
# --------------------------------------------------------------------------

def tuple_iadd_paradox():
    t = ([1, 2], 3)
    try:
        t[0] += [9]
    except TypeError as exc:
        return t, f"{type(exc).__name__}: {exc}"
    return t, "no error raised"


def list_iadd_vs_plus():
    a = [1, 2]
    b = a
    a += [3]
    same_after_iadd = a is b

    c = [1, 2]
    d = c
    c = c + [3]
    same_after_plus = c is d
    return (a, b, same_after_iadd), (c, d, same_after_plus)


# --------------------------------------------------------------------------
# D5 - structures that refer to themselves.
# --------------------------------------------------------------------------

def self_referential():
    a = [1, 2]
    a.append(a)
    return a, a[2] is a
