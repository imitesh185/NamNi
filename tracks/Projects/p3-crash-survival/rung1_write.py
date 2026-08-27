"""
Rung 1 - the stupidest possible worker.

Ten items. One per second. Each result appended to results.txt.
That is the entire program. There is nothing clever in it, on purpose.

Your job is to kill it halfway - twice, two different ways - and find out
whether the work it TOLD you it finished actually survived.

    python rung1_write.py

RUN A: let it reach item 5, then press Ctrl-C.
RUN B: let it reach item 5, then hard-kill it from a SECOND terminal
       using the PID this program prints:

           taskkill /F /PID <pid>

Delete results.txt between runs, or you will be reading run A's data:

           Remove-Item results.txt

Then look at what is actually on disk:

           Get-Content results.txt
"""

import os
import time


# ---------------------------------------------------------------------------
# Prediction gate. Fill both in before the program will run.
# Be specific: how many lines, which ones, or "empty". "Some of them" is not
# a prediction - it cannot be wrong, so it cannot teach you anything.
# ---------------------------------------------------------------------------

PREDICTIONS = {
    "A_ctrl_c": "1,2,3,4,5",
    "B_hard_kill": "Nothing, because OS will not flush the data.",
}


def gate():
    missing = [k for k, v in PREDICTIONS.items() if not v.strip()]
    if missing:
        print("\n  BLOCKED - commit your predictions first:\n")
        for k in missing:
            print(f"      PREDICTIONS[{k!r}] is empty")
        print("\n  The console will say 'processed item 5'.")
        print("  After each kill, what is in results.txt?\n")
        return False
    return True


def main():
    print(f"\n  pid {os.getpid()}  - kill me with: taskkill /F /PID {os.getpid()}\n")
    time.sleep(10)

    # beside this script, not beside wherever you happened to be standing
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.txt")

    out = open(path, "a")
    for i in range(10):
        out.write(f"item {i} done\n")
        print(f"  processed item {i}")
        time.sleep(1)
    out.close()

    print("\n  all 10 done\n")


if __name__ == "__main__":
    if gate():
        main()