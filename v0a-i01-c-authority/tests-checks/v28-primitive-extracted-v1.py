"""Exact production v28 name primitive with separate original fault-injection meter.
No analyzer, protected fixture or test body is present.
Production SHA256: 4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e
"""
from __future__ import annotations
from dataclasses import dataclass
from types import MappingProxyType
import sys
MAXIMUM_WORK = 262144
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
_NAME_RADIX_BITS = 4
_NAME_LEAF_SIZE = 16  # Fixed structural split threshold, never an admission limit.
_NAME_HASH_WIDTH = sys.hash_info.width
_NAME_HASH_MASK = (1 << _NAME_HASH_WIDTH) - 1
_NAME_MISSING = object()
_NAME_DELETED = object()
@dataclass(frozen=True, slots=True)
class _NameEntry:
    value: object
    no_work: bool = False
def _name_check_name(name):
    if not isinstance(name, str):
        raise TypeError("name must be str with ordinary string equality/ordering")
@dataclass(frozen=True, slots=True)
class _NameHistory:
    parent: _NameHistory | None
    changes: tuple
    depth: int
def _name_history(meter, parent, changes):
    meter.charge("history_allocation")
    meter.charge("history_reference_copies", 3)
    meter.charge("history_parent_depth_read", int(parent is not None))
    return _NameHistory(parent, changes, 0 if parent is None else parent.depth + 1)
@dataclass(frozen=True, slots=True)
class _NameRadixLeaf:
    data: object
    pending: tuple
@dataclass(frozen=True, slots=True)
class _NameRadixBranch:
    bitmap: int
    children: tuple
    pending_count: int
class _NameLeafEdit:
    __slots__ = ("data",)

    def __init__(self, meter, data):
        meter.charge("radix_leaf_editor_allocation")
        meter.charge("radix_editor_field_reference_copies")
        self.data = data
class _NameBranchEdit:
    __slots__ = ("base", "changes")

    def __init__(self, meter, base):
        meter.charge("radix_branch_editor_allocation")
        meter.charge("radix_editor_change_dictionary_allocation")
        meter.charge("radix_editor_field_reference_copies", 2)
        self.base, self.changes = base, {}
def _name_radix_hash(meter, name):
    meter.charge("radix_hash_requests")
    meter.charge("radix_hash_normalizations")
    return hash(name) & _NAME_HASH_MASK
def _name_radix_slot(meter, hashed, shift):
    meter.charge("radix_route_steps")
    return (hashed >> shift) & 15
def _name_radix_child(meter, branch, slot):
    if branch is None:
        return None
    meter.charge("radix_bitmap_reads")
    bit = 1 << slot
    if not branch.bitmap & bit:
        return None
    meter.charge("radix_child_index_operations")
    index = (branch.bitmap & (bit - 1)).bit_count()
    meter.charge("radix_child_reference_visits")
    return branch.children[index]
def _name_radix_lookup(meter, root, name):
    meter.charge("radix_root_reads")
    if root is None:
        return _NAME_MISSING
    hashed = _name_radix_hash(meter, name)
    node, shift = root, 0
    while isinstance(node, _NameRadixBranch):
        meter.charge("radix_lookup_node_visits")
        node = _name_radix_child(meter, node, _name_radix_slot(meter, hashed, shift))
        if node is None:
            return _NAME_MISSING
        shift += _NAME_RADIX_BITS
    meter.charge("radix_lookup_node_visits")
    if shift >= _NAME_HASH_WIDTH:
        meter.charge("radix_terminal_collision_lookup_operations")
    meter.charge("radix_leaf_dictionary_attempts")
    return node.data.get(name, _NAME_MISSING)
def _name_radix_pending_count(meter, node):
    if node is None:
        return 0
    meter.charge("radix_pending_count_reads")
    return len(node.pending) if isinstance(node, _NameRadixLeaf) else node.pending_count
