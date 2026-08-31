"""Publish finished engineering artifacts only; no Pontius source integration."""
from pathlib import Path
import hashlib
import json
import stat
import subprocess

H = Path(r"D:\Pontius-handoffs")
T = H / "v0a-i01-c-authority"
GIT = r"C:\Program Files\Git\cmd\git.exe"
EXPECTED = "c0587537c78324b2ab89308fa01c05f94ec39c83"
COPY = T / "coordinator-publish-v28-l8-checkpoint-v1.py"
OUT = T / "coordinator-v28-l8-checkpoint-publication01.json"
h = lambda raw: hashlib.sha256(raw).hexdigest()
def read(path):
    assert path.is_absolute() and ".." not in path.parts
    for ancestor in (path, *path.parents):
        assert not getattr(ancestor.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert path.is_file()
    return path.read_bytes()
def git(*args):
    return subprocess.run([GIT, "-c", "core.fsmonitor=false", "-c", "core.autocrlf=false", "-C", str(H), *args],
                          check=True, capture_output=True, timeout=60, creationflags=subprocess.CREATE_NO_WINDOW).stdout

pins = {'CURRENT.md': '8bacea70ec4512d85eea9b0a7c803f94e6cd7f5001074fd38f409915329d5550', 'coordinator-v28-storage-inspection-v1.json': '0c9ae56e485ab8a5d006ca70dc47b82d6e3e23f5139e2abe23e49cec242c46b3', 'coordinator-v28-design-verification-v1.json': 'a70eb13b0c3edb59d7944857a79d1d8c0d99aacbd715a7819c958f22e5fbf186', 'coordinator-depth-budget-v4-inspection-v1.json': '8452f8ca5c5450285f4c5cacf07e2d36aa2c4035b31e2721abff603d69c4ad78', 'coordinator-v26-sharing-verification-v1.json': 'a3d382e897e72d8c6e46c200418180823c9c1b727417e52dca9a42e68fc09801', 'coordinator-helper1050-contract-clarification-v1.json': '020b99d9e5fef402baf964eafd14fbda4416dc35bb2f095d27a7f3594d5de447', 'coordinator-class-owner-l8-inspection-v1.json': 'c41dc3ec37b377cf863d13044564187a856680dd026e0a3bd2a0878e2299c1a4', 'coordinator-v23-class-owner-l8-verification-v1.json': '0ff78f0573d8cae835509d987b61a7ec12574912f0b63e3d3121d918325def5b', 'engineer-generator-v28-storage-static-v1.json': 'cd0fc65d3df53188d3f8aa909ca9a14fc7409c549d27113b34e2268f98c9fff4', 'engineer-generator-v25-semantic-plan-v3.md': '1d661231a472fc689af06ea993234f27ab88a65da950d83f1811c1f941d94723', 'engineer-generator-v25-semantic-plan-v3-origin-clarification-v2.md': '458e182d3bfc8e715e1f9f2be0762fe1237088570a98c81f1958b1f766b22e70', 'engineer-v28-disabled-join-plan-v1.md': 'd8faada0f14b1f7ffb0e0062ebd90e6fe196718b663cba93d39cd8246ff1b7fa', 'engineer-v28-disabled-join-anchors-v1.json': '571f5bc305a43df9bf3965d000a2134c277de20ac8c4dd99b1de070b92e7dff8', 'tests-candidate-v5.py': '48c4620bf5585a76d500b3c9bf4cad4559a04d4f544bc3808832d37b58b03add', 'coordinator-budget-assertion-candidate-v1.md': 'a113ac115f7cf0e3097a4b9c321fe8a4f645285095edd68a7eb04c3de380a420', 'coordinator-budget-assertion-candidate-static-v1.json': 'e4074f8e906ea02bd15d0be4dbc0d9edcc8b61812db84937b71a136b2fc2d339'}
additional = ['coordinator-v26-diagnosis-checkpoint-publication01.json', 'coordinator-navigation-v14.json', 'coordinator-update-authority-navigation-v14.py', 'coordinator-navigation-v13-before-v14.md', 'coordinator-inspect-v28-storage-v1.py', 'coordinator-verify-v28-design-v1.py', 'coordinator-inspect-depth-budget-v4.py', 'coordinator-verify-sharing-v26-v1.py', 'coordinator-record-helper1050-contract-v1.py', 'coordinator-helper1050-contract-clarification-v1.md', 'coordinator-inspect-class-owner-l8-v1.py', 'coordinator-verify-v23-class-owner-l8-v1.py', 'coordinator-author-budget-assertion-candidate-v1.py', 'tests-candidate-v5-from-v4.diff', 'engineer-v26-cost-remedy-clarification-v2.md', 'engineer-generator-v25-semantic-plan-v3-origin-clarification-v1.md', 'engineer-depth-budget-v4-handoff-v1.md', 'engineer-depth-budget-v4-static-v1.json', 'engineer-depth-budget-probe-v4-from-v3.diff', 'tests-depth-budget-control-v4-from-v3.diff', 'tests-checks/depth-budget-v4-authoring-receipt-v1.json', 'tests-checks/depth-budget-v4-authoring-v1.py']
receipts = {'tests-checks/focused-v28-first01-design-311-receipt.json': '2002eab44b3ff699ad55298972696ad90aec2c2c38a9019cef12c848a9c0807a', 'tests-checks/depth-budget-v26-sharing01-generator70-311-receipt.json': '79339c7b8106d1eee699b41acf7c1c77b1eb54e382eef1483c5a99627b753eec', 'tests-checks/class-owner-late-store-v23-red01-311-receipt.json': '147beb79bd5182a92fe32a21e32d3b3e80b3e95ca7440cd887645bedf8b5c5e3', 'tests-checks/class-owner-late-store-v23-red01-314-receipt.json': 'b1ebed05ad93a5bd0dbd2b444034d6cd5e3b8717e36de052a95d2e3c460f6a5a'}
# These two exact families were released by their authors and all their runs completed.
# Active v25/v29 source and v28 primitive-harness authoring are deliberately excluded.
additional += [path.relative_to(T).as_posix() for path in T.glob("engineer-generator-v28-storage*") if path.is_file()]
additional += [path.relative_to(T).as_posix() for path in (T / "tests-checks").glob("class-owner-late-store-*") if path.is_file()]
assert not COPY.exists() and not OUT.exists()
assert git("rev-parse", "HEAD").decode().strip() == EXPECTED
assert not git("diff", "--cached", "--name-only", "-z")
assert all(h(read(T / name)) == pin for name, pin in pins.items())
pins.update(json.loads(read(T / "engineer-generator-v28-storage-static-v1.json"))["artifacts"])
for name, pin in receipts.items():
    raw = read(T / name)
    assert h(raw) == pin
    pins[name] = pin
    r = json.loads(raw)
    assert r.get("stage", "finished") == "finished" and not r.get("timed_out", False)
    for item in r["outputs"].values():
        path = Path(item["path"])
        assert path.is_relative_to(T)
        pins[path.relative_to(T).as_posix()] = item["sha256"]
    inputs = ([(Path(path), r["input_hashes_before"][key]) for key, path in r["input_paths"].items()]
              if "input_paths" in r else [(Path(item["path"]), item["sha256"]) for item in r["inputs_before"].values()])
    for path, digest in inputs:
        if path.is_relative_to(T):
            pins[path.relative_to(T).as_posix()] = digest
assert all(h(read(T / name)) == pin for name, pin in pins.items())
files = {T / name for name in (*pins, *additional)}
assert all(path.is_file() and path.resolve().is_relative_to(T.resolve()) for path in files)
with COPY.open("xb") as stream:
    stream.write(Path(__file__).read_bytes())
files.add(COPY)
contents = {path.relative_to(H).as_posix(): read(path) for path in sorted(files)}
attributes = H / ".gitattributes"
original_attributes = read(attributes)
assert git("show", "HEAD:.gitattributes") == original_attributes
rules = [f"{name} -text" for name, raw in contents.items()
         if b"\r\n" in raw and f"{name} -text" not in original_attributes.decode().splitlines()]
if rules:
    assert original_attributes.endswith(b"\n")
    attributes.write_bytes(original_attributes + ("\n# Preserve issued v28 and class-owner diagnostic checkpoint bytes.\n" + "\n".join(rules) + "\n").encode())
    contents[".gitattributes"] = read(attributes)
changed = {}
for name, raw in contents.items():
    result = subprocess.run([GIT, "-C", str(H), "show", "HEAD:" + name], capture_output=True,
                            timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
    if result.returncode or result.stdout != raw:
        changed[name] = raw
git("add", "--", *sorted(changed))
staged = set(git("diff", "--cached", "--name-only", "-z").decode().rstrip("\0").split("\0"))
assert staged == set(changed)
for name, raw in changed.items():
    assert git("cat-file", "blob", ":" + name) == raw
git("commit", "-m", "Retain v28 analyzer results and class-owner regression evidence")
commit = git("rev-parse", "HEAD").decode().strip()
for name, raw in contents.items():
    assert git("cat-file", "blob", commit + ":" + name) == raw and read(H / name) == raw
remote = git("ls-remote", "origin", "refs/heads/main").decode().split()
if not remote or remote[0] != commit:
    git("push", "origin", "HEAD:refs/heads/main")
    remote = git("ls-remote", "origin", "refs/heads/main").decode().split()
assert remote[0] == commit
report = {"standing": "Engineering evidence only; no Pontius integration or cold verdict.",
          "previous_commit": EXPECTED, "commit": commit, "remote_main_verified": True,
          "published_sha256": {name: h(raw) for name, raw in sorted(contents.items())},
          "new_or_changed_paths": sorted(changed), "all_stored_blobs_match_issued_bytes": True,
          "new_crlf_exceptions": rules}
with OUT.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2)
    stream.write("\n")
print(json.dumps({"commit": commit, "changed_files": len(changed), "remote_verified": True}))
