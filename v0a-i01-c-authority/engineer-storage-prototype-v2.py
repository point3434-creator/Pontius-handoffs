"""Isolated name-storage experiment. No production imports or authority model."""
from __future__ import annotations

from dataclasses import dataclass

MAXIMUM_WORK = 262144
MISSING = object()


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


@dataclass(frozen=True, slots=True)
class _Node:
    name: str
    entry: Entry
    left: _Node | None
    right: _Node | None
    height: int
    size: int
    pending: int


def _node(meter, name, entry, left, right):
    meter.charge("node_child_metadata_reads", (3 if left else 0) + (3 if right else 0))
    meter.charge("entry_certificate_reads")
    lh, rh = (left.height if left else 0), (right.height if right else 0)
    size = 1 + (left.size if left else 0) + (right.size if right else 0)
    pending = (not entry.no_work) + (left.pending if left else 0) + (right.pending if right else 0)
    meter.charge("node_height_comparison")
    meter.charge("node_allocation")
    meter.charge("node_reference_copies", 7)
    return _Node(name, entry, left, right, 1 + max(lh, rh), size, pending)


def _height(node):
    return node.height if node else 0


def _balance(meter, node):
    meter.charge("balance_metadata_reads", 2)
    delta = _height(node.left) - _height(node.right)
    meter.charge("balance_comparisons")
    if delta > 1:
        left = node.left
        meter.charge("balance_metadata_reads", 2)
        meter.charge("balance_comparisons")
        if _height(left.left) < _height(left.right):
            pivot = left.right
            left = _node(meter, pivot.name, pivot.entry,
                         _node(meter, left.name, left.entry, left.left, pivot.left), pivot.right)
        return _node(meter, left.name, left.entry, left.left,
                     _node(meter, node.name, node.entry, left.right, node.right))
    meter.charge("balance_comparisons")
    if delta < -1:
        right = node.right
        meter.charge("balance_metadata_reads", 2)
        meter.charge("balance_comparisons")
        if _height(right.right) < _height(right.left):
            pivot = right.left
            right = _node(meter, pivot.name, pivot.entry, pivot.left,
                          _node(meter, right.name, right.entry, pivot.right, right.right))
        return _node(meter, right.name, right.entry,
                     _node(meter, node.name, node.entry, node.left, right.left), right.right)
    return node


def _find(meter, node, name):
    while node is not None:
        meter.charge("lookup_node_visits")
        meter.charge("key_comparisons")
        if name == node.name:
            return node.entry
        meter.charge("key_comparisons")
        node = node.left if name < node.name else node.right
    return MISSING


def _set(meter, node, name, entry):
    meter.charge("set_node_visits")
    if node is None:
        return _node(meter, name, entry, None, None), True
    meter.charge("key_comparisons")
    if name == node.name:
        return _node(meter, node.name, entry, node.left, node.right), False
    meter.charge("key_comparisons")
    if name < node.name:
        left, inserted = _set(meter, node.left, name, entry)
        result = _node(meter, node.name, node.entry, left, node.right)
    else:
        right, inserted = _set(meter, node.right, name, entry)
        result = _node(meter, node.name, node.entry, node.left, right)
    return _balance(meter, result), inserted


def _delete(meter, node, name):
    meter.charge("delete_node_visits")
    if node is None:
        raise KeyError(name)
    meter.charge("key_comparisons")
    if name == node.name:
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        successor = node.right
        while successor.left is not None:
            meter.charge("delete_successor_visits")
            successor = successor.left
        right = _delete(meter, node.right, successor.name)
        return _balance(meter, _node(meter, successor.name, successor.entry, node.left, right))
    meter.charge("key_comparisons")
    if name < node.name:
        return _balance(meter, _node(meter, node.name, node.entry,
                                     _delete(meter, node.left, name), node.right))
    return _balance(meter, _node(meter, node.name, node.entry, node.left,
                                 _delete(meter, node.right, name)))


def _nodes(meter, root, pending_only=False):
    meter.charge("traversal_stack_allocation")
    stack = [root]
    meter.charge("traversal_stack_reference_copies")
    while stack:
        meter.charge("traversal_stack_pops")
        node = stack.pop()
        if node is None:
            continue
        meter.charge("traversal_node_visits")
        if pending_only and not node.pending:
            continue
        # Key ordering is irrelevant here; exact exposed order uses its recipe.
        meter.charge("traversal_child_tuple_allocation")
        meter.charge("traversal_child_reference_copies", 2)
        for child in (node.right, node.left):
            meter.charge("traversal_child_visits")
            if child is not None:
                meter.charge("traversal_stack_reference_copies")
                stack.append(child)
        if not pending_only or not node.entry.no_work:
            yield node