def _name_radix_leaf(meter, data, pending):
    """Own data/pending: no caller may mutate them after successful publication."""
    meter.charge("radix_pending_tuple_allocation")
    meter.charge("radix_pending_tuple_reference_copies", len(pending))
    names = tuple(pending)
    meter.charge("radix_leaf_proxy_allocation")
    meter.charge("radix_leaf_proxy_reference_copies")
    proxy = MappingProxyType(data)
    meter.charge("radix_leaf_allocation")
    meter.charge("radix_leaf_field_reference_copies", 2)
    return _NameRadixLeaf(proxy, names)
def _name_radix_seal_leaf(meter, data):
    meter.charge("radix_pending_list_allocation")
    pending = []
    for name, entry in data.items():
        meter.charge("radix_pending_entry_visits")
        meter.charge("radix_pending_certificate_reads")
        if not entry.no_work:
            meter.charge("radix_pending_list_reference_copies")
            pending.append(name)
    return _name_radix_leaf(meter, data, pending)
def _name_radix_copy_leaf(meter, leaf):
    meter.charge("radix_leaf_copy_dictionary_allocation")
    data = {}
    for name, entry in leaf.data.items():
        meter.charge("radix_leaf_copy_entry_visits")
        meter.charge("radix_leaf_copy_dictionary_writes")
        meter.charge("radix_leaf_copy_reference_copies", 2)
        data[name] = entry
    return _NameLeafEdit(meter, data)
def _name_radix_records(meter, data):
    meter.charge("radix_record_list_allocation")
    records = []
    for name, entry in data.items():
        meter.charge("radix_split_input_visits")
        hashed = _name_radix_hash(meter, name)
        meter.charge("radix_record_allocation")
        meter.charge("radix_record_reference_copies", 3)
        meter.charge("radix_record_list_reference_copies")
        records.append((name, entry, hashed))
    return records
def _name_radix_group(meter, records, shift):
    """One owned bucket list per occupied nibble; explicit record routing."""
    meter.charge("radix_group_dictionary_allocation")
    groups = {}
    for record in records:
        meter.charge("radix_group_record_visits")
        slot = _name_radix_slot(meter, record[2], shift)
        meter.charge("radix_group_dictionary_attempts")
        group = groups.get(slot)
        if group is None:
            meter.charge("radix_group_list_allocation")
            group = []
            meter.charge("radix_group_dictionary_writes")
            meter.charge("radix_group_reference_copies", 2)
            groups[slot] = group
        meter.charge("radix_group_list_reference_copies")
        group.append(record)
    return groups
def _name_radix_edit_records(meter, records, shift):
    """Build private paths for a split; no immutable root is yet published."""
    meter.charge("radix_record_size_reads")
    if len(records) <= _NAME_LEAF_SIZE or shift >= _NAME_HASH_WIDTH:
        if shift >= _NAME_HASH_WIDTH:
            meter.charge("radix_terminal_collision_edit_operations")
        meter.charge("radix_new_leaf_dictionary_allocation")
        data = {}
        for name, entry, _hashed in records:
            meter.charge("radix_split_leaf_entry_visits")
            meter.charge("radix_split_leaf_dictionary_writes")
            meter.charge("radix_split_leaf_reference_copies", 2)
            data[name] = entry
        return _NameLeafEdit(meter, data)
    groups = _name_radix_group(meter, records, shift)
    result = _NameBranchEdit(meter, None)
    for slot, group in groups.items():
        meter.charge("radix_group_child_visits")
        child = _name_radix_edit_records(meter, group, shift + _NAME_RADIX_BITS)
        meter.charge("radix_editor_dictionary_writes")
        meter.charge("radix_editor_child_reference_copies", 2)
        result.changes[slot] = child
    return result
