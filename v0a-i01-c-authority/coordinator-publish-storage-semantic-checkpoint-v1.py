"""Publish finished engineering artifacts only; no Pontius source integration."""
from pathlib import Path
import hashlib
import json
import stat
import subprocess

H = Path(r"D:\Pontius-handoffs")
T = H / "v0a-i01-c-authority"
GIT = r"C:\Program Files\Git\cmd\git.exe"
EXPECTED = "e2f7df1dd5ce75612959ede408727c117c9417e5"
COPY = T / "coordinator-publish-storage-semantic-checkpoint-v1.py"
OUT = T / "coordinator-storage-semantic-checkpoint-publication01.json"
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

pins = {'CURRENT.md': 'd649a2330a752cbb8c08759a5423f371032d36b51461f8db0beb63824ee174ed', 'coordinator-v28-primitive-311-verification-v1.json': '648ca365745b1d436a4245034f7172301c3d4236bb09a9b2995153573abb4ca9', 'coordinator-v28-primitive-314-verification-v1.json': 'bb6d58429de302b0c5ecebea380033b9c4dd623df4b242510db6fd1dec3d3b11', 'coordinator-v28-testfix-verification-v2.json': '1de262da99ffebe65d74e34409b1a06b4401e2bc2dc9e2196469ea07d5e47b14', 'engineer-generator-v25-semantic.py': '481098d0be86d27f1664d0705a44a91d50b3a1361280a4e28c82bc366a541853', 'engineer-generator-v29-storage.py': 'b53b905cd20dd97d7d09a3b81f955bf27498a572ce8a6d82e20f007993ab9466', 'tests-checks/v25-authority-carrier-engineering-review-codex-a-v1.md': '7b0b322d2c91c6db51b1c9c7549b59413b89c2d02edb4fce6865d5eaede1627c', 'tests-checks/v29-disabled-join-engineering-review-codex-a-v1.md': 'f397975e37f00ea9512563e91dea9bc89ae7f9dda2ce96ab2f5ed5ba1dc610ad', 'engineer-generator-v25-review-successor-plan-v1.md': '56c1b494349ea3b70af3eee2f26d9bf99fab72db1725b5b833b4af187be4ac34', 'engineer-v30-enumerate-accounting-plan-v1.md': 'a6fbc28533102f86341daac86cb76761517e2b2770421d29c6b8d94381bdf983', 'tests-checks/v28-primitive-engineering-review-mapping-v1.md': '31d1d6f88ce3fa35036c618f5b4ce866a0e72bbde98eb9d8dcb6daf5c81b8733', 'engineer-budget-assertion-candidate-review-v1.md': 'faf1bdb169669c5e252cfe679e8e4ed0fb08f522a5a14d1c753d0c56664de10c'}
additional = ['coordinator-v28-l8-checkpoint-publication01.json', 'coordinator-navigation-v15.json', 'coordinator-navigation-v14-before-v15.md', 'coordinator-update-authority-navigation-v15.py', 'coordinator-author-v28-primitive-config-v1.py', 'coordinator-verify-v28-primitive-v1.py', 'coordinator-v28-primitive-disposition-v1.json', 'coordinator-author-focused-control-v2.py', 'coordinator-focused-control-v2-static-v1.json', 'coordinator-focused-control-v2-handoff-v1.md', 'tests-focused-control-v2-from-v1.diff', 'tests-focused-population-v2.json', 'coordinator-verify-v28-testfix-v1.py', 'coordinator-verify-v28-testfix-v2.py', 'coordinator-testfix-verifier-v1-failure.json', 'coordinator-correct-testfix-verifier-v2.py', 'engineer-budget-assertion-candidate-review-v1.json', 'coordinator-disabled-join-operation-disposition-v1.md', 'engineer-checks/generator-v25-semantic-static-v1.json']
receipts = {'tests-checks/focused-v2-v28-testfix01-design-311-receipt.json': 'bba7e6c5368fd0a513fb43e008f7b7d4437f0629ad14e4db5f1b79efb9f557f1', 'tests-checks/v28-primitive-first01-311-seed0-receipt.json': '8c2dcb38a6fb00a977b10f7ef3e354066d093fd76d5f920ed3f50d68ba82f3f7', 'tests-checks/v28-primitive-first01-314-seed0-receipt.json': '6f4614f6ea451516ed3bf168793dc6db3843acd4986631122dfab90f6aec8e32'}
# These exact families are frozen/released; all included runs completed.
# Active v30/v31 authoring and any future payloads are deliberately excluded.
additional += [path.relative_to(T).as_posix() for pattern in ("engineer-generator-v25-*", "engineer-generator-v29-storage*") for path in T.glob(pattern) if path.is_file()]
additional += [path.relative_to(T).as_posix() for path in (T / "tests-checks").glob("v28-primitive-*") if path.is_file()]
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
    attributes.write_bytes(original_attributes + ("\n# Preserve issued storage and semantic-review checkpoint bytes.\n" + "\n".join(rules) + "\n").encode())
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
git("commit", "-m", "Retain production storage checks and semantic review blockers")
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
