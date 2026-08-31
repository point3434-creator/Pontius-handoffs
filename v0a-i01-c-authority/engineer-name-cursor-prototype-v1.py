"""Isolated owned name-cursor experiment; no production imports or authority model."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

MAXIMUM_WORK = 262144
MAXIMUM_SEALED_LAYERS = 8  # Representation threshold, never an admission/refusal limit.
MISSING = object()
_DELETED = object()


class BudgetExceeded(RuntimeError):
    pass


class Meter:
    """Storage work only; caller callback work is outside this primitive meter."""
    def __init__(self, limit=MAXIMUM_WORK):
        self.used = 0
        self.counts = {}
        self.limit = limit

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, value):
        if type(value) is not int or not 0 <= value <= MAXIMUM_WORK:
            raise ValueError("prototype limit must stay within 0..262144")
        self._limit = value

    def charge(self, kind, units=1):
        if type(units) is not int or units < 0:
            raise ValueError("invalid work charge")
        self.used += units
        self.counts[kind] = self.counts.get(kind, 0) + units
        if self.used > self.limit:
            raise BudgetExceeded(f"storage work {self.used} exceeds {self.limit}")


@dataclass(frozen=True, slots=True)
class Entry:
    value: object
    no_work: bool = False


def _check_name(name):
    if not isinstance(name, str):
        raise TypeError("name must be str with ordinary string equality/ordering")


@dataclass(frozen=True, slots=True)
class _History:
    parent: _History | None
    changes: tuple
    depth: int


def _history(meter, parent, changes):
    meter.charge("history_allocation")
    meter.charge("history_reference_copies", 3)
    meter.charge("history_parent_depth_read", int(parent is not None))
    return _History(parent, changes, 0 if parent is None else parent.depth + 1)


@dataclass(frozen=True, slots=True)
class _Layer:
    data: object
    pending: tuple


def _seal_layer(meter, data):
    """Caller must relinquish its sole mutable alias when publication commits."""
    meter.charge("pending_list_allocation")
    pending = []
    for name, entry in data.items():
        meter.charge("publication_tail_entry_visits")
        if entry is not _DELETED:
            meter.charge("pending_certificate_reads")
            if not entry.no_work:
                meter.charge("pending_list_reference_copies")
                pending.append(name)
    meter.charge("pending_tuple_allocation")
    meter.charge("pending_tuple_entry_visits", len(pending))
    meter.charge("pending_tuple_reference_copies", len(pending))
    names = tuple(pending)
    meter.charge("sealed_dictionary_proxy_allocation")
    meter.charge("sealed_dictionary_proxy_reference_copies")
    proxy = MappingProxyType(data)
    meter.charge("layer_allocation")
    meter.charge("layer_reference_copies", 2)
    return _Layer(proxy, names)


def _lookup_layers(meter, layers, name):
    for layer in reversed(layers):
        meter.charge("lookup_layer_visits")
        meter.charge("lookup_dictionary_attempts")
        entry = layer.data.get(name, MISSING)
        if entry is _DELETED:
            return MISSING
        if entry is not MISSING:
            return entry
    return MISSING


def _compact(meter, layers, tail):
    """Full oldest-to-newest compaction. Old snapshots retain their own layers."""
    meter.charge("compaction_dictionary_allocation")
    result = {}
    meter.charge("compaction_input_tuple_allocation")
    meter.charge("compaction_input_reference_copies", len(layers) + 1)
    tables = (*tuple(layer.data for layer in layers), tail)
    meter.charge("compaction_layer_reference_visits", len(layers))
    meter.charge("compaction_layer_reference_tuple_allocation")
    meter.charge("compaction_layer_reference_copies", len(layers))
    for table in tables:
        meter.charge("compaction_layer_visits")
        for name, entry in table.items():
            meter.charge("compaction_entry_visits")
            meter.charge("compaction_dictionary_attempts")
            old = result.get(name, MISSING)
            if entry is _DELETED:
                if old is not MISSING:
                    meter.charge("compaction_dictionary_deletes")
                    del result[name]
            else:
                meter.charge("compaction_dictionary_writes")
                meter.charge("compaction_reference_copies", 1 + int(old is MISSING))
                result[name] = entry
    layer = _seal_layer(meter, result)
    meter.charge("compaction_result_tuple_allocation")
    meter.charge("compaction_result_reference_copies")
    return (layer,)


class _Order:
    __slots__ = ("kind", "parents", "name", "cache")

    def __init__(self, kind, parents=(), name=None, cache=None):
        self.kind, self.parents, self.name, self.cache = kind, parents, name, cache


def _order(meter, kind, parents=(), name=None, cache=None):
    meter.charge("order_allocation")
    meter.charge("order_field_reference_copies", 4)
    if parents:
        meter.charge("order_parent_tuple_allocation")
        meter.charge("order_parent_reference_copies", len(parents))
    return _Order(kind, parents, name, cache)


def _known_order(meter, order, staged):
    meter.charge("order_cache_reads")
    if order.cache is not None:
        return order.cache
    meter.charge("order_staging_lookup")
    return staged[order]


def _seal_order_table(meter, table):
    meter.charge("order_proxy_allocation")
    meter.charge("order_proxy_reference_copies")
    return MappingProxyType(table)


def _realize_order(meter, root):
    """Build name-only order memos; publish none inside this preparation."""
    meter.charge("order_cache_reads")
    if root.cache is not None:
        return root.cache, ()
    meter.charge("order_temporary_allocations", 2)
    staged = {}
    stack = [("visit", root, None)]
    meter.charge("order_stack_record_allocations")
    meter.charge("order_stack_reference_copies", 4)
    while stack:
        meter.charge("order_stack_pops")
        action, order, detail = stack.pop()
        meter.charge("order_recipe_visits")
        if action == "visit":
            meter.charge("order_cache_reads")
            if order.cache is not None:
                continue
            meter.charge("order_staging_lookup")
            if order in staged:
                continue
            if order.kind in {"insert", "delete"}:
                meter.charge("order_edit_list_allocation")
                edits = []
                base = order
                while base.kind in {"insert", "delete"}:
                    meter.charge("order_cache_reads")
                    if base.cache is not None:
                        break
                    meter.charge("order_staging_lookup")
                    if base in staged:
                        break
                    meter.charge("order_edit_visits")
                    meter.charge("order_edit_reference_copies")
                    edits.append(base)
                    meter.charge("order_parent_reads")
                    base = base.parents[0]
                meter.charge("order_stack_record_allocations", 3)
                meter.charge("order_stack_reference_copies", 10)
                stack.append(("edit", order, (base, edits)))
                stack.append(("visit", base, None))
            elif order.kind == "union":
                meter.charge("order_stack_record_allocations")
                meter.charge("order_stack_reference_copies", 4)
                stack.append(("union", order, None))
                for parent in reversed(order.parents):
                    meter.charge("order_parent_visits")
                    meter.charge("order_stack_record_allocations")
                    meter.charge("order_stack_reference_copies", 4)
                    stack.append(("visit", parent, None))
            elif order.kind == "empty":
                meter.charge("order_dictionary_allocation")
                table = {}
                memo = _seal_order_table(meter, table)
                meter.charge("order_staging_write")
                meter.charge("order_staging_reference_copies", 2)
                staged[order] = memo
            else:
                raise AssertionError("unknown order recipe")
            continue
        meter.charge("order_dictionary_allocation")
        table = {}
        if action == "edit":
            base, edits = detail
            for name in _known_order(meter, base, staged):
                meter.charge("order_dictionary_key_visits")
                meter.charge("order_dictionary_writes")
                meter.charge("order_dictionary_reference_copies", 2)
                table[name] = None
            for edit in reversed(edits):
                meter.charge("order_edit_application_visits")
                if edit.kind == "insert":
                    meter.charge("order_dictionary_writes")
                    meter.charge("order_dictionary_reference_copies", 2)
                    table[edit.name] = None
                else:
                    meter.charge("order_dictionary_deletes")
                    del table[edit.name]
        else:
            meter.charge("order_union_view_list_allocation")
            views = []
            input_size = 0
            for parent in order.parents:
                meter.charge("order_parent_visits")
                supplied = _known_order(meter, parent, staged)
                meter.charge("order_union_input_size_reads")
                input_size += len(supplied)
                meter.charge("order_keys_view_allocation")
                view = supplied.keys()
                meter.charge("order_union_view_reference_copies")
                views.append(view)
            meter.charge("order_union_argument_tuple_allocation")
            meter.charge("order_union_argument_reference_copies", len(views))
            meter.charge("order_union_set_allocations", 2)
            meter.charge("order_union_input_visits", input_size)
            meter.charge("order_union_input_attempts", input_size)
            union = set().union(*views)
            meter.charge("order_union_unique_references", len(union))
            for name in union:
                meter.charge("order_union_output_visits")
                meter.charge("order_dictionary_writes")
                meter.charge("order_dictionary_reference_copies", 2)
                table[name] = None
        memo = _seal_order_table(meter, table)
        meter.charge("order_staging_write")
        meter.charge("order_staging_reference_copies", 2)
        staged[order] = memo
    return _known_order(meter, root, staged), staged


def _charge_cache_commit(meter, staged, extra_writes=0):
    meter.charge("cache_publication_visits", len(staged))
    meter.charge("cache_publication_writes", len(staged) + extra_writes)


def _commit_order(staged):
    if staged:
        for order, memo in staged.items():
            order.cache = memo


def _keys(owner):
    meter = owner._meter
    table, staged = _realize_order(meter, owner._order)
    meter.charge("keys_view_allocation")
    result = table.keys()
    meter.charge("keys_return_reference")
    _charge_cache_commit(meter, staged)
    _commit_order(staged)
    return result


def _ordered_items(owner):
    meter = owner._meter
    meter.charge("items_cache_reads")
    if owner._items_cache is not None:
        meter.charge("items_cached_return_reference")
        return owner._items_cache
    table, staged = _realize_order(meter, owner._order)
    meter.charge("items_result_tuple_allocation")
    meter.charge("items_pair_generator_allocation")
    def pairs():
        for name in table:
            meter.charge("items_key_visits")
            entry = owner._entry(name)
            if entry is MISSING:
                raise AssertionError("order contains an absent name")
            meter.charge("items_entry_value_reads")
            meter.charge("items_pair_allocation")
            meter.charge("items_pair_reference_copies", 2)
            meter.charge("items_result_reference_copies")
            yield name, entry.value
    result = tuple(pairs())
    meter.charge("items_return_reference")
    _charge_cache_commit(meter, staged, 1)
    _commit_order(staged)
    owner._items_cache = result
    return result


class NameVersion:
    __slots__ = ("_meter", "_layers", "_history", "_order", "_size", "_items_cache")

    def __init__(self, meter, layers, history, order, size, items_cache=None):
        meter.charge("version_allocation")
        meter.charge("version_reference_copies", 6)
        self._meter, self._layers, self._history = meter, layers, history
        self._order, self._size, self._items_cache = order, size, items_cache

    @classmethod
    def empty(cls, meter):
        meter.charge("empty_order_dictionary_allocation")
        memo = _seal_order_table(meter, {})
        return cls(meter, (), _history(meter, None, ()),
                   _order(meter, "empty", cache=memo), 0)

    def __len__(self):
        self._meter.charge("size_read")
        return self._size

    def _entry(self, name):
        return _lookup_layers(self._meter, self._layers, name)

    def get(self, name, default=None):
        _check_name(name)
        entry = self._entry(name)
        return default if entry is MISSING else entry.value

    def set(self, name, value, *, no_work=False):
        cursor = NameCursor(self)
        cursor.set(name, value, no_work=no_work)
        return cursor.snapshot()

    def delete(self, name):
        cursor = NameCursor(self)
        cursor.delete(name)
        return cursor.snapshot()

    def fork(self):
        self._meter.charge("fork_reference_copies")
        return self

    def keys(self):
        return _keys(self)

    def ordered_items(self):
        return _ordered_items(self)


@dataclass(frozen=True, slots=True)
class _Publication:
    version: NameVersion
    empty_tail: object
    changed: bool
    compacted: bool


def _prepare_publication(cursor):
    """No owner mutation, order memo publication, or exposed mutable alias."""
    meter = cursor._meter
    meter.charge("publication_tail_size_read")
    dirty = bool(cursor._tail) or cursor._order is not cursor._base._order
    if not dirty:
        meter.charge("publication_plan_allocation")
        meter.charge("publication_plan_reference_copies", 4)
        return _Publication(cursor._base, None, False, False)
    meter.charge("publication_change_tuple_allocation")
    meter.charge("publication_change_entry_visits", len(cursor._tail))
    meter.charge("publication_change_reference_copies", len(cursor._tail))
    changes = tuple(cursor._tail)
    history = _history(meter, cursor._base._history, changes)
    layers = cursor._base._layers
    compacted = False
    if cursor._tail:
        meter.charge("publication_layer_count_read")
        if len(layers) >= MAXIMUM_SEALED_LAYERS:
            layers = _compact(meter, layers, cursor._tail)
            compacted = True
        else:
            layer = _seal_layer(meter, cursor._tail)
            meter.charge("publication_layer_tuple_allocation")
            meter.charge("publication_layer_reference_copies", len(layers) + 1)
            layers = (*layers, layer)
    version = NameVersion(meter, layers, history, cursor._order,
                          cursor._size, cursor._items_cache)
    meter.charge("publication_fresh_tail_allocation")
    empty_tail = {}
    meter.charge("publication_plan_allocation")
    meter.charge("publication_plan_reference_copies", 4)
    return _Publication(version, empty_tail, True, compacted)


def _charge_publication_commit(meter, plan):
    if plan.changed:
        meter.charge("snapshot_publications")
        if plan.compacted:
            meter.charge("compaction_publication_charge")
        meter.charge("cursor_publication_reference_copies", 2)


def _commit_publication(cursor, plan):
    if plan.changed:
        # Only these two fields change: order, size, and content memo already
        # describe exactly this logical cursor. All later writes get a new tail.
        cursor._base = plan.version
        cursor._tail = plan.empty_tail


class NameCursor:
    __slots__ = ("_meter", "_base", "_tail", "_order", "_size", "_items_cache")

    def __init__(self, version):
        if not isinstance(version, NameVersion):
            raise TypeError("NameCursor requires an immutable NameVersion")
        meter = version._meter
        meter.charge("cursor_allocation")
        meter.charge("cursor_reference_copies", 6)
        meter.charge("cursor_tail_dictionary_allocation")
        self._meter, self._base, self._tail = meter, version, {}
        self._order, self._size = version._order, version._size
        self._items_cache = version._items_cache

    def __len__(self):
        self._meter.charge("size_read")
        return self._size

    def _entry(self, name):
        meter = self._meter
        meter.charge("lookup_private_tail_attempts")
        entry = self._tail.get(name, MISSING)
        if entry is _DELETED:
            return MISSING
        if entry is not MISSING:
            return entry
        return _lookup_layers(meter, self._base._layers, name)

    def get(self, name, default=None):
        _check_name(name)
        entry = self._entry(name)
        return default if entry is MISSING else entry.value

    def _replace_entry(self, name, replacement):
        """Private write. Compute/charge all new metadata before mutation."""
        meter = self._meter
        meter.charge("write_private_tail_attempts")
        tail_entry = self._tail.get(name, MISSING)
        if tail_entry is MISSING:
            old = _lookup_layers(meter, self._base._layers, name)
        else:
            old = MISSING if tail_entry is _DELETED else tail_entry
        if replacement is _DELETED and old is MISSING:
            raise KeyError(name)
        inserted = old is MISSING
        deleted = replacement is _DELETED
        order = self._order
        if inserted:
            order = _order(meter, "insert", (order,), name)
        elif deleted:
            order = _order(meter, "delete", (order,), name)
        meter.charge("write_size_read")
        size = self._size + int(inserted) - int(deleted)
        meter.charge("private_dictionary_writes")
        meter.charge("private_dictionary_reference_copies", 1 + int(tail_entry is MISSING))
        meter.charge("cursor_write_field_copies", 3)
        self._tail[name] = replacement
        self._order, self._size, self._items_cache = order, size, None

    def set(self, name, value, *, no_work=False):
        _check_name(name)
        if type(no_work) is not bool:
            raise TypeError("no_work must be bool")
        self._meter.charge("entry_allocation")
        self._meter.charge("entry_reference_copies", 2)
        self._replace_entry(name, Entry(value, no_work))

    def delete(self, name):
        _check_name(name)
        self._replace_entry(name, _DELETED)

    def snapshot(self):
        meter = self._meter
        meter.charge("snapshot_requests")
        plan = _prepare_publication(self)
        meter.charge("snapshot_return_reference")
        _charge_publication_commit(meter, plan)
        _commit_publication(self, plan)
        return plan.version

    def fork(self):
        meter = self._meter
        meter.charge("cursor_fork_requests")
        plan = _prepare_publication(self)
        result = NameCursor(plan.version)
        meter.charge("cursor_fork_return_reference")
        _charge_publication_commit(meter, plan)
        _commit_publication(self, plan)
        return result

    def keys(self):
        return _keys(self)

    def ordered_items(self):
        return _ordered_items(self)


def _common_history(meter, states):
    base = states[0]._history
    for index in range(1, len(states)):
        meter.charge("history_input_visits")
        other = states[index]._history
        while base is not other:
            meter.charge("history_identity_comparisons")
            if base is None or other is None:
                return None
            meter.charge("history_depth_reads", 2)
            if base.depth >= other.depth:
                meter.charge("history_parent_reads")
                base = base.parent
            else:
                meter.charge("history_parent_reads")
                other = other.parent
    return base


def _pending_names(meter, state):
    """Historical pending metadata is filtered through the effective newest entry."""
    meter.charge("pending_seen_dictionary_allocation")
    seen = {}
    for layer in reversed(state._layers):
        meter.charge("pending_layer_visits")
        for name in layer.pending:
            meter.charge("pending_name_visits")
            meter.charge("pending_seen_attempts")
            if name in seen:
                continue
            meter.charge("pending_seen_writes")
            meter.charge("pending_seen_reference_copies", 2)
            seen[name] = None
            entry = state._entry(name)
            if entry is not MISSING:
                meter.charge("pending_effective_certificate_reads")
                if not entry.no_work:
                    yield name


def join(meter, states, merge):
    meter.charge("join_input_tuple_allocation")
    states = tuple(state for state in states)
    meter.charge("join_input_reference_copies", len(states))
    for state in states:
        meter.charge("join_input_validation")
        if not isinstance(state, NameVersion) or state._meter is not meter:
            raise ValueError("all inputs must be immutable versions on the supplied meter")
    if not states:
        return NameVersion.empty(meter)
    if len(states) == 1:
        return states[0].fork()
    base = _common_history(meter, states)
    meter.charge("join_candidate_dictionary_allocation")
    candidates = {}
    def remember(name):
        meter.charge("candidate_dictionary_attempts")
        if name not in candidates:
            meter.charge("candidate_dictionary_writes")
            meter.charge("candidate_reference_copies", 2)
            candidates[name] = None
    for state in states:
        meter.charge("join_state_visits")
        if base is None:
            for layer in state._layers:
                meter.charge("join_unrelated_layer_visits")
                for name in layer.data:
                    meter.charge("join_unrelated_name_visits")
                    remember(name)
        else:
            token = state._history
            while token is not base:
                meter.charge("history_change_token_visits")
                for name in token.changes:
                    meter.charge("history_changed_name_visits")
                    remember(name)
                meter.charge("history_parent_reads")
                token = token.parent
        for name in _pending_names(meter, state):
            remember(name)
    cursor = NameCursor(states[0])
    for name in candidates:
        meter.charge("candidate_iteration")
        meter.charge("merge_argument_tuple_allocation")
        meter.charge("merge_argument_generator_allocation")
        def arguments():
            for state in states:
                meter.charge("merge_input_visits")
                entry = state._entry(name)
                meter.charge("merge_argument_reference_copies")
                yield MISSING if entry is MISSING else entry.value
        supplied = tuple(arguments())
        all_missing = True
        for value in supplied:
            meter.charge("merge_missing_visits")
            if value is not MISSING:
                all_missing = False
                break
        if all_missing:
            if cursor._entry(name) is not MISSING:
                cursor.delete(name)
            continue
        meter.charge("merge_callback_invocation")
        entry = merge(name, supplied)
        if not isinstance(entry, Entry) or type(entry.no_work) is not bool:
            raise TypeError("merge must return Entry(value, bool)")
        cursor._replace_entry(name, entry)
    meter.charge("order_parent_visits", len(states))
    order = _order(meter, "union", tuple(state._order for state in states))
    meter.charge("join_order_override_reference")
    cursor._order = order
    cursor._items_cache = None
    return cursor.snapshot()