def _name_radix_edit(meter, node, name, replacement, hashed, shift=0):
    """All mutations belong to an unpublished editor, never to the base root."""
    meter.charge("radix_edit_node_visits")
    if node is None:
        if replacement is _NAME_DELETED:
            return None
        meter.charge("radix_new_leaf_dictionary_allocation")
        node = _NameLeafEdit(meter, {})
    elif isinstance(node, _NameRadixLeaf):
        node = _name_radix_copy_leaf(meter, node)
    if isinstance(node, _NameLeafEdit):
        if shift >= _NAME_HASH_WIDTH:
            meter.charge("radix_terminal_collision_edit_operations")
        meter.charge("radix_leaf_edit_dictionary_attempts")
        present = name in node.data
        if replacement is _NAME_DELETED:
            if present:
                meter.charge("radix_leaf_edit_dictionary_deletes")
                del node.data[name]
        else:
            meter.charge("radix_leaf_edit_dictionary_writes")
            meter.charge("radix_leaf_edit_reference_copies", 1 + int(not present))
            node.data[name] = replacement
        meter.charge("radix_leaf_size_reads")
        if not node.data:
            return None
        if len(node.data) > _NAME_LEAF_SIZE and shift < _NAME_HASH_WIDTH:
            return _name_radix_edit_records(meter, _name_radix_records(meter, node.data), shift)
        return node
    if isinstance(node, _NameRadixBranch):
        node = _NameBranchEdit(meter, node)
    slot = _name_radix_slot(meter, hashed, shift)
    meter.charge("radix_editor_dictionary_attempts")
    old = node.changes.get(slot, _NAME_MISSING)
    if old is _NAME_MISSING:
        old = _name_radix_child(meter, node.base, slot)
        fresh_slot = True
    else:
        fresh_slot = False
    child = _name_radix_edit(meter, old, name, replacement, hashed, shift + _NAME_RADIX_BITS)
    meter.charge("radix_editor_dictionary_writes")
    meter.charge("radix_editor_child_reference_copies", 1 + int(fresh_slot))
    node.changes[slot] = child
    return node
def _name_radix_freeze(meter, node):
    """Freeze owned paths only; unchanged immutable siblings remain shared."""
    meter.charge("radix_freeze_node_visits")
    if node is None or isinstance(node, (_NameRadixLeaf, _NameRadixBranch)):
        return node
    if isinstance(node, _NameLeafEdit):
        return _name_radix_seal_leaf(meter, node.data)
    meter.charge("radix_freeze_base_reads")
    base = node.base
    meter.charge("radix_child_list_allocation")
    if base is None:
        children, bitmap, pending_count = [], 0, 0
        for slot in range(16):
            meter.charge("radix_freeze_slot_visits")
            meter.charge("radix_editor_dictionary_attempts")
            child = node.changes.get(slot, _NAME_MISSING)
            if child is _NAME_MISSING:
                child = _name_radix_child(meter, node.base, slot)
            else:
                child = _name_radix_freeze(meter, child)
            if child is not None:
                bitmap |= 1 << slot
                pending_count += _name_radix_pending_count(meter, child)
                meter.charge("radix_child_list_reference_copies")
                children.append(child)
    else:
        # All edits stay private. Each old child comes from the immutable base;
        # only packed-list ranks follow the evolving working bitmap.
        meter.charge("radix_freeze_base_metadata_reads", 3)
        base_bitmap, base_children, pending_count = base.bitmap, base.children, base.pending_count
        bitmap = base_bitmap
        meter.charge("radix_freeze_base_child_size_reads")
        meter.charge("radix_freeze_base_child_reference_copies", len(base_children))
        children = list(base_children)
        meter.charge("radix_freeze_change_view_and_iterator_allocations", 2)
        for slot, replacement in node.changes.items():
            meter.charge("radix_freeze_changed_slot_visits")
            bit = 1 << slot
            meter.charge("radix_freeze_base_slot_tests")
            if base_bitmap & bit:
                meter.charge("radix_child_index_operations")
                old_index = (base_bitmap & (bit - 1)).bit_count()
                meter.charge("radix_child_reference_visits")
                old_child = base_children[old_index]
            else:
                old_child = None
            child = _name_radix_freeze(meter, replacement)
            old_pending = _name_radix_pending_count(meter, old_child)
            new_pending = _name_radix_pending_count(meter, child)
            meter.charge("radix_freeze_pending_delta_operations", 2)
            pending_count += new_pending - old_pending
            meter.charge("radix_freeze_working_bitmap_reads")
            present = bool(bitmap & bit)
            meter.charge("radix_freeze_working_rank_operations")
            index = (bitmap & (bit - 1)).bit_count()
            if child is None:
                if present:
                    meter.charge("radix_freeze_child_delete_operations")
                    meter.charge("radix_freeze_working_child_size_reads")
                    meter.charge("radix_freeze_child_shift_reference_copies", len(children) - index - 1)
                    del children[index]
                    meter.charge("radix_freeze_working_bitmap_writes")
                    bitmap &= ~bit
            elif present:
                meter.charge("radix_freeze_child_replace_operations")
                meter.charge("radix_child_list_reference_copies")
                children[index] = child
            else:
                meter.charge("radix_freeze_child_insert_operations")
                meter.charge("radix_freeze_working_child_size_reads")
                meter.charge("radix_freeze_child_shift_reference_copies", len(children) - index)
                meter.charge("radix_child_list_reference_copies")
                children.insert(index, child)
                meter.charge("radix_freeze_working_bitmap_writes")
                bitmap |= bit
    if not children:
        return None
    meter.charge("radix_child_tuple_allocation")
    meter.charge("radix_child_tuple_reference_copies", len(children))
    frozen = tuple(children)
    meter.charge("radix_branch_allocation")
    meter.charge("radix_branch_field_reference_copies", 3)
    return _NameRadixBranch(bitmap, frozen, pending_count)
