"""The unchanged 17-target CPU wall, only after two bound CLEAN reviews."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import uuid

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-ab")
spec = importlib.util.spec_from_file_location("abc_snapshot_v2", ROOT / "snapshot-run-abc-v2.py")
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
CANDIDATE_KEYS = {"schema_version", "task_id", "round", "ref", "commit", "base",
                  "tree", "manifest_sha256", "date"}


def candidate_shape(candidate, round_id):
    h.require(type(candidate) is dict and set(candidate) == CANDIDATE_KEYS, "candidate schema")
    h.require(candidate["schema_version"] == "pontius-handoff-candidate-v1", "candidate version")
    h.require(candidate["task_id"] == ROOT.name and candidate["round"] == round_id,
              "candidate task/round mismatch")
    h.require(all(h.is_digest(candidate[field], 40) for field in ("commit", "base", "tree"))
              and h.is_digest(candidate["manifest_sha256"]), "candidate digests")
    expected_ref = "review/" + ROOT.name + "/" + round_id
    h.require(candidate["ref"] in (expected_ref, "refs/heads/" + expected_ref), "candidate ref")
    h.require(type(candidate["date"]) is str, "candidate date type")


def readiness_shape(ready, candidate):
    h.require(type(ready) is dict and set(ready) ==
              {"schema_version", "candidate", "manifest", "reviews"}, "readiness schema")
    h.require(ready["schema_version"] == "pontius-abc-broader-readiness-v2", "readiness version")
    h.require(ready["candidate"] == candidate["commit"]
              and ready["manifest"] == candidate["manifest_sha256"], "readiness candidate mismatch")
    reviews = ready["reviews"]
    h.require(type(reviews) is list and len(reviews) == 2, "exactly two reports required")
    for review in reviews:
        h.require(type(review) is dict and set(review) == {"reviewer_id", "path", "sha256"},
                  "review entry schema")
        h.require(type(review["reviewer_id"]) is str and
                  re.fullmatch("[A-Za-z0-9][A-Za-z0-9._/-]{0,100}", review["reviewer_id"]),
                  "invalid reviewer identity")
        h.require(type(review["path"]) is str and
                  re.fullmatch(r"reviews/[A-Za-z0-9][A-Za-z0-9._-]*\.md", review["path"]),
                  "review must be a direct packet reviews file")
        h.require(h.is_digest(review["sha256"]), "invalid report digest")
    for field in ("reviewer_id", "path", "sha256"):
        h.require(len({review[field] for review in reviews}) == 2, "duplicate review " + field)


def review_fields(raw):
    fields = {}
    labels = {"reviewer id", "candidate commit", "manifest sha-256", "defect verdict"}
    for line in raw.decode("utf-8").splitlines():
        clean = line.replace("**", "").replace("__", "").replace(chr(96), "").strip()
        clean = clean.lstrip("#-* ").strip()
        name, separator, value = clean.partition(":")
        name = name.strip().lower()
        if separator and name in labels:
            h.require(name not in fields, "duplicate labelled report field: " + name)
            fields[name] = value.strip()
    h.require(set(fields) == labels, "missing labelled report identity/verdict")
    return fields


def validate_reports(packet, ready, candidate):
    for review in ready["reviews"]:
        raw = h.checked_path(packet / review["path"]).read_bytes()
        h.require(h.digest_bytes(raw) == review["sha256"], "report digest mismatch")
        fields = review_fields(raw)
        h.require(fields == {"reviewer id": review["reviewer_id"],
                             "candidate commit": candidate["commit"],
                             "manifest sha-256": candidate["manifest_sha256"],
                             "defect verdict": "CLEAN"}, "report is not bound CLEAN")


def verify_manifest(packet, candidate, temporary):
    def git(*args):
        return h.git_bytes(h.REPOSITORY, temporary, *args)
    commit = candidate["commit"]
    h.require(git("rev-parse", "--verify", candidate["ref"] + "^{commit}").decode().strip()
              == commit, "review ref changed")
    h.require(git("rev-parse", "--verify", commit + "^").decode().strip()
              == candidate["base"], "candidate parent mismatch")
    h.require(git("rev-parse", "--verify", commit + "^{tree}").decode().strip()
              == candidate["tree"], "candidate tree mismatch")
    changed = git("diff-tree", "-r", "--no-renames", "--no-commit-id", "--name-status",
                  "-z", candidate["base"], commit).decode("utf-8").split("\0")
    h.require(changed[-1] == "" and len(changed) % 2 == 1, "malformed changed-path list")
    rows, paths = [], []
    for index in range(0, len(changed) - 1, 2):
        status, path = changed[index:index + 2]
        h.require(status in {"A", "M", "T", "D"} and path in h.PATHS, "candidate outside 17 paths")
        h.require(path not in paths, "duplicate changed path")
        paths.append(path)
        value = "0" * 64 if status == "D" else h.digest_bytes(git("cat-file", "blob", commit + ":" + path))
        rows.append((value + "  " + path + "\n").encode("utf-8"))
    h.require(bool(rows), "empty candidate")
    manifest = h.checked_path(packet / "manifest.sha256").read_bytes()
    h.require(manifest == b"".join(sorted(rows)), "manifest differs from frozen blob rows")
    h.require(h.digest_bytes(manifest) == candidate["manifest_sha256"], "manifest digest mismatch")


def main(argv):
    h.require_control_runtime()
    h.require(len(argv) == 1 and re.fullmatch("r[0-9]{3}", argv[0]), "expected rNNN")
    round_id = argv[0]
    packet = h.checked_path(ROOT / round_id, directory=True)
    h.checked_path(packet / "checks", directory=True)
    candidate_path = packet / "candidate.json"
    ready_path = packet / "checks/broader-gate-readiness-v2.json"
    candidate = h.json_bytes(h.checked_path(candidate_path).read_bytes())
    ready = h.json_bytes(h.checked_path(ready_path).read_bytes())
    candidate_shape(candidate, round_id)
    readiness_shape(ready, candidate)
    validate_reports(packet, ready, candidate)
    pins = {str(path): h.digest(path) for path in
            (candidate_path, packet / "manifest.sha256", ready_path)}
    pins.update({str(packet / item["path"]): item["sha256"] for item in ready["reviews"]})
    scripts = h.harness_hashes()
    result_path = packet / "checks/broader-gate-results-v2.json"
    h.require(not result_path.exists(), "broader results already exist")
    for slot in h.SLOTS:
        label = "acceptance-" + round_id + "-v2-" + slot
        h.require(not (ROOT / (label + "-snapshot-v2.json")).exists(), "slot already prepared")
        for name, _, _ in h.TARGETS:
            stem = "acceptance-" + round_id + "-v2-" + name + "-" + slot
            for suffix in (".txt", "-receipt.json"):
                h.require(not (ROOT / "abc-checks" / (stem + suffix)).exists(), "run output exists")
    h.checked_path(h.SNAPSHOTS, directory=True)
    temporary = h.SNAPSHOTS / ("abc-v2-preflight-" + round_id + "-" + uuid.uuid4().hex)
    temporary.mkdir()
    verify_manifest(packet, candidate, temporary)

    def unchanged_inputs():
        h.require(h.harness_hashes() == scripts, "harness changed during wall")
        for path, expected in pins.items():
            h.require(h.digest(path) == expected, "frozen input changed: " + path)

    results = []
    floor = h.SLOTS["311"][0]
    for slot in ("311", "314"):
        unchanged_inputs()
        label = "acceptance-" + round_id + "-v2-" + slot
        command = [floor, "-I", "-S", "-B", "-P", str(ROOT / "snapshot-run-abc-v2.py"),
                   "prepare", label, candidate["commit"]]
        subprocess.run(command, cwd=ROOT, env=h.control_environment(temporary), check=True)
        metadata = ROOT / (label + "-snapshot-v2.json")
        metadata_sha = h.digest(metadata)
        setup = h.load_setup(metadata, metadata_sha)
        h.require(setup["base"] == setup["source"] == candidate["commit"], "wrong tested candidate")
        for name, target, args in h.TARGETS:
            unchanged_inputs()
            h.require(h.digest(metadata) == metadata_sha, "metadata changed before launch")
            runlabel = "acceptance-" + round_id + "-v2-" + name
            receipt_path = ROOT / "abc-checks" / (runlabel + "-" + slot + "-receipt.json")
            log_path = ROOT / "abc-checks" / (runlabel + "-" + slot + ".txt")
            print(slot + " " + target + " " + " ".join(args) + " START", flush=True)
            proc = subprocess.run(
                [floor, "-I", "-S", "-B", "-P", str(ROOT / "snapshot-run-abc-v2.py"),
                 "run", str(metadata), metadata_sha, slot, runlabel, target, *args],
                cwd=ROOT, env=h.control_environment(Path(setup["temporary"])), capture_output=True)
            h.require(receipt_path.is_file(), "runner produced no receipt: " +
                      proc.stderr.decode("utf-8", errors="replace")[-2000:])
            data = h.json_bytes(h.checked_path(receipt_path).read_bytes())
            exe, version = h.SLOTS[slot]
            expected_command = [exe, "-B", "-P", "-c", h.WRAPPER, exe, version, target, *args]
            expected = {"schema_version": "pontius-abc-receipt-v2", "label": runlabel,
                        "slot": slot, "base": candidate["commit"], "snapshot": setup["snapshot"],
                        "command": expected_command, "environment": setup["environment"],
                        "metadata_sha256": metadata_sha, "harness_sha256": scripts,
                        "log": str(log_path), "before_sha256": setup["stored_blob_sha256"],
                        "after_sha256": setup["stored_blob_sha256"],
                        "stored_blob_sha256": setup["stored_blob_sha256"], "changed_paths": []}
            h.require(all(data.get(key) == value for key, value in expected.items()),
                      "receipt does not bind requested execution")
            h.require(type(data.get("exit")) is int and data["exit"] == proc.returncode,
                      "receipt exit mismatch")
            h.require(h.digest(log_path) == data.get("sha256"), "payload log changed")
            h.require(h.digest(metadata) == metadata_sha, "metadata changed after launch")
            unchanged_inputs()
            results.append({"slot": slot, "target": target, "args": list(args),
                            "exit": proc.returncode, "receipt": str(receipt_path),
                            "receipt_sha256": h.digest(receipt_path), "metadata_sha256": metadata_sha})
            print(slot + " " + target + " EXIT " + str(proc.returncode), flush=True)
    unchanged_inputs()
    create_value = {"candidate": candidate, "scope":
                    "ADR0485 permitted CPU CI + five v0a suites; no guarded profile or scientific population",
                    "readiness_sha256": pins[str(ready_path)], "input_sha256": pins,
                    "harness_sha256": scripts, "control_runtime_identity": h.runtime_identity(),
                    "results": results}
    h.create(result_path, create_value)
    return 0 if all(item["exit"] == 0 for item in results) else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        print(json.dumps({"blocker": type(exc).__name__, "reason": str(exc)}), file=sys.stderr)
        sys.exit(2)

