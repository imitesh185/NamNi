# METHOD — the project as a discovery environment

This is not a plan. There are no weeks, phases, or day numbers in this document,
and none may be added. It describes **how a session runs**, not what order topics
arrive in.

Adopted 2026-08-27, replacing lesson-first sequencing.

---

## The objective

> Develop a deep mental model of Python, and become capable of reasoning about
> and building software in Python.

Not a syllabus. Not isolated exercises that demonstrate one concept at a time.
Experimenting with `id()`, implementing `__eq__` on a toy class, writing a
decorator exercise — these teach a concept without ever building the intuition
for **why software needs that concept in the first place.**

---

## The project is not the goal

The environment is a laboratory. It may fail, change direction, or be abandoned
outright. That is fine and costs nothing.

The success criterion is never "did it work". It is:

> **Did encountering the problem force me to understand something important
> about Python?**

### What counts as an interesting environment

Banned: todo apps, CRUD APIs, library management systems, blogs, chat clones,
and concept demonstrations wearing a project costume.

Required: a question whose answer I actually want to know, that reaches outside
Python, and that makes Python the instrument rather than the subject.

- Can a program survive being killed halfway through an operation?
- Can multiple independently running programs coordinate without processing
  the same thing twice?
- Can a system detect that something abnormal is happening in a continuous
  stream of events?
- Can two computers communicate using sound?
- Can Python control a physical TV over Wi-Fi?

---

## The core loop

```
Interesting goal
      ↓
Simplest possible implementation
      ↓
It works, or partially works
      ↓
A real limitation / failure / new requirement appears
      ↓
Investigate WHY the limitation exists      ← time-boxed, see Amendment 1
      ↓
Identify the concept the problem demands
      ↓
Learn that concept in the context of the problem
      ↓
Improve the implementation
      ↓
New limitation appears
      ↓
Repeat
```

**The failure must arrive before the concept.** A concept is never introduced
because it is next in a syllabus.

---

## Amendment 1 — the stopping rule (non-negotiable)

The loop above says "investigate why". Unbounded, that instruction produces a
four-hour circle around one concept with nothing to show. It has already
happened. The bound is the fix.

> **25 minutes per investigation.** When the box expires, exactly one of three
> things happens. There is no fourth option.

| Outcome | Action |
|---|---|
| **Resolved** | One line in the log: what broke, why, what fixed it. Move on. |
| **Parked** | The question goes on the **concept-debt list** below. Not chased. Not dropped. Back to code. |
| **Wrong rung** | The rung was too large. Shrink it and restart — never re-read the same material. |

Parking is the important one. Without it the only two moves are *chase it to the
bottom* or *abandon it and feel bad*. Debt is paid later, when a rung forces it.
If the method is right, a rung eventually will.

### Concept-debt list

Questions raised by a rung, deliberately not answered yet.

| # | Question | Raised by | Paid off |
|---|---|---|---|
| 1 | Local variables "live on the stack" — but where do their *values* live? Stack vs heap, and which one a Python name actually points into. | P3 Rung 1 Q1 | |
| 2 | Can a write be torn in half — a partially written record, not just a missing one? Is that possible on a real filesystem, or is it prevented? | P3 Rung 1 Q2 | |

---

## Amendment 2 — one artifact per rung

Day-at-a-time, plus emergent structure, plus no written record, equals amnesia.
Every rung produces the artifact defined in
[tracks/Projects/README.md](tracks/Projects/README.md):

- **A claim** — precise enough that it could turn out false.
- **A measurement** — the number that would falsify it.
- **A surprise** — a written prediction, committed *before* running, that
  reality contradicted.

Plus the annotation table, whose fourth column ("what breaks without it") is
**executed by ablation, never asserted from memory.** Failures classify as
`LOUD` (raises), `QUIET` (wrong answer, no error — the ones that reach
production), or `NONE` (then the code was decoration; delete it).

Emergence supplies the *why*. The research bar supplies the *proof*.

---

## Amendment 3 — constraints are injected, and I say so

The original draft said both "do not artificially create problems" and "you may
deliberately introduce realistic constraints". Those fight. Resolved in favour
of honesty:

> **The guide injects constraints. I am not told which one is coming.**

The constraint must be a genuine property of the domain — the device really
does take seconds to answer, the stream really is unbounded, the process really
can be killed mid-write. Never synthetic, never "now let's do concurrency
because it's Tuesday".

The pedagogical value was never that the problem arrived by accident. It is that
**the problem is met before the concept is.** That is fully preserved. What is
dropped is the theatre of pretending it wasn't aimed.

---

## The guide's role

Create and help investigate **productive friction**. Do not solve immediately.
When something unexpected happens, work these in order:

1. What did I expect?
2. What actually happened?
3. Which assumption was wrong?
4. **At what layer is this happening?** — Python language / Python runtime /
   object model / OS / filesystem / network / protocol / application logic.
