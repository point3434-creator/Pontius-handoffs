"""Bounded synthetic lookup benchmark; timings never run under tracemalloc."""
import gc
import hashlib
import itertools
import json
import platform
import statistics
import sys
import time
import tracemalloc
from pathlib import Path

from pontius.blueprint_preparation.lookup import PreparedBlueprint
from pontius.decision_provider.model import DecisionObservation
from pontius.decision_provider.providers import BlueprintProvider
from pontius.holdem_cards import OneSeatCardState
from pontius.immutable_blueprint import BlueprintActionEntry, BlueprintDecisionKey
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.no_limit_betting import CALL, NoLimitBettingState


def timing(fn, repeats=20):
    assert not tracemalloc.is_tracing()
    samples = []
    for _ in range(5):
        start = time.perf_counter_ns()
        for _ in range(repeats):
            fn()
        samples.append((time.perf_counter_ns() - start) / repeats / 1e6)
    return {'median_ms': statistics.median(samples), 'batch_means_ms': samples}


state = NoLimitBettingState.six_max_100bb(button=0)
decision = state.legal_decision()
cards = [OneSeatCardState.preflop(controlled_seat=3, private_hand=h)
         for h in itertools.combinations(range(52), 2)]
entries = tuple(BlueprintActionEntry(BlueprintDecisionKey.from_state(
    cards=c, betting=state, decision=decision), CALL) for c in cards)
rows = []
for n in (1, 100, 1326):
    def construct():
        return ImmutableBlueprintActionSource('performance-v1', entries[:n])
    source = construct()
    digest = source.digest
    prepared, provider = PreparedBlueprint(source), BlueprintProvider(source)
    query = dict(cards=cards[n-1], betting=state, decision=decision)
    obs = DecisionObservation('pontius-decision-observation-v1', 'performance', 1,
                              cards[n-1], state, decision, 14_000_000_000)
    selection = source.action_for(**query)
    assert selection == prepared.action_for(**query)
    assert provider.propose(obs).action == selection.action
    record = dict(n=n, digest=digest, canonical_sha256=hashlib.sha256(
        source.canonical_bytes()).hexdigest(), construction=timing(construct),
        digest_read=timing(lambda: source.digest),
        legacy_hit=timing(lambda: source.action_for(**query)),
        prepared_hit=timing(lambda: prepared.action_for(**query)),
        provider_hit=timing(lambda: provider.propose(obs)),
        provider_construction=timing(lambda: BlueprintProvider(source), 3),
        prepared_construction=timing(lambda: PreparedBlueprint(source), 3))
    if n < 1326:
        miss = dict(query, cards=cards[-1])
        assert not source.action_for(**miss).table_hit
        record['legacy_miss'] = timing(lambda: source.action_for(**miss))
    # Separate full graph + identity memory experiment; never used as timing.
    gc.collect()
    tracemalloc.start()
    fresh_entries = tuple(BlueprintActionEntry(BlueprintDecisionKey.from_state(
        cards=c, betting=state, decision=decision), CALL) for c in cards[:n])
    fresh = ImmutableBlueprintActionSource('performance-v1', fresh_entries)
    assert fresh.digest == digest
    record['construction_identity_traced_bytes'] = dict(zip(('current', 'peak'),
                                                           tracemalloc.get_traced_memory()))
    tracemalloc.stop()
    rows.append(record)
output = dict(python=platform.python_version(), rows=rows,
              assumptions='Synthetic preflop CALL table; warm process; five batches; '
              'construction uses prebuilt entries except separate memory experiment. '
              'No tracemalloc during timings; no retained phase invocation.')
Path(sys.argv[1]).write_text(json.dumps(output, indent=2) + '\n', newline='\n')
print(json.dumps(output, indent=2))
