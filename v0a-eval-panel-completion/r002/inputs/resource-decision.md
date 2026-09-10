# Controller resource decision — 2026-09-09

Controller, verbatim: "that envelope looks reasonable we will adopt it."

In reply to measured-report.md, which proposed a full-pool solve envelope on the
measured basis of the retained capacity and preflight runs on beb84be5.

## What this records

- Pool: H = 1,081, the whole compatible hero universe on 2c 7d 9h Js Qc, as
  selected by the retained capacity run a89932e7 (1,012,625 wire bytes, 3.4%
  headroom under the 1,048,576-byte cap).
- Envelope for the full-pool T1 solve: 600 seconds and 2048 MiB worker Job memory.
  Measured basis: preflight run 7ce5ab4f — production 15.8–71.4 s estimated over H
  (untraced), peak worker Job about 0.8 GiB; headroom at least 8x on time and about
  2.5x on memory.
- Source: beb84be566aa28029284bd35c526d33cd27af369.

This is the "measured resource decision" that design section 6, step 4 requires
before bridge-completion implementation begins. It is a recorded decision, not an
invocation: the full-pool solve, export and agreement runs each still need their
own bound plan and one-shot authorization (design step 7; prerequisite-run-plan.md).

Next under the recorded alternation: Codex drafts design steps 4-7 parented on
beb84be5; Claude cold-reviews.
