"""
Drill 1.1 - Objects: identity, type, value
==========================================

Tooling for the hands-on. Run `python d11_object_identity.py` first to get
your environment report, then work the drills.

Depth: contains CPython implementation-detail probes (ctypes header reads).
Everything marked [CPython] is NOT a Python language guarantee.
"""

import ctypes
import sys
import sysconfig


# --------------------------------------------------------------------------
# Environment report. Your drill results are uninterpretable without this.
# --------------------------------------------------------------------------

def whoami():
    gil_disabled = sysconfig.get_config_var("Py_GIL_DISABLED")
    print("implementation :", sys.implementation.name)
    print("version        :", sys.version.split()[0])
    print("pointer size   :", ctypes.sizeof(ctypes.c_void_p), "bytes")
    print("free-threaded  :", bool(gil_disabled))
    print("immortal ints  :", sys.version_info >= (3, 12))
    if hasattr(sys, "_is_gil_enabled"):
        print("GIL enabled    :", sys._is_gil_enabled())


# --------------------------------------------------------------------------
# [CPython] Reading the object header out of live memory.
#
# In a standard (GIL) CPython build, every object starts with:
#     offset 0 : Py_ssize_t   ob_refcnt
#     offset 8 : PyTypeObject *ob_type      (on 64-bit)
#
# In a free-threaded build the header is a completely different struct.
# So we do not assume - we verify.
# --------------------------------------------------------------------------

_WORD = ctypes.sizeof(ctypes.c_void_p)


def raw_refcount(obj):
    """[CPython] Read ob_refcnt directly. Does NOT create a temp reference,
    unlike sys.getrefcount()."""
    return ctypes.c_ssize_t.from_address(id(obj)).value


def raw_type_ptr(obj):
    """[CPython] Read ob_type directly."""
    return ctypes.c_void_p.from_address(id(obj) + _WORD).value


def layout_is_sane():
    """Verify the classic header layout actually holds on this build.
    If this returns False, every raw_* reading below is garbage - stop and
    tell me, do not trust the numbers."""
    probe = ["sentinel"]
    return raw_type_ptr(probe) == id(list)


def header(obj, label=""):
    print(f"{label:<14} id={id(obj):#x}  refcnt={raw_refcount(obj)}  "
          f"ob_type={raw_type_ptr(obj):#x} ({type(obj).__name__})")


# --------------------------------------------------------------------------
# [CPython] Reading an int's VALUE out of its payload.
#
# A PyLongObject is the standard header followed by a size/tag word and then
# an array of 30-bit digits:
#     offset 0  : ob_refcnt
#     offset 8  : ob_type
#     offset 16 : ob_size (<=3.11) / lv_tag (3.12+)  - same slot, new meaning
#     offset 24 : ob_digit[0]  - the low 30 bits of the value
# --------------------------------------------------------------------------

def raw_int_value(n):
    """[CPython] Read ob_digit[0] straight out of the object.
    Valid for 1 <= n < 2**30 on standard builds."""
    return ctypes.c_uint32.from_address(id(n) + 3 * _WORD).value


def int_layout_is_sane():
    """If this is False, raw_int_value is reading the wrong offset on your
    build - stop and report it rather than trusting the numbers."""
    return all(raw_int_value(v) == v for v in (1, 7, 100, 12345, 2 ** 29))


def dissect_int(n):
    """Show address, type pointer and payload side by side, so the address
    and the value cannot be confused for each other."""
    print(f"python-level value : {n}")
    print(f"id(n)  [address]   : {id(n):#x}  ({id(n)})")
    print(f"ob_type            : {raw_type_ptr(n):#x}  == id(int)? "
          f"{raw_type_ptr(n) == id(int)}")
    print(f"ob_refcnt          : {raw_refcount(n)}")
    print(f"ob_digit[0] [value]: {raw_int_value(n)}")


def show_layout(*values):
    """[CPython] Print the type-object / instance-object split with real
    addresses. 'int is an object' means ONE shared type object that every
    instance points at - not one box that all integers live inside."""
    groups = {}
    for v in values:
        groups.setdefault(type(v), []).append(v)
    for t, members in groups.items():
        print(f"TYPE OBJECT  {t.__name__:<9} @ {id(t):#x}")
        for v in members:
            verdict = "points at it" if raw_type_ptr(v) == id(t) else "MISMATCH"
            print(f"   instance  {v!r:<9} @ {id(v):#x}   "
                  f"ob_type -> {raw_type_ptr(v):#x}  {verdict}")


# --------------------------------------------------------------------------
# D3 scaffold - an object that lies about its class.
# --------------------------------------------------------------------------

class Liar:
    @property
    def __class__(self):
        return int


# --------------------------------------------------------------------------
# D7 scaffold - watch what happens to identity across a "value change".
# --------------------------------------------------------------------------

def mutate_vs_rebind():
    a = [1, 2, 3]
    before = id(a)
    a.append(4)
    after_mutate = id(a)
    a = a + [5]
    after_rebind = id(a)
    return before, after_mutate, after_rebind


if __name__ == "__main__":
    whoami()
    print("\nheader layout verified:", layout_is_sane())
