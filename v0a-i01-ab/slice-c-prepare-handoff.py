from pathlib import Path
import hashlib
import json
import subprocess

root = Path("D:/Pontius-worktrees/codex-v0a-i01-c-integration")
packet = Path("D:/Pontius-handoffs/v0a-i01-ab")
git = "C:/Program Files/Git/cmd/git.exe"
capture = json.loads((packet / "slice-c-replay-capture.json").read_bytes())
rows = []
result = {"base":capture["base"], "worktree":str(root), "files":[], "source_unchanged":True}
for entry in capture["files"]:
    relative = entry["path"]
    original = Path(capture["source"]) / relative
    assert hashlib.sha256(original.read_bytes()).hexdigest() == entry["sha256"], relative
    raw = (root / relative).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    rows.append(f"{digest}  {relative}\n")
    result["files"].append({"path":relative, "initial_sha256":entry["sha256"],
                            "final_sha256":digest, "changed_after_replay":digest != entry["sha256"]})
manifest = "".join(sorted(rows)).encode()
(packet / "slice-c-final-working-files.sha256").write_bytes(manifest)
result["working_rows_sha256"] = hashlib.sha256(manifest).hexdigest()
tracked = subprocess.run([git, "-C", str(root), "diff", "--binary", "HEAD", "--",
                          *(entry["path"] for entry in capture["files"])],
                         capture_output=True, check=True).stdout
added = subprocess.run([git, "diff", "--no-index", "--binary", "--",
                        "/dev/null", "tests/test_v0a_boundaries.py"],
                       cwd=root, capture_output=True)
assert added.returncode == 1, added.stderr.decode(errors="replace")
patch = tracked + added.stdout
(packet / "slice-c-integration.patch").write_bytes(patch)
result["patch_sha256"] = hashlib.sha256(patch).hexdigest()
result["patch_bytes"] = len(patch)
result["governance_regenerated"] = False
(packet / "slice-c-final-working-identity.json").write_text(
    json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(result, indent=2))
