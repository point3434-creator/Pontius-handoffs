"""Independent public-boundary diagnostics; no source mutation or private writes."""
from dataclasses import fields, is_dataclass, replace
import json
import sys
from pontius.holdem_cards import OneSeatCardState
from pontius.immutable_blueprint import BlueprintActionEntry, BlueprintDecisionKey, ImmutableBlueprintActionSource
from pontius.no_limit_betting import BettingAction, BettingActionRecord, BettingActionKind, BettingStreet, LegalBettingDecision, NoLimitBettingState, RaiseBounds, CALL, FOLD, raise_to
from pontius.v0a.model import ActionMailbox, FailureCode, HandAction, HandStartedEvent, OpponentActionEvent, SelectionReason
from pontius.v0a.replay import ReplayHost, FIXTURE_A, FIXTURE_B, PROTOCOL_ID
from pontius.v0a.runtime import HandRuntime, InvalidDecisionContextError, InvalidBlueprintEntryError, select_blueprint_action
import pontius.v0a.runtime as runtime_module

HOOKS = []
class Clock:
    def __init__(self): self.now = 1000
    def __call__(self): return self.now
class IntHook(int):
    def __eq__(self, other): HOOKS.append("int.eq"); return int.__eq__(self, other)
    __hash__ = int.__hash__
class StrHook(str):
    def __eq__(self, other): HOOKS.append("str.eq"); return str.__eq__(self, other)
    def strip(self, *args): HOOKS.append("str.strip"); return str.strip(self, *args)
    __hash__ = str.__hash__
class TupleHook(tuple):
    def __iter__(self): HOOKS.append("tuple.iter"); return tuple.__iter__(self)
    def __eq__(self, other): HOOKS.append("tuple.eq"); return tuple.__eq__(self, other)
    __hash__ = tuple.__hash__

record_kinds = (BlueprintActionEntry, BlueprintDecisionKey, BettingAction, BettingActionRecord, OneSeatCardState, NoLimitBettingState, LegalBettingDecision, RaiseBounds)
subclasses = {}
for kind in record_kinds:
    def getter(self, name, base=kind):
        HOOKS.append(base.__name__ + "." + name)
        return object.__getattribute__(self, name)
    subclasses[kind] = type(kind.__name__ + "Hook", (kind,), {"__getattribute__": getter})

def altered(value):
    kind = type(value)
    if kind is int: return IntHook(value)
    if kind is str: return StrHook(value)
    if kind is tuple: return TupleHook(value)
    if kind in subclasses:
        return subclasses[kind](**{field.name: getattr(value, field.name) for field in fields(kind)})
    return None

def members(value, prefix=()):
    yield prefix, value
    if type(value) is tuple:
        for index, child in enumerate(value): yield from members(child, prefix + (index,))
    elif type(value) in record_kinds or type(value) is ImmutableBlueprintActionSource:
        for field in fields(value): yield from members(getattr(value, field.name), prefix + (field.name,))

def at(value, path):
    for part in path: value = value[part] if type(part) is int else getattr(value, part)
    return value

def change(value, path, new):
    if not path: return new
    part, *tail = path
    if type(part) is int:
        items = list(value); items[part] = change(items[part], tail, new); return tuple(items)
    return replace(value, **{part: change(getattr(value, part), tail, new)})

betting = NoLimitBettingState.six_max_100bb(button=0)
cards = OneSeatCardState.preflop(controlled_seat=3, private_hand=(0, 13))
decision = betting.legal_decision()
key = BlueprintDecisionKey.from_state(cards=cards, betting=betting, decision=decision)
policy = ImmutableBlueprintActionSource("cold-b-exact", (BlueprintActionEntry(key, raise_to(6)),))
empty = ImmutableBlueprintActionSource("cold-b-empty")
start = HandStartedEvent(hand_id="cold-b-hand", event_index=0, button=0, controlled_seat=3, starting_stacks=(200,)*6, small_blind=1, big_blind=2, private_cards=(0,13))
rows = []

