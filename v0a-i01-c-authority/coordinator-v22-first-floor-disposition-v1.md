# v22 first floor disposition

Engineering evidence, not a cold review or an integration verdict.

The first retained v22 candidate (61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3) completed all 53 original
design test methods on actual CPython 3.11.15: 51 passed, two failed, no errors,
skips or timeout. Receipt SHA-256: 0ce67a5f0846dd67655234cc27d51a560ee3711dda8f5b0a9194432ff6ee62fd.

Both failures are work-cap rejection before the expected depth rejection:
the 1050-helper source at original test line 4949, and the 70-generator source
at line 14551. The unchanged 32-generator assertion before the latter was
reached and passed; this closes the specific v20 chain32 failure only. Later
assertions after an exception in a failed method are not counted as exercised.

The coordinator independently rehashed all 1766 tracked/payload files and all
retained input/output pins. The snapshot contains 1761 original tracked paths;
only its generator differs from r010. W remains v20 and the retained candidate
is untouched. See coordinator-v22-focused-red-verification-v1.json.

Matrix, public24, dev-slot and corpus expansion remain held. The next allowed
engineering step is a floor-only diagnosis of these exact two failing source
cases. Sensitive fixtures remain AST-only; original consume logic, caps, tests,
and semantic expectations are unchanged. No message-only permission can turn
these failures into a pass. No source integration, main commit or main push
has occurred.
