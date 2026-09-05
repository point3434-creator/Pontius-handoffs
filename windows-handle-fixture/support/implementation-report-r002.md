# Windows fixture correction r002

Commit c7de23de276c50463d831f3983fede82a5400ce8;
manifest f5e06a5fa9d0fdf37888d29f8bfe6b395b6fc40a4c6f87258f66c95aa17421ed.

Both r001 reviewers found Spec PASS, design SOUND, no Critical/Important
findings, and the same five Minor E501 lines. Those five statements were
wrapped. Before the census update, a complete parsed-AST comparison against
the frozen r001 test blob was identical. The untouched analyzer then reported
c62e275fa42bcb8cc9bef4a382990793adc03ecc9d9db1b6fcd35aeb9b23372e
as the new source-position-sensitive decoy digest; all census counts and the
analyzed-call digest stayed fixed. Receipt r002-census-diagnostic-311 retains
the mismatch before updating the expected literal.

The corrected test is AST-identical to r001 after normalizing exactly that
one expected digest literal. No added line exceeds 100 columns. Inventory
and profile bytes remain equal to r001; codec and analyzer remain equal to
the codec-r002 base. Original candidates, reports, and receipts are unchanged.

Two fresh-context correction reviews are pending. The one correction budget
is now used. Full post-review acceptance is not yet claimed.
