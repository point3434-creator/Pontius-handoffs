# Independent Tier C design review B — resolution

Resolution target:

- Original review: `design-review-b.md` SHA-256
  `194cda75021b8f4f828958ccf05fc8cacf43b6312908f6017f0200f374b45f15`
- Retained brief: `brief-design.md` SHA-256
  `cae851310c2517106a3bddd7fba36fa154f751bc85b2e323d86fb69da9682022`
- Retained correction 1: `design-addendum-1.md` SHA-256
  `00a9acb667102562f3a4019f9359c0271216bc91f3ffb5d41c77ffcfb346f9f9`
- Retained correction 2: `design-addendum-2.md` SHA-256
  `e6aeeefd5a5607a70ec63b23bab3fa8b43e66ab685df2e36ade02a9ed7290cc0`
- Existing source baseline: authoring HEAD
  `5e56e4454f7b8ccb360d3e36245abc33318349bb`

Review mode: bounded read-only design inspection. No fixture, test, or
production execution was performed.

## Resolution of B-01

**Resolved.** Design clarification 2 supplies each required invariant and
verification boundary from B-01:

- Every successful native acquisition has exactly one destination: unchanged
  transfer to CRT ownership or publication as one live token. Failure during
  validation or token publication raw-closes the newly acquired native handle
  before propagating the error.
- Token reassignment transfers, rather than duplicates, the single ownership
  entry; a successful delegated close retires it once.
- Facade teardown restores the private ctypes reference, raw-closes all
  remaining adapter-owned handles before discarding state, fails on every
  unexpected live entry even when fallback closure succeeds, and preserves an
  original exception when fallback closure also fails.
- Every replacement retains its actual native HANDLE. Positive survival and
  identity checks call the original `GetHandleInformation` and
  `GetFileInformationByHandleEx` functions on that handle, bypassing token
  translation.
- The negative replay reaches the native replacement through the real
  production retry path, and the same raw-native checks must observe closure.
  Final test cleanup verifies both native closure and an empty token table.

The correction also distinguishes the teardown leak guard from evidence of
successful production cleanup, preventing fallback cleanup from manufacturing
a positive result.

## Final verdict

Defect verdict: **PASS / CLEAN**.

Finding counts (Critical / Important / Minor): **0 / 0 / 0**.

Design verdict: **SOUND**. The corrected private-ctypes facade has a bounded
single-owner lifecycle, a non-self-confirming raw-native oracle, and an
explicit CRT-transfer boundary. It retains the real production writer,
ownership/rollback, files and namespace effects, native IO/identity/close, all
three helpers, all four former allocation loops, and their 14 existing
role/family cases. Codec and analyzer remain outside the change surface, and
the claim remains limited to production cleanup under controlled numeric reuse.

This is a design verdict only. Implementation and executable acceptance remain
subject to the frozen-round reviews and snapshot gates specified by the brief.