def _name_radix_bulk(meter, records, shift=0):
    """Complete unique inputs build once; no predecessor lookup or immutable set."""
    meter.charge("bulk_record_size_reads")
    if not records:
        return None
    if len(records) <= _NAME_LEAF_SIZE or shift >= _NAME_HASH_WIDTH:
        if shift >= _NAME_HASH_WIDTH:
            meter.charge("radix_terminal_collision_bulk_operations")
        meter.charge("bulk_leaf_dictionary_allocation")
        meter.charge("radix_pending_list_allocation")
        data, pending = {}, []
        for name, entry, _hashed in records:
            meter.charge("bulk_leaf_entry_visits")
            meter.charge("bulk_leaf_dictionary_writes")
            meter.charge("bulk_leaf_reference_copies", 2)
            data[name] = entry
            meter.charge("radix_pending_certificate_reads")
            if not entry.no_work:
                meter.charge("radix_pending_list_reference_copies")
                pending.append(name)
        return _name_radix_leaf(meter, data, pending)
    groups = _name_radix_group(meter, records, shift)
    meter.charge("radix_child_list_allocation")
    children, bitmap, pending_count = [], 0, 0
    for slot in range(16):
        meter.charge("bulk_slot_visits")
        meter.charge("bulk_group_dictionary_attempts")
        group = groups.get(slot)
        if group is None:
            continue
        child = _name_radix_bulk(meter, group, shift + _NAME_RADIX_BITS)
        bitmap |= 1 << slot
        pending_count += _name_radix_pending_count(meter, child)
        meter.charge("radix_child_list_reference_copies")
        children.append(child)
    meter.charge("radix_child_tuple_allocation")
    meter.charge("radix_child_tuple_reference_copies", len(children))
    frozen = tuple(children)
    meter.charge("radix_branch_allocation")
    meter.charge("radix_branch_field_reference_copies", 3)
    return _NameRadixBranch(bitmap, frozen, pending_count)
def _name_radix_names(meter, root, pending_only=False):
    """Enumerate effective names; history contains no value-bearing roots."""
    meter.charge("radix_walk_node_visits")
    if root is None:
        return
    if pending_only and not _name_radix_pending_count(meter, root):
        return
    if isinstance(root, _NameRadixLeaf):
        names = root.pending if pending_only else root.data
        for name in names:
            meter.charge("radix_walk_name_visits")
            yield name
    else:
        for child in root.children:
            meter.charge("radix_walk_child_reference_visits")
            yield from _name_radix_names(meter, child, pending_only)
class _NameOrder:
    __slots__ = ("kind", "parents", "name", "cache")

    def __init__(self, kind, parents=(), name=None, cache=None):
        self.kind, self.parents, self.name, self.cache = kind, parents, name, cache
def _name_order(meter, kind, parents=(), name=None, cache=None):
    meter.charge("order_allocation")
    meter.charge("order_field_reference_copies", 4)
    if parents:
        meter.charge("order_parent_tuple_allocation")
        meter.charge("order_parent_reference_copies", len(parents))
    return _NameOrder(kind, parents, name, cache)
