"""Publish finished engineering artifacts only; no Pontius source integration."""
from pathlib import Path
import hashlib
import json
import stat
import subprocess

H = Path(r"D:\Pontius-handoffs")
T = H / "v0a-i01-c-authority"
GIT = r"C:\Program Files\Git\cmd\git.exe"
EXPECTED = "b969c2e96c459c798594fec5accc90576f6ab8d3"
COPY = T / "coordinator-publish-v26-diagnosis-checkpoint-v1.py"
OUT = T / "coordinator-v26-diagnosis-checkpoint-publication01.json"
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

pins = {
    "CURRENT.md": "a23bd4da38ab3118b975cd1e01316fa64f43c96f839e9b269e466f2b7733ec2b",
    "coordinator-v26-storage-inspection-v1.json": "37937253b7b483429607d1d54341c5cf9e80c0344b1cf123d3ee2145ebe52084",
    "coordinator-class-r8-harness-inspection-v2.json": "cbe508beaaa240402007b7f8b294c3cd5600051895e58fa4f7ca632e6de23f10",
    "coordinator-v26-r8-verification-v1.json": "181248855d1947c775d21728ed3ae5c2bb62b7deb15604154f88b95290e89bac",
    "coordinator-depth-budget-v3-inspection-v1.json": "c8b31bcb1e2250047d35c11c458b3efaf72843919cf74a177d5fc4ce332e0de5",
    "coordinator-v26-depth-budget-verification-v1.json": "2e729e903ed0f0c869e88aa595d62bc0da5a2f3a47d29962f901a4865a87bf30",
    "engineer-v26-cost-remedy-plan-v1.md": "e32d45c914cf9422429f493b3dfec475e23d05d58f957dca896ec95b75bb2d93",
    "engineer-generator-v25-semantic-plan-v1.md": "39807c39a14e6f2009ffa69f5f09604c8354c1043a09be6c63e5982412621c2d",
    "engineer-generator-v25-semantic-plan-v2.md": "e2ed7f88a6c081be3ec54556e47a327ce1ea2d336e55200e788857cfec099bb8",
}
additional = [
    "coordinator-v23-v24-checkpoint-publication01.json",
    "coordinator-navigation-v12.json", "coordinator-update-authority-navigation-v12.py",
    "coordinator-navigation-v13.json", "coordinator-update-authority-navigation-v13.py",
    "coordinator-navigation-v12-before-v13.md", "coordinator-inspect-v26-storage-v1.py",
    "coordinator-inspect-class-r8-harness-v2.py", "coordinator-verify-v26-r8-results-v1.py",
    "coordinator-inspect-depth-budget-v3.py", "coordinator-verify-depth-budget-v26-v1.py",
    "engineer-generator-v26-storage-binding-map-v1.json",
    "engineer-generator-v26-storage-handoff-v1.md", "engineer-generator-v26-storage-static-v1.json",
    "engineer-generator-v26-storage-root-cause-v1.md", "engineer-generator-v26-storage-root-cause-v2.md",
    "engineer-generator-v26-storage-from-v22.diff", "engineer-generator-v26-storage-from-r010.diff",
    "engineer-depth-budget-probe-v3-from-v2.diff", "tests-depth-budget-control-v3-from-v2.diff",
]
additional += ["tests-checks/class-comprehension-extension-" + suffix for suffix in (
    "probe-v1.py", "control-v1.py", "probe-v1-from-boundary-v1.diff", "control-v1-from-boundary-v1.diff",
    "probe-v2-from-v1.diff", "control-v2-from-v1.diff", "handoff-v1.md",
    "authoring-v1.json", "authoring-v2.json", "static-proof-v1.json", "static-recipe-v1.txt",
    "static-v1-receipt.json", "harness-static-proof-v2.json", "harness-static-v2-receipt.json",
    "harness-static-recipe-v1.txt", "harness-static-recipe-v2.txt")]
receipts = {
    "tests-checks/focused-v26-first01-design-311-receipt.json": "284ddc5bbadbcc2f46c89b8a0ae782eeadade716090d3788ae122d591b1ef7fe",
    "tests-checks/class-comprehension-extension-v23-red01-311-receipt.json": "5c56ae9cc8a0c6a46be61e10ca7786505caa8173145878d18df0842ddc62add1",
    "tests-checks/class-comprehension-extension-v23-red01-314-receipt.json": "6df879fcdf435dda1ba5a234ab2f41eaf6f0358e028789985c5d68b11e1267e8",
    "tests-checks/depth-budget-v26-cost01-helper1050-311-receipt.json": "39c226dd9a619edc22da425d846a4e07319eb24bb42064f5e323392fb352015f",
    "tests-checks/depth-budget-v26-cost01-helper65-311-receipt.json": "9544ba20d5eb289a10032166a764e302a02d2eb1f20229e7953d1c04e4562cbe",
    "tests-checks/depth-budget-v26-cost01-generator70-311-receipt.json": "14351189ec337a045a8e812174bad3f018901804d4f52c72b1929bbdc950f366",
}
assert not COPY.exists() and not OUT.exists()
assert git("rev-parse", "HEAD").decode().strip() == EXPECTED
assert not git("diff", "--cached", "--name-only", "-z")
assert all(h(read(T / name)) == pin for name, pin in pins.items())
for name, prefix in (("coordinator-v26-storage-inspection-v1.json", ""),
                     ("coordinator-depth-budget-v3-inspection-v1.json", ""),
                     ("coordinator-class-r8-harness-inspection-v2.json", "tests-checks/")):
    pins.update({prefix + key: value for key, value in json.loads(read(T / name))["pins"].items()})
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
    attributes.write_bytes(original_attributes + ("\n# Preserve issued v26 diagnostic checkpoint bytes.\n" + "\n".join(rules) + "\n").encode())
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
git("commit", "-m", "Retain analyzer cost diagnosis and semantic repair plan")
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
