"""Independent baseline sensitivity check for ordinary malformed fields."""
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from dataclasses import fields, replace

expected_version = sys.argv[1]
snapshot = Path(r'D:\pontius-snapshots\v0a-i01-ab-r003-cold-a-base-20260830')
assert platform.python_version() == expected_version
assert platform.python_implementation() == 'CPython'
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert Path.cwd().resolve() == snapshot
assert os.environ['PYTHONPATH'] == str(snapshot / 'src')
assert set(os.environ) <= {'SYSTEMROOT','WINDIR','COMSPEC','TEMP','TMP','PYTHONPATH',
    'PYTHONNOUSERSITE','PYTHONDONTWRITEBYTECODE','PONTIUS_GIT'}
git = r'C:\Program Files\Git\cmd\git.exe'
assert os.environ['PONTIUS_GIT'] == git
head = subprocess.run([git, '-C', str(snapshot), 'rev-parse', 'HEAD'],
                      check=True, capture_output=True, text=True).stdout.strip()
assert head == '2f4287f68a83fac4225a05a91daffdb3f2977a43'
print(json.dumps({'version': sys.version, 'executable': sys.executable, 'cwd': str(snapshot),
                  'environment': dict(os.environ), 'safe_path': sys.flags.safe_path,
                  'dont_write_bytecode': sys.dont_write_bytecode, 'commit': head}), flush=True)
import pontius.v0a.runtime as runtime
assert Path(runtime.__file__).resolve() == snapshot / 'src/pontius/v0a/runtime.py'
from pontius.holdem_cards import OneSeatCardState
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.no_limit_betting import NoLimitBettingState
cards = OneSeatCardState.preflop(controlled_seat=3, private_hand=(0,13))
source = ImmutableBlueprintActionSource('cold-a-baseline')
states = [NoLimitBettingState.six_max_100bb(button=0),
          NoLimitBettingState.new_hand(button=0, starting_stacks=(2,)*6,
                                       small_blind=1,big_blind=2)]
deep = 200
for _ in range(2500):
    deep = (deep,)
observations = []
for state in states:
    decision = state.legal_decision()
    cases = [(f'decision.{f.name}', replace(decision, **{f.name: deep}))
             for f in fields(decision)]
    if decision.raise_bounds is not None:
        cases += [(f'bounds.{f.name}', replace(decision,
                   raise_bounds=replace(decision.raise_bounds, **{f.name: deep})))
                  for f in fields(decision.raise_bounds)]
    for label, supplied in cases:
        observed = None
        try:
            runtime.select_blueprint_action(source, cards, state, supplied)
        except BaseException as error:
            observed = type(error).__name__
        observations.append({'field': label, 'raises_allowed': decision.raise_bounds is not None,
                             'observed': observed})
assert len(observations) == 23
assert all(row['observed'] == 'RecursionError' for row in observations)
print(json.dumps({'baseline_failure_class_verified': True, 'module_origin': runtime.__file__,
                  'cases': observations}), flush=True)
