# Windows handle fixture implementation r001

Frozen commit 76309774b551a874b8f9c677bc59e51299cee0e4;
manifest 755c34175c060a4f0ef55616c9e52e336989645763cb16c0fd5a26293a7a37a6.

The controller approved the bounded repair and the task-local rule-8 exception.
Two independent design reviews cleared the retained brief and two addenda.
The source was then changed in a separate no-hardlinks clone of frozen codec
r002, not the unfrozen codec authoring bytes.

## Implementation

The 173-nonblank-line test adapter routes directory CreateFileW and NtCreateFile
tokens to real Windows handles, restores embedded RootDirectory arguments, and
forwards IO/identity/close calls. Ordinary CreateFileW read handles remain native
through CRT ownership. Its scope is the three existing reuse helpers only.
The four allocation-dependent numeric-search setups become one controlled
reassignment each. All 14 role/family cases and existing ownership/rollback
assertions remain. Two early replay-veto assertions were removed so a bad close
can reach the actual replacement; raw-native survival checks detect the damage.

Three new methods cover deterministic reassignment with real CRT readback,
four production replay mutations (including directory ownership), and failed
publication/leak-guard cleanup. Registration adds exactly three stable IDs:
2851 -> 2854 entries. Profile bytes do not change. The self-census keeps all
counts and analyzed-call digest; only its source-position-sensitive decoy digest
changes to 37b7508932c784b6898999b2c024eeb8e004aa492b10cf1a948a1028f3cc9ed2.

## Retained development evidence (not post-review acceptance)

All payloads ran in fresh D-local snapshots, CPython 3.11.15 first, -B -P,
scrubbed environment, absolute Git. Receipt names below are in run-records/.

- adapter-red-311: FAIL, 1 test; two simultaneously live native handles differed
  (772 != 764), so the native-only setup could not meet deterministic reuse.
- adapter-green-311: PASS, 1 test, after routing implementation.
- fixture-green-311: PASS, original encompassing Windows method, including
  the 14 controlled cases and its unchanged native helpers.
- controls-green-311: 4 tests, one ERROR in the publication-failure control:
  its initial expected exception was too narrow for the real acquisition path.
  Subsequent changes preserve the acquisition error and clear unpublished
  output handles during rollback; this receipt remains retained.
- controls-green-2-311: PASS, 4 focused tests.
- controls-final-311 and controls-final-314: PASS, 4 focused tests per slot,
  including all four bad-replay schedules and native raw closure observations.
- regenerate-311: generator --write exit 0; generated inventory copied from
  this snapshot; profile output identical to frozen codec r002.
- inventory-dev-native-311: 91 tests, one FAIL, exclusively the old decoy
  self-census digest. All fixture and other suite assertions passed.
- census-diagnostic-311 and final-census-diagnostic-311 retain the old/new
  digest mismatch with maxDiff=None. Counts and analyzed sites stayed fixed.
  The final observed digest was then updated mechanically before freezing.
- An earlier native snapshot clone attempt refused dubious ownership before
  Python execution. The runner now uses only exact command-local safe.directory
  settings for the isolated source clone; no global Git settings changed.

The final freeze also includes stricter native error checking, retired-token
checks, and drain-all teardown. Post-freeze reviews and acceptance must verify
these exact bytes; earlier development greens do not substitute for that gate.

Independent audit.py r001 confirms parent/ref/tree, raw Git blobs, sorted
manifest, exact exported files, and the two-path scope. Primary HEAD remains
c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98 with no tracked changes.
No previous packet, primary source, codec, analyzer, decision, or seal was edited.
