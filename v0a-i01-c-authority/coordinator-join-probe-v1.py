"""Bounded public diagnostic: alternative activation cells at a branch join."""
import importlib.util
import json
import sys
import textwrap
from hashlib import sha256
from pathlib import Path

path = Path.cwd() / 'tools/generate_test_inventory.py'
spec = importlib.util.spec_from_file_location('coordinator_join_generator', path)
generator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = generator
spec.loader.exec_module(generator)
sid = 'tests/test_cold.py::ColdTests::test_case'
assignment = {'profile_name': 'current', 'payload_id': 'current:tests/test_cold.py',
              'expectation': {'kind': 'pass'}}
census = {'test_file_count': 1, 'stable_id_count': 1,
          'stable_ids_sha256': sha256((sid + '\n').encode()).hexdigest()}
inventory = {'schema_version': 'pontius-test-inventory-v1', 'baseline_commit': '1' * 40,
             'baseline_discovery': census, 'discovery': census,
             'entries': [{'stable_id': sid, 'relative_path': 'tests/test_cold.py',
                          'case_name': 'ColdTests', 'method_name': 'test_case',
                          'assignment': assignment, 'baseline_assignment': assignment}]}


def program(body, *, sensitive):
    imports = 'import unittest\n'
    sink = '_events.append("sink"); return "fixed"'
    if sensitive:
        imports += 'import subprocess, sys\n'
        sink = ('subprocess.run([sys.executable, "-m", "fixed"], cwd=".", '
                'env={**__import__("os").environ, "SAFE":"1"}, timeout=5, check=False)')
        body = '\n'.join(line for line in body.splitlines() if '# ORACLE' not in line)
    return (imports + 'class ColdTests(unittest.TestCase):\n'
            '    @staticmethod\n    def _launch():\n        ' + sink + '\n'
            '    def test_case(self):\n' + textwrap.indent(body, '        ') + '\n')


results = []
for capture in ('cell', 'default'):
    for order in ('unsafe-first', 'safe-first', 'both-safe', 'both-unsafe'):
        first = 'ColdTests' if order in {'unsafe-first', 'both-unsafe'} else 'None'
        second = 'ColdTests' if order in {'safe-first', 'both-unsafe'} else 'None'
        declaration = 'def callback():' if capture == 'cell' else 'def callback(owner=owner):'
        body = ('def make(owner):\n    ' + declaration + '\n'
                '        _events.append("body") # ORACLE\n'
                '        if owner is not None:\n'
                '            _events.append("write") # ORACLE\n'
                '            owner._launch = None\n'
                '    return callback\n'
                f'a = make({first})\nb = make({second})\n'
                'if self.choice:\n    chosen = a\nelse:\n    chosen = b\n'
                'chosen()\nreturn self._launch()')
        name = capture + '/' + order
        pure = program(body, sensitive=False)
        assert 'subprocess' not in pure and 'pontius' not in pure
        traces = []
        for choice in (False, True):
            events = []
            namespace = {'_events': events}
            exec(compile(pure, '<pure-' + name + '>', 'exec', dont_inherit=True), namespace)
            instance = namespace['ColdTests']()
            instance.choice = choice
            writes = (first if choice else second) == 'ColdTests'
            try:
                actual = instance.test_case()
            except TypeError:
                actual = 'TypeError'
            expected_trace = ['body', 'write'] if writes else ['body', 'sink']
            assert events == expected_trace, (name, choice, events, expected_trace)
            assert actual == ('TypeError' if writes else 'fixed'), (name, actual)
            traces.append({'choice': choice, 'trace': events, 'result': actual})
        source = program(body, sensitive=True).encode()
        review = generator.derive_design_review(
            baseline_commit='1' * 40, baseline_root_tree_oid='2' * 40,
            inventory_document=inventory,
            inventory_document_bytes=(json.dumps(inventory, sort_keys=True,
                                                 separators=(',', ':')) + '\n').encode(),
            sources={'tests/test_cold.py': source}, item_universe=(('stable_id', sid),))
        blockers = review['unresolved_dynamic_blockers']
        argv = [row['argv'] for row in review['receipt']['expanded_rows']
                if row['capability_kind'] == 'subprocess']
        must_refuse = order != 'both-safe'
        # Safe returned-callable precision may conservatively refuse. It is not
        # a newly granted requirement to resolve arbitrary effective results.
        passed = bool(blockers) if must_refuse else bool(blockers) or argv == [['-m', 'fixed']]
        item = {'case': name, 'pure_sha256': sha256(pure.encode()).hexdigest(),
                'source_sha256': sha256(source).hexdigest(), 'source': source.decode(),
                'oracle': traces, 'must_refuse': must_refuse, 'argv': argv,
                'blockers': blockers, 'passed': passed}
        print(json.dumps(item), flush=True)
        results.append(item)
failures = [item['case'] for item in results if not item['passed']]
print(json.dumps({'cases': len(results), 'failures': failures,
                  'probe_sha256': sha256(Path(__file__).read_bytes()).hexdigest()}), flush=True)
raise SystemExit(bool(failures))
