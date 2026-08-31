# Radix metering clarification v1

Append-only clarification to engineer-radix-api-boundary-plan-v1.md
SHA6e37ce7ce7d768c157bd00490f4d0bc8f92753385bfa375b73bab610d2e87150,
agreed with coordinator and independent oracle author before implementation.

A charged Python dictionary attempt is one get/membership/write/delete call.
It is NOT a measured count of CPython's internal hash-table/equality probes.
Every explicit entry traversal, hash request, routing step, allocation and
reference copy performed by prototype code is metered. Thus copying a full
collision leaf visits and charges all entries, while a dict.get may perform
O(bucket size) hidden equality work behind one charged dictionary attempt.

The independent closed-domain colliding keys count __hash__/__eq__ calls and
report that work separately from Meter units. Their counters delegate ordinary
comparison and are not installed into production. No extra linear scan,
fabricated collision charge or claim of internal-probe introspection is used.
Logical attempt counts, explicit-copy growth, callback protocol counts and
elapsed performance are distinct evidence categories.

This preserves the existing meter abstraction. It does not establish a strict
CPU-instruction/time bound from the work cap under pathological collisions.
The fixed extension specification11d11003b3ce84d485df549e73a494e358db69cc6f5db6faea5dae8f50c330f9
states the same distinction. No source or payload is authored by this note.
