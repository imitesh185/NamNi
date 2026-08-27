"""
P2 / the ladder - what actually decides whether dedup is correct
===============================================================

Prerequisites: lesson 1.1 (identity vs value), 1.3 (aliasing, mutation),
2.1 sec 06 (__eq__ / __hash__). Nothing else. No trees, no recursion.

    python ladder.py 1

Refuses to run a rung until PREDICTIONS[n] is filled in. Predict, run, compare,
grade. Six rungs. By rung 4 you will have an object that is sitting inside a set
while the set denies containing it.
"""

import inspect
import sys
import time

PREDICTIONS = {
    1: "False - different instantiated objects, even though values are same; False - different id's for different objects, 2, True - Both have the same items",
    2: "",
    3: "",
    4: "",
    5: "",
    6: "",
}

GRADES = {}


# ---------------------------------------------------------------------------
# R1 - two rows, same data. Are they the same row?
# ---------------------------------------------------------------------------

def rung1():
    """A plain class, no dunders. Predict all four values."""

    class Txn:
        def __init__(self, txn_id, amount):
            self.txn_id = txn_id
            self.amount = amount

    a = Txn("T1", 500)
    b = Txn("T1", 500)

    return {
        "a == b": a == b,
        "a is b": a is b,
        "len({a, b})": len({a, b}),
        "a.__dict__ == b.__dict__": a.__dict__ == b.__dict__,
    }


# ---------------------------------------------------------------------------
# R2 - teach it what "same" means
# ---------------------------------------------------------------------------

def rung2():
    """Only __eq__ added. Predict each line - one of them raises."""

    class Txn:
        def __init__(self, txn_id, amount):
            self.txn_id = txn_id
            self.amount = amount

        def __eq__(self, other):
            return (self.txn_id, self.amount) == (other.txn_id, other.amount)

    a = Txn("T1", 500)
    b = Txn("T1", 500)

    out = {"a == b": repr(a == b), "Txn.__hash__": repr(Txn.__hash__)}
    for label, fn in [("hash(a)", lambda: hash(a)),
                      ("len({a, b})", lambda: len({a, b})),
                      ("{a: 1}", lambda: {a: 1})]:
        try:
            out[label] = repr(fn())
        except Exception as exc:
            out[label] = f"{type(exc).__name__}: {exc}"
    return out


# ---------------------------------------------------------------------------
# R3 - dedup finally works
# ---------------------------------------------------------------------------

def rung3():
    """__hash__ restored. PREDICT THE NUMBER: how many rows survive dedup?"""

    class Txn:
        def __init__(self, txn_id, amount):
            self.txn_id = txn_id
            self.amount = amount

        def __eq__(self, other):
            return (self.txn_id, self.amount) == (other.txn_id, other.amount)

        def __hash__(self):
            return hash((self.txn_id, self.amount))

        def __repr__(self):
            return f"Txn({self.txn_id!r}, {self.amount})"

    raw = [Txn("T1", 500), Txn("T1", 500), Txn("T2", 900),
           Txn("T1", 501), Txn("T2", 900)]

    deduped = set(raw)
    return {"input rows": len(raw), "after dedup": len(deduped),
            "survivors": sorted(repr(t) for t in deduped)}


# ---------------------------------------------------------------------------
# R4 - THE CRIME. An object hidden inside the set that contains it.
# ---------------------------------------------------------------------------

def rung4():
    """One field is mutated AFTER insertion. Predict all five lines.

    Pay attention to the last two together - they are the point of this project.
    """

    class Txn:
        def __init__(self, txn_id, amount):
            self.txn_id = txn_id
            self.amount = amount

        def __eq__(self, other):
            return (self.txn_id, self.amount) == (other.txn_id, other.amount)

        def __hash__(self):
            return hash((self.txn_id, self.amount))

        def __repr__(self):
            return f"Txn({self.txn_id!r}, {self.amount})"

    t = Txn("T1", 500)
    seen = {t}

    before = t in seen
    t.amount = 999            # lesson 1.3: mutation through a live reference
    after = t in seen

    return {
        "t in seen (before mutation)": before,
        "t in seen (after mutation)": after,
        "len(seen)": len(seen),
        "list(seen)": [repr(x) for x in seen],
        "list(seen)[0] is t": list(seen)[0] is t,
    }


# ---------------------------------------------------------------------------
# R5 - how much data does this silently lose?
# ---------------------------------------------------------------------------

def rung5():
    """PREDICT TWO NUMBERS: rows in, rows out. They should be equal. Are they?"""

    class Txn:
        def __init__(self, txn_id, amount):
            self.txn_id = txn_id
            self.amount = amount

        def __eq__(self, other):
            return (self.txn_id, self.amount) == (other.txn_id, other.amount)

        def __hash__(self):
            return hash((self.txn_id, self.amount))

    rows = [Txn(f"T{i}", i) for i in range(10_000)]
    seen = set(rows)

    # a downstream stage "enriches" every row - a totally ordinary thing to do
    for r in rows:
        r.amount = r.amount * 100

    findable = sum(1 for r in rows if r in seen)
    return {
        "rows inserted": len(rows),
        "len(seen) still": len(seen),
        "rows findable by `in`": findable,
        "rows LOST (no error raised)": len(rows) - findable,
    }


# ---------------------------------------------------------------------------
# R6 - a legal __hash__ that destroys performance. (This is data skew.)
# ---------------------------------------------------------------------------

def rung6():
    """Both classes are CORRECT: equal objects hash equal. One is unusable.

    PREDICT: when n doubles, what happens to each timing?
    """

    class Good:
        __slots__ = ("k",)

        def __init__(self, k):
            self.k = k

        def __eq__(self, other):
            return self.k == other.k

        def __hash__(self):
            return hash(self.k)

    class Skewed:
        __slots__ = ("k",)

        def __init__(self, k):
            self.k = k

        def __eq__(self, other):
            return self.k == other.k

        def __hash__(self):
            return 42          # legal: equal objects still hash equal

    out = {}
    for n in (2_000, 4_000, 8_000):
        for name, cls in (("good", Good), ("skewed", Skewed)):
            items = [cls(i) for i in range(n)]
            start = time.perf_counter()
            set(items)
            out[f"n={n:<5} {name}"] = f"{(time.perf_counter() - start) * 1000:8.2f} ms"
    return out


RUNGS = {1: rung1, 2: rung2, 3: rung3, 4: rung4, 5: rung5, 6: rung6}


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) not in RUNGS:
        print(__doc__)
        return
    n = int(sys.argv[1])

    if not PREDICTIONS.get(n, "").strip():
        print(f"\n  BLOCKED. PREDICTIONS[{n}] is empty.\n")
        print(inspect.getsource(RUNGS[n]))
        return

    print("\n" + "=" * 70)
    print(inspect.getsource(RUNGS[n]))
    print("=" * 70)
    try:
        actual = RUNGS[n]()
    except Exception as exc:
        actual = f"{type(exc).__name__}: {exc}"
    print(f"\n  YOU PREDICTED : {PREDICTIONS[n]}\n")
    if isinstance(actual, dict):
        print("  ACTUAL        :")
        for k, v in actual.items():
            print(f"      {k:<32} {v}")
    else:
        print(f"  ACTUAL        : {actual!r}")
    print()


if __name__ == "__main__":
    main()
