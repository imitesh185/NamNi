"""
Rung 2b - what does durability cost?

The crash test showed flush and sync producing identical files. This one
shows what you paid for the sync.

Each mode gets a fixed time budget and we count how many records it managed
to write. No sleeps, no kills - just throughput.

    python rung2_bench.py
"""

import os
import time


# ---------------------------------------------------------------------------
# Predict before running. Numbers, not adjectives.
# ---------------------------------------------------------------------------

PREDICTIONS = {
    "naive_vs_flush": "",   # how many times slower is flush than naive?
    "flush_vs_sync": "",    # how many times slower is sync than flush?
}

SECONDS = 2.0
HERE = os.path.dirname(os.path.abspath(__file__))


def bench(mode):
    path = os.path.join(HERE, f"results_bench_{mode}.txt")
    n = 0
    with open(path, "w") as out:
        deadline = time.perf_counter() + SECONDS
        while time.perf_counter() < deadline:
            out.write(f"item {n} done\n")
            if mode in ("flush", "sync"):
                out.flush()
            if mode == "sync":
                os.fsync(out.fileno())
            n += 1
    return n


def gate():
    missing = [k for k, v in PREDICTIONS.items() if not v.strip()]
    if missing:
        print("\n  BLOCKED - commit your predictions first:\n")
        for k in missing:
            print(f"      PREDICTIONS[{k!r}] is empty")
        print()
        return False
    return True


def main():
    print(f"\n  {SECONDS:.0f}s per mode. Writing as fast as each mode allows.\n")

    results = {}
    for mode in ("naive", "flush", "sync"):
        print(f"  running {mode} ...", end="", flush=True)
        results[mode] = bench(mode)
        print(f" {results[mode]:>12,} records")

    base = results["naive"]
    print(f"\n  {'mode':<8}{'records/sec':>15}{'vs naive':>14}")
    print("  " + "-" * 37)
    for mode in ("naive", "flush", "sync"):
        rate = results[mode] / SECONDS
        print(f"  {mode:<8}{rate:>15,.0f}{base / results[mode]:>13.1f}x")

    print(f"\n  sync is {results['flush'] / results['sync']:.1f}x slower than flush\n")


if __name__ == "__main__":
    if gate():
        main()
