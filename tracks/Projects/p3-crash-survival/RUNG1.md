# Rung 1 — what does "processed" actually mean?

**Box: 10 minutes.** Ideas only. No code, no syntax, no Python API names.
If you catch yourself writing a function name, you've left the rung.

**Do not open `rung1_write.py` yet.** It is the answer sheet.

---

## The situation

A program has a list of 10 items. For each one it does a little work, records the
result to a file on disk, and prints `processed item N` to your console.

At item 5 the program dies. Two different deaths, on two different runs:

- **Run A** — you press Ctrl-C.
- **Run B** — someone hard-kills the process. No warning, no cleanup, gone.

The console said `processed item 5` in both runs. It is now dead. You go and open
the file.

> **The question: was the console telling the truth?**

---

## 1. What actually happens between "the loop body ran" and "the bytes are on the disk"?

The program says it wrote item 5. List every distinct stage that data has to pass
through before it is genuinely, durably on the disk. Name the stages however you
want — you're not expected to know the official terms. You are expected to
suspect that it is more than one stage.

```
your answer:
Stages are - 
1. Open / Read Item.
2. Process the Item.
3. Record the Result on disk.
4. Print - completed.

What Happens -> My assumptions.
Open -> Process happens in Main-Memory {RAM} - Each Program gets its own Stack {where local variables are stored}, to write the result to disk, the result will be popped/flushed to disk. Not sure about the procedure, how ist being done.

```

## 2. Where could item 5 be sitting at the instant the process dies?

For each stage you listed above — if the process dies while the data is at that
stage, does the data survive? Who is holding it?

```
your answer:
The core assumption (might be wrong), if the program dies while executing, the stack which holds the variables is gone so everything might be lost.
Stage -> If dies
1. Open / Read Item. ->  No
2. Process the Item. -> No
3. Record the Result on disk. -> Yes, if the program dies once the data is on disk, the data can be accessed again (that depends if the writing to disk is completed or crashed mid-write (corrupt data))
4. Print - completed. -> Just the console, the console might not remember its previous state and will open a fresh clean slate to print again.


```

## 3. Should Run A and Run B produce the same file?

Ctrl-C versus hard kill. Same file contents, or different? Commit to one.
Then say *why* — what does one death allow the program to do that the other
doesn't?

```
your answer:
Assumption -  Different.
because killing a process {kill -<pid>} will kill the particular process; there might be multiple process involved {multi-threading} which will let other process continue (unless killing the root process) - whereas Ctrl-C will stop all the processes running in that terminal. 
Eg : kill -<pid> will kill the process running on port 5500, where as Ctrl-C will kill the active port (disengage)

```

## 4. If they differ — what is the general principle?

State it as a sentence about programs in general, not about this program.

```
your answer:
I believe I answered in Q3.


```

## 5. What would you have to change to make the console's claim trustworthy?

Idea only. Not how — what.

```
your answer:
not sure but for console claim to be trustworthy, the *result should only be printed once the acknoeledgment is received that data has been written to the disk for that particular process. Not pre or mid-write; not my job is done for processing writing will be done by other process; unless the write is completed and acknowledgment is given no further execution.

```

---

## Layer check

For the failure you're describing, which layer owns it? Circle one and defend it.

```
Python language  /  Python runtime  /  operating system  /  filesystem  /  disk hardware  /  application logic
```

```
your answer:

Not sure, but application logic.
Because logic will be the one who commits the push and verify if the printing to console is trustworhty or not.

```
