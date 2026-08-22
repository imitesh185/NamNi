"""
Drill 1.3P - prediction ledger
==============================

Protocol:
  1. Fill in ALL 16 entries in PREDICTIONS below. Exact repr of the return value.
  2. No REPL, no searching, no asking anyone while predicting.
  3. Only then: python d13_predict.py
  4. Ignore hits. For every miss, write the rule you broke in your own words.

A blank prediction counts as a miss. Target: 14/16.
"""

import copy


def p01():
    rows = [[]] * 3
    rows[0].append("x")
    return rows


def p02():
    rows = [[]] * 3
    rows[0] = 9
    return rows


def p03():
    rows = [[] for _ in range(3)]
    rows[0].append("x")
    return rows


def p04():
    m = [[1, 2], [3, 4]]
    s = m[:]
    s.append(9)
    return m


def p05():
    m = [[1, 2], [3, 4]]
    s = m[:]
    s[0].append(9)
    return m


def p06():
    m = [[1, 2]]
    d = copy.deepcopy(m)
    d[0].append(9)
    return m


def p07():
    a = [1, 2]
    b = a
    a += [3]
    return b


def p08():
    a = [1, 2]
    b = a
    a = a + [3]
    return b


def p09():
    t = ([1, 2], 3)
    try:
        t[0] += [9]
    except TypeError:
        pass
    return t


def p10():
    def f(item, bucket=[]):
        bucket.append(item)
        return bucket

    f(1)
    return f(2)


def p11():
    x = [3, 1, 2]
    y = x
    x.sort()
    return y


def p12():
    x = [3, 1, 2]
    y = x
    x = sorted(x)
    return y


def p13():
    inner = []
    d = {"a": inner, "b": inner}
    d["a"].append(1)
    return d


def p14():
    def f(seq):
        seq.append(1)
        seq = [9]
        seq.append(2)

    xs = []
    f(xs)
    return xs


def p15():
    a = [1, 2, 3]
    b = a
    a[:] = [9]
    return b


def p16():
    inner = [1]
    m = [inner, inner]
    d = copy.deepcopy(m)
    d[0].append(2)
    return d


PREDICTIONS = {
    "p01": "",
    "p02": "",
    "p03": "",
    "p04": "",
    "p05": "",
    "p06": "",
    "p07": "",
    "p08": "",
    "p09": "",
    "p10": "",
    "p11": "",
    "p12": "",
    "p13": "",
    "p14": "",
    "p15": "",
    "p16": "",
}


def _norm(text):
    return "".join(text.split())


def check():
    misses = []
    for name in sorted(PREDICTIONS):
        actual = repr(globals()[name]())
        guess = PREDICTIONS[name]
        if guess and _norm(guess) == _norm(actual):
            print(f"{name}  HIT")
        else:
            print(f"{name}  MISS")
            misses.append((name, guess or "(blank)", actual))

    score = len(PREDICTIONS) - len(misses)
    print(f"\nscore: {score}/{len(PREDICTIONS)}")

    if misses:
        print("\nreview these — write the rule, do not just read the value:")
        for name, guess, actual in misses:
            print(f"  {name}  you: {guess}")
            print(f"       actual: {actual}")


if __name__ == "__main__":
    check()
