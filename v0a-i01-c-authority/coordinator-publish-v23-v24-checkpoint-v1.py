"""Publish completed engineering results only; no source integration."""
from pathlib import Path
import hashlib
import json
import subprocess

H = Path(r"D:\Pontius-handoffs")
T = H / "v0a-i01-c-authority"
GIT = r"C:\Program Files\Git\cmd\git.exe"
EXPECTED = "169cb6907715ac27cf10076fa6de57bdfadff50c"
COPY = T / "coordinator-publish-v23-v24-checkpoint-v1.py"
OUT = T / "coordinator-v23-v24-checkpoint-publication01.json"
h = lambda raw: hashlib.sha256(raw).hexdigest()
pins = {
    "CURRENT.md": "65ffc56c09408ce5cb4714084aa40a57f1fdbf6d913a9bbaf99fab5dd13f654f",
    "coordinator-v23-semantic-verification-v2.json": "33a2257f5ec5ac31ec3f4b59342dc46e86bcab6451df1656ca7fd1931aa1d1a7",
    "coordinator-v24-port-red-verification-v1.json": "a6d29d7391f048f353bca409c37ec8342901a25ac2612a5be2f8a27b894c091b",
    "coordinator-class-comprehension-red-verification-v1.json": "29753b2f8ee8c413ad050b692a91db85055d088b252a16fb1a0f86c811bfbf8d",
    "coordinator-v23-semantic-inspection-v1.json": "bae0b60c7a6aa098fa132ba5db1e0d4d9d249383a893022d0e1ead618f4f6a47",
    "coordinator-v24-storage-inspection-v1.json": "3a49b00cd10a41d317b1d4d92f3fee219c3b08fce9da48cbce525450cc0758a6",
    "coordinator-original-ten-inspection-v1.json": "5368059136316f1f86937f64c7109784aa6338969c2936f3a09acdd4c3b841af",
    "coordinator-class-comprehension-harness-inspection-v1.json": "6e4042208114b70ac2d655f0c522f5f94fa8a1dd35195da3455da186fdb221af",
    "tests-checks/class-comprehension-v23-engineering-review-codex-a-v1.md": "84461f44efa2da40cfc8729a0d80eb45c0266e4e88a67d88d9d7703c955d44cc",
    "engineer-generator-v23-semantic-from-v22.diff": "a6a69bfa10ad120f423c025d76112391320a71bb5222319a4e339351851eaec8",
    "engineer-generator-v23-semantic-from-r010.diff": "5d1032f321e120b64f0c084409920a721005c7d4deae0757a888bc9c9c48f7c7",
    "engineer-checks/generator-v23-semantic-static-v1.json": "64439a89ea77835aabf68f29290ad6d491ca1602a4e6ee5bdfed1034c3e709e0",
    "engineer-generator-v23-semantic-category-inventory-v1.md": "48d803bb88096ae9a7796f50b74e48c1c8a7136cc06f747061d8bbc4ac2af275",
    "engineer-generator-v24-storage-from-v22.diff": "891d9efa90db1428fe96fb56eca40a5da7271c843f4c603e614de90b94ea71f2",
    "engineer-generator-v24-storage-from-r010.diff": "ea618b085802781132f97718234f3a4dc44d6d6a0ce21334619b47ffc9b5f7a8",
    "engineer-generator-v24-storage-static-v1.json": "1ba6352dc8a7130f361ef962cdee7816d348c3322bb6c4179b56de2a41dca29e",
    "engineer-generator-v24-storage-namespacing-v1.json": "39858fc73cdd3b2279184de3838f1d70533aacc9d382a477494caf39bf07c38a",
    "engineer-generator-v24-storage-handoff-v1.md": "66f72788e7f4081704ddd5392f00cdc12d49c477b4750b4ea0dd6ba58bc400a3",
    "engineer-radix-production-adapter-plan-v1.md": "3c75c841feaabdd15f1bcce99b729746d9f6e463f41c09eeb76da72a0622a819",
}
additional = [
    "coordinator-radix-class-checkpoint-publication01.json",
    "coordinator-navigation-v11.json", "coordinator-update-authority-navigation-v11.py",
    "coordinator-inspect-v23-semantic-v1.py", "coordinator-inspect-v24-storage-v1.py",
    "coordinator-verify-v23-semantic-v2.py", "coordinator-verify-v23-semantic-v1-failed.py",
    "coordinator-verify-v24-port-red-v1.py", "coordinator-verify-class-comprehension-red-v1.py",
    "coordinator-inspect-original-ten-control-v1.py", "coordinator-inspect-class-comprehension-control-v1.py",
]
def git(*args):
    return subprocess.run([GIT, "-c", "core.fsmonitor=false", "-c", "core.autocrlf=false", "-C", str(H), *args],
                          check=True, capture_output=True, timeout=60, creationflags=subprocess.CREATE_NO_WINDOW).stdout

