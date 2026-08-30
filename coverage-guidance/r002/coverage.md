# Coverage claim
Category: review-finding closure paths that must distinguish a demonstrated
behavioral defect from missing or unsound acceptance evidence.

Discovery: searched the frozen workflow for RED/GREEN obligations and read
Stage 1, Stage 4 and both embedded templates. The two unconditional obligations
were Stage 1 and Stage 4; both now distinguish evidence closure. Templates
inherit those rules and add no contradictory RED requirement.

Cases: demonstrated behavioral defect -> deterministic RED before production
edit, then integrated GREEN; missing evidence with an independent check that
already passes -> document the evidence gap and actual result, no fabricated
failure or production edit; a new check exposing a behavioral defect -> ordinary
RED/GREEN path for that defect; advisory coverage suggestions -> existing
severity and acceptance rules, no automatic blocker.

Limits: this is a documentation consistency review, not a proof of test
adequacy or authorization to weaken acceptance. No code, ADR, runtime, historical
evidence or source integration changes. Existing freeze and review gates stay.

Falsifier: any operative instruction still makes product RED mandatory for
closing a coverage-only finding whose independent check already passes.
