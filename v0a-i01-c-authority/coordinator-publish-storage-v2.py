"""Publish only completed storage-prototype evidence, never the live C port."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

H = Path(r"D:\Pontius-handoffs")
T = H / "v0a-i01-c-authority"
GIT = r"C:\Program Files\Git\cmd\git.exe"
EXPECTED = "ade1a7faa6f0efe5fd2fa744b874495b72dff55b"
LABEL = "storage-prototype-v2-oracle-v2-01"
OUT = T / "coordinator-storage-publication02.json"
COPY = T / "coordinator-publish-storage-v2.py"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*arguments):
    return subprocess.run([GIT, "-C", str(H), *arguments], check=True,
                          capture_output=True).stdout


assert sys.version_info[:3] == (3, 11, 15)
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
assert sys.dont_write_bytecode and not sys.flags.optimize
assert not OUT.exists() and not COPY.exists()
assert git("rev-parse", "HEAD").decode().strip() == EXPECTED
assert not git("diff", "--cached", "--name-only", "-z")
pins = {
    "coordinator-storage-verification-v1.json": "e77700c7f8ee03cfb7c16cc590ba561454956e6e7410a692542e6091975ef381",
    "coordinator-storage-integration-disposition-v1.md": "b3e717986f6f8a554e7b1bc544b763e50692ef9cfbc71ea94600ec1e23322aa2",
    "coordinator-storage-trial-history-v1.md": "cc2ba7d41d71bfef89d0eb21bd8d1e0a471f3fdae43465856264d07b8cfb631c",
    "engineer-storage-prototype-v2.py": "22cc3966435fd4e6e0cecbcbb242275e72d34b36c835b4e960c7c712613822ff",
    "engineer-storage-control-v2.py": "8a1d17448ad7a7298a5fda5a78261c04ad4567996b3f474b8853b915a06b400e",
    "engineer-storage-run-config-v1.json": "07351a2ba5b508c43a5eee009a9be5365b18e1a6d01cb156ce9f55402786d316",
    "engineer-storage-mapping-compatibility-v1.md": "9617c9b5d9d502a707e124483586b59488f7b1ec670d3f375f0615132a762180",
    "engineer-object-order-assessment-v1.md": "748e19189c35865cf9d486c48557a7ed60d6c60c2893815f2b0c4961b779033d",
    "tests-checks/storage-oracle-v2.py": "6a58ef82832d53510f7d44d58cf5a8fa3764f8be5f2c28dcb7e555a83c72cfba",
    "tests-checks/storage-oracle-cases-v2.json": "3bd5678da334fb551c2f179906e8b4d2cf7a0b0e7a3779e0fad2fb4b4a9c548f",
    "tests-checks/storage-oracle-plan-v2.md": "0b3d2b56616fe8cee21528330825678c13b57f79856537dc5e584c0226ecc4b8",
    "tests-checks/storage-oracle-report-v1.md": "251501b84396d2300dfdcba4b680fb41652fd2b70ffbe42983be5558a4ef17cf",
    "tests-checks/storage-oracle-proof-v1.json": "ee6509c1c036a154d3fe134ba57c90b63dc3da97ab2c5d15d671f18f600704e3",
    "CURRENT.md": "ccd28b1e953bfe4d8d2a6b24ae9fc7233ced3a415dd90edd042d74a4bb61133b",
}
for relative, digest in pins.items():
    assert sha((T / relative).read_bytes()) == digest, relative
files = [T / relative for relative in pins]
files.extend(T / relative for relative in (
    "coordinator-storage-publication01.json", "coordinator-verify-storage-prototype-v1.py",
    "engineer-storage-api-v1.md", "engineer-storage-api-clarification-v1.md",
    "engineer-storage-exact-string-v1.md", "engineer-storage-prototype-v1.py",
    "engineer-storage-prototype-v3.py", "engineer-storage-control-v1.py",
    "tests-checks/storage-oracle-v1.py", "tests-checks/storage-oracle-cases-v1.json",
    "tests-checks/storage-oracle-report-v1.md", "tests-checks/storage-oracle-proof-v1.json",
))
files.extend(T / "tests-checks" / f"storage-casepart-v2-{i}.txt" for i in range(3))
for slot in ("311", "314"):
    for seed in ("0", "1", "17"):
        files.extend(T / "engineer-checks" / f"{LABEL}-{slot}-seed{seed}{suffix}"
                     for suffix in ("-setup.json", "-receipt.json", ".txt"))
assert all(path.is_file() and path.resolve().is_relative_to(H.resolve()) for path in files)
with COPY.open("xb") as stream:
    stream.write(Path(__file__).read_bytes())
files.append(COPY)
contents = {path.relative_to(H).as_posix(): path.read_bytes() for path in sorted(set(files))}
attributes = H / ".gitattributes"
old_attributes = attributes.read_bytes()
assert git("show", "HEAD:.gitattributes") == old_attributes
rules = [f"{name} -text" for name, raw in contents.items()
         if b"\r\n" in raw and f"{name} -text" not in old_attributes.decode().splitlines()]
if rules:
    assert old_attributes.endswith(b"\n")
    attributes.write_bytes(old_attributes + (
        "\n# Retain issued storage-prototype artifacts byte-for-byte.\n"
        + "\n".join(rules) + "\n").encode())
    contents[".gitattributes"] = attributes.read_bytes()
git("add", "--", *sorted(contents))
staged = set(git("diff", "--cached", "--name-only", "-z").decode().rstrip("\0").split("\0"))
assert staged == set(contents), (staged, set(contents))
for name, raw in contents.items():
    assert git("cat-file", "blob", ":" + name) == raw, name
git("commit", "-m", "Record C storage-prototype verification and bounded port")
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
    "standing": "Completed prototype engineering evidence only; no main-source integration or cold verdict.",
    "previous_commit": EXPECTED, "commit": commit, "remote_main_verified": True,
    "published_sha256": {name: sha(raw) for name, raw in sorted(contents.items())},
    "all_stored_blobs_match_issued_bytes": True, "new_crlf_exceptions": rules,
}
with OUT.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(receipt, stream, indent=2)
    stream.write("\n")
print(json.dumps({"commit": commit, "published_files": len(contents), "remote_verified": True}))
