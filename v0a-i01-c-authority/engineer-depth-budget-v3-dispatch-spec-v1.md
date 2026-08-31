# v26 three-case cost diagnostic dispatch specification

Authoring only; root reviews exact bytes before any dispatch. No product or cold
review verdict. Source 1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951; probe 7aa9f188b2917fec149485501eafcc4d516d3104a10b026e5ec33262b24962ae; controller 91533776e028ad57513611940423cd1cb2c6d8c0d85f8cafd49f089ebfd9e2d7.
Original tests c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf; W watch e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679.

Fixed population (one per fresh r010 snapshot):
- helper1050, original4920-4959, terminal1049: 'analysis.*(?:depth|budget)'.
  Fixture 148ffd41c2a5d5616a4b8d1cf8bc297f488ae8f6ddc1109d1d2842afa9183754.
- helper65, original20418-20456, terminal64, original inline test and argument
  layout preserved: '^analysis helper depth exceeds 64$'. Fixture 94b070b8fcf2e66c42e1a779558e830d7caae670366f9313faf0989c722818c6.
- generator70, original14528-14556, not bounded32:
  '^analysis deferred generator depth exceeds 64$'. Fixture 635e682b2253cd44201e2afdb95c288b9973f5629ec4eeb3c5bfd078743eb5e3.

All builders are AST-equivalent to original construction; existing helper1050 and
generator70 builder ASTs are unchanged. Only the existing _source reference is
qualified through fixtures. Static authoring generated inert text for hashes;
returned source and repository/test/candidate modules were not executed/imported.

Invoke tests-depth-budget-control-v3.py with actual floor
D:/Pontius-tools/py311/Scripts/python.exe -I -S -B -P, passing --label, --case,
--source-path, --source-sha, --probe-sha, --control-sha, --watch-sha explicitly.
It pins v26 and the exact probe, creates a fresh D-local r010 clone/detach each
time, checks1761 originals and1766 total before/after paths, and validates actual
identity before imports. Retain original child -B -P, site/no-user, scrubbed
PYTHONPATH/Git and absent PYTHONHASHSEED.60s owned direct-child watchdog; immutable
output names/raw logs/incomplete receipts. No314/matrix/corpus/owner/GPU execution.

Original budget init/consume and NameMeter charge bodies remain unchanged.
Every request delegates once, unchanged units/exceptions. Initial plus all
requested units (including cap crossing) must equal actual final work.
component_units and phase_units are aliases of ONE disjoint nearest-original-frame
partition. Stage totals and NameMeter kinds are separate views, not extra work.
Publication preparation deltas are inclusive cross-cuts and include nested radix
work; never add them to the budget partition. Histograms retain only raw integer
tail/base sizes, dirty/completed booleans and numeric min/max/total/call counts.
The completion event after unwind includes failed preparation costs absent from
the first failure record. Changed publication commits are counted separately.
Bulk first/final-charge events are attempts, not completed-build claims.
Bulk shape attempts record raw source/parent counts at constructors and union/
per-input counts at full joins (exact dict/set/tuple/private cursor sizes only).
No Mapping/view/get/len/items observer calls, state/Flow/AST/budget/frame retention
or cache mutation. Existing partial-construction guards remain unchanged.

Components distinguish leaf copying, radix edit/freeze/bulk, lookups, ordering,
publication/snapshot/fork, constructor/full-join bulk preparation, transfer/
certificate/cell and authority stores/forks/joins. Immediate/parent/third origins
retain original call sites. All added counter wrappers delegate originals once.
Measure tiny-publication cost versus repeated full environments/upstream work;
also retain ordered read cost and partial failure costs. No remedy, speed ratio,
cap discount or general production fitness can be inferred from this alone.
