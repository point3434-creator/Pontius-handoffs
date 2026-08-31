"""Publish completed engineering evidence only, preserving every issued byte."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

H = Path(r"D:\Pontius-handoffs")
T = H / "v0a-i01-c-authority"
GIT = r"C:\Program Files\Git\cmd\git.exe"
EXPECTED = "f8a2cf4c77f1474690bbcb4a40e315cfed78f26f"
OUT = T / "coordinator-radix-class-checkpoint-publication01.json"
COPY = T / "coordinator-publish-radix-class-checkpoint-v1.py"
PINS = {
    "CURRENT.md": "59d53d2e83188a9c3d9d2a48dce12ef5695a30d588393e2aff7a0eaaba0bee5e",
    "engineer-indexed-storage-config-v1.json": "60485a4ea41ab146e89c4da4fb0bfd8cfad98c0908322025e62512dfd1ce97aa",
    "coordinator-indexed-verification-allsix01.json": "3e3af131f3c4839bb26e993f7d188f0c92d129f129b3edbc392b1a04f1f7151b",
    "coordinator-indexed-prototype-result-disposition-v1.md": "bb293b7112f7d833aff1b8c72d134ae53d998bce5930c41a393dd930ff943d1e",
    "coordinator-radix-prototype-inspection-v1.json": "1bee12ba553d3b4a42155a2c67a19471601ef0dee159093312d8951394d97bd7",
    "coordinator-indexed-oracle-inspection-v1.json": "eb069f08af0395a8e913e8a5ae7cc1e842fb1b8aa972879ffde31d162beef127",
    "engineer-indexed-storage-control-v4-review-codex-v1.md": "20cfa26f732abdf31effe4e9ceeb24cb8b9cae88690ccb861ea9e1310368078c",
    "coordinator-class-name-boundary-red-verification-v1.json": "74f243ebf84c11a38ecb66b5f3ff61f4e5a36eb2c9166bb91ce155c18642ff22",
    "coordinator-class-name-boundary-red-disposition-v1.md": "3e3064b5ac177fd82f8223dd4834f6e64b0961bdf2b543308cb81d4029ba0e27",
    "coordinator-class-semantic-v23-disposition-v1.md": "d5b1d838a1d5bbbf591dff8974c7c8d7fb8e0a033477573b9c8143d92d1dd72a",
    "tests-checks/class-comprehension-boundary-cases-v1.json": "9df895eb5bd645a5e4ef05be0f7c0a3db76df458ca023bbfbd36407ee3496b71",
    "tests-checks/class-comprehension-boundary-spec-v1.md": "8a4220e2a9f41a4171c585f6f5fa36ace1e22fb38e8849f96cd29a490facea82",
    "tests-checks/class-comprehension-boundary-static-proof-v1.json": "f54e0635608a98b97214a190d4cc2c09856d9f39b3ae514ef78d36a7931d1fca",
    "tests-checks/indexed-storage-oracles-release-v1.md": "165cbaee7cada2206fef8da4e2a43f45ce6b9e7d39c665250c36e597b53ed155",
    "tests-checks/indexed-storage-oracles-static-proof-v2.json": "8fddb6ca3fcaf432175aace69d1f7a3b7d8e4e1c7949ec3994ba53662ebed939",
}
RECEIPTS = {
    "engineer-checks/indexed-radix-v1-first01-311-seed0-receipt.json": "adb85019461361a35ab724587c9bc63a19b1a27ffe77e0d3cf0a719f87c822fc",
    "engineer-checks/indexed-radix-v1-first01-311-seed1-receipt.json": "5d241a6c5844b89a618b81888a7f67ed26c62d691b4868fe7b92f9723ebcff9b",
    "engineer-checks/indexed-radix-v1-first01-311-seed17-receipt.json": "de00f5298fb29e660b2be2437811c3415fc4ab9b0f45917ecb095b1ca3236a23",
    "engineer-checks/indexed-radix-v1-first01-314-seed0-receipt.json": "c35143c7c68e72600c5f7cfe47a057ae11ea0c3b1b8cc81b3d0b2bbb78b5c948",
    "engineer-checks/indexed-radix-v1-first01-314-seed1-receipt.json": "ab0b93a8e1d7961613eceb6ce98ee03fe795c92e90f174007b174fbe9a763f63",
    "engineer-checks/indexed-radix-v1-first01-314-seed17-receipt.json": "cbc8b500b621f30316c64eee25fdefabee554ba2359b6f70f25af63c48c0f25a",
    "tests-checks/class-name-boundary-v19-red01-311-receipt.json": "5285ffaf0ad76c3cf0170e5dc101da343ead3f750dc3a027378ea358dc721cf5",
    "tests-checks/class-name-boundary-v19-red01-314-receipt.json": "3916d1258069dd0191af44dd2fd38847f12d951aab819339ac101e5ddf62b829",
}
ADDITIONAL = [
    "coordinator-cost-class-checkpoint-publication01.json",
    "coordinator-navigation-v10.json", "coordinator-update-authority-navigation-v10.py",
    "coordinator-radix-prototype-disposition-v1.md", "coordinator-authorize-radix-prototype-v1.py",
    "coordinator-inspect-radix-prototype-v1.py", "coordinator-configure-indexed-prototype-v1.py",
    "coordinator-indexed-prototype-first-dispatch-v1.md",
    "coordinator-verify-class-name-boundary-red-v1.py", "coordinator-authorize-class-semantic-v23.py",
    "engineer-name-radix-ownership-v1.md", "engineer-name-radix-static-v1.json",
    "engineer-name-radix-prototype-v1-from-cursor.diff", "engineer-radix-metering-clarification-v1.md",
    "engineer-class-name-boundary-addendum-v1.md", "engineer-class-name-boundary-addendum-v2.md",
    "tests-checks/class-name-boundary-cases-v1.json", "tests-checks/class-name-boundary-control-v1.py",
    "tests-checks/class-name-boundary-probe-v1.py", "tests-checks/class-name-boundary-control-plan-v1.md",
    "tests-checks/class-name-boundary-control-static-proof-v1.json",
    "tests-checks/class-name-boundary-control-v1-from-class12-v2.diff",
    "tests-checks/class-name-boundary-probe-v1-from-class12-v2.diff",
    "tests-checks/class-semantic-extension-control-v2.py", "tests-checks/class-semantic-extension-probe-v2.py",
    "tests-checks/class-semantic-extension-control-v2-from-v1.diff",
    "tests-checks/class-semantic-extension-probe-v2-from-v1.diff",
    "tests-checks/class-semantic-extension-v2-authoring.json", "tests-checks/class-semantic-extension-v2-review-codex-v1.md",
    "tests-checks/cursor-oracle-v2-from-v1.diff", "tests-checks/indexed-storage-extension-oracle-v1.py",
    "tests-checks/indexed-storage-extension-oracle-v1-from-empty.diff",
    "tests-checks/indexed-storage-extension-oracle-v2-from-empty.diff",
    "tests-checks/indexed-storage-extension-oracle-v2-from-v1.diff",
    "tests-checks/indexed-storage-p-boundary-clarification-v1.md",
    "tests-checks/class-comprehension-boundary-static-recipe-v1.txt",
    "tests-checks/class-comprehension-boundary-static-v1-receipt.json",
    "tests-checks/class-comprehension-boundary-static-v1.stdout.txt",
    "tests-checks/class-comprehension-boundary-static-v1.stderr.txt",
]
for version in (1, 2, 3, 4):
    ADDITIONAL += [f"engineer-indexed-storage-control-v{version}.py",
                   f"coordinator-build-indexed-storage-control-v{version}.py",
                   f"engineer-checks/indexed-control-authoring-v{version}.json"]
    origin = "cursor-v3" if version == 1 else f"v{version - 1}"
    ADDITIONAL.append(f"engineer-indexed-storage-control-v{version}-from-{origin}.diff")
for label in ("first01", "floors01", "allsix01"):
    ADDITIONAL += [f"coordinator-indexed-verification-{label}.json", f"coordinator-verify-indexed-prototype-{label}.py"]
for version in (1, 2):
    for suffix in (f"static-control-v{version}.py", f"static-proof-v{version}.json",
                   f"static-v{version}-receipt.json", f"static-v{version}.stderr.txt"):
        ADDITIONAL.append("tests-checks/indexed-storage-oracles-" + suffix)
ADDITIONAL += ["tests-checks/indexed-storage-oracles-static-v2.stdout.txt"]
ADDITIONAL += [f"tests-checks/indexed-storage-oracle-source-part{i}-v1.txt" for i in (1, 2, 3)]
ADDITIONAL += [f"engineer-name-radix-source-v1-part-{i:02d}.txt" for i in range(1, 7)]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def git(*args):
    return subprocess.run([GIT, "-c", "core.fsmonitor=false", "-c", "core.autocrlf=false", "-C", str(H), *args],
        check=True, capture_output=True, timeout=60, creationflags=subprocess.CREATE_NO_WINDOW).stdout

assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
assert not OUT.exists() and not COPY.exists()
assert git("rev-parse", "HEAD").decode().strip() == EXPECTED
assert not git("diff", "--cached", "--name-only", "-z")
config_raw = (T / "engineer-indexed-storage-config-v1.json").read_bytes()
assert sha(config_raw) == PINS["engineer-indexed-storage-config-v1.json"]
for entry in json.loads(config_raw).values():
    if type(entry) is dict and set(entry) == {"path", "sha256"}:
        PINS[entry["path"]] = entry["sha256"]
for name, pin in RECEIPTS.items():
    raw = (T / name).read_bytes()
    assert sha(raw) == pin, name
    PINS[name] = pin
    for item in json.loads(raw)["outputs"].values():
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
    attributes.write_bytes(original_attributes + ("\n# Preserve issued radix/class checkpoint bytes.\n" + "\n".join(rules) + "\n").encode())
    contents[".gitattributes"] = attributes.read_bytes()
changed = {}
for name, raw in contents.items():
    existing = subprocess.run([GIT, "-C", str(H), "show", "HEAD:" + name], capture_output=True,
                              timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
    if existing.returncode or existing.stdout != raw:
        changed[name] = raw
git("add", "--", *sorted(changed))
staged = set(git("diff", "--cached", "--name-only", "-z").decode().rstrip("\0").split("\0"))
assert staged == set(changed)
for name, raw in changed.items():
    assert git("cat-file", "blob", ":" + name) == raw, name
git("commit", "-m", "Retain verified radix storage trials and class repair boundaries")
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
          "published_sha256": {name: sha(raw) for name, raw in sorted(contents.items())},
          "new_or_changed_paths": sorted(changed), "all_stored_blobs_match_issued_bytes": True,
          "new_crlf_exceptions": rules}
with OUT.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2)
    stream.write("\n")
print(json.dumps({"commit": commit, "changed_files": len(changed), "remote_verified": True}))
