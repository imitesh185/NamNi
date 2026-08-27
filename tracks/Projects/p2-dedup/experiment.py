"""
P2 - the measurement harness. You do not need to edit this file.

Three experiments, three claims:

  A. Value semantics vs identity semantics - does dedup remove anything at all?
  B. The ghost - mutating a hashed field after insertion silently loses rows.
  C. Skew - a provably CORRECT __hash__ that turns O(n) into O(n^2).

    python experiment.py
"""

import time

from dedup import Txn, dedup


# ---------------------------------------------------------------------------
# readiness check - fails loudly and specifically, never mysteriously
# ---------------------------------------------------------------------------

def check_ready():
    problems = []
    a, b = Txn("T1", 500), Txn("T1", 500)

    def probe(label, fn):
        try:
            fn()
        except NotImplementedError as exc:
            problems.append(str(exc))
        except Exception as exc:
            problems.append(f"{label} raised {type(exc).__name__}: {exc}")

    probe("Txn.__eq__", lambda: a == b)
    probe("Txn.__hash__", lambda: hash(a))
    probe("Txn.__repr__", lambda: repr(a))
    probe("dedup", lambda: dedup([a, b]))

    if problems:
        print("\n  NOT READY - fill these in dedup.py, then run again:\n")
        for p in problems:
            print(f"      - {p}")
        print()
        return False

    checks = [
        ("__eq__ says equal rows are equal", a == b),
        ("__eq__ says different rows differ", not (a == Txn("T1", 501))),
        ("__hash__ agrees with __eq__", hash(a) == hash(b)),
        ("__repr__ returns a str", isinstance(repr(a), str)),
        ("dedup collapses duplicates", len(dedup([a, b])) == 1),
        ("dedup preserves order", dedup([Txn("B", 2), Txn("A", 1), Txn("B", 2)])
         == [Txn("B", 2), Txn("A", 1)]),
    ]
    failed = [name for name, ok in checks if not ok]
    if failed:
        print("\n  IMPLEMENTED BUT WRONG:\n")
        for name in failed:
            print(f"      FAIL  {name}")
        print()
        return False

    print("\n  All contracts satisfied. Running experiments.\n")
    return True


# ---------------------------------------------------------------------------
# A - value semantics vs identity semantics
# ---------------------------------------------------------------------------

class RawTxn:
    """Deliberately has no __eq__ and no __hash__ - inherits object's."""

    def __init__(self, txn_id, amount):
        self.txn_id = txn_id
        self.amount = amount


def experiment_a(n=1_000_000, distinct=1_000):
    print("=" * 72)
    print("  A. DOES DEDUP REMOVE ANYTHING?")
    print("=" * 72)
    print(f"  {n:,} rows drawn from only {distinct:,} distinct values.\n")

    raw = [RawTxn(f"T{i % distinct}", i % distinct) for i in range(n)]
    t0 = time.perf_counter()
    raw_out = len(set(raw))
    raw_ms = (time.perf_counter() - t0) * 1000

    rows = [Txn(f"T{i % distinct}", i % distinct) for i in range(n)]
    t0 = time.perf_counter()
    val_out = len(dedup(rows))
    val_ms = (time.perf_counter() - t0) * 1000

    print(f"  {'identity semantics (no __eq__/__hash__)':<44}"
          f"{n:>9,} -> {raw_out:>9,}   {raw_ms:8.1f} ms")
    print(f"  {'value semantics (yours)':<44}"
          f"{n:>9,} -> {val_out:>9,}   {val_ms:8.1f} ms")
    print(f"\n  rows removed by the default object model : {n - raw_out:,}")
    print(f"  rows removed by your value object        : {n - val_out:,}")
    print("\n  Both 'succeeded'. Only one deduplicated anything.\n")


# ---------------------------------------------------------------------------
# B - the ghost
# ---------------------------------------------------------------------------

def experiment_b(n=100_000):
    print("=" * 72)
    print("  B. THE GHOST - mutation after insertion")
    print("=" * 72)
    print(f"  {n:,} rows inserted into a set, then a fraction of them are")
    print("  'enriched' by a downstream stage - an ordinary, innocent write.\n")
    print(f"  {'mutated':>9}  {'len(set)':>9}  {'findable':>9}  {'LOST':>9}  {'error?':>8}")
    print("  " + "-" * 54)

    for pct in (0, 1, 10, 50, 100):
        rows = [Txn(f"T{i}", i) for i in range(n)]
        seen = set(rows)
        cutoff = n * pct // 100
        for r in rows[:cutoff]:
            r.amount += 1
        findable = sum(1 for r in rows if r in seen)
        print(f"  {pct:>8}%  {len(seen):>9,}  {findable:>9,}  "
              f"{n - findable:>9,}  {'none':>8}")

    print("\n  The set never shrank. The rows are still inside it.")
    print("  They simply cannot be found - including by themselves.\n")

    t = Txn("T1", 500)
    box = {t}
    t.amount = 999
    print(f"      t                     = {t!r}")
    print(f"      the set               = {box!r}")
    print(f"      len(set)              = {len(box)}")
    print(f"      list(set)[0] is t     = {list(box)[0] is t}")
    print(f"      t in set              = {t in box}   <-- it is in there")
    print()


# ---------------------------------------------------------------------------
# C - skew
# ---------------------------------------------------------------------------

class SkewedTxn(Txn):
    """Inherits your __eq__ unchanged. Only __hash__ differs.

    This is CORRECT: equal objects still hash equal. The invariant holds.
    """

    def __hash__(self):
        return 42


def experiment_c(sizes=(1_000, 2_000, 4_000, 8_000)):
    print("=" * 72)
    print("  C. SKEW - a correct hash that destroys performance")
    print("=" * 72)
    print("  SkewedTxn.__hash__ returns a constant. Equal objects still hash")
    print("  equal, so the invariant is satisfied and dedup stays CORRECT.\n")
    print(f"  {'n':>8}  {'good':>12}  {'skewed':>12}  {'ratio':>9}  {'growth':>8}")
    print("  " + "-" * 56)

    prev = None
    for n in sizes:
        good = [Txn(f"T{i}", i) for i in range(n)]
        t0 = time.perf_counter()
        dedup(good)
        good_ms = (time.perf_counter() - t0) * 1000

        skewed = [SkewedTxn(f"T{i}", i) for i in range(n)]
        t0 = time.perf_counter()
        dedup(skewed)
        skew_ms = (time.perf_counter() - t0) * 1000

        growth = f"{skew_ms / prev:.1f}x" if prev else "-"
        prev = skew_ms
        print(f"  {n:>8,}  {good_ms:>9.2f} ms  {skew_ms:>9.2f} ms  "
              f"{skew_ms / good_ms:>8.0f}x  {growth:>8}")

    print("\n  Watch the 'growth' column as n doubles. If it reads ~2x the cost")
    print("  is linear; ~4x means every new row is compared against every")
    print("  existing one. One bucket, one worker, all the work.\n")


if __name__ == "__main__":
    if check_ready():
        experiment_a()
        experiment_b()
        experiment_c()
