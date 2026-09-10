# Deferred r003 category and evidence

Category: raw input is normalized or admitted under weaker bounds before the
received-record validator runs. A later valid decoded object cannot establish
that its original frame was valid. Parent I-01 is the framing residual.

Discovery followed read_stream -> decode_json -> WireConsumer -> frames_for ->
admitted_decision -> replay -> classify -> summarize/phase acceptance. The
pre-edit boundary-plan records each ownership boundary and the test strategy.

1. Capture -> physical frames: 0 < decoded stdout <=2097152 bytes, final LF,
   byte split on LF only. Falsifier: an alternative separator is normalized into
   a hit, or an unfinished/oversized capture reaches schema admission.
2. Physical frame -> JSON: size <=16384 including LF, no CR or leading BOM,
   nesting <=8 outside quoted/escaped text, integers <=640 signless digits.
   Falsifier: host-rejected framing, byte size or integer tokens retain credit.
3. JSON -> parsed values: invalid UTF-8, syntax, duplicate keys, constants and
   nonfinite floats refuse; unexpected parser recursion becomes an excluded
   cause. Existing exact object/decision schema checks remain unchanged.
4. Parsed records -> outcomes: unchanged v1/v2 admission, kernel settlement and
   agreement logic. Actual v1 CHECK and v2 premium-diverged controls are retained,
   including exact-at-frame-limit acceptance and one-byte-over rejection.
5. Related boundaries: parser tests compare independently with the unchanged host
   at depths 8/9, integer lengths 640/641, quoted braces/escaped quotes, valid
   Unicode inside strings, BOM/CR/invalid UTF-8, duplicates, constants and size.
   Exponent overflow remains deliberately stricter than raw host JSON parsing.

Frozen RED: test-only child of r002, identical test bytes to final candidate;
26 real-capture exclusion assertion failures plus the missing raw-decoder seam
assertion, 2 unittest cases, no errors, zero skips. The missing-seam assertion
is not counted as another product counterexample. Final focused GREEN: 80
unittest cases in six suites, zero skips, exit 0, source_verified=true on 3.14.6.
Subtest matrices are not counted as separate unittest cases.

The capture cap is a retained-resource guard. Its test uses an oversized stream
that also exceeds a per-frame bound; it is not evidence of a natural completed
four-chip hand at that capture size. The direct parser oracle tests exercise the
named helper; actual-capture mutations exercise the public classify path. No new
proof of OS containment or natural corrupted captures follows from these checks.

The old semantic/schema validation and agreement code have no changed bytes.
Strategy attribution, outer unused fields, summary interpretation and ref
retirement advisories remain as disposed in the parent. No full-H run, strength,
calibration, timing adequacy or phase execution is claimed by this candidate.