def _name_known_order(meter, order, staged):
    meter.charge("order_cache_reads")
    if order.cache is not None:
        return order.cache
    meter.charge("order_staging_lookup")
    return staged[order]
def _name_seal_order_table(meter, table):
    meter.charge("order_proxy_allocation")
    meter.charge("order_proxy_reference_copies")
    return MappingProxyType(table)
def _name_realize_order(meter, root):
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
                memo = _name_seal_order_table(meter, table)
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
            for name in _name_known_order(meter, base, staged):
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
                supplied = _name_known_order(meter, parent, staged)
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
        memo = _name_seal_order_table(meter, table)
        meter.charge("order_staging_write")
        meter.charge("order_staging_reference_copies", 2)
        staged[order] = memo
    return _name_known_order(meter, root, staged), staged
def _name_charge_cache_commit(meter, staged, extra_writes=0):
    meter.charge("cache_publication_visits", len(staged))
    meter.charge("cache_publication_writes", len(staged) + extra_writes)
def _name_commit_order(staged):
    if staged:
        for order, memo in staged.items():
            order.cache = memo
def _name_keys(owner):
    meter = owner._meter
    table, staged = _name_realize_order(meter, owner._order)
    meter.charge("keys_view_allocation")
    result = table.keys()
    meter.charge("keys_return_reference")
    _name_charge_cache_commit(meter, staged)
    _name_commit_order(staged)
    return result
def _name_ordered_items(owner):
    meter = owner._meter
    meter.charge("items_cache_reads")
    if owner._items_cache is not None:
        meter.charge("items_cached_return_reference")
        return owner._items_cache
    table, staged = _name_realize_order(meter, owner._order)
    meter.charge("items_result_tuple_allocation")
    meter.charge("items_pair_generator_allocation")
    def pairs():
        for name in table:
            meter.charge("items_key_visits")
            entry = owner._entry(name)
            if entry is _NAME_MISSING:
                raise AssertionError("order contains an absent name")
            meter.charge("items_entry_value_reads")
            meter.charge("items_pair_allocation")
            meter.charge("items_pair_reference_copies", 2)
            meter.charge("items_result_reference_copies")
            yield name, entry.value
    result = tuple(pairs())
    meter.charge("items_return_reference")
    _name_charge_cache_commit(meter, staged, 1)
    _name_commit_order(staged)
    owner._items_cache = result
    return result
class _NameVersion:
    __slots__ = ("_meter", "_root", "_history", "_order", "_size", "_items_cache")

    def __init__(self, meter, root, history, order, size, items_cache=None):
        meter.charge("version_allocation")
        meter.charge("version_reference_copies", 6)
        self._meter, self._root, self._history = meter, root, history
        self._order, self._size, self._items_cache = order, size, items_cache

    @classmethod
    def empty(cls, meter):
        meter.charge("empty_order_dictionary_allocation")
        memo = _name_seal_order_table(meter, {})
        return cls(meter, None, _name_history(meter, None, ()),
                   _name_order(meter, "empty", cache=memo), 0)


    @classmethod
    def from_unique_entries(cls, meter, entries):
        """One staged detached build; input iteration itself is not rolled back."""
        meter.charge("bulk_input_iterator_requests")
        meter.charge("bulk_record_list_allocation")
        meter.charge("bulk_order_dictionary_allocation")
        records, order = [], {}
        for pair in entries:
            meter.charge("bulk_input_visits")
            meter.charge("bulk_pair_validation")
            if type(pair) is not tuple or len(pair) != 2:
                raise TypeError("bulk entries must be two-element tuples")
            name, entry = pair
            meter.charge("bulk_key_validation")
            _name_check_name(name)
            meter.charge("bulk_entry_validation")
            if type(entry) is not _NameEntry or type(entry.no_work) is not bool:
                raise TypeError("bulk entries require exact Entry(value, bool)")
            meter.charge("bulk_uniqueness_attempts")
            if name in order:
                raise ValueError("bulk input contains a duplicate name")
            meter.charge("bulk_order_writes")
            meter.charge("bulk_order_reference_copies", 2)
            order[name] = None
            hashed = _name_radix_hash(meter, name)
            meter.charge("bulk_record_allocation")
            meter.charge("bulk_record_reference_copies", 3)
            meter.charge("bulk_record_list_reference_copies")
            records.append((name, entry, hashed))
        root = _name_radix_bulk(meter, records)
        memo = _name_seal_order_table(meter, order)
        history = _name_history(meter, None, ())
        recipe = _name_order(meter, "known", cache=memo)
        meter.charge("bulk_size_reads")
        result = cls(meter, root, history, recipe, len(order))
        meter.charge("bulk_return_reference")
        return result


    def __len__(self):
        self._meter.charge("size_read")
        return self._size

    def _entry(self, name):
        return _name_radix_lookup(self._meter, self._root, name)

    def get(self, name, default=None):
        _name_check_name(name)
        entry = self._entry(name)
        return default if entry is _NAME_MISSING else entry.value

    def set(self, name, value, *, no_work=False):
        cursor = _NameCursor(self)
        cursor.set(name, value, no_work=no_work)
        return cursor.snapshot()

    def delete(self, name):
        cursor = _NameCursor(self)
        cursor.delete(name)
        return cursor.snapshot()

    def fork(self):
        self._meter.charge("fork_reference_copies")
        return self

    def keys(self):
        return _name_keys(self)

    def ordered_items(self):
        return _name_ordered_items(self)
