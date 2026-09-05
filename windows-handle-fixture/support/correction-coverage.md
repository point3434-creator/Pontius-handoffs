# FIX r002 coverage: added-line width

Failure category: newly added test lines exceeding pyproject.toml's E501
100-column limit. Independent r001 reviewers found the same five sites:
21184 (107), 21337 (104), 21338 (103), 21382 (101), 21424 (106).
Both found no behavioral/spec defect. This uses the one allowed correction.

Discovery and limits: scan every added line in the frozen r001 diff for width,
not just the five examples. Wrap those expressions without changing their AST.
Run a parsed-AST comparison before changing the mechanically derived decoy
self-census digest. Obtain that new digest by executing the unchanged analyzer
against the new line positions, then change that literal only. Inventory and
profile bytes must stay equal to r001; codec/analyzer/fixture behavior unchanged.
An added line over 100 columns, any other AST change, changed registrations,
or failing exact-byte focused/suite verification falsifies the claim.

Retain r001 and its reports. r002 receives a fresh raw-blob manifest and two
fresh-context reviews; no third correction round is authorized.
