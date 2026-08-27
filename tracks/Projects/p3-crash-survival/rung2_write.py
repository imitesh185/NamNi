"""
Rung 2 - make the print unable to lie.

Same naive worker as rung 1, except the write path is now yours to control.
Three modes, run as:

    python rung2_write.py naive
    python rung2_write.py flush
    python rung2_write.py sync

Each mode writes to its own file (results_naive.txt, etc) so you cannot
contaminate one run with another. That trap already cost you once.

For each mode: let it reach item 5, then HARD kill it from a second terminal.

    taskkill /F /PID <pid>

Then compare:

    Get-Item results_*.txt | Select-Object Name, Length
"""

import os
import sys
import time


# ---------------------------------------------------------------------------
# Predict all three before the program will run. Say how many items survive.
# "It depends" is not a prediction.
# ---------------------------------------------------------------------------

PREDICTIONS = {
    "naive_hard_kill": "Empty file",
    "flush_hard_kill": "Data Present",
    "sync_vs_flush": "Still unable to say difference",   # under a HARD KILL, do these two differ? why / why not?
}


def record(out, i):
    """Write item i, and do not return until the data has crossed as far as MODE demands."""
    out.write(f"item {i} done\n")

    if MODE in ("flush", "sync"):
        out.flush()

    if MODE == "sync":
        os.fsync(out.fileno()) #got it from python documentation

# ---------------------------------------------------------------------------

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
    print(f"\n  mode={MODE}   pid {os.getpid()}   taskkill /F /PID {os.getpid()}\n")
    time.sleep(10)

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        f"results_{MODE}.txt")

    out = open(path, "a")
    for i in range(10):
        record(out, i)
        print(f"  processed item {i}")     # is this true yet?
        time.sleep(1)
    out.close()

    print("\n  all 10 done\n")


if __name__ == "__main__":
    MODE = sys.argv[1] if len(sys.argv) > 1 else ""
    if MODE not in ("naive", "flush", "sync"):
        sys.exit("\n  usage: python rung2_write.py [naive|flush|sync]\n")
    if gate():
        main()
