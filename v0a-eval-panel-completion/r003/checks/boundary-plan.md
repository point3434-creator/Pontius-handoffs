# Authorized r003 boundary inventory before edits

Controller: "I authorize it", responding to the bounded r003 repair plan.
Base 430ad75de79cec13d66ff3dc4981dd3770a371b7. Tier C FIX. Python 3.14.6 only.
Scope: eval_agreement.py and test_eval_protocol.py. No sealed producer changes.

Host read_stream owns physical LF frames (including the LF in the 16384-byte
limit), rejects unfinished final bytes, and marks stdout beyond 2097152 bytes
truncated. Its decoder rejects CR, leading BOM, depth >8 outside quoted strings,
integer tokens beyond 640 signless digits, duplicate keys, constants and invalid
UTF-8/JSON; recursion errors become refusals. WireConsumer then owns exact
schema, identity, successful status, timing and replay comparisons.

Classifier gap: universal str.splitlines normalizes invalid physical frames;
unbounded raw parsing misses frame/capture/depth/integer limits. Existing exact
schema checks cannot recover discarded byte distinctions. Current constant and
float hooks already reject nonfinite numbers; keep that stricter finite contract.

Mechanism: one decode_frame boundary with the frozen host's size/byte/depth/int
predicates and duplicate/nonfinite/UTF-8 parsing; frames_for splits only physical
LF and enforces retained stdout bounds before calling it. No normalization.
Typed record admission, settled chips and later agreement remain unchanged.

Discovery: enumerate read_stream, decode_json and WireConsumer separately;
compare permitted raw inputs before reading typed values. Test the unchanged
host decoder as an independent oracle for shared JSON boundaries. Preserve
the existing stricter rejection of exponent overflow and semantic schema rules.

Verification: actual v1 CHECK and v2 premium-divergence capture mutations;
alternative separators, CR/BOM, size exactly at and above the limit, invalid
encoding, duplicate keys, numeric limit, depth and parser refusal. Positive
parser controls cover quoted braces/escaped quotes and Unicode inside strings.
The 2 MiB bound is a resource guard; invalid extra-frame streams must exclude
regardless of other schema errors, with no fabricated claim of a natural large
completed four-chip hand. RED on frozen base before production edit, then final
six-suite focused GREEN, exact freeze and two cold passes before broad/adoption.
