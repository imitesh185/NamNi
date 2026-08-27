# P1 — design ledger

> **STATUS: deferred, on purpose (2026-08-26).** This was originally the gate
> before `expr.py`. That was the wrong order — these questions ask you to recall
> pain you haven't felt yet. Do `step1_ladder.py` first, then build `expr.py`,
> then come back and answer these. By then most will be obvious, and the ones
> that aren't are the real questions.

Committed answers only. "Not sure" is not an answer; a wrong answer you actually
believe is worth ten times a hedge, because only a wrong answer can be corrected.

---

## Part A — six design questions

### Q1. What does `col("amt") > 100` return?

Name the type. Then write, by hand, what you want `repr()` of it to print.

> **Your answer:**
>
> Type returned:
>
> Desired repr output:

---

### Q2. Where does `and` break?

You will overload `&` (`__and__`) and `|` (`__or__`). Now consider:

```python
col("a") > 1 and col("b") < 2
```

What does Python actually do here? Answer in terms of *which method the `and`
keyword calls* — and note carefully that `and` is not `&`. What is the returned
value, and why is it not the tree you wanted?

> **Your answer:**
>
> What `and` calls:
>
> What comes back:
>
> Why this is dangerous rather than merely wrong:

---

### Q3. `__eq__` is now a tree builder. What happened to `__hash__`?

Lesson 2.1 §06 established a rule. Apply it here.

State: (a) what `Expr.__hash__` is after you define `__eq__`, (b) one operation in
the standard library that now fails because of it, and (c) whether you should
restore it — with a reason, not a preference.

> **Your answer:**
>
> (a)
>
> (b)
>
> (c)

---

### Q4. What does `bool(expr)` do — return, or raise?

Both are defensible. Pick one and defend it. Your defence must name a concrete
piece of code that behaves badly under the option you rejected.

> **Your answer:**
>
> Choice:
>
> Concrete code that misbehaves under the rejected option:

---

### Q5. Where is the boundary between plan and execution?

`Frame` holds a plan. Something eventually runs it. Which object owns `__iter__`,
and what exactly happens on the *second* iteration of the same `Frame` — does it
re-run the query, replay a cache, or raise?

> **Your answer:**
>
> Owner of `__iter__`:
>
> Behaviour on second iteration, and the reason:

---

### Q6. What does `len(df)` mean before execution?

`__len__` must return an integer. But the row count is unknown until the query
runs. So: does `len(df)` execute the plan, raise, or return something else?

Note what this forces — and compare it to Q4. There is a pattern here about
protocols that demand a concrete answer from a lazy object.

> **Your answer:**
>
> Behaviour:
>
> The pattern shared with Q4:

---

## Part B — three numeric predictions

Commit numbers. Ranges are allowed; "it depends" is not.

| # | Quantity | Your prediction | Actual | Verdict |
|---|---|---|---|---|
| P1 | **Rows materialized ratio** — Python backend ÷ SQL backend, 1M rows, 0.1% selectivity | | | |
| P2 | **Wall-time ratio** for the same run | | | |
| P3 | **Peak memory ratio** (`tracemalloc`) for the same run | | | |

Then, in one sentence each:

- **Why P2 will differ from P1** (they are not the same number — say what absorbs
  the difference):

- **The condition under which the SQL backend is *slower*** (there is one; name it):

---

## Part C — Claim A prediction

For each operation below, predict the verdict **before** `ablate.py` runs:

- `LOUD` — raises immediately
- `QUIET` — returns a wrong answer, no error
- `NONE` — behaves correctly

| Operation on an `Expr` | Predicted | Actual |
|---|---|---|
| `if expr:` | | |
| `expr in [other_expr]` | | |
| `[e1, e2].index(e1)` | | |
| `assert expr` | | |
| `{expr: 1}` | | |
| `set([e1, e2])` | | |
| `sorted([e1, e2])` | | |
| `max([e1, e2])` | | |
| `e1 == e2` inside `unittest.assertEqual` | | |
| `expr is other` | | |

**Predicted count of `QUIET` rows:** ___

That last number is the one to care about. Loud failures are free — the program
stops. Quiet failures are the ones that ship.

---

## Part D — after the run

Do not write this section until every "Actual" column is filled.

- Which prediction was most wrong, and what was broken in the model that produced it?
- Which result was genuinely surprising?
- What would you now check first if you saw this bug class in real production code?
