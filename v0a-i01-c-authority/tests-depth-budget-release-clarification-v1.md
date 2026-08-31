# Diagnostic release prose clarification v1

This clarifies tests-depth-budget-release-v1.md SHA256
8f54e836f55b5fd0c887793891d7c923406507fa1f74d6b1914afdc2fe2f5bab,
whose bytes remain immutable.

The generator70 fixture's exact expected message includes a space before 64:
`analysis deferred generator depth exceeds 64`.
The original regular expression is
`^analysis deferred generator depth exceeds 64$`.
The prior prose accidentally joined "exceeds64"; it is not a changed expectation.
No test, candidate, probe or controller byte has been changed.

Controller completion requires `caps_unchanged is True` and
`original_methods_restored is True`, both JSON booleans, together with
`completed is True`, the selected case and exact source/tests hashes.
A dictionary in either boolean field does not satisfy the controller.
The cost author confirmed this schema before completing the new probe.

Controller SHA256 remains
9df274065efc48c9bd31d208c0ac0a3d13bc6217bf3fee762ef06cf7d7a2e407.
No payload or Python parse/import was executed by this author.
