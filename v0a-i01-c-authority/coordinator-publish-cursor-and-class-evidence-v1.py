"""Publish completed engineering evidence to H only; no source integration."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

H = Path(r"D:\Pontius-handoffs")
T = H / "v0a-i01-c-authority"
GIT = r"C:\Program Files\Git\cmd\git.exe"
EXPECTED = "62ad2f1e8e331cb2fdfdb9e2fdae0c485ecefde8"
OUT = T / "coordinator-cursor-class-publication01.json"
COPY = T / "coordinator-publish-cursor-and-class-evidence-v1.py"
PINS = {
    "CURRENT.md": "3408f46d3a809ca4eed7fd7bc2dce0766cd32bbbf06d4ddeae8242a49d505dbe",
    "coordinator-cursor-verification-v1.json": "beea083a71bcbb9e32df5e11a01e9e17af2ca4238958fe27e55661cce24972aa",
    "coordinator-class-mechanism-verification-v1.json": "529fe91786c2b4f699d5476d0d0f6cf6e60594f464c23e01d7475bddcd06f6ee",
    "coordinator-class-adoption-finding-v1.md": "9c1368b7bd5a86970ffe17a21ae3b8707c61be20f6bf1c7bfd179cbd82e40e6d",
    "coordinator-name-cursor-prototype-disposition-v1.md": "973191b8b26c71132185d42203a720bdc5b28d4fd23fc1bc4b9c9ec4da46a7b7",
    "coordinator-name-cursor-candidate-disposition-v1.md": "8cabe43873bddfc7871ff671c96eec85fccfc29cf774dd3c748167fc9dabae21",
    "engineer-name-cursor-adapter-proposal-v1.md": "16e315f394baebf957350f33c90dd9cc8e96918817af4a0d64841f7b824116a2",
    "engineer-name-cursor-prototype-v1.py": "67acb279510924311266b985e15e95e53ae9d0a11d64a50d108f254a690deb2a",
    "engineer-name-cursor-prototype-v1-ownership.md": "4c98864b19327a2bd50f91bd56a55fe21b7429fafbec2df01cbab976b4de0f49",
    "engineer-checks/name-cursor-prototype-v1-static.json": "43574d05da2f728933e7b8c4f4334b89997899787790f1f95c5774e68c4495b2",
    "engineer-cursor-prototype-v1-config.json": "afb9d33f3ec5110e822a0a7e44710fbe025940985ecf82ce7ffc533c084ab958",
    "engineer-storage-control-v3.py": "882016384c6b9bc4e6a4d9d81e829dee9eb95120942650f63006fea8f0ad1cbf",
    "tests-checks/cursor-oracle-v1.py": "15a4741e2532a755fd45f01d4d999dd5d293846b8ae4e9d4e7abedf84c0a8d1e",
    "tests-checks/cursor-oracle-cases-v1.json": "ecddd020ffb2a0d85e624aeb7fb544f631b302839f9a5f3542c998b36c37ac61",
    "tests-checks/cursor-oracle-spec-v1.md": "29c0238aa24e0c6d4a9f3834d6f94b46c4bd6ed29f263f0c57511e1ee1b0bfd1",
    "tests-checks/cursor-oracle-release-v1.md": "e95e4a155e6e843c2f99ee66e5fbc4201c3a2624b790b00837fec2ce5628e943",
    "tests-checks/class-composition-mechanism-probe-v1.py": "4e2e0cb1f472a6cf7f0c38bd699f4fc54c084db29e5f903305e88f1358dbe83e",
    "tests-checks/class-composition-mechanism-control-v1.py": "67cf68877e9c3daffe980360cdb0ff3c41d06237374dd4aab1f7f6892562702c",
    "tests-checks/class-composition-mechanism-control-v2.py": "5dd1e6692f82d096a976ca248b45e313a93a97922331186e2cf3e462c2c37717",
    "tests-checks/scalar-class-composition-cases-v1.json": "50e88cedf77f902012237ccd88700c911fa8f3681c8dada380cca6c3142659ac",
    "engineer-class-composition-static-mechanism-v1.md": "3ab96beb2aec398145b312ae3f701d1952e674f78e6359438bebe35e76cd7144",
}


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
files = {T / name for name in PINS}
files.update(T / name for name in (
    "coordinator-v20-diagnostics-publication01.json",
    "coordinator-cursor-prototype-v1-source-review.json",
    "coordinator-release-cursor-prototype-v1.py",
    "coordinator-verify-cursor-prototype-v1.py",
    "coordinator-retain-class-adoption-finding-v1.py",
    "coordinator-verify-class-mechanism-v1.py",
    "coordinator-update-authority-navigation-v7.py",
    "coordinator-navigation-v7.json",
    "engineer-class-composition-control-schema-correction-v1.md",
    "tests-checks/cursor-oracle-proof-v1.json",
))
cursor = json.loads((T / "coordinator-cursor-verification-v1.json").read_bytes())
for result in cursor["slots"]:
    prefix = f"engineer-checks/cursor-prototype-v1-01-{result['slot']}-seed{result['seed']}"
    PINS[prefix + "-receipt.json"] = result["receipt_sha256"]
    PINS[prefix + ".txt"] = result["log_sha256"]
    files.update(T / (prefix + suffix) for suffix in
                 ("-receipt.json", "-setup.json", ".txt", ".stdout.txt", ".stderr.txt"))
mechanism = json.loads((T / "coordinator-class-mechanism-verification-v1.json").read_bytes())
for result in mechanism["results"]:
    prefix = f"tests-checks/class-composition-{result['scope']}-v19-mechanism01-{result['slot']}"
    PINS[prefix + "-receipt.json"] = result["receipt_sha256"]
    PINS[prefix + ".txt"] = result["log_sha256"]
    files.update(T / (prefix + suffix) for suffix in ("-receipt.json", "-setup.json", ".txt"))
for slot, pin in (
    ("311", "210890c5e24e2eb227a99fba0c5a859c131c53d77fa4cf41e6069d56275e001f"),
    ("314", "c094edd7cc9cebf3c684644f03a590e4ba22393f58ba9cbfbff51351ec6b849d"),
):
    prefix = f"tests-checks/storage-composition-storage-composition-v19-01-{slot}"
    PINS[prefix + "-receipt.json"] = pin
    r = json.loads((T / (prefix + "-receipt.json")).read_bytes())
    PINS[prefix + ".txt"] = r["log_sha256"]
    files.update(T / (prefix + suffix) for suffix in ("-receipt.json", "-setup.json", ".txt"))
for name, pin in PINS.items():
    assert sha((T / name).read_bytes()) == pin, name
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
        "\n# Preserve cursor prototype and class diagnostic issued bytes.\n"
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
git("commit", "-m", "Retain cursor prototype verification and class-flow diagnosis")
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
    "standing": "Completed engineering evidence only; no Pontius main integration or cold verdict.",
    "previous_commit": EXPECTED, "commit": commit, "remote_main_verified": True,
    "published_sha256": {name: sha(raw) for name, raw in sorted(contents.items())},
    "new_or_changed_paths": sorted(changed),
    "all_stored_blobs_match_issued_bytes": True, "new_crlf_exceptions": rules,
}
with OUT.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2)
    stream.write("\n")
print(json.dumps({"commit": commit, "changed_files": len(changed), "remote_verified": True}))
