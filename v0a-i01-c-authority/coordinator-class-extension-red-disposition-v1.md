# Class/capture extension: replicated pre-repair RED

All twelve fixed harmless models pass on actual Python 3.11.15 and 3.14.6.
The public analyzer completes all twelve sources without errors on both slots.
Ten semantic requirements fail identically: all five required-unsafe cases
are incorrectly clean; five of six required-clean cases are refused. The
explicit read/write control passes; the permitted-refusal forwarding control
is refused as allowed.

The unsafe known-raise case also emits the class-local module inner instead
of outer. This is an observed public namespace leak, not just an inferred
exception-join risk. The recursive clean case enters invoke at closure depth
one with armed=True, although the harmless model changed it to False. It
returns no subprocess row and two blockers. Route coverage is entry-without-row;
it is not correct to call this route unexecuted.

The coordinator rehashed every snapshot/payload/input/output file. Complete
per-case records are equal across runtimes. See
coordinator-class-extension-red-verification-v1.json for receipt and log pins.
The fixed source/model pack is tests-checks/class-semantic-extension-cases-v1.json.

These are failures already present in retained v19. They do not attribute a
regression to v22 storage. The original ten composition cases remain unchanged.
No semantic source repair, acceptance result, integration or cold verdict is
claimed. Next: approve a concrete lexical-ownership and class-successor design,
implement it as a separate retained candidate, then rerun the fixed scopes.
