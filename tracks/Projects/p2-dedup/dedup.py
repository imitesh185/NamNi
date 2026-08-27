"""
P2 - the dedup engine.

THIS IS THE MODULE YOU WRITE. Four things are missing, each marked TODO with
its contract. Everything else in this project imports from here.

Run `python experiment.py` at any time - it will tell you exactly which TODO is
still unfilled and stop cleanly instead of exploding.
"""


class Txn:
    """One transaction row.

    A VALUE object: two rows carrying the same field values must behave as the
    same row - in `==`, in a set, and as a dict key.
    """

    def __init__(self, txn_id, amount):
        self.txn_id = txn_id
        self.amount = amount

    # -- TODO 1 --------------------------------------------------------------
    # Contract: True when `other` carries the same txn_id AND the same amount.
    # Lesson 2.1 sec 06. One line is enough. Compare the two field tuples.
    def __eq__(self, other):
        if isinstance(other, Txn):
            return (self.txn_id, self.amount) == (other.txn_id, other.amount)
        return False

    # -- TODO 2 --------------------------------------------------------------
    # Contract: objects that are == MUST return the same hash. Build it from
    # the SAME fields __eq__ uses - any other choice breaks the invariant.
    def __hash__(self):
        return hash((self.txn_id, self.amount))

    # -- TODO 3 --------------------------------------------------------------
    # Contract: unambiguous, ideally valid Python that recreates the object.
    # Lesson 2.1 sec 03.
    def __repr__(self):
        return f"Txn({self.txn_id!r}, {self.amount!r})"


# -- TODO 4 ------------------------------------------------------------------
def dedup(rows):
    """Return unique rows: FIRST occurrence kept, original order preserved.

    `set(rows)` deduplicates but destroys order, so it is not enough on its own.
    You need a `seen` set plus an output list.
    """
    seen = set()
    outcomes = []
    for row in rows:
        if row not in seen:
            seen.add(row)
            outcomes.append(row)
    return outcomes