class _Order:
    __slots__ = ("kind", "parents", "name", "cache")

    def __init__(self, kind, parents=(), name=None, cache=None):
        self.kind, self.parents, self.name, self.cache = kind, parents, name, cache


def _order(meter, kind, parents=(), name=None, cache=None):
    meter.charge("order_allocation")
    meter.charge("order_field_reference_copies", 4)
    # Nonempty parent tuples were built by the private callers below. Retain
    # that exact tuple; do not create an unaccounted second copy here.
    if parents:
        meter.charge("order_parent_tuple_allocation")
        meter.charge("order_parent_reference_copies", len(parents))
    return _Order(kind, parents, name, cache)


def _known_keys(meter, order, staged):
    meter.charge("order_cache_reads")
    if order.cache is not None:
        return order.cache
    meter.charge("order_staging_lookup")
    return staged[order]


def _realize(meter, root):
    """Return keys plus unpublished complete memos; never mutate an order node."""
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
                meter.charge("order_staging_write")
                staged[order] = ()
            else:
                raise AssertionError("unknown order recipe")
            continue
        if action == "edit":
            base, edits = detail
            keys = _known_keys(meter, base, staged)
            meter.charge("order_dictionary_allocation")
            meter.charge("order_dictionary_key_visits", len(keys))
            meter.charge("order_dictionary_reference_copies", 2 * len(keys))
            table = dict.fromkeys(keys)
            for edit in reversed(edits):
                meter.charge("order_edit_application_visits")
                if edit.kind == "insert":
                    meter.charge("order_dictionary_reference_copies", 2)
                    table[edit.name] = None
                else:
                    meter.charge("order_dictionary_deletes")
                    del table[edit.name]
            meter.charge("order_key_tuple_allocation")
            meter.charge("order_key_iteration", len(table))
            meter.charge("order_key_reference_copies", len(table))
            keys = tuple(table)
        else:
            meter.charge("order_dictionary_list_allocation")
            tables = []
            input_size = 0
            for parent in order.parents:
                meter.charge("order_parent_visits")
                supplied = _known_keys(meter, parent, staged)
                input_size += len(supplied)
                meter.charge("order_dictionary_allocation")
                meter.charge("order_dictionary_key_visits", len(supplied))
                meter.charge("order_dictionary_reference_copies", 2 * len(supplied))
                tables.append(dict.fromkeys(supplied))
                meter.charge("order_dictionary_list_reference_copies")
            meter.charge("order_union_set_allocations", 2)
            meter.charge("order_union_input_visits", input_size)
            meter.charge("order_union_input_lookups", input_size)
            union = set().union(*(table.keys() for table in tables))
            meter.charge("order_union_unique_references", len(union))
            meter.charge("order_key_tuple_allocation")
            meter.charge("order_key_iteration", len(union))
            meter.charge("order_key_reference_copies", len(union))
            keys = tuple(union)
        meter.charge("order_staging_write")
        staged[order] = keys
    return _known_keys(meter, root, staged), staged


