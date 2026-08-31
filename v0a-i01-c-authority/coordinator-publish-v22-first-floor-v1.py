"""Publish completed engineering evidence to H only. No Pontius source integration."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

H = Path(r"D:\Pontius-handoffs")
T = H / "v0a-i01-c-authority"
GIT = r"C:\Program Files\Git\cmd\git.exe"
EXPECTED = "611df3f283759667c6a3dcb2e6861e73d173c102"
OUT = T / "coordinator-v22-first-floor-publication01.json"
COPY = T / "coordinator-publish-v22-first-floor-v1.py"
PINS = {
    "CURRENT.md": "73eff5377b56557868f3a007292d2b44cd9738009f14a9be4025a62cc2fe22f7",
    "engineer-generator-v21.py": "181993a34985a7eaa045744f662be20b9cee3b2e3c63752af15810ea47ef7ff6",
    "engineer-generator-v22.py": "61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3",
    "tests-focused-control-v1.py": "2676cc5e58db5a1e70044610de1876c96e23b38cd1a55c4f22f47aaa59118eba",
    "tests-focused-wrapper-v1.py": "839e30c19b825defae4fea30ec899a43cd0ad346953215421b81478ffc20ca35",
    "tests-focused-population-v1.json": "8799fd0f5996b84397b42f12b84f19a120a3b99f4be76a78775a4e5666856362",
    "tests-focused-release-v1.md": "9d979e02b260b07432fd2345c204f8fe5438a9e3a4b4d709ed0c59f6d2672a56",
    "tests-checks/focused-v22-first01-design-311-receipt.json": "0ce67a5f0846dd67655234cc27d51a560ee3711dda8f5b0a9194432ff6ee62fd",
    "coordinator-v22-focused-red-verification-v1.json": "82cefb7ed8bf2dffdc497c9e84dfa0ad7a402e484504d16171087a43230048f9",
    "coordinator-v22-first-floor-disposition-v1.md": "fe8d135dd4466a8c4b9a554d78e0ac96b18a10b20dbf8a9121ca28dcb05cb6a3",
    "coordinator-v22-first-floor-disposition-v2.md": "b3ba2b9ee0086234d0c96611057fbed20fb7a370da8a8fc6c3552cab7843c513",
    "coordinator-cursor-adapter-v22-inspection-v2.json": "e899a7e7a6192206dad67026087f02114662a821873b1a8788d6abbd18e71245",
    "tests-checks/cursor-oracle-report-v1.md": "217d83296cf48255026e81f9d79601522c6ab90b845b50b944a17ceaf2ef0d00",
    "tests-checks/cursor-oracle-run-proof-v1.json": "21d32132376dfa1bfb1aa62c66408fa30527532ea911f0c7ae3586d4cb2151c8",
    "engineer-class-composition-findings-repair-proposal-v1.md": "6bc11ee035a6388d73b954d1c5e9b6cd24e8815452fc56bb58197d4ae1b6c143",
    "engineer-class-proposal-challenge-v1.md": "14c406145d6eac98529a58c818987afc75f0bbfbc2c4521cc5708281ef6a09d4",
}
ADDITIONAL = (
    "coordinator-cursor-class-publication01.json",
    "coordinator-navigation-v8.json",
    "coordinator-update-authority-navigation-v8.py",
    "coordinator-inspect-cursor-adapter-v22-v1.py",
    "coordinator-inspect-cursor-adapter-v22-v2.py",
    "coordinator-verify-v22-focused-red-v1.py",
    "engineer-generator-v21.diff",
    "engineer-generator-v21-from-v20.diff",
    "engineer-generator-v22.diff",
    "engineer-generator-v22-from-v20.diff",
    "engineer-generator-v22-from-v21.diff",
    "engineer-name-cursor-v21-namespacing.json",
    "engineer-name-cursor-v22-namespacing.json",
    "engineer-name-cursor-candidate-v22-return.md",
    "engineer-checks/v21-cursor-candidate-static.json",
    "engineer-checks/v22-cursor-candidate-static.json",
    "engineer-build-cursor-candidate-v21.py",
    "engineer-build-cursor-candidate-v22.py",
    "tests-checks/focused-controller-authoring-proof-v1.json",
    "tests-checks/focused-control-v1-authoring-part1.txt",
    "tests-checks/focused-control-v1-authoring-part2.txt",
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.run(
        [GIT, "-c", "core.fsmonitor=false", "-c", "core.autocrlf=false",
         "-C", str(H), *args], check=True, capture_output=True, timeout=60,
        creationflags=subprocess.CREATE_NO_WINDOW).stdout


assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
assert not OUT.exists() and not COPY.exists()
assert git("rev-parse", "HEAD").decode().strip() == EXPECTED
assert not git("diff", "--cached", "--name-only", "-z")
receipt = json.loads((T / "tests-checks/focused-v22-first01-design-311-receipt.json").read_bytes())
for item in receipt["outputs"].values():
    path = Path(item["path"])
    assert path.is_relative_to(T)
    PINS[path.relative_to(T).as_posix()] = item["sha256"]
for name, pin in PINS.items():
    assert sha((T / name).read_bytes()) == pin, name
files = {T / name for name in (*PINS, *ADDITIONAL)}
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
    attributes.write_bytes(original_attributes + (
        "\n# Preserve issued v22 candidate and first-floor evidence bytes.\n"
        + "\n".join(rules) + "\n").encode())
    contents[".gitattributes"] = attributes.read_bytes()
changed = {}
for name, raw in contents.items():
    existing = subprocess.run(
        [GIT, "-C", str(H), "show", "HEAD:" + name], capture_output=True,
        timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
    if existing.returncode or existing.stdout != raw:
        changed[name] = raw
git("add", "--", *sorted(changed))
staged = set(git("diff", "--cached", "--name-only", "-z").decode().rstrip("\0").split("\0"))
assert staged == set(changed)
for name, raw in changed.items():
    assert git("cat-file", "blob", ":" + name) == raw, name
git("commit", "-m", "Retain v22 storage candidate and first release-floor result")
commit = git("rev-parse", "HEAD").decode().strip()
for name, raw in contents.items():
    assert git("cat-file", "blob", commit + ":" + name) == raw, name
    assert (H / name).read_bytes() == raw, name
remote = git("ls-remote", "origin", "refs/heads/main").decode().split()
if not remote or remote[0] != commit:
    git("push", "origin", "HEAD:refs/heads/main")
    remote = git("ls-remote", "origin", "refs/heads/main").decode().split()
assert remote[0] == commit
report = {
    "standing": "Engineering failure evidence only; no source integration or cold verdict.",
    "previous_commit": EXPECTED, "commit": commit, "remote_main_verified": True,
    "published_sha256": {name: sha(raw) for name, raw in sorted(contents.items())},
    "new_or_changed_paths": sorted(changed),
    "all_stored_blobs_match_issued_bytes": True, "new_crlf_exceptions": rules,
}
with OUT.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2)
    stream.write("\n")
print(json.dumps({"commit": commit, "changed_files": len(changed), "remote_verified": True}))
