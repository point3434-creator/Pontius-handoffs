# Prospective R1 unittest entry reserved-name table v1

Author: codex/cold_review_a, engineering source inspection. This is a proposed narrow unsupported-entry guard for root approval, not a candidate edit, runtime pass, or cold verdict.

Binding table: rewrite-r1-unittest-entry-reserved-names-v1.json; SHA256 55ed71468da3c480e4805672b2b254e1bff5d6d0cf99a2c36ed0fbcfec202ceb.
Frozen Task5 v1: 810cbb934e20a13c9c4794e3574bcb6a248ddc8b4a84a56045f6370c1a066cea.
Separate v1 semantic review: 93f14ff8e628377ad121602033d78b861866b2e7283fbc8eb73f3a7c6457934a.

## Guard and exact boundary

Before manufacturing a receiver for a selected canonical unittest entry, inspect only the explicit class namespace members. Refuse if any name has dunder spelling (starts and ends with two underscores) OR belongs to the frozen reserved_names union. Do not execute the hook to decide whether its body is harmless. Do not apply this entry guard to construction of dormant local classes. Do not scan arbitrary user helper names or lexical locals for framework-like spelling. Other class decorators/bases, custom descriptors and unsupported entry kinds retain their independent refusal rules.

The union contains 111 names: 102 distinct names actually bound in TestCase class scope across the two source versions plus 9 explicit receiver/class lifecycle storage fields. Seven union entries are dunders, so the fixed nondunder set has 104 names if the implementation uses the separate any-dunder predicate. Either literal representation must have exactly the same predicate. The whole framework override union is deliberately conservative for R1; not every member is reached on every entry.

The generic dunder predicate covers constructors, attribute lookup/store/delete, descriptors, __call__, skip/expected-failure metadata and other unproved language hooks without enumerating examples. The fixed names cover run/debug, _call* dispatch, cleanup, default result and constructor addTypeEqualityFunc, plus the remaining exact inherited TestCase surface. Inherited unmodified framework names are not explicit user overrides. Ordinary user methods remain allowed subject to existing evaluation rules.

Six instance fields are _cleanups, _outcome, _subtest, _testMethodDoc, _testMethodName and _type_equality_funcs. Three class lifecycle fields are _classSetupFailed, _class_cleanups and tearDown_exceptions. A custom same-named class descriptor/override cannot be assumed inert during inherited initialization, cleanup or dispatch.

## Source provenance and derivation

Read each pyvenv.cfg, resolve home/Lib/unittest/case.py, hash raw bytes, then ast.parse them. No unittest import, runtime introspection or candidate/fixture/Model/test execution occurred. The scanner itself used actual Python3.11.15 -I -S -B -P; version_info in each pinned pyvenv.cfg associates each source tree with the already configured runtime. It did not execute the3.14 interpreter merely to derive a static table.

TestCase bodies in these exact files contain only method definitions, direct-name assignments and docstring expressions; the derivation asserts that closed shape. All such class names are included. Lifecycle fields come only from self/cls Attribute Store/Del in those methods; the derivation asserts those receiver names are neither rebound nor shadowed by nested parameters. There are no external TestCase.attribute stores in either case.py. Method locals, other classes and arbitrary string constants are excluded. Every included name has source line/category provenance in the JSON.

- Slot 311 configured 3.11.15: C:\Users\point\AppData\Roaming\uv\python\cpython-3.11.15-windows-x86_64-none\Lib\unittest\case.py
  Source SHA256 f062e82d6bcdc231865b62bd3f8fc8847e49211f4884c685ec696216e227b957; 58503 bytes; TestCase lines 344-1384.
  Config D:\Pontius-tools\py311\pyvenv.cfg; SHA256 05e8c6723a649a094e741cc2c3d1bf78e0bdb740dde0e002ac4cced97fd3ea22.
  91 class-scope names; 9 lifecycle fields.
- Slot 314 configured 3.14.6: C:\Users\point\AppData\Local\Python\pythoncore-3.14-64\Lib\unittest\case.py
  Source SHA256 6c233f91c98b16899cb09801178c2313f48d58dce66a36d2d144facedb6bdbc4; 65855 bytes; TestCase lines 371-1534.
  Config D:\Pontius\.venv\pyvenv.cfg; SHA256 5dd9ef4595660a5702ad9aa254f696ad2370fa936d4fb2d5b0d2a6290d7fe770.
  85 class-scope names; 9 lifecycle fields.

The initial sandbox source read could not access the3.14 installation; the authorized owner-context read succeeded. This is access provenance, not a test result. No production/source/test/generated/ledger files were changed.

## Exact proposed union

The JSON reserved_names list is authoritative and sorted. The readable literal below repeats it; per-name provenance remains in the JSON.

~~~text
__call__
__eq__
__hash__
__init__
__init_subclass__
__repr__
__str__
_addDuration
_addExpectedFailure
_addUnexpectedSuccess
_assertNotWarns
_baseAssertEqual
_callCleanup
_callSetUp
_callTearDown
_callTestMethod
_classSetupFailed
_class_cleanups
_cleanups
_deprecate
_diffThreshold
_formatMessage
_getAssertEqualityFunc
_outcome
_subtest
_tail_type_check
_testMethodDoc
_testMethodName
_truncateMessage
_type_equality_funcs
addClassCleanup
addCleanup
addTypeEqualityFunc
assertAlmostEqual
assertAlmostEquals
assertCountEqual
assertDictContainsSubset
assertDictEqual
assertEndsWith
assertEqual
assertEquals
assertFalse
assertGreater
assertGreaterEqual
assertHasAttr
assertIn
assertIs
assertIsInstance
assertIsNone
assertIsNot
assertIsNotNone
assertIsSubclass
assertLess
assertLessEqual
assertListEqual
assertLogs
assertMultiLineEqual
assertNoLogs
assertNotAlmostEqual
assertNotAlmostEquals
assertNotEndsWith
assertNotEqual
assertNotEquals
assertNotHasAttr
assertNotIn
assertNotIsInstance
assertNotIsSubclass
assertNotRegex
assertNotRegexpMatches
assertNotStartsWith
assertRaises
assertRaisesRegex
assertRaisesRegexp
assertRegex
assertRegexpMatches
assertSequenceEqual
assertSetEqual
assertStartsWith
assertTrue
assertTupleEqual
assertWarns
assertWarnsRegex
assert_
countTestCases
debug
defaultTestResult
doClassCleanups
doCleanups
enterClassContext
enterContext
fail
failIf
failIfAlmostEqual
failIfEqual
failUnless
failUnlessAlmostEqual
failUnlessEqual
failUnlessRaises
failureException
id
longMessage
maxDiff
run
setUp
setUpClass
shortDescription
skipTest
subTest
tearDown
tearDownClass
tearDown_exceptions
~~~

Module fixture roots refused by R1 are distinct from custom hooks affecting a manufactured stable test receiver. This table does not establish module fixture safety or expand async, descriptor, inheritance or arbitrary protocol execution. No test population, oracle labels, caps, budgets or dynamic input assumptions changed.
