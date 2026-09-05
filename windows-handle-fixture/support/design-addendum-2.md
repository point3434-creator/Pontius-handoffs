# Design clarification 2: adapter ownership and independent oracle

Applies with design-addendum-1.md to the retained brief. This makes explicit
the leak and self-confirmation protections required by its acceptance contract.

Every successful native acquisition is either returned unchanged into the CRT
path or published as one live token. If validation or token publication raises,
the acquisition wrapper raw-closes that newly acquired handle before propagating
the error. Token reassignment transfers that single ownership entry; it does
not duplicate it. A successful delegated close retires its live entry once.

On every context exit the facade is restored. Before discarding any state,
teardown attempts a raw close of every remaining adapter-owned native handle.
Unexpected live entries make the test fail even if fallback closure succeeds;
failed fallback closure also fails and preserves the original exception as
context. Teardown is a leak guard, never successful production cleanup evidence.

Each replacement records its actual native HANDLE at the moment of reassignment.
Survival and identity assertions use original GetHandleInformation and
GetFileInformationByHandleEx functions directly against that captured native
handle, bypassing the token facade. The negative replay must close that native
replacement through the real production retry path, and those raw checks must
observe the failure. Token bookkeeping alone cannot satisfy an assertion.
Final explicit test cleanup verifies native closure as well as an empty table.

No new production seam or exception is introduced. Size and round caps remain.
