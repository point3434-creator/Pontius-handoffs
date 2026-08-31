"""Independent full R1-baseline receipt replay: stdlib/data/Git only, no payload imports."""
from pathlib import Path
import hashlib
import json
import re
import stat
import subprocess
import sys

H = Path(r'D:\Pontius-handoffs')
T = H / 'v0a-i01-c-authority'
C = T / 'tests-checks'
SNAPSHOTS = Path(r'D:\pontius-snapshots')
GIT = r'C:\Program Files\Git\cmd\git.exe'
SOURCE = 'c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f'
POPULATION = '8ab800c1361ca53f4f294bd32e308ecb7061e031b60d32dc74d7fdf52cc5ce3b'
BASE = '29c02f6fbd5eb0b7ddc9e816ef28f570b9839358'
PAYLOAD = '.rewrite-r2-identity'
FUTURE = {'_c_identity_compare', '_c_raise_known', '_c_handle_known_exception', '_c_resume_generator'}


def check(value, message):
    if not value:
        raise RuntimeError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(root, *args):
    return subprocess.run([GIT, '-c', 'core.fsmonitor=false', '-c', 'core.autocrlf=false',
                           '-C', str(root), *args], capture_output=True, check=True,
                          timeout=60, creationflags=subprocess.CREATE_NO_WINDOW).stdout


