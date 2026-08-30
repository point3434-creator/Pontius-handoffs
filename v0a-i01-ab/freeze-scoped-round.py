"""Freeze an explicit path set without changing the worktree HEAD or real index."""
import hashlib, json, os, subprocess, sys, uuid
from pathlib import Path
G = r"C:\Program Files\Git\cmd\git.exe"
ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-ab")
work, base, round_id, *paths = sys.argv[1:]
w = Path(work)
assert round_id.startswith("r") and len(round_id) == 4 and round_id[1:].isdigit()
assert paths and len(set(paths)) == len(paths)
assert all(not p.startswith("/") and ".." not in p.split("/") for p in paths)
packet = ROOT / round_id
assert not packet.exists(), "round already exists"
def git(*args, env=None, data=None):
    return subprocess.run([G, "-C", str(w), *args], env=env, input=data,
                          capture_output=True, check=True).stdout
head = git("rev-parse", "HEAD").decode().strip()
assert head == base
index_path = Path(git("rev-parse", "--path-format=absolute", "--git-path", "index").decode().strip())
index_before = index_path.read_bytes() if index_path.exists() else None
working = {p: hashlib.sha256((w / p).read_bytes()).hexdigest() for p in paths}
index = w / ("freeze-index-" + uuid.uuid4().hex)
assert not index.exists()
env = dict(os.environ, GIT_INDEX_FILE=str(index))
try:
    git("read-tree", base, env=env)
    git("add", "--", *paths, env=env)
    tree = git("write-tree", env=env).decode().strip()
    commit = git("commit-tree", tree, "-p", base, env=env,
                 data=("Freeze v0a-i01-ab/" + round_id + " for review\n").encode()).decode().strip()
finally:
    if index.exists():
        assert index.parent == w and index.read_bytes()[:4] == b"DIRC"
        index.unlink()
assert git("rev-parse", "HEAD").decode().strip() == head
assert (index_path.read_bytes() if index_path.exists() else None) == index_before
fields = git("diff-tree", "--no-renames", "-r", "-z", "--no-commit-id",
             "--name-status", base, commit).decode("utf-8").split("\0")
rows = []
changed = []
for i in range(0, len(fields)-1, 2):
    if not fields[i]: break
    status, path = fields[i], fields[i+1]
    assert path in paths, path
    digest = ("0" * 64 if status == "D" else
              hashlib.sha256(git("cat-file", "blob", commit + ":" + path)).hexdigest())
    rows.append((digest + "  " + path + "\n").encode())
    changed.append(path)
assert set(changed) == set(paths), (changed, paths)
manifest = b"".join(sorted(rows))
ref = "refs/heads/review/v0a-i01-ab/" + round_id
git("update-ref", ref, commit, "0" * 40)
git("push", "origin", ref)
remote = git("ls-remote", "origin", ref).decode().split()
assert remote[0] == commit
candidate = dict(schema_version="pontius-handoff-candidate-v1", task_id="v0a-i01-ab",
                 round=round_id, ref=ref, commit=commit, base=base, tree=tree,
                 manifest_sha256=hashlib.sha256(manifest).hexdigest(), date="2026-08-30")
packet.mkdir()
(packet / "checks").mkdir()
(packet / "reviews").mkdir()
for name, data in (("manifest.sha256", manifest),
                   ("candidate.json", (json.dumps(candidate, indent=2) + "\n").encode())):
    with (packet / name).open("xb") as f: f.write(data)
verification = dict(candidate=candidate, working_sha256=working,
                    index_unchanged=True, worktree_head_unchanged=True,
                    manifest_from_git_blobs=True, remote_ref_verified=True)
with (packet / "checks" / "freeze-verification.json").open("xb") as f:
    f.write((json.dumps(verification, indent=2) + "\n").encode())
print(json.dumps(candidate, indent=2))