5. What new requirement has emerged?
6. What designs could satisfy it?

Only after the problem is understood do we choose an implementation.

### Teaching a concept once it has become necessary

1. Start from my current code and my current problem.
2. State precisely why the present design is insufficient.
3. Ask me to predict what would solve it — **committed in writing, before code.**
4. Introduce the smallest relevant piece of Python.
5. Connect that behaviour to Python's underlying model.
6. I modify the code.
7. Observe the new behaviour.
8. Move.

Go deep enough for a correct mental model. Do not turn every interruption into a
lecture. The question is always *why is Python behaving this way*, never *what
syntax do I type*.

---

## Do not over-architect

Begin with the stupidest thing that runs. `def main(): ...` is acceptable and
usually correct. Never begin with `src/ domain/ application/ infrastructure/
repositories/ factories/ services/ adapters/`.

The point is to **experience the moment simple code stops being sufficient**, and
to feel the evolutionary pressure that produces architecture. Structure added
before that pressure exists is cargo cult.

---

## Concepts I expect this to eventually force

Not a checklist. Not an order. A list of debts the environment is expected to
call in. Each entry names the *pressure* that should produce it, not the lesson
that teaches it.

| Pressure that must appear first | Concepts it should force |
|---|---|
| Badly structured state; unclear ownership | objects, identity, references, mutability, state vs behaviour, composition vs inheritance, protocols, special methods |
| Things staying alive longer than expected; resources not released; memory growth | reference counting, cyclic GC, `weakref`, object lifetime, finalization, context managers, memory vs resource management |
| `get_all_data()` becomes a bad design — data is continuous, too large, or has no known end | iterables, iterators, `__iter__`/`__next__`, lazy evaluation, generators, why `yield` changes the nature of computation |
| The program is blocked while something else needs to happen | blocking vs waiting, threads, processes, async, event loop, coroutines, tasks, races, locks — driven by *"what is my program doing while it waits?"* |
| The same wrapper logic repeated around many functions | first-class functions, closures, callable objects, decorators |
| Real failures: unavailable peer, malformed response, connection lost mid-operation | exceptions, custom hierarchies, propagation, where to handle, cleanup, context managers |

---

## Current environment

> **Can a program survive being killed halfway through an operation — and can
> two independent programs coordinate without processing the same item twice?**

Chosen over the LG webOS TV because the environment is disposable by design, and
this one exercises the same Python concepts while sitting directly on the data
engineering path: crash consistency, idempotency, checkpointing, and exactly-once
processing are what Spark task retries and Kafka consumer groups are made of.
[tracks/Projects/p2-dedup](tracks/Projects/p2-dedup) is the miniature seed of the
second half of the question.

Do not optimize for finishing it. Optimize for what it forces.

---

## The session loop

The core loop above describes the arc of a project. This describes a single
sitting. Six steps, in order, no skipping.

| # | Step | Who | Box |
|---|---|---|---|
| S1 | **Problem** — the situation and the question, stated without naming any concept. | guide | ~5 min |
| S2 | **Rung** — the *core idea only*. What is actually happening, what could go wrong, what would be needed. **No code. No syntax.** Written down. | me | 10 min |
| S3 | **Verdict + minimum** — where the idea was right, where it was wrong, then the smallest piece of Python the problem now demands. | guide | — |
| S4 | **Build** — write the wrong version. Return with questions. | me | 30 min |
| S5 | **Scaffold** — on request: a template with named holes, and a roadmap. Never a filled answer. | guide | — |
| S6 | **Grill** — edge cases, failure modes, cost, and "what breaks if this line is deleted" — *proven by deleting it and running it.* | guide | — |

A new limitation surfaces during S6. That limitation is the next S1.

**Amendment 1's 25-minute box applies inside any step.** S2 and S4 have their own
boxes and those are hard stops, not targets.

### When an HTML lesson gets written

A lesson under `tracks/python/` is authored at **S3 and only S3**, when both hold:

1. S2 or S4 produced a real demand for the concept — the code is now bad *in a
   way I can point at* without it.
2. Every prerequisite is already covered. Audit as a have/don't-have table
   first. **More than one missing prerequisite means the rung is wrong, not
   hard** — shrink it instead.

A lesson written before the demand exists is a syllabus, and this document
exists to prevent that.

### The spoiler rule

Code written by the guide is not read until the rung it answers has been
written. Reading the implementation first destroys the experiment.

---

## The outcome that matters

Not "I know OOP" or "I know asyncio". The ability to meet an unfamiliar problem
and ask:

> What is the actual problem? What state exists? What objects exist? What owns
> what? What happens over time? What can fail? What is blocking? Is this finite
> data or a stream? What happens if two things run at once? What does Python
> actually do here? What is the simplest thing I can try?

Reasoning from a problem toward a design. **The project is only the laboratory.
Python is what is being learned.**
