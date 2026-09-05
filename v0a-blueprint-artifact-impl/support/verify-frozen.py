"""Independent read-only raw Git object and packet identity audit."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
packet = root / "packets" / sys.argv[1]
identity = json.loads((packet / "candidate.json").read_bytes())
repository = root / "authoring"

def git(*args):
    return subprocess.check_output([
        r"C:\Program Files\Git\cmd\git.exe", "-c",
        "safe.directory=" + repository.as_posix(), "-C", str(repository), *args])

commit = identity["commit"]
assert git("rev-parse", identity["ref"]).strip().decode() == commit
assert git("rev-parse", commit + "^").strip().decode() == identity["base"]
assert git("rev-parse", commit + "^{tree}").strip().decode() == identity["tree"]
fields = git("diff-tree", "-r", "-z", "--no-renames", "--no-commit-id",
             "--name-status", identity["base"], commit).split(b"\0")
rows = []
for status, raw_path in zip(fields[::2], fields[1::2]):
    assert status in (b"A", b"M")
    path = raw_path.decode("utf-8")
    blob = git("cat-file", "blob", commit + ":" + path)
    assert blob == (packet / "files" / path).read_bytes(), path
    rows.append(hashlib.sha256(blob).hexdigest() + "  " + path + "\n")
assert len(rows) == 12
manifest = "".join(sorted(rows)).encode()
assert manifest == (packet / "manifest.sha256").read_bytes()
assert hashlib.sha256(manifest).hexdigest() == identity["manifest_sha256"]
print(json.dumps({"identity": identity, "raw_blobs_verified": len(rows)}, indent=2))