@dataclass(frozen=True, slots=True)
class _NamePublication:
    version: _NameVersion
    empty_tail: object
    changed: bool
def _name_prepare_publication(cursor):
    """Stage private index paths/history; no owner or order-cache mutation."""
    meter = cursor._meter
    meter.charge("publication_tail_size_read")
    dirty = bool(cursor._tail) or cursor._order is not cursor._base._order
    if not dirty:
        meter.charge("publication_plan_allocation")
        meter.charge("publication_plan_reference_copies", 3)
        return _NamePublication(cursor._base, None, False)
    meter.charge("publication_change_tuple_allocation")
    meter.charge("publication_change_entry_visits", len(cursor._tail))
    meter.charge("publication_change_reference_copies", len(cursor._tail))
    changes = tuple(cursor._tail)
    history = _name_history(meter, cursor._base._history, changes)
    root = cursor._base._root
    for name, replacement in cursor._tail.items():
        meter.charge("publication_private_entry_visits")
        root = _name_radix_edit(meter, root, name, replacement, _name_radix_hash(meter, name))
    if cursor._tail:
        root = _name_radix_freeze(meter, root)
    version = _NameVersion(meter, root, history, cursor._order,
                          cursor._size, cursor._items_cache)
    meter.charge("publication_fresh_tail_allocation")
    empty_tail = {}
    meter.charge("publication_plan_allocation")
    meter.charge("publication_plan_reference_copies", 3)
    return _NamePublication(version, empty_tail, True)
def _name_charge_publication_commit(meter, plan):
    if plan.changed:
        meter.charge("snapshot_publications")
        meter.charge("cursor_publication_reference_copies", 2)
def _name_commit_publication(cursor, plan):
    if plan.changed:
        cursor._base = plan.version
        cursor._tail = plan.empty_tail
