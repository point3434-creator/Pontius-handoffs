from pathlib import Path
import hashlib

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
navigation = T / "CURRENT.md"
raw = navigation.read_bytes()
assert hashlib.sha256(raw).hexdigest() == "ccd28b1e953bfe4d8d2a6b24ae9fc7233ced3a415dd90edd042d74a4bb61133b"
old = """The [bounded port disposition](coordinator-storage-integration-disposition-v1.md)
authorizes the next production edit in the isolated C worktree only. The source
there is now an engineering work surface until its exact successor is returned
and reviewed; v19 remains the last tested production source. All five caps, test
contracts, accepted A/B and the other three C paths remain fixed. No main source
integration or new frozen handoff is implied.
"""
new = """The port produced v20 source
e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679,
which is rejected for production fitness. Its first floor DesignReview run
completed 53 tests with two failures and one error: bounded helper analysis
exhausts the unchanged work cap. The [single-chain diagnosis](engineer-checks/chain32-v20-diagnosis01-311-receipt.json)
locates the dominant cost in helper-disabled joins that repeatedly rebuild name
trees, followed by ordered reads.

The [v20 public24 assessment](tests-checks/name-environment-v20-floor-report-v1.md)
confirms all 24 public expectations and 58 harmless witnesses still pass on 3.11.
Shared forks and enabled sparse joins improve locally, but total charged work
rises 8.07 times versus v19. This is a consumed-budget comparison, not a runtime
multiplier. [Coordinator verification](coordinator-v20-diagnostics-verification-v3.json)
rehashes the retained snapshots and checks these results.

The [fitness disposition](coordinator-v20-storage-fitness-disposition-v1.md)
closes the port lease and reassesses the name-store lifetime before another edit.
W remains exact v20; v19 is the last source with both focused populations green.
No further v20 acceptance run, developer-slot run, matrix or ordinary generation
is planned. All five caps, test contracts, accepted A/B and the other three C paths
remain fixed. No main source integration or new frozen handoff is implied.
"""
text = raw.decode().replace("\r\n", "\n")
assert text.count(old) == 1
text = text.replace("Last completed behavioral checks: v19 source",
                    "Last successful full focused checks: v19 source")
text = text.replace(old, new)
copies = {
    "coordinator-v20-storage-fitness-disposition-v1.md": Path(r"D:\Pontius\codex-v20-storage-fitness-disposition-v1.md"),
    "coordinator-verify-authority-v20-diagnostics-v1.py": Path(r"D:\Pontius\codex-verify-authority-v20-diagnostics-v1.py"),
    "coordinator-verify-authority-v20-diagnostics-v2.py": Path(r"D:\Pontius\codex-verify-authority-v20-diagnostics-v2.py"),
    "coordinator-update-authority-navigation-v6.py": Path(__file__),
}
assert not any((T / name).exists() for name in copies)
for name, source in copies.items():
    with (T / name).open("xb") as stream:
        stream.write(source.read_bytes())
navigation.write_bytes(text.encode())
print(hashlib.sha256(navigation.read_bytes()).hexdigest())
