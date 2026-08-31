"""Pinned bootstrap for exactly design53 or the released matrix192.

This file does not authorize execution. The root must review the controller,
candidate, population, and this bootstrap before dispatching one child.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import runpy
import stat
import sys
import traceback
import unittest

SCHEMA = "c-authority-focused-wrapper-v1"


def require(value, message):
    if not value:
        raise RuntimeError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def checked(path, regular=True):
    require(path.is_absolute() and ".." not in path.parts, "unsafe child path")
    for ancestor in (path, *path.parents):
        information = ancestor.lstat()
        require(not (getattr(information, "st_file_attributes", 0)
                     & stat.FILE_ATTRIBUTE_REPARSE_POINT), "child reparse path")
        if ancestor != path:
            require(stat.S_ISDIR(information.st_mode), "child path ancestor")
    if regular:
        require(stat.S_ISREG(path.lstat().st_mode), "child nonregular file")
    return path


def emit(record):
    print(json.dumps({"focused_control": record}, sort_keys=True), flush=True)


def flatten(suite):
    result = []
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            result.extend(flatten(item))
        else:
            require(isinstance(item, unittest.TestCase), "non-test suite member")
            result.append(item.id())
    return result


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *arguments, **keywords):
        super().__init__(*arguments, **keywords)
        self.started_ids = []
        self.completed_ids = []

    def startTest(self, test):
        self.started_ids.append(test.id())
        emit({"event": "test_started", "id": test.id()})
        super().startTest(test)

    def stopTest(self, test):
        super().stopTest(test)
        self.completed_ids.append(test.id())
        emit({"event": "test_finished", "id": test.id()})


def main():
    require(len(sys.argv) == 4, "bootstrap arguments")
    job_path = checked(Path(sys.argv[1]))
    job_raw = job_path.read_bytes()
    require(digest(job_raw) == sys.argv[2], "job hash mismatch")
    job = json.loads(job_raw)
    require(job["schema"] == "c-authority-focused-job-v1", "job schema")
    snapshot = checked(Path(job["snapshot"]), regular=False)
    require(snapshot.is_dir() and Path.cwd().resolve() == snapshot.resolve(),
            "payload must run from fresh snapshot")
    require(job_path == snapshot / job["payload"] / "job.json", "job location")
    require(Path(__file__).resolve() == snapshot / job["payload"] / "wrapper.py",
            "bootstrap location")
    require(sys.implementation.name == "cpython", "payload implementation")
    require(list(sys.version_info[:3]) == job["version"], "payload patch version")
    executable = checked(Path(job["executable"]))
    require(Path(sys.executable).resolve() == executable.resolve(),
            "payload executable")
    require(sys.flags.safe_path and sys.dont_write_bytecode
            and sys.flags.optimize == 0 and sys.flags.no_site == 0
            and sys.flags.isolated == 0 and sys.flags.ignore_environment == 0
            and sys.flags.no_user_site == 1, "payload isolation flags")
    require(dict(os.environ) == job["environment"], "payload environment mismatch")
    require(os.environ["PYTHONPATH"] == str(snapshot / "src"), "snapshot PYTHONPATH")
    require(os.environ["TEMP"] == job["temp"] and os.environ["TMP"] == job["temp"],
            "D-local temporary directory")
    checked(Path(job["temp"]), regular=False)
    checked(Path(os.environ["PONTIUS_GIT"]))
    require(not any(name == "pontius" or name.startswith("pontius.")
                    for name in sys.modules), "premature project import")
    manifest_path = checked(snapshot / job["payload"] / "manifest.json")
    manifest_raw = manifest_path.read_bytes()
    require(digest(manifest_raw) == sys.argv[3], "snapshot manifest hash")
    manifest = json.loads(manifest_raw)
    require(manifest["schema"] == "c-authority-focused-manifest-v1"
            and manifest["base_commit"] == job["base_commit"]
            and manifest["tracked_count"] == 1761, "snapshot manifest identity")
    names = manifest["files"]
    require(type(names) is dict and len(names) == job["manifest_count"],
            "full snapshot manifest population")
    for name, expected in names.items():
        relative = Path(name)
        require(not relative.is_absolute() and not relative.drive
                and ".." not in relative.parts, "manifest path")
        path = checked(snapshot / relative)
        require(path.is_relative_to(snapshot), "manifest path containment")
        require(digest(path.read_bytes()) == expected, "snapshot hash: " + name)
    require(names[job["test_relative"]] == job["tests_sha256"], "test hash binding")
    require(names["tools/generate_test_inventory.py"] == job["source_sha256"],
            "generator hash binding")
    require(names[job["payload"] + "/control.py"] == job["control_sha256"],
            "controller hash binding")
    require(names[job["payload"] + "/wrapper.py"] == job["wrapper_sha256"],
            "bootstrap hash binding")
    require(names[job["payload"] + "/population.json"] == job["population_sha256"],
            "population hash binding")
    population = json.loads((snapshot / job["payload"] / "population.json").read_bytes())
    require(population["schema"] == "c-authority-focused-population-v1"
            and population["base_commit"] == job["base_commit"]
            and population["tracked_count"] == 1761, "population identity")
    expected = population[job["kind"]]
    require(expected["tests_sha256"] == job["tests_sha256"], "selected tests")
    specification = importlib.util.find_spec("pontius")
    require(specification is not None and specification.origin is not None,
            "project import resolution")
    require(Path(specification.origin).resolve().is_relative_to(snapshot / "src"),
            "project resolves outside snapshot/src")
    identity = {
        "event": "identity", "schema": SCHEMA, "kind": job["kind"],
        "version": list(sys.version_info[:3]), "full_version": sys.version,
        "executable": str(Path(sys.executable).resolve()),
        "cwd": str(snapshot), "source_sha256": job["source_sha256"],
        "tests_sha256": job["tests_sha256"], "control_sha256": job["control_sha256"],
        "wrapper_sha256": job["wrapper_sha256"], "population_sha256": job["population_sha256"],
        "base_commit": job["base_commit"], "manifest_sha256": sys.argv[3],
        "manifest_count": len(names), "tracked_count": 1761,
        "safe_path": bool(sys.flags.safe_path), "dont_write_bytecode": sys.dont_write_bytecode,
        "optimize": sys.flags.optimize, "no_site": sys.flags.no_site,
        "no_user_site": sys.flags.no_user_site, "isolated": sys.flags.isolated,
        "ignore_environment": sys.flags.ignore_environment,
        "project_origin": specification.origin,
    }
    emit(identity)
    namespace = runpy.run_path(str(snapshot / job["test_relative"]),
                              run_name="focused_frozen_tests")
    test_class = namespace[expected["class_name"]]
    require(isinstance(test_class, type) and issubclass(test_class, unittest.TestCase),
            "selected unittest class")
    loader = unittest.TestLoader()
    method_names = loader.getTestCaseNames(test_class)
    require(method_names == expected["methods"], "exact unittest method population")
    require(len(method_names) == expected["planned_methods"], "unittest method count")
    suite = loader.loadTestsFromTestCase(test_class)
    planned_ids = ["focused_frozen_tests." + expected["class_name"] + "." + name
                   for name in expected["methods"]]
    require(not loader.errors and flatten(suite) == planned_ids, "loaded suite population")
    emit({"event": "population", "kind": job["kind"],
          "planned_methods": expected["planned_methods"], "ids": planned_ids})
    result = unittest.TextTestRunner(
        verbosity=2, stream=sys.stderr, resultclass=RecordingResult,
        failfast=False, buffer=False,
    ).run(suite)
    complete = (result.testsRun == expected["planned_methods"]
                and result.started_ids == planned_ids
                and result.completed_ids == planned_ids)
    summary = {
        "event": "unittest_summary", "kind": job["kind"],
        "planned_methods": expected["planned_methods"], "tests_run": result.testsRun,
        "started_ids": result.started_ids, "completed_ids": result.completed_ids,
        "complete_population": complete, "successful": result.wasSuccessful(),
        "failures": [test.id() for test, _ in result.failures],
        "errors": [test.id() for test, _ in result.errors],
        "skips": [test.id() for test, _ in result.skipped],
        "expected_failures": [test.id() for test, _ in result.expectedFailures],
        "unexpected_successes": [test.id() for test in result.unexpectedSuccesses],
    }
    emit(summary)
    if not complete:
        return 2
    if result.skipped or result.expectedFailures or result.unexpectedSuccesses:
        return 1
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    try:
        status = main()
    except BaseException as error:
        if isinstance(error, KeyboardInterrupt):
            raise
        emit({"event": "bootstrap_error", "type": type(error).__name__,
              "message": str(error)})
        traceback.print_exc()
        status = 2
    raise SystemExit(status)