def policy_boundaries(name, supplied):
    for boundary in ("runtime", "selector", "host"):
        mailbox = ActionMailbox(); HOOKS.clear()
        try:
            if boundary == "runtime": HandRuntime(blueprint=supplied, mailbox=mailbox, clock=Clock())
            elif boundary == "selector": select_blueprint_action(supplied, cards, betting, decision)
            else: ReplayHost(FIXTURE_A, run_id=PROTOCOL_ID+"-correctness-cold-b", blueprint=supplied, mailbox=mailbox, clock=Clock())
        except Exception as error:
            accepted_error = type(error) in ((TypeError, ValueError) if boundary != "selector" else (InvalidDecisionContextError,))
            assert accepted_error, (name,boundary,type(error).__name__)
            assert not HOOKS, (name,boundary,HOOKS)
            assert not mailbox.accepted
            rows.append({"category":"policy-rejection", "path":name, "boundary":boundary, "exception":type(error).__name__, "hooks":0})
        else: raise AssertionError(("policy admitted",name,boundary))

for method in ("digest", "canonical_bytes", "action_for"):
    def hook(self, *args, **kwargs): HOOKS.append("outer"); return empty.digest
    foreign = type("Foreign"+method, (ImmutableBlueprintActionSource,), {method: property(hook) if method == "digest" else hook})
    policy_boundaries(method, foreign(policy.source_id, policy.entries))
class Pretender:
    @property
    def __class__(self): HOOKS.append("class"); return ImmutableBlueprintActionSource
policy_boundaries("class-pretender", Pretender())

history_state = betting.apply_action(CALL)
history_cards = OneSeatCardState.preflop(controlled_seat=4, private_hand=(1,14))
history_decision = history_state.legal_decision()
history_key = BlueprintDecisionKey.from_state(cards=history_cards, betting=history_state, decision=history_decision)
history_policy = ImmutableBlueprintActionSource("cold-b-history", (BlueprintActionEntry(history_key, CALL),))
for source_name, source in (("preflop", policy), ("history", history_policy)):
    for path, value in list(members(source)):
        new = altered(value)
        if new is None: continue
        label = source_name + "/" + "/".join(map(str,path))
        try: supplied = change(source,path,new)
        except Exception as error:
            rows.append({"category":"constructor-refusal", "path":label,"exception":type(error).__name__}); continue
        if type(at(supplied,path)) is not type(new):
            rows.append({"category":"constructor-normalization", "path":label}); continue
        policy_boundaries(label,supplied)

for context_name, context in (("cards", history_cards), ("betting", history_state), ("decision", history_decision)):
    for path, value in list(members(context)):
        new = altered(value)
        if new is None: continue
        label = context_name + "/" + "/".join(map(str,path))
        try: supplied = change(context,path,new)
        except Exception as error:
            rows.append({"category":"constructor-refusal", "path":label,"exception":type(error).__name__}); continue
        if type(at(supplied,path)) is not type(new):
            rows.append({"category":"constructor-normalization", "path":label}); continue
        args = {"source":empty,"cards":history_cards,"betting":history_state,"decision":history_decision}
        args[context_name] = supplied
        HOOKS.clear()
        try: select_blueprint_action(**args)
        except Exception as error:
            assert type(error) is InvalidDecisionContextError, (label,type(error).__name__)
            assert not HOOKS, (label,HOOKS)
            rows.append({"category":"context-rejection", "path":label,"exception":type(error).__name__,"hooks":0})
        else: raise AssertionError(("context admitted",label))

for field in fields(decision):
    value = getattr(decision,field.name)
    if type(value) is not int: continue
    for alias in (float(value), bool(value) if value in (0,1) else None):
        if alias is None: continue
        supplied=replace(decision,**{field.name:alias})
        try: select_blueprint_action(empty,cards,betting,supplied)
        except Exception as error: assert type(error) is InvalidDecisionContextError
        else: raise AssertionError(("numeric alias",field.name,type(alias).__name__))
        rows.append({"category":"numeric-alias-rejection","path":field.name,"alias":type(alias).__name__})

