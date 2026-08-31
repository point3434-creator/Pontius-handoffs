"""Publish completed engineering checkpoint only; no Pontius source integration."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

H = Path(r"D:\Pontius-handoffs")
T = H / "v0a-i01-c-authority"
GIT = r"C:\Program Files\Git\cmd\git.exe"
EXPECTED = "68ace766a6b1f6b54d5a9b023dec1f0243daff0a"
OUT = T / "coordinator-cost-class-checkpoint-publication01.json"
COPY = T / "coordinator-publish-cost-class-checkpoint-v1.py"
PINS = {
    "CURRENT.md": "3bef658b804a56dcf91e2d626dead32bdeea938c81ace1a24d454827a8365a6a",
    "coordinator-v22-depth-budget-verification-v1.json": "0c65680c640e4c35bca18d8b2472838bfb1ad41cfef5a7a0dd24e46418815613",
    "coordinator-v22-depth-budget-disposition-v1.md": "88a97afa135113e99f558a18affab2c0df2d2d4cf8c0cd55ea5aaf4cf6a690c8",
    "coordinator-class-extension-red-verification-v1.json": "e00ca0a8d01b1812420a1fb345c702b4650549fc1f3853cf5d3da130996bb5e0",
    "coordinator-class-extension-red-disposition-v1.md": "a656fb5b976f91ba909a3347bab54e124156e0efb7858f7238241f4a8a674823",
    "engineer-v22-two-case-storage-decision-v1.md": "8ac28ed870ecd2fcf5c516aa034357f7d634b14181501960fc6bc44f76b384b6",
    "engineer-radix-api-boundary-plan-v1.md": "6e37ce7ce7d768c157bd00490f4d0bc8f92753385bfa375b73bab610d2e87150",
    "engineer-lexical-cell-ownership-api-v1.md": "bf5cf20ac2174707e70eb73d73126a489d68b4c316467517aaf8b071a81b383b",
    "engineer-class-frame-api-plan-v1.md": "3d57a76a1224db8312fcb614b218c58084753172f1f75aeb10df722033d56536",
    "engineer-class-semantic-schedules-v1.md": "e540dd8c8e6d127363747b8548007ce0b45b3928927516ed3f93fbe2d0033307",
    "engineer-class-semantic-schedules-v2.md": "6f3c8c917f896cc1ffa352b054d4aeee73cb4a4dde85657c9da97a8996363913",
    "tests-checks/class-semantic-extension-cases-v1.json": "925ae5b9354377a5957f0c32c8bf5b58fea01612498b835abd6392f9cc87d268",
    "tests-checks/class-semantic-extension-control-v1.py": "71c4a91950a59589a39a8859c6a3ef00637db7fd346df1da2ff303e50f2b81c1",
    "tests-checks/class-semantic-extension-probe-v1.py": "ca88145516744909acba5010aa4aeeb85351b17df9379b46d15550f8829c009c",
    "engineer-depth-budget-probe-v1.py": "41ca38516e71d29bcb95869396c08fa177edd12a0f905a472080a05d1b18fb52",
    "engineer-depth-budget-probe-v2.py": "8db7415b97750e8880b25351be76b6fdf75d767a03a3a589d739113a73b6cae0",
    "tests-depth-budget-control-v1.py": "9df274065efc48c9bd31d208c0ac0a3d13bc6217bf3fee762ef06cf7d7a2e407",
    "tests-depth-budget-control-v2.py": "bbdc550c042fe62c8c19e838ffe35a9cabc09f22fdd4d941bdb0d9d0a41599a5",
    "tests-depth-budget-release-v1.md": "8f54e836f55b5fd0c887793891d7c923406507fa1f74d6b1914afdc2fe2f5bab",
    "tests-checks/depth-budget-controller-authoring-proof-v1.json": "32f8c2cb7d68435e56dad2012310fa98f411be3ce339b62496fba1dd05864a12",
}
RECEIPTS = {
    "tests-checks/depth-budget-v22-cost01-helper1050-311-receipt.json": "0a18f257eef1c3aa9d4113bd91e58694f7e7a3e2524f533cb55e97d880a71df2",
    "tests-checks/depth-budget-v22-cost02-helper1050-311-receipt.json": "7ebaa9657dbd47f91ecad3d5f20c18930a84b746d05feda356b8bc21247bcfe2",
    "tests-checks/depth-budget-v22-cost02-generator70-311-receipt.json": "bbb9b75f161f7d9a06f1295d5cf3ae5a62ba11f1dfe1e01f152fb9d246059f57",
    "tests-checks/class-extension-v19-red01-311-receipt.json": "88467325038d7d2395c28c291daa42014f562b66f961a8d7983d6dd02cb4c2f9",
    "tests-checks/class-extension-v19-red01-314-receipt.json": "e3b19f47b0b976fa22e4294dc39dda8422021aeceab8a8a03cd201591f2b0cd8",
}
ADDITIONAL = (
    "coordinator-v22-first-floor-publication01.json",
    "coordinator-verify-depth-budget-v22-v1.py",
    "coordinator-verify-class-extension-red-v1.py",
    "coordinator-navigation-v9.json",
    "coordinator-update-authority-navigation-v9.py",
    "engineer-depth-budget-probe-v1-static.json",
    "engineer-depth-budget-probe-v1-handoff.md",
    "engineer-depth-budget-probe-v1-from-chain32.diff",
    "engineer-depth-budget-probe-v2-from-v1.diff",
    "engineer-depth-budget-v2-static.json",
    "engineer-depth-budget-v2-handoff.md",
    "tests-depth-budget-control-v2-from-v1.diff",
    "tests-depth-budget-release-clarification-v1.md",
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.run([GIT, "-c", "core.fsmonitor=false", "-c", "core.autocrlf=false",
                           "-C", str(H), *args], check=True, capture_output=True,
                          timeout=60, creationflags=subprocess.CREATE_NO_WINDOW).stdout


assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
assert not OUT.exists() and not COPY.exists()
assert git("rev-parse", "HEAD").decode().strip() == EXPECTED
assert not git("diff", "--cached", "--name-only", "-z")
for name, pin in RECEIPTS.items():
    raw = (T / name).read_bytes()
    assert sha(raw) == pin
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
    attributes.write_bytes(original_attributes + (
        "\n# Preserve issued cost/class diagnostic checkpoint bytes.\n"
        + "\n".join(rules) + "\n").encode())
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
git("commit", "-m", "Retain C cost diagnostics and replicated class capture findings")
commit = git("rev-parse", "HEAD").decode().strip()
for name, raw in contents.items():
    assert git("cat-file", "blob", commit + ":" + name) == raw, name
    assert (H / name).read_bytes() == raw, name
remote = git("ls-remote", "origin", "refs/heads/main").decode().split()
if not remote or remote[0] != commit:
    git("push", "origin", "HEAD:refs/heads/main")
    remote = git("ls-remote", "origin", "refs/heads/main").decode().split()
assert remote[0] == commit
report = {"standing": "Engineering findings/designs only; no source integration or cold verdict.",
          "previous_commit": EXPECTED, "commit": commit, "remote_main_verified": True,
          "published_sha256": {name: sha(raw) for name, raw in sorted(contents.items())},
          "new_or_changed_paths": sorted(changed), "all_stored_blobs_match_issued_bytes": True,
          "new_crlf_exceptions": rules}
with OUT.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2)
    stream.write("\n")
print(json.dumps({"commit": commit, "changed_files": len(changed), "remote_verified": True}))
