# How a rubric is built

The rules a rubric has to follow, whatever audience it judges. `customer.md`
is the first one written against this; `technical.md` and `product.md` inherit
it rather than rediscovering it.

It exists because of what went wrong without it. Four defects cost real money
to find, and every one of them was visible in the text: two rules of one axis
answering the same sentence differently, an axis deciding by a list of words,
an axis quietly taking over a question that belonged to its neighbour, and a
rule contradicting the format document. None of those are judgement calls -
they are breaches of the four rules below.

---

## 1. An axis owns one question, and says which one it does not own

Every axis states two things before its procedure:

- **Judges:** the one question it answers.
- **Does not judge:** the questions a reader might expect it to answer and
  which belong to a named neighbour.

The second line is the one that was missing. Without it a rule added to one
axis can take over a neighbour's question, and nothing in the document
disagrees. C4 grew a rule about how a setting is written, which is C5's
question, and the two then failed the same sentence in opposite directions.

The test for a new rule: does it decide the question in the **Judges** line?
If it decides something else, it belongs to the axis that owns that, or
nowhere.

Two axes may both fail one entry. That is not an overlap - one defect can
answer two different questions badly. An overlap is when the *same* question
is asked twice, and then one of the two has to give it up.

## 2. A rule is a procedure, not a list of cases

A rule tells the reader what to do with the text in front of them. It does not
enumerate the cases that fail, because that enumeration is never finished:
after "no longer" and "instead of" come "rather than" and "without", and every
missing word is a wrong verdict.

- **Not a rule:** "these phrases fail", "these kinds of expression are not
  allowed", "refactors, test changes and CI changes do not belong here".
- **A rule:** "strike slot 1 and read what is left - does it still tell the
  reader something they did not already have?"

Where a list already exists, it is either an illustration of the procedure, and
then it is written as one, or it is the procedure, and then it has to be
replaced by one.

The same holds for examples: they show the procedure being applied. An example
that can only be recognised by matching its words is not doing any work.

An example taken from a real entry stands for that entry whole. Read the entry
to its end before it is used: if the procedure decides it the other way once
the last sentence is in, the example teaches the wrong verdict, and it will be
recognised by its subject long before anyone reaches the procedure. C4's n/a
example names a summary printed at the end of every run, and the entry it came
from closes by handing the reader a decision, so the axis prints n/a beside a
case its own procedure fails. It is still there: repairing it edits an axis and
costs that column a re-pass, so it is recorded under its version in
`../docs/criterion-versions.md` and waits for a cycle where the rubric is open.

## 3. Every axis states what makes it fail, not only what makes it pass

A procedure that only says when something passes cannot fail anything, and the
axis silently becomes a formality. Both directions are written down, and both
are reachable: an axis nothing can fail, and an axis that fails nearly
everything, are the same defect - they separate nothing.

If a run shows an axis failing almost every entry, that is a finding about the
axis before it is a finding about the runs.

## 4. Form belongs to the format document, judgement to the rubric

`docs/output-format.md` defines what a rendering looks like: headings, group
names, entry shape, what may appear at all. The rubric judges against that and
never restates it. A group name in both documents is a contradiction waiting
for one of them to be edited.

Consequence for the judge: an axis that refers to the format needs that part of
the format in its prompt, or the model is asked about a rule it cannot read.

---

## Writing or changing an axis

1. Write the **Judges** and **Does not judge** lines first. If the second is
   hard to write, the axis is not carved out yet.
2. Write the procedure. One question per step, applied to the text.
3. State the fail condition explicitly.
4. Read the whole section back, top to bottom, and check that every sentence
   asks the same question. A rule added at the bottom does not override the
   five sentences above it - that is how C3 came to have two readings, one in
   its title and one in its last step.
5. Put every example of the section back through the changed procedure. An
   example that survives a rewrite untouched is where the old reading goes on
   living: C4's first rule was rewritten and the justification under its n/a
   example reworded in the same commit, while the case itself was never
   re-decided, and it goes on deciding by the rule the axis no longer has.
6. Check the neighbours named in **Does not judge**: does any of them now say
   something about this axis' question?
7. Then, and only then, the columns judged against the old text are stale. Re-
   read them, record what moved, and measure.

## What this does not decide

The content of any axis. What a customer entry has to contain is a product
question, argued from what a reader needs, not from this file. This file only
says what shape the answer has to take, and where it is allowed to live.
