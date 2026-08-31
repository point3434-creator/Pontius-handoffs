"""Issue bounded engineering authoring scope after independent schedules are fixed."""
from pathlib import Path
import hashlib

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
pins = {
    "engineer-radix-api-boundary-plan-v1.md": "6e37ce7ce7d768c157bd00490f4d0bc8f92753385bfa375b73bab610d2e87150",
    "tests-checks/indexed-storage-extension-spec-v1.md": "11d11003b3ce84d485df549e73a494e358db69cc6f5db6faea5dae8f50c330f9",
    "tests-checks/indexed-storage-extension-cases-v1.json": "795e893c4fbeee3963a3ea3cbbffdfacbea193f53063eb4848c8e9ac6d12984a",
    "coordinator-v22-depth-budget-verification-v1.json": "0c65680c640e4c35bca18d8b2472838bfb1ad41cfef5a7a0dd24e46418815613",
}
for name, pin in pins.items():
    assert hashlib.sha256((T / name).read_bytes()).hexdigest() == pin, name
note = """# Indexed name storage: one bounded prototype

Coordinator authoring disposition, 2026-08-31. This is engineering work within
the existing C repair. It is not a cold verdict, production port, test dispatch,
W installation, frozen handoff or main integration/commit authorization.

Root read the complete API plan and independent fixed schedule specification.
The exact pins below bind this experiment before prototype code is written.
The two measured cost mechanisms justify an indexed persistent name map and
linear unique-entry bulk construction; they do not establish that either will
fit the unchanged analysis budget in production.

Authorize create-only T/engineer-name-radix-prototype-v1.py plus its static
accounting/ownership map and source diff. Keep the reviewed public APIs, add
only NameVersion.from_unique_entries, and keep immutable radix children/leaves,
fully staged publication, exact legacy-order recipes, name-only history,
effective pending proofs and explicit collisions. Preserve the original Meter
implementation and maximum262144. No caps, refunds, discounting copies or
disabled-mode certificate shortcut. Root will inspect source before execution.

Independently authorize the oracle author to implement the fixed16-schedule/
31-run extension and one explicit cursor-oracle successor. The old casepack,
24-publication retention sequence and weakref obligations remain unchanged.
Only its layer-specific compaction trigger is replaced by successful changed
publication plus direct positive-owner/current-value/release evidence. I11
adds the stronger one-publication release check. Do not fabricate compaction
counts or describe all old62 executable paths as byte-identical.

The prospective combined scope is34 unchanged storage runs,28 cursor runs
including the disclosed trigger successor, and31 extension runs. Growth8x/6x
falsifiers, fixed N values, closed collision domain and three fault offsets
are preregistered. Authors may not execute any payload. Controller, oracle,
prototype and accounting map must be pinned and inspected first; root owns
serial floor-first snapshot dispatch. A failed run is retained, not retried
with edited expectations or a changed cap.

Metering clarification: one builtin dictionary attempt is the existing unit;
explicit code-level entry visits, allocations and reference copies remain
separately charged. Internal C dictionary equality probes are not observable
Meter units. The collision oracle reports independent key-protocol counts
separately. Neither charged-work ratios nor this prototype prove wall-time
ratios. Claims of every internal hash-table probe being charged are excluded.

Stop if the replacement cannot preserve order/proof/lifetime and exact failed
operation retry within the name-store API. No threshold sweep or interpreter
expansion follows. Production constructor/full-merge adapters need a later
source review; their transfer and cell writes remain owed in original order.
Class/capture semantic repair is separate. Accepted A/B and other C paths,
W v20, original tests and generated files remain untouched.

Pinned inputs:
"""
note += "\n".join("- " + name + ": " + pin for name, pin in pins.items()) + "\n"
path = T / "coordinator-radix-prototype-disposition-v1.md"
with path.open("xb") as f:
    f.write(note.encode())
with (T / "coordinator-authorize-radix-prototype-v1.py").open("xb") as f:
    f.write(Path(__file__).read_bytes())
print(hashlib.sha256(path.read_bytes()).hexdigest())