class NameVersion:
    __slots__ = ("_meter", "_root", "_order", "_parent", "_changes", "_depth", "_items_cache")

    def __init__(self, meter, root, order, parent, changes):
        meter.charge("version_allocation")
        meter.charge("version_reference_copies", 7)
        self._meter, self._root, self._order = meter, root, order
        self._parent, self._changes = parent, changes
        self._depth = parent._depth + 1 if parent is not None else 0
        self._items_cache = None

    @classmethod
    def empty(cls, meter):
        return cls(meter, None, _order(meter, "empty", cache=()), None, ())

    def __len__(self):
        self._meter.charge("size_read")
        return self._root.size if self._root else 0

    def get(self, name, default=None):
        _check_name(name)
        entry = _find(self._meter, self._root, name)
        return default if entry is MISSING else entry.value

    def set(self, name, value, *, no_work=False):
        _check_name(name)
        if type(no_work) is not bool:
            raise TypeError("no_work must be bool")
        meter = self._meter
        meter.charge("entry_allocation")
        meter.charge("entry_reference_copies", 2)
        root, inserted = _set(meter, self._root, name, Entry(value, no_work))
        order = _order(meter, "insert", (self._order,), name) if inserted else self._order
        meter.charge("change_tuple_allocation")
        meter.charge("change_reference_copies")
        return NameVersion(meter, root, order, self, (name,))

    def delete(self, name):
        _check_name(name)
        meter = self._meter
        root = _delete(meter, self._root, name)
        order = _order(meter, "delete", (self._order,), name)
        meter.charge("change_tuple_allocation")
        meter.charge("change_reference_copies")
        return NameVersion(meter, root, order, self, (name,))

    def fork(self):
        self._meter.charge("fork_reference_copies")
        return self

    def ordered_items(self):
        meter = self._meter
        meter.charge("items_cache_reads")
        if self._items_cache is not None:
            meter.charge("items_result_tuple_allocation")
            def copied():
                for item in self._items_cache:
                    meter.charge("items_cached_visits")
                    meter.charge("items_result_reference_copies")
                    yield item
            return tuple(copied())
        keys, staged = _realize(meter, self._order)
        meter.charge("items_index_allocation")
        index = {}
        for node in _nodes(meter, self._root):
            meter.charge("items_index_reference_copies", 2)
            index[node.name] = node.entry
        meter.charge("items_result_tuple_allocation")
        def pairs():
            for name in keys:
                meter.charge("items_key_visits")
                meter.charge("items_index_lookups")
                value = index[name].value
                meter.charge("items_pair_allocation")
                meter.charge("items_pair_reference_copies", 2)
                meter.charge("items_result_reference_copies")
                yield name, value
        result = tuple(pairs())
        # One atomic publication boundary: charge before writing any new cache.
        # Like production consume, a throwing requested charge remains spent.
        meter.charge("cache_publication_visits", len(staged))
        meter.charge("cache_publication_writes", len(staged) + 1)
        for order, materialized in staged.items():
            order.cache = materialized
        self._items_cache = result
        return result


def _check_name(name):
    if not isinstance(name, str):
        raise TypeError("name must be str with ordinary string equality/ordering")


def _common_base(meter, states):
    base = states[0]
    for index in range(1, len(states)):
        meter.charge("history_input_visits")
        other = states[index]
        while base is not other:
            meter.charge("history_identity_comparisons")
            if base is None or other is None:
                return None
            meter.charge("history_depth_reads", 2)
            if base._depth >= other._depth:
                meter.charge("history_parent_reads")
                base = base._parent
            else:
                meter.charge("history_parent_reads")
                other = other._parent
    return base


def join(meter, states, merge):
    meter.charge("join_input_tuple_allocation")
    states = tuple(state for state in states)
    meter.charge("join_input_reference_copies", len(states))
    for state in states:
        meter.charge("join_input_validation")
        if not isinstance(state, NameVersion) or state._meter is not meter:
            raise ValueError("all versions must belong to the supplied meter")
    if not states:
        return NameVersion.empty(meter)
    if len(states) == 1:
        return states[0].fork()
    base = _common_base(meter, states)
    meter.charge("join_candidate_dictionary_allocation")
    candidates = {}
    def remember(name):
        meter.charge("candidate_lookup")
        if name not in candidates:
            meter.charge("candidate_reference_copies", 2)
            candidates[name] = None
    for state in states:
        meter.charge("join_state_visits")
        if base is None:
            for node in _nodes(meter, state._root):
                remember(node.name)
        else:
            cursor = state
            while cursor is not base:
                meter.charge("history_change_version_visits")
                for name in cursor._changes:
                    meter.charge("history_changed_name_visits")
                    remember(name)
                meter.charge("history_parent_reads")
                cursor = cursor._parent
        for node in _nodes(meter, state._root, pending_only=True):
            remember(node.name)
    root = states[0]._root
    for name in candidates:
        meter.charge("candidate_iteration")
        meter.charge("merge_argument_tuple_allocation")
        def arguments():
            for state in states:
                meter.charge("merge_input_visits")
                entry = _find(meter, state._root, name)
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
            if _find(meter, root, name) is not MISSING:
                root = _delete(meter, root, name)
            continue
        meter.charge("merge_callback_invocation")
        entry = merge(name, supplied)
        if not isinstance(entry, Entry) or type(entry.no_work) is not bool:
            raise TypeError("merge must return Entry(value, bool)")
        root, _inserted = _set(meter, root, name, entry)
    meter.charge("change_tuple_allocation")
    meter.charge("change_iteration", len(candidates))
    meter.charge("change_reference_copies", len(candidates))
    changes = tuple(candidates)
    meter.charge("order_parent_visits", len(states))
    order = _order(meter, "union", tuple(state._order for state in states))
    return NameVersion(meter, root, order, states[0], changes)
