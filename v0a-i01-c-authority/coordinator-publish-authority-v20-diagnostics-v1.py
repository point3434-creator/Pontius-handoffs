"""Publish completed rejected-port evidence to the handoff repo only."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

H = Path(r"D:\Pontius-handoffs")
T = H / "v0a-i01-c-authority"
GIT = r"C:\Program Files\Git\cmd\git.exe"
EXPECTED = "40cbe0354252ee7db902f1388e92f1916bef0875"
OUT = T / "coordinator-v20-diagnostics-publication01.json"
COPY = T / "coordinator-publish-authority-v20-diagnostics-v1.py"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*arguments):
    return subprocess.run([GIT, "-c", "core.fsmonitor=false", "-C", str(H), *arguments],
                          check=True, capture_output=True).stdout


assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
assert sys.dont_write_bytecode and not sys.flags.optimize
assert not OUT.exists() and not COPY.exists()
assert git("rev-parse", "HEAD").decode().strip() == EXPECTED
assert not git("diff", "--cached", "--name-only", "-z")
pins = {
    "CURRENT.md": "61bca3a8288d33a40dfb4b8354c34f77397263b275146cc287d0369d5fd48fc4",
    "engineer-generator-v20.py": "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679",
    "engineer-generator-v20.diff": "b5e1c1829223b4ac9c263e94217dd3343c7eb9f3f74ec49b6f4fe00f7f460dfb",
    "engineer-generator-v20-from-v19.diff": "a7ea75b1d27299b4bba698135da34193ccd543313eca95d61839fb1e9db3a8a6",
    "engineer-checks/v20-storage-port-static.json": "12bfc43364de5e98279acb8669dfb0bacfb39f6bce4cd58628e531eccfacec3d",
    "coordinator-v20-inspection-v1.json": "f7e3bd6011127f5f25b7dd7ab03c65d5b4bc081ebb890b1026ab327edbb7150d",
    "coordinator-v20-diagnostics-verification-v3.json": "bb85cea1a3215499be58469d983c57a241626c198abd8a469deef1af70cd883c",
    "coordinator-v20-storage-fitness-disposition-v1.md": "52b0319d5f3fdee8802f4950f2b4043d34d6e3ba1a0aae5755c4b01b3db6ba22",
    "engineer-storage-construction-inventory-v1.md": "c5c949cca879d900dcffde0b1518aa9f2ac75f4f94346ec2da7eda43c377b6ba",
    "engineer-storage-fitness-successor-v1.md": "1307b0c2b10ab8fce5de974b26fdce5721969e599f6f121bf9b4ffe36747decb",
    "tests-checks/name-environment-v20-floor-report-v1.md": "5ed00d464ec049ba638b455fe2db44d2e5063211d973aa0c95b44bcb30f7d6ff",
}
verification = json.loads((T / "coordinator-v20-diagnostics-verification-v3.json").read_bytes())
pins.update(verification["inputs_sha256"])
files = {T / relative for relative in pins}
files.update(T / relative for relative in (
    "coordinator-storage-publication02.json",
    "coordinator-inspect-authority-v20-v1.py",
    "coordinator-verify-authority-v20-diagnostics-v1.py",
    "coordinator-verify-authority-v20-diagnostics-v2.py",
    "coordinator-verify-authority-v20-diagnostics-v3.py",
    "coordinator-update-authority-navigation-v6.py",
    "engineer-storage-port-prerepair-v20.md",
    "engineer-chain32-budget-probe-v1.py",
    "engineer-chain32-budget-control-v1.py",
    "engineer-chain32-budget-plan-v1.md",
    "engineer-checks/chain32-v20-diagnosis01-311-setup.json",
    "tests-checks/name-environment-control-v20-v1.py",
    "tests-checks/name-environment-v20-hook-map-v1.md",
    "tests-checks/name-environment-v20-measurement-plan-v1.md",
    "tests-checks/name-environment-v20-outcome-criteria-v1.md",
    "engineer-storage-coverage-inspection-v1.md",
    "tests-checks/storage-composition-cases-v1.json",
    "tests-checks/storage-composition-probe-v1.py",
    "tests-checks/storage-composition-control-v1.py",
    "tests-checks/storage-composition-plan-v1.md",
))
for relative, expected in pins.items():
    assert sha((T / relative).read_bytes()) == expected, relative
assert all(path.is_file() and path.resolve().is_relative_to(H.resolve()) for path in files)
with COPY.open("xb") as stream:
    stream.write(Path(__file__).read_bytes())
files.add(COPY)
contents = {path.relative_to(H).as_posix(): path.read_bytes() for path in sorted(files)}
attributes = H / ".gitattributes"
old_attributes = attributes.read_bytes()
assert git("show", "HEAD:.gitattributes") == old_attributes
rules = [f"{name} -text" for name, raw in contents.items()
         if b"\r\n" in raw and f"{name} -text" not in old_attributes.decode().splitlines()]
if rules:
    assert old_attributes.endswith(b"\n")
    attributes.write_bytes(old_attributes + (
        "\n# Retain rejected C storage-port and diagnostic bytes.\n"
        + "\n".join(rules) + "\n").encode())
    contents[".gitattributes"] = attributes.read_bytes()
# Prior already-published inputs are verified above but need no new staged blob.
changed = {}
for name, raw in contents.items():
    existing = subprocess.run([GIT, "-C", str(H), "show", "HEAD:" + name],
                              capture_output=True)
    if existing.returncode != 0 or existing.stdout != raw:
        changed[name] = raw
git("add", "--", *sorted(changed))
staged = set(git("diff", "--cached", "--name-only", "-z").decode().rstrip("\0").split("\0"))
assert staged == set(changed), (staged, set(changed))
for name, raw in changed.items():
    assert git("cat-file", "blob", ":" + name) == raw, name
git("commit", "-m", "Record rejected C storage port and bounded diagnostics")
commit = git("rev-parse", "HEAD").decode().strip()
for name, raw in contents.items():
    assert git("cat-file", "blob", commit + ":" + name) == raw, name
    assert (H / name).read_bytes() == raw, name
remote = git("ls-remote", "origin", "refs/heads/main").decode().split()
if not remote or remote[0] != commit:
    git("push", "origin", "HEAD:refs/heads/main")
    remote = git("ls-remote", "origin", "refs/heads/main").decode().split()
assert remote[0] == commit
receipt = {
    "standing": "Retained rejected-port engineering evidence; no main-source integration or cold verdict.",
    "previous_commit": EXPECTED, "commit": commit, "remote_main_verified": True,
    "published_sha256": {name: sha(raw) for name, raw in sorted(contents.items())},
    "new_or_changed_paths": sorted(changed),
    "all_stored_blobs_match_issued_bytes": True, "new_crlf_exceptions": rules,
}
with OUT.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(receipt, stream, indent=2)
    stream.write("\n")
print(json.dumps({"commit": commit, "changed_files": len(changed), "remote_verified": True}))