class _NameCursor:
    __slots__ = ("_meter", "_base", "_tail", "_order", "_size", "_items_cache")

    def __init__(self, version):
        if not isinstance(version, _NameVersion):
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
        entry = self._tail.get(name, _NAME_MISSING)
        if entry is _NAME_DELETED:
            return _NAME_MISSING
        if entry is not _NAME_MISSING:
            return entry
        return _name_radix_lookup(meter, self._base._root, name)

    def get(self, name, default=None):
        _name_check_name(name)
        entry = self._entry(name)
        return default if entry is _NAME_MISSING else entry.value

    def _replace_entry(self, name, replacement):
        """Private write. Compute/charge all new metadata before mutation."""
        meter = self._meter
        meter.charge("write_private_tail_attempts")
        tail_entry = self._tail.get(name, _NAME_MISSING)
        if tail_entry is _NAME_MISSING:
            old = _name_radix_lookup(meter, self._base._root, name)
        else:
            old = _NAME_MISSING if tail_entry is _NAME_DELETED else tail_entry
        if replacement is _NAME_DELETED and old is _NAME_MISSING:
            raise KeyError(name)
        inserted = old is _NAME_MISSING
        deleted = replacement is _NAME_DELETED
        order = self._order
        if inserted:
            order = _name_order(meter, "insert", (order,), name)
        elif deleted:
            order = _name_order(meter, "delete", (order,), name)
        meter.charge("write_size_read")
        size = self._size + int(inserted) - int(deleted)
        meter.charge("private_dictionary_writes")
        meter.charge("private_dictionary_reference_copies", 1 + int(tail_entry is _NAME_MISSING))
        meter.charge("cursor_write_field_copies", 3)
        self._tail[name] = replacement
        self._order, self._size, self._items_cache = order, size, None

    def set(self, name, value, *, no_work=False):
        _name_check_name(name)
        if type(no_work) is not bool:
            raise TypeError("no_work must be bool")
        self._meter.charge("entry_allocation")
        self._meter.charge("entry_reference_copies", 2)
        self._replace_entry(name, _NameEntry(value, no_work))

    def delete(self, name):
        _name_check_name(name)
        self._replace_entry(name, _NAME_DELETED)

    def snapshot(self):
        meter = self._meter
        meter.charge("snapshot_requests")
        plan = _name_prepare_publication(self)
        meter.charge("snapshot_return_reference")
        _name_charge_publication_commit(meter, plan)
        _name_commit_publication(self, plan)
        return plan.version

    def fork(self):
        meter = self._meter
        meter.charge("cursor_fork_requests")
        plan = _name_prepare_publication(self)
        result = _NameCursor(plan.version)
        meter.charge("cursor_fork_return_reference")
        _name_charge_publication_commit(meter, plan)
        _name_commit_publication(self, plan)
        return result

    def keys(self):
        return _name_keys(self)

    def ordered_items(self):
        return _name_ordered_items(self)
def _name_common_history(meter, states):
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
def _name_pending_names(meter, state):
    """Only effective pending entries exist in the current immutable root."""
    yield from _name_radix_names(meter, state._root, pending_only=True)
def _join_name_versions(meter, states, merge):
    meter.charge("join_input_tuple_allocation")
    states = tuple(state for state in states)
    meter.charge("join_input_reference_copies", len(states))
    for state in states:
        meter.charge("join_input_validation")
        if not isinstance(state, _NameVersion) or state._meter is not meter:
            raise ValueError("all inputs must be immutable versions on the supplied meter")
    if not states:
        return _NameVersion.empty(meter)
    if len(states) == 1:
        return states[0].fork()
    base = _name_common_history(meter, states)
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
            for name in _name_radix_names(meter, state._root):
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
        for name in _name_pending_names(meter, state):
            remember(name)
    cursor = _NameCursor(states[0])
    for name in candidates:
        meter.charge("candidate_iteration")
        meter.charge("merge_argument_tuple_allocation")
        meter.charge("merge_argument_generator_allocation")
        def arguments():
            for state in states:
                meter.charge("merge_input_visits")
                entry = state._entry(name)
                meter.charge("merge_argument_reference_copies")
                yield _NAME_MISSING if entry is _NAME_MISSING else entry.value
        supplied = tuple(arguments())
        all_missing = True
        for value in supplied:
            meter.charge("merge_missing_visits")
            if value is not _NAME_MISSING:
                all_missing = False
                break
        if all_missing:
            if cursor._entry(name) is not _NAME_MISSING:
                cursor.delete(name)
            continue
        meter.charge("merge_callback_invocation")
        entry = merge(name, supplied)
        if not isinstance(entry, _NameEntry) or type(entry.no_work) is not bool:
            raise TypeError("merge must return Entry(value, bool)")
        cursor._replace_entry(name, entry)
    meter.charge("order_parent_visits", len(states))
    order = _name_order(meter, "union", tuple(state._order for state in states))
    meter.charge("join_order_override_reference")
    cursor._order = order
    cursor._items_cache = None
    return cursor.snapshot()
Entry = _NameEntry
MISSING = _NAME_MISSING
NameVersion = _NameVersion
NameCursor = _NameCursor
join = _join_name_versions
_NameMeter = Meter