def read(path):
    path = Path(path)
    check(path.is_absolute() and '..' not in path.parts, 'absolute regular path')
    for part in (path, *path.parents):
        info = part.lstat()
        check(not getattr(info, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT,
              'no reparse path: ' + str(part))
    check(stat.S_ISREG(path.lstat().st_mode), 'regular file')
    return path.read_bytes()


check(sys.version_info[:3] == (3, 11, 15) and sys.implementation.name == 'cpython'
      and sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
      and sys.dont_write_bytecode and not sys.flags.optimize, 'isolated floor verifier')
check(len(sys.argv) == 6, 'LABEL RECEIPT_SHA HARNESS_REF MANIFEST_NAME MANIFEST_SHA')
label, receipt_sha, href, manifest_name, manifest_sha = sys.argv[1:]
check(re.fullmatch('[a-z0-9-]+', label) and re.fullmatch('[0-9a-f]{40}', href), 'explicit label/ref')
check(Path(manifest_name).name == manifest_name, 'manifest basename')
manifest_raw = git(H, 'show', href + ':v0a-i01-c-authority/' + manifest_name)
check(digest(manifest_raw) == manifest_sha and read(T / manifest_name) == manifest_raw, 'frozen manifest')
pins = {}
for line in manifest_raw.decode().splitlines():
    pin, name = line.split('  ', 1)
    check(not Path(name).is_absolute() and '..' not in Path(name).parts and name not in pins, 'manifest key')
    raw = git(H, 'show', href + ':v0a-i01-c-authority/' + name)
    check(digest(raw) == pin and read(T / name) == raw, 'frozen harness blob: ' + name)
    pins[name] = pin
receipt_path = C / ('rewrite-r2-identity-' + label + '-311-receipt.json')
receipt_raw = read(receipt_path)
check(digest(receipt_raw) == receipt_sha, 'receipt pin')
r = json.loads(receipt_raw)
check(r['label'] == label and r['slot'] == '311' and r['schema'] == 'pontius-rewrite-r2-identity-v1', 'receipt context')
check(r['generator_sha256'] == SOURCE and r['core_watch_sha256'] == SOURCE
      and r['population_sha256'] == POPULATION and r['adapter'] == 'r1-baseline-only', 'exact baseline inputs')
check(r['payload_started'] is True and r['integrity_ok'] is True
      and 'error' not in r and 'cleanup_error' not in r, 'complete infrastructure')
check(r['before'] == r['after'] and r['input_hashes_before'] == r['input_hashes_after'], 'before/after equality')
for key in ('probe', 'control', 'plan', 'observer_map'):
    relative = Path(r['input_paths'][key]).relative_to(T).as_posix()
    check(pins[relative] == r['input_hashes_before'][key] == r[key + '_sha256'], 'frozen ' + key)
snapshot = Path(r['snapshot'])
check(snapshot.parent.parent == SNAPSHOTS and snapshot.name == 'snapshot'
      and Path(r['temp']) == snapshot.parent / 'temp', 'snapshot/temp roots')
tracked = git(snapshot, 'ls-tree', '-r', '-z', '--name-only', BASE).decode().split('\0')[:-1]
check(len(tracked) == len(set(tracked)) == r['tracked_file_count'] == 1761, 'tracked population')
payload_names = {'authoring-disposition.md', 'control.py', 'depth-provenance.py', 'identity-coverage.json',
                 'name-environment-cases-v1.json', 'observer-map.json', 'observer-spec.md', 'plan-addendum.md',
                 'plan.md', 'population.json', 'prior-population.json', 'probe.py', 'retained-source.py',
                 'rewrite-r2-identity-cases-v1.json', 'run.json', 'source-model.diff', 'storage-composition-cases-v1.json'}
check(r['payload_file_count'] == len(payload_names) == 17 and len(r['before']) == 1778, 'exact payload count')
check(set(r['before']) == set(tracked) | {PAYLOAD + '/' + n for n in payload_names}, 'exact manifest keys')
for name, pin in r['before'].items():
    check(not Path(name).is_absolute() and '..' not in Path(name).parts, 'relative snapshot path')
    check(digest(read(snapshot / name)) == pin, 'snapshot file: ' + name)
raw_manifest = read(snapshot / PAYLOAD / 'manifest.json')
check(digest(raw_manifest) == r['manifest_sha256'] == r['manifest_after_sha256']
      and json.loads(raw_manifest) == r['before'], 'snapshot manifest')
check(git(snapshot, 'rev-parse', 'HEAD').decode().strip() == r['base'] == BASE, 'snapshot head')
dirty = git(snapshot, 'status', '--porcelain=v1', '-z', '--untracked-files=all').decode()
check(dirty == r['status_after'] and set(dirty.split('\0')[:-1]) ==
      {' M tools/generate_test_inventory.py'} | {'?? ' + PAYLOAD + '/' + n for n in payload_names | {'manifest.json'}},
      'snapshot index/worktree/untracked population')
for name, pin in r['input_hashes_before'].items():
    check(digest(read(r['input_paths'][name])) == pin, 'original input: ' + name)
copies = {
    'probe.py': 'probe', 'control.py': 'control', 'plan.md': 'plan', 'observer-map.json': 'observer_map',
    'retained-source.py': 'overlay', 'population.json': 'population', 'depth-provenance.py': 'depth_provenance',
    'storage-composition-cases-v1.json': 'storage', 'name-environment-cases-v1.json': 'name_environment',
    'rewrite-r2-identity-cases-v1.json': 'identity', 'prior-population.json': 'prior_population',
    'identity-coverage.json': 'coverage', 'observer-spec.md': 'spec', 'authoring-disposition.md': 'authorization',
    'plan-addendum.md': 'addendum', 'source-model.diff': 'source_model_diff'}
check(set(copies) | {'run.json'} == payload_names, 'complete runtime-copy closure')
for name, key in copies.items():
    check(read(snapshot / PAYLOAD / name) == read(r['input_paths'][key]), 'runtime copy equals verified input: ' + name)
check(digest(read(snapshot / 'tools/generate_test_inventory.py')) == SOURCE
      and digest(read(snapshot / PAYLOAD / 'retained-source.py')) == SOURCE
      and r['input_hashes_before']['overlay'] == r['input_hashes_before']['core_watch'] == SOURCE,
      'actual executable and retained source equal held R1')
run_config = json.loads(read(snapshot / PAYLOAD / 'run.json'))
check(all(key in r and r[key] == value for key, value in run_config.items()), 'run config equals verified receipt context')
outputs = {key: read(entry['path']) for key, entry in r['outputs'].items()}
check(all(digest(outputs[key]) == entry['sha256'] for key, entry in r['outputs'].items()), 'raw outputs')
check(outputs['log'] == outputs['stdout'] + b'\nCONTROL STDERR\n' + outputs['stderr'], 'combined log')
setup = json.loads(outputs['setup'])
check(all(r[k] == v for k, v in setup.items()), 'raw setup')
check(outputs['stdout'].endswith(b'\n') and b'\r' not in outputs['stdout'], 'complete LF stream')
records = [json.loads(line) for line in outputs['stdout'].splitlines()]
check(len(records) == 14 and records[0] == {'identity_before_imports': r['identity']}
      and records[-1] == r['summary'], 'identity/twelve cases/summary stream')
identity, summary = r['identity'], r['summary']
check(identity['version_info'] == [3, 11, 15] and identity['implementation'] == 'cpython'
      and Path(identity['executable']).resolve() == Path(r'D:\Pontius-tools\py311\Scripts\python.exe').resolve()
      and identity['cwd'] == str(snapshot) and identity['generator_sha256'] == SOURCE
      and identity['environment'] == setup['environment'] and identity['verified_files'] == 1778
      and identity['manifest_sha256'] == r['manifest_sha256'], 'actual pre-import interpreter/custody')
population_raw = read(snapshot / PAYLOAD / 'population.json')
check(digest(population_raw) == POPULATION, 'population raw pin')
pop = json.loads(population_raw)
check([c['rewrite_gate_b_case'] for c in records[1:-1]] == pop['gates']['B_identity']['ordered_case_ids'], 'frozen order')
packs = {}
for scope, filename in (('storage', 'storage-composition-cases-v1.json'),
                        ('name_environment', 'name-environment-cases-v1.json'),
                        ('identity', 'rewrite-r2-identity-cases-v1.json')):
    pack_raw = read(snapshot / PAYLOAD / filename)
    population_key = 'tests-checks/' + filename
    population_pin = (pop['new_inputs'][population_key] if scope == 'identity'
                      else pop['original_inputs_unchanged'][population_key]['sha256'])
    check(digest(pack_raw) == r['pack_sha256'][scope] == population_pin, 'population-bound pack pin')
    packs[scope] = {c['id']: c for c in json.loads(pack_raw)['cases']}
failures, analyzer_errors, reserve, mechanism_failures, case_rows = [], [], [], [], []
projections = returned = depth_errors = 0
for case in records[1:-1]:
    name, scope = case['rewrite_gate_b_case'], case['original_pack']
    desc = pop['cases'][name]
    check(case['source_sha256'] == desc['source']['sha256'] and case['classification'] == desc['classification'], 'case identity')
    depth = scope == 'depth'
    fixture = None if depth else packs[scope][name]
    if fixture is not None:
        record_raw = json.dumps(fixture, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
        check(digest(record_raw) == desc['case_record_canonical_sha256']
              and digest(fixture['source'].encode()) == desc['source']['sha256']
              and digest(fixture['oracle_source'].encode()) == desc['model']['sha256'], 'selected frozen record/source/Model')
    witnesses = [] if depth else [fixture['expected']] if scope == 'storage' else fixture['witnesses']
    check(case['oracle_actuals'] == case['expected_projections'] == witnesses
          and case['oracle_passed'] is True and case['oracle_error'] is None, 'all independent Model projections')
    check(case['oracle_sha256'] == (None if depth else desc['model']['sha256']), 'Model identity')
    projections += len(witnesses)
    error = case['public_exception']
    depth_match = bool(depth and error is not None and error['is_inventory_error'] is True
                       and re.fullmatch(desc['oracle']['regex'], error['message']))
    check(case['expected_depth_error'] is depth_match, 'exact original depth result')
    check(case['analyzer_error'] == (None if depth_match else error), 'analysis exception attribution')
    if case['analyzer_error'] is not None:
        analyzer_errors.append(name)
    argv = [row['argv'] for row in case['expanded_rows'] if row['capability_kind'] == 'subprocess']
    expected_argv = None if depth else fixture['required_argv'] if scope == 'storage' else [['-m', 'fixed']]
    check(case['argv'] == argv and case['required_argv'] == expected_argv, 'exact argv projection')
    has_receipt = case['receipt_sha256'] is not None
    returned += has_receipt
    depth_errors += depth_match
    clean = not case['blockers'] and argv == expected_argv
    public = bool(case['blockers']) if case['classification'] == 'refuse' else (
        bool(case['blockers']) or clean if case['classification'] == 'permitted-refusal' else clean)
    passed = depth_match if depth else has_receipt and error is None and public
    check(case['semantic_passed'] is passed, 'semantic predicate')
    if not passed:
        failures.append(name)
    check(case['accounting_error'] is None and case['original_methods_restored'] is True, 'budget observation/restoration')
    m = case['budget_metrics']
    check(m['epoch_count'] == m['initialization_attempts'] == len(m['epochs']) > 0
          and not m['initialization_errors'] and m['unscoped_events'] == 0, 'budget creation coverage')
    local_reserve = []
    for i, e in enumerate(m['epochs'], 1):
        for key in ('epoch', 'initial_work', 'requested_units', 'last_observed_work', 'consume_calls',
                    'completed_consume_calls', 'exceptional_consume_calls'):
            check(type(e[key]) is int and e[key] >= 0, 'exact budget scalar')
        check(e['epoch'] == i and e['initial_work'] + e['requested_units'] == e['last_observed_work'], 'epoch arithmetic')
        check(e['consume_calls'] == e['completed_consume_calls'] + e['exceptional_consume_calls']
              and len(e['consume_exceptions']) == e['exceptional_consume_calls'], 'charge completion partition')
        check(sum(v['units'] for v in e['origins'].values()) == sum(e['phase_units'].values()) == e['requested_units']
              and sum(v['calls'] for v in e['origins'].values()) == e['consume_calls'], 'disjoint charge sums')
        for exc in e['consume_exceptions']:
            check(exc['before'] + exc['requested_units'] == exc['after'] > 262144
                  and exc['type'] == 'InventoryError' and exc['message'] == 'analysis work units exceed 262144', 'throwing charge')
        if e['requested_units'] > 196608:
            local_reserve.append({'case': name, 'epoch': i, 'requested_units': e['requested_units'],
                                  'initial_work': e['initial_work'], 'last_observed_work': e['last_observed_work'], 'maximum': 196608})
    check(case['reserve_violations'] == local_reserve, 'requested-unit reserve')
    reserve.extend(local_reserve)
    check(m['requested_units_across_epochs'] == sum(e['requested_units'] for e in m['epochs'])
          and m['maximum_epoch_observed_work'] == max(e['last_observed_work'] for e in m['epochs']), 'epoch totals')
    mechanism, verdict = case['mechanism'], case['mechanism_verdict']
    check(case['mechanism_error'] is None and mechanism['errors'] == []
          and mechanism['original_methods_restored'] is True and verdict['complete'] is True, 'complete scalar observer')
    check(mechanism['source_sha256'] == SOURCE and mechanism['adapter'] == 'r1-baseline-only'
          and {k for k, v in mechanism['availability'].items() if v is False} == FUTURE, 'unavailable is not passing')
    for count in mechanism['counters'].values():
        check(count['attempts'] == count['completed'] + count['raised'], 'hook completion partition')
    births, writes, forks, origins = {}, 0, 0, 0
    for i, event in enumerate(mechanism['events'], 1):
        check(event['n'] == i and type(event['span']) is int and event['span'] > 0
              and event['epoch'] in range(1, m['epoch_count'] + 1), 'event order/epoch')
        kind = event['kind']
        if kind in ('birth', 'fork'):
            check(event['birth'] not in births, 'unique birth ordinal')
            births[event['birth']] = {} if kind == 'birth' else dict(births[event['parent']])
            forks += kind == 'fork'
        elif kind == 'write':
            births[event['birth']][(event['activation'], event['variable'])] = event['value']
            writes += 1
        elif kind == 'depth_rejection':
            check(event['incoming_depth'] > 64 and event['message'] == 'analysis helper depth exceeds 64', 'helper origin')
            origins += 1
        elif kind == 'snapshot':
            check(event['birth'] in births, 'snapshot known birth')
        else:
            check(kind in ('join', 'evaluation_exit', 'statement_exit', 'sink_exit', 'review_exit'), 'known event role')
            check(all(o['birth'] in births for o in event['outcomes']), 'outcomes retain state birth')
    check(verdict['lineage'] == {'births': len(births), 'forks': forks, 'completed_writes': writes,
                                'inheritance_at_fork_ordinal': True} and origins <= 1, 'independent lineage replay')
    met = not verdict['unavailable'] and all(v is True for v in verdict['predicates'].values())
    check(verdict['met'] is met, 'mechanism admission')
    if not met:
        mechanism_failures.append(name)
    case_rows.append({'id': name, 'semantic_passed': passed, 'public_exception': error, 'argv': argv,
                      'blockers': case['blockers'], 'mechanism_met': met, 'unavailable': verdict['unavailable'],
                      'epoch_count': m['epoch_count'], 'maximum_epoch_requested_units': max(e['requested_units'] for e in m['epochs']),
                      'total_requested_units': m['requested_units_across_epochs'], 'lineage': verdict['lineage']})
check(projections == summary['projections'] == 24 and summary['attempted_analyses'] == summary['case_count'] == 12,
      'complete fixed observation scope')
check(summary['semantic_failures'] == failures and summary['analyzer_errors'] == analyzer_errors
      and summary['reserve_violations'] == reserve and summary['mechanism_failures'] == mechanism_failures,
      'independent summary replay')
check(summary['returned_receipts'] == returned and summary['expected_depth_errors'] == depth_errors
      and not summary['oracle_errors'] and not summary['accounting_errors'] and not summary['mechanism_errors'], 'summary counts/errors')
completed = returned == 10 and depth_errors == 2 and not analyzer_errors
check(r['completed'] is completed and summary['completed'] is completed and r['observation_complete'] is True, 'observation vs completion')
check(r['semantic_ok'] is (not failures) and r['accounting_ok'] is True and r['reserve_ok'] is (not reserve)
      and r['mechanism_ok'] is (not mechanism_failures) and r['mechanism_methods_restored'] is True, 'separate gate results')
exit_code = int(bool(failures or analyzer_errors or reserve or mechanism_failures))
check(type(r['exit']) is int and r['exit'] == r['process_returncode'] == exit_code, 'actual exit')
check(r['success'] is (completed and exit_code == 0), 'success is not mere observation')
report = {'kind': 'independent R1 full-baseline custody and raw-record replay; no candidate or Model imports',
          'harness_ref': href, 'harness_manifest_sha256': manifest_sha, 'receipt_sha256': receipt_sha,
          'source_sha256': SOURCE, 'snapshot_manifest_sha256': r['manifest_sha256'], 'snapshot_files_rehashed': 1778,
          'harness_blobs_rehashed': len(pins), 'input_files_rehashed': len(r['input_paths']),
          'observation_complete': True, 'completed': completed, 'success': r['success'],
          'semantic_failures': failures, 'mechanism_failures': mechanism_failures,
          'reserve_violations': reserve, 'cases': case_rows, 'script_sha256': digest(read(Path(__file__).absolute()))}
out = T / ('coordinator-rewrite-r2-' + label + '-311-verification-v2.json')
with out.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'verification': str(out), 'sha256': digest(read(out)), 'semantic_failures': failures,
                  'mechanism_failures': mechanism_failures, 'reserve_violations': reserve}))
