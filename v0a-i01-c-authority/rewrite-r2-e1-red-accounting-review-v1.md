# R2 E1 RED accounting and authority review v1

Review type: independent read-only engineering evidence review, not a cold review.

## Bound result

- Receipt SHA-256:
  `2040b896281e161f5fee285bc7c62506a867a1dc168feadc96f89ddd4fd4bd00`
- Candidate source SHA-256:
  `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`
- Controller SHA-256:
  `c76a6e170062094986e7cdea90ad8e2e7737da2d38657c6f604da8eb86417ec0`
- Probe SHA-256:
  `7ac823d560034a140275d2447bf68bbe1f98adc8c250e61d46aedada018656a3`
- Case pack SHA-256:
  `59b8457a2323634d883fb2c9b0ff82a1e60cd980c5f2a4b50e627c8ca32cdb9b`
- Schedule SHA-256:
  `4fcb92ed30a86be1664d9b1981e5e8dc8c47d5d76eaab7b08dc09db74abc9f11`

## Verdict

This is the anticipated product RED. It is not an oracle, harness, timeout,
interpreter, or custody failure.

All four harmless runtime Models matched their frozen expectations. All four
public analyzer calls completed without an analyzer exception. The candidate
then failed exactly the two module-level builtin-context cases:

- `E01-standard` is CLEAN. The Model reaches `constructor, launch`; the analyzer
  emits the required `[-m, fixed]` row with no blocker.
- `E02-module-empty` is RED. The Model captures an empty builtin mapping and
  raises `NameError(name='ValueError')` before launch. The analyzer emits the
  launch row with no blocker although this case is classified `refuse`.
- `E03-module-empty-deleted` is RED. The function retains the captured empty
  builtin mapping after the module key is deleted and raises the same
  `NameError` before launch. The analyzer again emits the launch row with no
  blocker although this case is classified `refuse`.
- `E04-local-empty` is CLEAN. A function-local spelling does not alter the
  function's captured builtin context; Model and analyzer both reach launch.

The independently rederived semantic-failure set is exactly:

```text
E02-module-empty
E03-module-empty-deleted
```

It matches the final summary and receipt. The child return code and controller
exit are both `1`, exactly the controller's declared semantic-RED result. The
receipt has `completed=true`, `integrity_ok=true`, `payload_started=true`,
`error=null`, and `cleanup_error=null`.

## Public result and receipt identities

Every digest below was recomputed from canonical sorted compact JSON plus LF.
Every projected row and blocker list also equals its full public result.

- `E01-standard`
  - public result:
    `a175a6743b873f82d444a3e691c3413c784748a5130f534a0fb14cf3c6b92b4d`
  - embedded receipt:
    `abfeb9d36d8373b0933ae1f96cf57a16ed7a8cb0cb86b7bc89688e598b88f174`
- `E02-module-empty`
  - public result:
    `9faee45c48ffab109cacf4d9e0b49552881d474faeaf2a67026f25552f723f7f`
  - embedded receipt:
    `c05d496d396b90280fe5cd7b14618a98923c5b442cd8fa4599614d06fbd0b9c8`
- `E03-module-empty-deleted`
  - public result:
    `8f9f2434494a7a52599c5a17d75d7d2340399ccf435802f72869ece3e2e057fb`
  - embedded receipt:
    `8e0305d20fb53d33aa9b10141d4fd9695d811c7798ed3c4d61088cba7a69ea56`
- `E04-local-empty`
  - public result:
    `c2cdcd271b0f4c54a8a127719dacf9a06d02742820019bed7d155c65430b8603`
  - embedded receipt:
    `bf0e0f750b91586dc236a07c3b75f045482cdd05ef57d88631259ebe3ef185d0`

## Raw-stream reconciliation

The stdout stream contains exactly six nonempty LF-only JSON-object records:
one pre-import identity, four cases in frozen pack order, and one final summary.
Stderr is empty. The retained log is byte-for-byte
`stdout + LF + CONTROL STDERR + LF + stderr`.

- setup:
  `10b90cbe412f1a183440f6fafa894da8a7d114a610eac2ac7d626c1464b7e1a4`
- stdout:
  `c6e7becd72c14caace3e9a79b0ba016920747c6f3956ee539954a1862b5ca1ed`
- stderr:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- framed log:
  `ade557dae560aea98c29b4459f60ad74f5202e296a0007b4ba910ce6a8d3f3a2`

The pre-import identity binds CPython 3.11.15 at the approved absolute
interpreter, the exact snapshot cwd, the exact source and probe, and all 1,767
manifest entries.

## Custody reconciliation

- All 22 external inputs rehash to both `input_hashes_before` and
  `input_hashes_after`: source overlay, W watch, controller, probe, case pack,
  schedule, and 16 protected paths.
- The current source overlay and W watch both still hash to the candidate pin.
- The manifest has exactly 1,767 entries: 1,761 detached-base files and six
  payload inputs. Its bytes are exactly the controller's canonical encoding of
  the receipt's `before` map.
- The manifest SHA-256 independently rederives as
  `c3272bfbeb87b2b45d5c07501df3196faf19b499047dc8f8b808c5dab89ccfea`.
  This equals the pre-import identity, setup, receipt, and after-run manifest
  identity.
- Every one of the 1,767 snapshot files presently rehashes to its manifest
  entry. There are zero missing or mismatched files.
- The receipt's `before` and `after` maps are identical. All integrity,
  after-file, and after-original error lists are empty.
- The setup file has 23 fields, and every field equals the corresponding
  receipt field.
- The retained dirty-path set is exactly the overlaid generator plus the six
  payload inputs and generated manifest; no extra path is recorded.

## Budget evidence and limit

The run revalidates the five unchanged integer caps before and after analysis:
helper depth 64, child depth 4, container elements 4,096, cardinality
2,147,483,647, and work units 262,144.

This E1 harness deliberately has no budget observer. Neither the raw records
nor the receipt contains actual requested or consumed work-unit epochs. The
evidence therefore establishes cap identity and semantic behavior, but it does
not establish actual-work headroom. No work amount can be inferred from this
receipt.

## Method and limits

I parsed and rehashed the retained bytes and the still-present snapshot using
CPython 3.11 standard-library JSON and SHA-256 code. I did not import or execute
the candidate, probe, controller, Models, or analyzer, and I did not rerun the
one-shot payload. This review classifies the retained floor result only; the
floor RED correctly provides no authority for a 3.14 run.
