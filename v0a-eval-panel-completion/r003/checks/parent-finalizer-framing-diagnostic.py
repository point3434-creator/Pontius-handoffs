"""Verify framing consequences on r002 using an existing actual host capture."""
import ast
import base64
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

assert sys.version_info[:3] == (3, 14, 6)
ROOT = Path('D:/Pontius-worktrees/eval-completion-check-r002-verified')
sys.path[:0] = [str(ROOT / 'src'), str(ROOT)]
os.chdir(ROOT)
from pontius.execution import begin_run, finish_run
from pontius.eval_agreement import classify, summarize
from pontius import eval_bridge as bridge
from pontius.immutable_blueprint import BlueprintActionEntry, ImmutableBlueprintActionSource

started = time.perf_counter()
context = begin_run(ROOT, reviewed_commit='430ad75de79cec13d66ff3dc4981dd3770a371b7')
spec = importlib.util.spec_from_file_location('framing_host_authority',
                                             ROOT / 'tools/v0a_table_host.py')
host = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = host
spec.loader.exec_module(host)
capture_path = Path('D:/Pontius-handoffs/v0a-eval-panel-completion/r001/checks/'
                    'classifier-red-real-host.txt')
capture_raw = capture_path.read_bytes()
line = next(line for line in capture_raw.decode().splitlines()
            if line.startswith(" : {'label': 'check-control'"))
captured = ast.literal_eval(line[3:])
board = bridge.board_cards(['2c', '7d', '9h', 'Js', 'Qc'])
hands = tuple(map(tuple, captured['witness']['private_hands']))
row = BlueprintActionEntry(bridge.root_key(bridge.replay_root(), board, hands[2]), bridge.CHECK)
blueprint = ImmutableBlueprintActionSource('test-check-control', (row,))
kwargs = dict(blueprint=blueprint, teacher_actions={bridge.hand_name(hands[2]): bridge.CHECK},
              board=board, private_hands=hands)
report = captured['session']
wire = base64.b64decode(report['hands'][0]['result']['child_stdout_base64'], validate=True)
assert b'\r' not in wire and wire.endswith(b'\n')
baseline = classify(report, **kwargs)
assert baseline['classification'] == 'hit', baseline

def host_parse(raw):
    try:
        for frame in raw.split(b'\n')[:-1]:
            host.decode_json(frame + b'\n', code='protocol_invalid', digits=640, floats=True)
        return 'accepted'
    except host.HostRefusal as error:
        return 'rejected:' + str(error)

assert host_parse(wire) == 'accepted'
variants = {
    'CRLF': wire.replace(b'\n', b'\r\n'),
    'record_separator': wire.replace(b'\n', b'\x1e', 1),
    'unicode_line_separator': wire.replace(b'\n', '\u2028'.encode(), 1),
    'oversized_ready_frame': wire.replace(b'\n', b' ' * 16384 + b'\n', 1),
}
observations = []
for name, raw in variants.items():
    changed = copy.deepcopy(report)
    changed['hands'][0]['result']['child_stdout_base64'] = base64.b64encode(raw).decode()
    outcome = classify(changed, **kwargs)
    observations.append(dict(mutation=name, raw_sha256=hashlib.sha256(raw).hexdigest(),
        raw_length=len(raw), host_parser=host_parse(raw), classifier=outcome,
        summary=summarize([outcome], scheduled=1)))
    assert host_parse(raw).startswith('rejected:'), name
    assert outcome['classification'] == 'hit' and outcome['chip_eligible'], outcome
result = dict(status='completed', summary='Confirmed 4 malformed streams retain hit/chip credit',
    candidate=context['commit'], source_verified=context['verified'], python=sys.version,
    diagnostic_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    capture_path=str(capture_path), capture_sha256=hashlib.sha256(capture_raw).hexdigest(),
    provenance='Existing actual host capture; no new host launch. Only retained wire bytes mutate.',
    ground_truth='Unchanged host decode_json on LF-delimited physical frames',
    baseline=baseline, observations=observations)
finish_run(context, 'isolated r002 framing diagnostic', result, time.perf_counter() - started)
output = Path('D:/Pontius/tmp/eval-completion/r002-framing-diagnostic.json')
with output.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps(result, indent=2))
