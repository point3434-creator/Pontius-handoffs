# R2-E1 issued harness engineering review

Verdict: STRAINED by one acceptance-gate defect, E1-H1. Full result, custody, case count and floor rules otherwise reconcile. This is static engineering review of issued, unexecuted bytes; it is not runtime evidence, cold acceptance or payload authorization. No candidate, probe, controller, Model, test or sensitive source was executed.

Reviewed members: probe7ac823d560034a140275d2447bf68bbe1f98adc8c250e61d46aedada018656a3; control09f9fccdca6790d9299c49692eb78f2440206393261994d4df1fe35621e00336; probe delta fbedd43d3fa92568ff5b58575dc54ed3693b12fdbfa017f4caebecd7d53e0de5; control delta4e83c9e2a47b8bf79e27c4a44b110b68211cd909d767590a4479fc95ecd722c2; static map73246b42a82a8cbf113c7507ad47be1f51365a43f8e7794c2cc57560b5c53308.

The exact issued deltas were independently reconstructed from class-owner-late-store v1 predecessor bytes. Changed probe definitions are load_pack, oracle, public_review and main; changed controller definitions are validate_result and main. Adopted custody/hash/environment helpers remain AST-exact.

## Acceptance defect E1-H1: unexpected child output can be ignored

rewrite-r2-e1-control-v1.py:134 constructs records only from stdout lines whose first byte is an opening brace. Any nonempty line that does not begin with that byte, including arbitrary import-time output, whitespace-prefixed JSON, blank lines between records or other text, is ignored. The remaining expected six JSON records can still satisfy all count/order/semantic checks and produce a GREEN receipt. Child stderr is retained in the raw log but is not constrained before success either.

That does not meet the family’s full raw result reconciliation contract. Retaining bytes for later inspection does not make unexpected bytes part of the automated admission decision.

Required category closure: parse every stdout line as exactly one JSON object and require the exact identity/four-case/summary sequence, without a prefix filter. Require empty stderr unless a nonempty exact stderr contract is separately frozen. Malformed, extra or blank records and unexpected stderr must make the run infrastructure/validation failure, never product GREEN. This is a harness acceptance defect, not a candidate result and not a request to execute a falsifier.

## Hygiene H2: pre-try output acquisition can leave no receipt

The controller opens its five output streams by create-exclusive comprehension at247 and writes initial setup at256 before entering the protected try. Failure partway through stream creation or initial setup write can leave partial files and no completed receipt.

This is recoverability/diagnostic hygiene rather than an acceptance defect: the path cannot produce completed/integrity/success true, cannot unlock development and launches no child. Root must treat missing receipt as infrastructure failure and choose a fresh label after inspecting partial outputs. It need not block focused reproduction if retained as an explicit inherited limit.

## Result and custody reconciliation

- The probe executes only separately frozen harmless oracle source. Sensitive case source is parsed for shape and passed as bytes to derive_design_review; it is never compiled or executed. Harmless namespace supplies FunctionType and a fresh builtin dictionary explicitly, verifies exact function/globals/builtins ownership and catches external NameError with its name.
- public_review’s body is AST-exact to the adopted name-environment function; only its generator parameter differs. It constructs the fixed path, stable ID, inventory and serialized bytes. Casepack additionally verifies its embedded envelope.
- Each case record carries complete public result and canonical digest. validate_result rehashes full result and nested receipt after JSON decoding, rederives rows/blockers/argv, and counts analyzed cases only from present reconciled public results. Missing public result is allowed only with oracle or analyzer failure and cannot count as completion.
- Exactly one identity, four ordered cases and one final summary are required among parsed records. Summary analyzed count must equal controller count; classification/caps/failure lists and child exit are recomputed.
- Four-case/2clean+2refuse population is consistent. Payload membership is an exact basename set: six files on floor, eleven on development, plus1761 tracked paths. Probe and controller derive count from those sets.
- Current new-core WATCH hashes to explicit candidate SHA and retained overlay matches it. Sixteen protected paths are before/after original inputs at exact hashes. Fresh r010 snapshot retains all1761 tracked hashes, one generator overlay, exact payload set, manifest and HEAD/status checks.
- Interpreter, executable, flags, environment digest, PYTHONPATH, Git, hash seed, preimport state, candidate/probe/pack/schedule/control hashes, source copy and manifest are checked before import. Final source/payload/manifest/caps are rechecked.
- Development requires matching floor receipt plus setup/raw outputs, fresh snapshot rehash, integrity/completion/semantic success true and exact exit0. Semantic RED/exit1 does not unlock3.14.
-60-second watchdog, kill/final wait, final integrity and create-exclusive outputs prevent interrupted/reused run from success. Cleanup/validation failures force non-GREEN.

## Static evidence and limits

No other material acceptance or custody issue was found. Control helpers require/sha/canonical/valid_digest/checked/create/write_json/environment/git/file_hashes and probe helpers require/digest/canonical/checked/hashes are AST-exact to predecessor. Exact public-review body and both source deltas were independently reconstructed with stdlib AST/hash operations only.

This review does not validate candidate behavior, harmless oracle runtime, repair, Python3.14 or GateB. E1-H1 requires a create-only successor and exact review before dispatch. H2 may be retained as disclosed infrastructure hygiene if root accepts its no-receipt failure mode.
