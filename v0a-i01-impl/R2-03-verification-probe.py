"""Verify the two claims that most change the r005 design (read-only)."""

import sys

sys.path.insert(0, r"D:\Pontius-worktrees\v0a-increment-1\src")

from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.replay import FIXTURE_A, PROTOCOL_ID, ReplayHost


def blueprint():
    return ImmutableBlueprintActionSource(source_id="verify")


class Counting:
    def __init__(self):
        self.now = 1_000
        self.reads = 0

    def __call__(self):
        self.reads += 1
        value = self.now
        self.now += 1_000
        return value


print("=" * 72)
print("CLAIM: the dead-witness echo would create spurious duplicates")
print("=" * 72)
# Once the witness has failed, every later read raises ClockInvalidError as an
# echo. If the abort seam appended unconditionally, each echo would add a code.
clock = Counting()
ReplayHost(FIXTURE_A, run_id=f"{PROTOCOL_ID}-correctness-c", blueprint=blueprint(),
           clock=clock).run()
total = clock.reads


class Faulting:
    def __init__(self, at, kind="invalid"):
        self.now = 1_000
        self.reads = 0
        self.at = at
        self.kind = kind

    def __call__(self):
        self.reads += 1
        if self.reads == self.at:
            if self.kind == "reversed":
                self.now -= 5_000
                return self.now
            return True
        value = self.now
        self.now += 1_000
        return value


echo_counts = []
for k in (5, total // 2, total - 4, total):
    c = Faulting(k)
    host = ReplayHost(FIXTURE_A, run_id=f"{PROTOCOL_ID}-correctness-e{k}",
                      blueprint=blueprint(), clock=c)
    host.run()
    retained = host.runtime.closure_failures
    # how many times would a dead witness have been re-read after death?
    echo_counts.append((k, len(retained), c.reads - k))
print("  fault_at | codes retained today | reads attempted after death")
for k, n, after in echo_counts:
    print(f"  {k:8} | {n:20} | {after}")
print("  -> each post-death read raises an echo; an unconditional append")
print("     at every seam would record one code per echo, not one per fault")

print()
print("=" * 72)
print("CLAIM G1: a raising settlement oracle escapes ReplayHost.run entirely")
print("=" * 72)


def exploding_oracle(**kwargs):
    raise ZeroDivisionError("oracle blew up")


try:
    host = ReplayHost(FIXTURE_A, run_id=f"{PROTOCOL_ID}-correctness-g1",
                      blueprint=blueprint(), clock=Counting(),
                      settlement_oracle=exploding_oracle)
    outcome = host.run()
    print(f"  run() returned normally: passed={outcome.receipt.passed} "
          f"reason={outcome.receipt.failure_reason}")
except BaseException as error:
    print(f"  ESCAPED: {type(error).__name__}: {error}")
    print("  -> confirmed: an oracle exception is not contained by the host")
