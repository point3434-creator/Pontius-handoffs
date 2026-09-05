"""Read-only negative source-map checks for reviewer B."""
import importlib.util
from pathlib import Path

root = Path.cwd()
spec = importlib.util.spec_from_file_location('review_b_boundary', root / 'tools/check_stabilization_boundaries.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
sources = {p.relative_to(root).as_posix(): p.read_bytes() for p in (root / 'src/pontius').rglob('*.py')}
tool_sources = {p.relative_to(root).as_posix(): p.read_bytes() for p in (root / 'tools').rglob('*.py')}
baseline = checker._BASELINE.parse_baseline_bytes((root / checker.BASELINE_RELATIVE_PATH).read_bytes())
checker.authenticate_approved_baseline(baseline)
for path in ['src/pontius/blueprint_artifact.py', 'src/pontius/blueprint_artifact/extra.py']:
    candidate = {**sources, path: b'"""Undeclared review source-map negative fixture."""\n'}
    try:
        graph = checker._BASELINE.scan_sources(candidate)
        checker.enforce_origin_classification(candidate, tool_sources)
        checker.enforce_legacy_edges(baseline.graph, graph)
        checker.enforce_no_new_or_expanded_scc(baseline.graph, graph)
        checker.enforce_evidence_import_policy(candidate)
        checker.enforce_v0a_import_policy(candidate)
        checker.enforce_blueprint_artifact_import_policy(candidate)
        checker.enforce_orchestration_import_policy(tool_sources)
    except checker.BoundaryError as error:
        print(path, 'REFUSED:', str(error))
    else:
        print(path, 'ACCEPTED BY ALL SEVEN PUBLIC-GATE CONTENT PREDICATES')
print('No filesystem source or snapshot metadata was modified.')
