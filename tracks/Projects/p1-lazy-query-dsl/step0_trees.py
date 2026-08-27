"""
P1 / Step 0 - what a "node" and a "tree" actually are
====================================================

You do not need graph theory. You need one sentence:

    A NODE is an object whose attribute points at ANOTHER OBJECT OF THE SAME KIND.

That is the whole idea. Everything else is vocabulary. You already used this in
lesson 1.3 without calling it a tree.

    python step0_trees.py t1

Same rule as the main ladder: write your prediction first, or it refuses to run.
Four rungs. Then go back to step1_ladder.py rung 7 and re-predict.
"""

import inspect
import sys

PREDICTIONS = {
    "t0": "",
    "t1": "",
    "t2": "",
    "t3": "",
    "t4": "",
}

GRADES = {}


# ---------------------------------------------------------------------------
# T0 - THE TWO KINDS OF TREE. Start here.
# ---------------------------------------------------------------------------

def t0():
    """Two trees. Same numbers. Totally different meaning.

    PREDICT: in panel B, what sits at the ROOT - a number, or a symbol?
    You know the answer from school arithmetic, not from computer science.
    """
    import ast

    class N:
        def __init__(self, label, left=None, right=None):
            self.label, self.left, self.right = label, left, right

    def render(n, depth=0):
        pad = "      " + "    " * depth
        if not isinstance(n, N):
            return f"{pad}{n!r}"
        out = [f"{pad}{n.label}"]
        if n.left is not None:
            out.append(render(n.left, depth + 1))
        if n.right is not None:
            out.append(render(n.right, depth + 1))
        return "\n".join(out)

    # Panel A - a SEARCH tree. Nodes are data. Left is smaller, right is bigger.
    search = N(150, N(100), N(200))

    # Panel B - an EXPRESSION tree for  2 + 3 * 4.  Nodes are operations.
    expression = N("+", 2, N("*", 3, 4))

    print("\n  PANEL A - search tree (what you already know)")
    print("  nodes hold DATA. left < node < right. built to FIND things.")
    print(render(search))

    print("\n  PANEL B - expression tree for  2 + 3 * 4")
    print("  nodes hold OPERATIONS. children are OPERANDS. built to COMPUTE.")
    print(render(expression))
    print("      ^ '*' is deeper than '+' because it is evaluated FIRST.")
    print("        the root is whatever happens LAST.")

    print("\n  PANEL C - Python's own parse of the same source, no library:")
    print("      " + ast.dump(ast.parse("2 + 3 * 4", mode="eval").body))
    return "same shape as panel B - Python builds this for every line you write"


# ---------------------------------------------------------------------------
# T1 - you have already built trees, using lists
# ---------------------------------------------------------------------------

def t1():
    """A list holding a list. Predict each printed value before running."""
    x = [1, [2, 3]]
    return {
        "x[0]": x[0],
        "x[1]": x[1],
        "type of x[1]": type(x[1]).__name__,
        "x[1][0]": x[1][0],
        "how many list objects exist": "you tell me",
    }


# ---------------------------------------------------------------------------
# T2 - the same shape, with names instead of positions
# ---------------------------------------------------------------------------

def t2():
    """Identical structure to T1, but attributes replace indices.

    Predict: what is b.right.left ?
    """

    class Box:
        def __init__(self, left, right):
            self.left = left
            self.right = right

    b = Box(1, Box(2, 3))
    return {
        "b.left": b.left,
        "b.right": b.right.__class__.__name__,
        "b.right.left": b.right.left,
        "b.right.right": b.right.right,
    }


# ---------------------------------------------------------------------------
# T3 - when is a child a COPY, and when is it the SAME object? (lesson 1.3)
# ---------------------------------------------------------------------------

def t3():
    """One leaf, referenced from two places. Predict the two identity checks."""

    class Node:
        def __init__(self, op, left, right):
            self.op = op
            self.left = left
            self.right = right

    leaf = Node("col", "amount", None)
    tree = Node("&",
                Node(">", leaf, 100),
                Node(">", leaf, 200))

    return {
        "tree.left.left is leaf": tree.left.left is leaf,
        "tree.left.left is tree.right.left": tree.left.left is tree.right.left,
        "tree.left is tree.right": tree.left is tree.right,
    }


# ---------------------------------------------------------------------------
# T4 - walking a tree. This is exactly what compile.py will do.
# ---------------------------------------------------------------------------

def t4():
    """PREDICT A NUMBER: how many Node objects does `tree` contain in total?

    Count the leaves too. Then read `walk` and see if you believe it.
    """

    class Node:
        def __init__(self, op, left, right):
            self.op = op
            self.left = left
            self.right = right

    def count(n):
        if not isinstance(n, Node):
            return 0
        return 1 + count(n.left) + count(n.right)

    def render(n, depth=0):
        pad = "    " * depth
        if not isinstance(n, Node):
            return f"{pad}{n!r}"
        out = [f"{pad}{n.op}"]
        out.append(render(n.left, depth + 1))
        if n.right is not None:
            out.append(render(n.right, depth + 1))
        return "\n".join(out)

    amount = Node("col", "amount", None)
    status = Node("col", "status", None)
    tree = Node("&",
                Node(">", amount, 100),
                Node(">", status, 0))

    return "\n\n" + render(tree) + f"\n\n    total Node objects = {count(tree)}\n"


RUNGS = {"t0": t0, "t1": t1, "t2": t2, "t3": t3, "t4": t4}


def main():
    if len(sys.argv) != 2 or sys.argv[1].lower() not in RUNGS:
        print(__doc__)
        return
    key = sys.argv[1].lower()

    if not PREDICTIONS.get(key, "").strip():
        print(f"\n  BLOCKED. PREDICTIONS[{key!r}] is empty.\n")
        print(inspect.getsource(RUNGS[key]))
        return

    print("\n" + "=" * 68)
    print(inspect.getsource(RUNGS[key]))
    print("=" * 68)
    try:
        actual = RUNGS[key]()
    except Exception as exc:
        actual = f"{type(exc).__name__}: {exc}"
    print(f"\n  YOU PREDICTED : {PREDICTIONS[key]}")
    if isinstance(actual, dict):
        print("  ACTUAL        :")
        for k, v in actual.items():
            print(f"      {k:<36} {v!r}")
    else:
        print(f"  ACTUAL        : {actual}")
    print()


if __name__ == "__main__":
    main()
