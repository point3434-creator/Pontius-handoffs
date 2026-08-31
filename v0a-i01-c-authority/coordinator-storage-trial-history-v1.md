# Storage prototype trial history clarification v1

2026-08-31. Append-only clarification of engineering drafts and their standing.

The six completed trials executed prototype v2 only, SHA-256
22cc3966435fd4e6e0cecbcbb242275e72d34b36c835b4e960c7c712613822ff,
through control v2 and run config v1. Prototype v1, prototype v3 and control v1
were retained but never executed. No production source was imported by the
prototype/oracle child.

The coordinator requested an exact-str restriction, then withdrew that request
after reading the existing API clarification. Prototype v3 and
engineer-storage-exact-string-v1.md were issued before the withdrawal arrived.
Their narrowing was not adopted. The selected primitive remains v2 under the
ordinary-comparison precondition in engineer-storage-api-clarification-v1.md.
All actual oracle keys were exact builtin strings; arbitrary string-subclass
behavior was neither exercised nor approved. The exact-string note's metering
scope remains accurate: semantic storage work, not individual CPU opcodes.

The oracle/case/control hashes and six-child order were approved before root
dispatch. storage-oracle-plan-v2.md was not a control-bound input and its final
issuance/acknowledgment arrived after the six runs. File metadata suggests its
physical creation preceded the first setup, but mutable timestamps are not used
as authorization evidence. It is treated as post-execution-issued documentation
for evidentiary standing, not as a preregistration hash for these trials. The
integration disposition's reference to post-execution documentation has this
meaning; it does not assert a physical authoring time. The plan's execution-held
wording is stale for its final acknowledgment and must not be used as current
status. The root's earlier bounded disposition and pinned dispatch inputs remain
the actual scope record.

The resulting204 checks establish pure-storage compatibility. They do not prove
production transfer ordering, corpus headroom, a cold-review verdict, or main
integration. The bounded production port has its separate coordinator decision.
