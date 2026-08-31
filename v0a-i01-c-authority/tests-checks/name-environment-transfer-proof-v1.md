# Restricted completed-transfer certificate: bounded proof

Engineering inspection only by codex/cold_review_a; no payload or source/test edit. Exact inspected source: D:/Pontius-handoffs/v0a-i01-c-authority/engineer-generator-v19.py, SHA-256 3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1. This note answers the coordinator's four-fact question, not the complete persistent-name design.

Verdict: SUPPORT. On the exact _FlowValue class and current _transfer_authority function, the following observed facts are sufficient; no repeated scan of the other fields is needed:

1. An actual full transfer completed with its store enabled.
2. The returned object is the original input object, using is rather than equality.
3. The returned object's authority_refs is empty.
4. The returned object's helper_provenance is None.

Reason, by exhaustive current control-flow partition:

- The disabled-store return at14043-14044 is excluded by fact1.
- The existing-root return at14046-14048 cannot qualify: it returns the input with nonempty authority_refs, contradicting facts2/3. The missing-root path at14052 creates a replacement and never restores the original object.
- Every executed sequence/slice/maybe_unbound, mapping/mapping_keys, effective starred_argument, defaults, receiver or obligations update at14056-14073 puts an entry into updates. Even an empty container/update value leaves that dictionary nonempty. Line14074 then calls the standard dataclasses.replace imported at10. For this exact frozen slots dataclass9018-9037, replace constructs a new instance; there is no identity-preserving constructor hook or path back to the original input. Thus fact2 excludes every such executed branch, including all nested transfer work it could perform.
- Every registration path14075-14082 allocates an authority identity and returns a replacement carrying a reference. Facts2/3 exclude it. No earlier identity allocation exists outside the already-excluded recursive/missing-reference paths.
- Consequently the qualifying execution reaches14083 with its original ref-free input, without an object-store read/write, recursive transfer, replacement or authority-identity allocation. The remaining authority-side action is the existing budget.consume at14045. No lexical-cell operation occurs in this function.
- A later retained=True call could otherwise newly activate the sole retained-dependent registration term, retained and helper_provenance is not None at14075. Fact4 rules that out. The other executed branch conditions depend on unchanged fields of the same frozen _FlowValue, and the ref-free path does not inspect store contents. Thus no store-ancestry certificate is required for this restricted no-effect fact.

This is more precise than my earlier conservative all-field/kind blacklist. For example, starred_argument with a non-_FlowValue payload does not execute the update branch at14064, so it may meet the four facts without violating the proof. The proof excludes executed stateful branches; it need not reject every value merely bearing a broadly excluded kind label.

The stated use is appropriately narrow: consult the metadata only to omit repeated top-level merge transfer of an unchanged entry. It does not certify safe consumption, omit recursive/retained consumer work, discharge sensitivity/refusal rules, skip cell writes, or establish that a projected name is unchanged across deletion/reinsertion. Roots remain pending, all raw projections remain pending even for the same object, and all strong/weak cell writes remain. Sensitive qnames can qualify; their consumer analysis still runs.

Preserve existing raw/adoption timing: captured-cell projection14453, parameter installation18407, caller-cell refresh18471 and state adoption14159-14162 must not acquire eager transfer or semantic cell writes. Pending metadata is processed at the next boundary that previously transferred; it does not create a new transfer boundary. Full transfer must complete before certification; a disabled transfer or exception never earns it. Certificate lookup/bookkeeping remains metered appropriately; this proof does not claim identical budget-failure timing after redundant operations are removed.

No concrete counterexample exists within those exact conditions on the inspected function. No broader transfer memoization, store-root certificate, production implementation, test run, or acceptance verdict is asserted by this note.
