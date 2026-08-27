"""
P1 / Step 1 - the ladder
========================

Eight rungs. Each is two or three lines. By rung 8 you will have built the core
of `expr.py` without me ever handing it to you.

HOW TO USE
----------
    python step1_ladder.py 1

The runner REFUSES to execute a rung until you have written a prediction for it
in PREDICTIONS below. That refusal is the whole point: a result you see without
having committed a guess first teaches you nothing, because your model was never
exposed and so can never be corrected.

Write the prediction in plain English. It does not need to be right. A confident
wrong answer is worth ten times a hedge - only a wrong answer can be corrected.

One rung at a time. Predict, run, compare, self-grade in GRADES. Then next rung.
"""

import inspect
import sys

# ---------------------------------------------------------------------------
# YOUR PREDICTIONS. Fill one line before running that rung. Leave the rest.
# ---------------------------------------------------------------------------

PREDICTIONS = {
    1: "True, True, True - Because __gt__ is called explicilty it will check 5>3 and return True, for second as 5>3 will implicilty call __gt__ {as it will default to special mehtod} and return True, not sure about third but it seems as both are of Type bool and has value True it will point to 1 object id which will result in True",
    2: "It will return a string, I cannot reason why but I feel its because of type",
    3: "result will be the string return from rung2, bool(result) will be True because the string is not empty",
    4: "I'm not sure if it will print the string of __gt__ implemented but since if will evaluate to True it will print 'TOOK THE TRUE BRANCH'",
    5: "with & will return '&-node' because it will call __and__ explicitly, and keyword will return 'x' as it will check Truthness of a and b, as a will return Non-Zero value and 'x' will give Non-Zero value it will print b",
    6: "All will raise TypeError apart from last __gt__; 1st and 2nd will raise TypeError as it will call __bool__; Not sure about 3rd because it should resolve to Truthness; first I thought we are explicilty raising TypeError but when I checked with some random value if T returns string it should be True but its giving should return __bool__ returned __str__ not understanding",
    7: "",
    8: "",
}

# After running, mark yourself: "hit" or "miss". Misses are the valuable ones.
GRADES = {1: "hit", 2:"hit", 3:"hit", 4:"hit", 5:"hit", 6:"partial hit", 7:"", 8:""}


# ---------------------------------------------------------------------------
# Rung 1 - is `>` really a method call?
# ---------------------------------------------------------------------------

def rung1():
    """What does `>` actually do on two ints? Predict the printed value."""
    a = (5).__gt__(3)
    b = 5 > 3
    return a, b, a == b


# ---------------------------------------------------------------------------
# Rung 2 - what is a comparison ALLOWED to return?
# ---------------------------------------------------------------------------

def rung2():
    """Predict what `t > 3` evaluates to. Look hard at the return statement."""

    class Thing:
        def __gt__(self, other):
            return f"a greater-than between me and {other!r}"

    t = Thing()
    return t > 3


# ---------------------------------------------------------------------------
# Rung 3 - so what is that thing's truthiness?
# ---------------------------------------------------------------------------

def rung3():
    """`t > 3` gave you a string last rung. Predict bool() of it."""

    class Thing:
        def __gt__(self, other):
            return f"a greater-than between me and {other!r}"

    t = Thing()
    result = t > 3
    return result, bool(result)


# ---------------------------------------------------------------------------
# Rung 4 - the danger
# ---------------------------------------------------------------------------

def rung4():
    """Which branch runs? Predict BEFORE reading the branch bodies twice."""

    class Thing:
        def __gt__(self, other):
            return f"a greater-than between me and {other!r}"

    t = Thing()
    if t > 999999999:
        return "TOOK THE TRUE BRANCH"
    return "took the false branch"


# ---------------------------------------------------------------------------
# Rung 5 - `and` is not `&`
# ---------------------------------------------------------------------------

def rung5():
    """Two lines, two very different mechanisms. Predict both return values."""

    class Thing:
        def __gt__(self, other):
            return "gt-node"

        def __and__(self, other):
            return "and-node"

        def __repr__(self):
            return "Thing()"

    t = Thing()
    with_ampersand = t & "x"
    with_keyword = t and "x"
    return with_ampersand, with_keyword


# ---------------------------------------------------------------------------
# Rung 6 - the refusal
# ---------------------------------------------------------------------------

def rung6():
    """Now the object refuses to be a boolean. Predict what each attempt does."""

    class Thing:
        def __gt__(self, other):
            return "gt-node"

        def __bool__(self):
            raise TypeError("ambiguous: use & and | , not `and` / `or`")

    t = Thing()
    outcomes = {}
    for label, fn in [
        ("bool(t)", lambda: bool(t)),
        ("t and 1", lambda: t and 1),
        ("if t:", lambda: "true branch" if t else "false branch"),
        ("t > 5", lambda: t > 5),
    ]:
        try:
            outcomes[label] = repr(fn())
        except Exception as exc:
            outcomes[label] = f"{type(exc).__name__}: {exc}"
    return outcomes


# ---------------------------------------------------------------------------
# Rung 7 - nesting. Where does a TREE come from?
# ---------------------------------------------------------------------------

def rung7():
    """Predict the STRUCTURE of the final object. How many Nodes exist, nested how?"""

    class Node:
        def __init__(self, op, left, right):
            self.op = op
            self.left = left
            self.right = right

        def __gt__(self, other):
            return Node(">", self, other)

        def __and__(self, other):
            return Node("&", self, other)

    leaf = Node("col", "amount", None)
    built = (leaf > 100) & (leaf > 200)
    return type(built).__name__, built.op, type(built.left).__name__, built.left.op


# ---------------------------------------------------------------------------
# Rung 8 - make the tree visible
# ---------------------------------------------------------------------------

def rung8():
    """One method added since rung 7. Predict the printed line."""

    class Node:
        def __init__(self, op, left, right):
            self.op = op
            self.left = left
            self.right = right

        def __gt__(self, other):
            return Node(">", self, other)

        def __and__(self, other):
            return Node("&", self, other)

        def __repr__(self):
            if self.op == "col":
                return f"col({self.left!r})"
            return f"({self.left!r} {self.op} {self.right!r})"

    amount = Node("col", "amount", None)
    status = Node("col", "status", None)
    return (amount > 100) & (status > 0)


RUNGS = {1: rung1, 2: rung2, 3: rung3, 4: rung4,
         5: rung5, 6: rung6, 7: rung7, 8: rung8}


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print(__doc__)
        return
    n = int(sys.argv[1])
    if n not in RUNGS:
        print(f"No rung {n}. Pick 1-8.")
        return

    if not PREDICTIONS.get(n, "").strip():
        print(f"\n  BLOCKED. PREDICTIONS[{n}] is empty.\n")
        print("  Read the rung below, write what you think it prints into")
        print(f"  PREDICTIONS[{n}] in this file, then run it again.\n")
        print(inspect.getsource(RUNGS[n]))
        return

    print("\n" + "=" * 68)
    print(inspect.getsource(RUNGS[n]))
    print("=" * 68)
    try:
        actual = RUNGS[n]()
    except Exception as exc:
        actual = f"{type(exc).__name__}: {exc}"
    print(f"\n  YOU PREDICTED : {PREDICTIONS[n]}")
    print(f"  ACTUAL        : {actual!r}\n")
    print("  Same? Put 'hit' or 'miss' in GRADES. A miss is the useful case -")
    print("  write one line on what your model got wrong, then go to the next rung.\n")


if __name__ == "__main__":
    main()
