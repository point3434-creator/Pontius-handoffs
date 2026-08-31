# Independent engineering review: proposed helper1050 assertion

Verdict: no material defect found in this one-line correction. Static review only;
this is not a test pass, source acceptance, or permission to relabel earlier runs.

Reviewed tests-candidate-v5.py
48c4620bf5585a76d500b3c9bf4cad4559a04d4f544bc3808832d37b58b03add
against v4 06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd
and original r010 tests c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf.
Root explanation coordinator-budget-assertion-candidate-v1.md
a113ac115f7cf0e3097a4b9c321fe8a4f645285095edd68a7eb04c3de380a420.
One-line diff 3a6abc077a0cd7f21788ae89adc0332330d920f3f3e9f95745776022d8e926c6.

The old helper1050 assertion expressly admitted analysis depth OR budget failure
but did not match the unchanged canonical work-budget error. The replacement
admits precisely helper depth64 or work262144. It narrows arbitrary depth/budget
wording while recognizing the separately exact-required work error.

Inverse replacement recovers every v4 byte. Independent AST comparison against
original r010 proves the complete helper1050 method unchanged except this literal,
and helper65, generator70 and the canonical work-cap method wholly unchanged.
The1050 helper population/body and review invocation are not weakened or skipped.
All three helper-depth error origins in exact v28 use the accepted spelling; the
production work cap is262144. No production source/error/cap changes occurred.

At v5 lines4951/20448/14553/20587, respectively: helper1050 now admits the two
canonical outcomes; helper65 remains exact helper depth64; generator70 remains
exact deferred-generator depth64; the separate work-cap boundary remains exact
work262144. Thus generator70 cannot be made green by this correction.

Use v5 only as a new pinned test candidate in new receipts. All prior v4/original
failures remain failures under their original snapshots. Neither tests nor
candidate source was imported or executed during this review.
