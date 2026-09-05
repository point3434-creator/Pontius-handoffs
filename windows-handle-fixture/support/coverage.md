# FIX coverage claim: native handle-reuse fixture setup

Failure category declared before implementation in brief-design.md: requiring
a particular native numeric handle to recur within a finite allocation loop.
Discovery: read the complete existing failing helpers, search range(4096), and
trace their Windows acquisition/identity/close consumers. Independent design
review B separately inventoried the three helpers, four loops, and 14 cases.

| Fixture family | Members | Replacement property |
| --- | --- | --- |
| final3 role isolation | staging, published, recovery, directory, deterministic_lock | Captured native replacement remains open and identity-stable. |
| round7 prebound ownership | staging, original, recovery, published, readback, published_disposal | Independent unrelated-file native handle survives; existing rollback and ownership assertions remain. |
| round9 same-inode disposition | staging, published_disposal, recovery | Native hardlink handle survives with same file identity; exact owned-name absence remains decisive. |

All four allocation loops are removed, not enlarged or retried. Numeric reuse
is simulated only at the approved private native-call boundary. The outer
Windows method's other fixture helpers run without the facade. The existing
status-failure and still-present-name controls inside the selected helpers
remain, with their existing assertions.

Added controls: simultaneously live native resources make the native-only
setup deterministically fail the same-token requirement (adapter-red-311);
real read_regular_snapshot preserves exact bytes through native CRT transfer;
retired tokens remain invalid until reassigned; native acquisition survives
only successful publication; unpublished-handle failures close the native
resource; normal/error teardown detects and closes unexpected live handles.

Negative production controls deliberately replay ambiguous closes through
_WindowsGovernanceFileOwner in each of the three helpers, and separately
through _WindowsHandleOwner in the role-isolation helper. The replacement is
actually closed; facade-bypassing native queries observe that closure, and
the existing writer fixture fails its added raw-native survival assertion.

The oracle is the captured native HANDLE and full-width identity, queried with
original GetHandleInformation/GetFileInformationByHandleEx. Table bookkeeping
and production liveness helpers routed through that table are not sufficient.
The facade neither vetoes replay nor supplies successful IO/identity results.

Limits: finite governed API call surface, current Windows ABI and documented
interpreter slots; not a Windows allocator proof, every possible native fault,
hostile ctypes replacement, or general filesystem emulation. Ordinary native
integration tests and full acceptance must still pass. Codec, analyzer,
original failed receipts and all earlier candidates remain unchanged.