for action, expected in ((raise_to(6),"hit"),(raise_to(1000),"illegal")):
    real=ImmutableBlueprintActionSource("cold-b-outcomes",(BlueprintActionEntry(key,action),))
    mailbox=ActionMailbox(); outcome=HandRuntime(blueprint=real,mailbox=mailbox,clock=Clock()).dispatch(start)
    if expected == "hit":
        assert outcome.status == "decided" and len(mailbox.accepted)==1 and outcome.decision.selection_reason is SelectionReason.TABLE_HIT
        assert outcome.decision.selected_action.raise_to == 6
    else:
        assert outcome.status == "failed" and not mailbox.accepted and outcome.failure.code is FailureCode.INVALID_BLUEPRINT_ENTRY
        try: select_blueprint_action(real,cards,betting,decision)
        except Exception as error: assert type(error) is InvalidBlueprintEntryError
        else: raise AssertionError("illegal helper entry admitted")
    rows.append({"category":"real-outcome","outcome":expected})
miss=select_blueprint_action(empty,cards,betting,decision)
assert not miss.table_hit and miss.action == CALL
rows.append({"category":"real-outcome","outcome":"miss-call"})

profile_events=[]
targets = {ImmutableBlueprintActionSource.canonical_bytes.__code__: "canonical", ImmutableBlueprintActionSource.action_for.__code__: "lookup", runtime_module._admit_blueprint.__code__: "admit"}
def profile(frame,event,arg):
    if event == "call" and frame.f_code in targets:
        label=targets[frame.f_code]
        source=frame.f_locals.get("self",frame.f_locals.get("source"))
        profile_events.append((label,id(source)))
previous=sys.getprofile(); sys.setprofile(profile)
try:
    for fixture in (FIXTURE_A,FIXTURE_B):
        profile_events.clear()
        host=ReplayHost(fixture,run_id=PROTOCOL_ID+"-correctness-cold-b-owned",blueprint=empty,clock=Clock())
        outcome=host.run()
        assert outcome.receipt.passed
        event_copy=list(profile_events)
        assert sum(label == "admit" for label,_ in event_copy)==1
        owned={identity for label,identity in event_copy if label in ("canonical","lookup")}
        assert len(owned)==1 and id(empty) not in owned
        lookups=sum(label == "lookup" for label,_ in event_copy)
        hashes=sum(label == "canonical" for label,_ in event_copy)
        assert lookups == len(outcome.decisions)
        assert hashes == lookups+2, (fixture.name,hashes,lookups)
        expected=empty.digest
        header=json.loads(outcome.trace.splitlines()[0])
        assert header["blueprint_sha256"] == expected
        assert all(record.blueprint_sha256 == expected for record in outcome.decisions)
        rows.append({"category":"owned-policy-host", "fixture":fixture.name,"admissions":1,"lookups":lookups,"canonicalizations":hashes,"caller_used_for_hash_or_lookup":False,"header_matches_decisions":True})
finally: sys.setprofile(previous)

clock=Clock(); mailbox=ActionMailbox(); runtime=HandRuntime(blueprint=policy,mailbox=mailbox,clock=clock)
charged=[]
def delay(frame,event,arg):
    if event == "call" and frame.f_code is ImmutableBlueprintActionSource.canonical_bytes.__code__:
        charged.append(1)
        if len(charged)==1: clock.now += 16_000_000_000
previous=sys.getprofile(); sys.setprofile(delay)
try: outcome=runtime.dispatch(start)
finally: sys.setprofile(previous)
assert outcome.status == "failed" and outcome.failure.code is FailureCode.ACTION_DEADLINE_EXCEEDED
assert not mailbox.accepted
rows.append({"category":"initial-digest-measured","failure":outcome.failure.code.value,"accepted":0,"canonicalizations":len(charged)})

# Exploratory malformed exact graph: every node is an admitted built-in tuple,
# but nesting is invalid for LegalBettingDecision.stack. No constructor bypass.
for depth in (1,200,600):
    nested=200
    for _ in range(depth): nested=(nested,)
    malformed=replace(decision,stack=nested)
    try:
        select_blueprint_action(empty,cards,betting,malformed)
    except Exception as error:
        rows.append({"category":"malformed-exact-depth","depth":depth,"exception":type(error).__name__,"typed_context_failure":type(error) is InvalidDecisionContextError})
    else: raise AssertionError("malformed exact graph accepted")

summary={}
for row in rows: summary[row["category"]]=summary.get(row["category"],0)+1
print(json.dumps({"summary":summary,"observations":rows},indent=2))