assert not COPY.exists() and not OUT.exists()
assert git("rev-parse", "HEAD").decode().strip() == EXPECTED
assert not git("diff", "--cached", "--name-only", "-z")
for name, digest in pins.items():
    assert h((T / name).read_bytes()) == digest, name
receipts = {}
for run in json.loads((T / "coordinator-v23-semantic-verification-v2.json").read_bytes())["runs"]:
    receipts["tests-checks/" + run["group"] + "-v23-diag01-" + run["slot"] + "-receipt.json"] = run["receipt_sha256"]
for run in json.loads((T / "coordinator-class-comprehension-red-verification-v1.json").read_bytes())["runs"]:
    receipts["tests-checks/class-comprehension-boundary-v22-red01-" + run["slot"] + "-receipt.json"] = run["receipt_sha256"]
receipts["tests-checks/focused-v24-first01-design-311-receipt.json"] = "c9e6cb1e958bc6a8e15f0989841e5a1562dc3682286c07e7a6b44b95ee9339e1"
for name, digest in receipts.items():
    raw = (T / name).read_bytes()
    assert h(raw) == digest
    pins[name] = digest
    r = json.loads(raw)
    for item in r["outputs"].values():
        path = Path(item["path"])
        assert path.is_relative_to(T)
        pins[path.relative_to(T).as_posix()] = item["sha256"]
    if "input_paths" in r:
        inputs = [(Path(path), r["input_hashes_before"][key]) for key, path in r["input_paths"].items()]
    else:
        inputs = [(Path(item["path"]), item["sha256"]) for item in r["inputs_before"].values()]
    for path, digest in inputs:
        if path.is_relative_to(T):
            pins[path.relative_to(T).as_posix()] = digest
for name, digest in pins.items():
    assert h((T / name).read_bytes()) == digest, name
files = {T / name for name in (*pins, *additional)}
assert all(path.is_file() and path.resolve().is_relative_to(T.resolve()) for path in files)
with COPY.open("xb") as stream:
    stream.write(Path(__file__).read_bytes())
files.add(COPY)
contents = {path.relative_to(H).as_posix(): path.read_bytes() for path in sorted(files)}
attributes = H / ".gitattributes"
original_attributes = attributes.read_bytes()
assert git("show", "HEAD:.gitattributes") == original_attributes
rules = [f"{name} -text" for name, raw in contents.items()
         if b"\r\n" in raw and f"{name} -text" not in original_attributes.decode().splitlines()]
if rules:
    assert original_attributes.endswith(b"\n")
    attributes.write_bytes(original_attributes + ("\n# Preserve issued v23/v24 checkpoint bytes.\n" + "\n".join(rules) + "\n").encode())
    contents[".gitattributes"] = attributes.read_bytes()
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
    assert git("cat-file", "blob", ":" + name) == raw, name
git("commit", "-m", "Retain class repair progress and adapter port failure")
commit = git("rev-parse", "HEAD").decode().strip()
for name, raw in contents.items():
    assert git("cat-file", "blob", commit + ":" + name) == raw, name
    assert (H / name).read_bytes() == raw, name
remote = git("ls-remote", "origin", "refs/heads/main").decode().split()
if not remote or remote[0] != commit:
    git("push", "origin", "HEAD:refs/heads/main")
    remote = git("ls-remote", "origin", "refs/heads/main").decode().split()
assert remote[0] == commit
report = {"standing": "Engineering evidence only; no Pontius source integration or cold verdict.",
          "previous_commit": EXPECTED, "commit": commit, "remote_main_verified": True,
          "published_sha256": {name: h(raw) for name, raw in sorted(contents.items())},
          "new_or_changed_paths": sorted(changed), "all_stored_blobs_match_issued_bytes": True,
          "new_crlf_exceptions": rules}
with OUT.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2)
    stream.write("\n")
print(json.dumps({"commit": commit, "changed_files": len(changed), "remote_verified": True}))
