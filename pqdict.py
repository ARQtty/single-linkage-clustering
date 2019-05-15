from collections import MutableMapping as _MutableMapping
from operator import lt, gt

"""
Priority Queue Dictionary (pqdict)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A Pythonic indexed priority queue.
- O(1) search min
- O(log n) extract min
- O(log n) insert new item

Additionally, an index maps elements to their location in the heap and is kept
up to date as the heap is manipulated. As a result, pqdict also supports:
- O(1) get element by key
- O(log n) delete any item
- O(log n) increase/decrease key

Documentation at <http://pqdict.readthedocs.org/en/latest>.
:copyright: (c) 2012-2015 by Nezar Abdennur.
:license: MIT, see LICENSE for more details.

Modified 14.05.2019 by Ilya Shamov 
"""


class _Node(object):
    __slots__ = ('key', 'value', 'prio', 'prev_i', 'next_i')
    def __init__(self, key, value, prio):
        self.key = key
        self.value = value
        self.prio = prio
        self.prev_i = -1
        self.next_i = -1

    def __repr__(self):
        return self.__class__.__name__ + \
            "(%s, %s, %s) L=%s R=%s" % (repr(self.key), repr(self.value), repr(self.prio), str(self.prev_i), str(self.next_i))


class pqdict(_MutableMapping):
    """
    A collection that maps hashable objects (keys) to priority-determining
    values. The mapping is mutable so items may be added, removed and have
    their priority level updated.
    """

    def __init__(self, data=None, key=None):
        self._heap = []
        self._position = {}
        self._keyfn = key
        self._precedes = lt
        if data is not None:
            self.update(data)
        self.heapify()

    @property
    def precedes(self):
        """Priority key precedence function"""
        return self._precedes

    @property
    def keyfn(self):
        """Priority key function"""
        return self._keyfn if self._keyfn is not None else lambda x: x

    def __repr__(self):
        things = ', '.join([
            '%s: %s' % (repr(node.key), repr(node.value))
            for node in self._heap])
        return self.__class__.__name__ + '({' + things + '})'

    ############
    # dict API #
    ############
    __marker = object()
    __eq__ = _MutableMapping.__eq__
    __ne__ = _MutableMapping.__ne__
    keys = _MutableMapping.keys
    values = _MutableMapping.values
    items = _MutableMapping.items
    get = _MutableMapping.get
    clear = _MutableMapping.clear
    update = _MutableMapping.update
    setdefault = _MutableMapping.setdefault

    @classmethod
    def fromkeys(cls, iterable, value, **kwargs):
        """
        Return a new pqict mapping keys from an iterable to the same value.

        """
        return cls(((k, value) for k in iterable), **kwargs)

    def __len__(self):
        """
        Return number of items in the pqdict.

        """
        return len(self._heap)

    def __contains__(self, key):
        """
        Return ``True`` if key is in the pqdict.

        """
        return key in self._position

    def __iter__(self):
        """
        Return an iterator over the keys of the pqdict. The order of iteration
        is arbitrary! Use ``popkeys`` to iterate over keys in priority order.

        """
        for node in self._heap:
            yield node.key

    def __getitem__(self, key):
        """
        Return the priority value of ``key``. Raises a ``KeyError`` if not in
        the pqdict.

        """
        return self._heap[self._position[key]].value  # raises KeyError

    def __setitem__(self, key, newValue, node_factory=_Node):
        """
        Assign a priority  to ``key``.
        """
        heap = self._heap
        position = self._position
        keygen = self._keyfn
        try:
            pos = position[key]
        except KeyError:
            # add
            n = len(heap)
            prio = keygen(newValue) if keygen is not None else newValue
            heap.append(node_factory(key, newValue, prio))
            position[key] = n
            self._swim(n)
        else:
            # update
            #prio = keygen(value) if keygen is not None else value
            print('\nAt update get newPrio=', newPrio, '  and newVal=', newValue, '  with key=', key, "\n")
            if newPrio != None:
                heap[pos].prio = newPrio
            if newValue != None:
                heap[pos].value = newValue
            self._reheapify(pos)

    def __delitem__(self, key):
        """
        Remove item. Raises a ``KeyError`` if key is not in the pqdict.

        """
        heap = self._heap
        position = self._position
        pos = position.pop(key)  # raises KeyError
        node_to_delete = heap[pos]
        # Take the very last node and place it in the vacated spot. Let it
        # sink or swim until it reaches its new resting place.
        end = heap.pop(-1)
        if end is not node_to_delete:
            heap[pos] = end
            position[end.key] = pos
            self._reheapify(pos)
        del node_to_delete

    def pop(self, key=__marker, default=__marker):
        """
        If ``key`` is in the pqdict, remove it and return its priority value,
        else return ``default``. If ``default`` is not provided and ``key`` is
        not in the pqdict, raise a ``KeyError``.

        If ``key`` is not provided, remove the top item and return its key, or
        raise ``KeyError`` if the pqdict is empty.

        """
        heap = self._heap
        position = self._position
        # pq semantics: remove and return top *key* (value is discarded)
        if key is self.__marker:
            if not heap:
                raise KeyError('pqdict is empty')
            key = heap[0].key
            del self[key]
            return key
        # dict semantics: remove and return *value* mapped from key
        try:
            pos = position.pop(key)  # raises KeyError
        except KeyError:
            if default is self.__marker:
                raise
            return default
        else:
            node_to_delete = heap[pos]
            end = heap.pop()
            if end is not node_to_delete:
                heap[pos] = end
                position[end.key] = pos
                self._reheapify(pos)
            value = node_to_delete.value
            del node_to_delete
            return value

    ######################
    # Priority Queue API #
    ######################

    def popitem(self):
        """
        Remove and return the item with highest priority. Raises ``KeyError``
        if pqdict is empty.

        """
        heap = self._heap
        position = self._position

        try:
            end = heap.pop(-1)
        except IndexError:
            raise KeyError('pqdict is empty')

        if heap:
            node = heap[0]
            heap[0] = end
            position[end.key] = 0
            self._sink(0)
        else:
            node = end
        del position[node.key]
        return node

    def getitem(self, key):

        return self._heap[self._position[key]]

    def topitem(self):
        """
        Return the item with highest priority. Raises ``KeyError`` if pqdict is
        empty.

        """
        try:
            node = self._heap[0]
        except IndexError:
            raise KeyError('pqdict is empty')
        return node.key, node.value

    def additem(self, key, value):
        """
        Add a new item. Raises ``KeyError`` if key is already in the pqdict.

        """
        if key in self._position:
            raise KeyError('%s is already in the queue' % repr(key))
        self[key] = value

    def updateitem(self, key, new_prio=None, new_val=None):
        """
        Update the priority value of an existing item. Raises ``KeyError`` if
        key is not in the pqdict.

        """
        if key not in self._position:
            raise KeyError(key)

        heap = self._heap
        position = self._position
        pos = position[key]
        if new_prio != None:
            heap[pos].prio = new_prio
        if new_val != None:
            heap[pos].value = new_val
        self._reheapify(pos)

    def updateItemLink(self, itemKey, newPrev=None, newNext=None):
        if itemKey not in self._position:
            raise KeyError(itemKey)

        heap = self._heap
        position = self._position
        pos = position[itemKey]
        if newPrev:
            heap[pos].prev_i = newPrev
        if newNext:
            heap[pos].next_i = newNext

    def heapify(self, key=__marker):
        """
        Repair a broken heap. If the state of an item's priority value changes
        you can re-sort the relevant item only by providing ``key``.

        """
        if key is self.__marker:
            n = len(self._heap)
            for pos in reversed(range(n//2)):
                self._sink(pos)
        else:
            try:
                pos = self._position[key]
            except KeyError:
                raise KeyError(key)
            self._reheapify(pos)

    # Heap algorithms
    def _reheapify(self, pos):
        # update existing node:
        # bubble up or down depending on values of parent and children
        heap = self._heap
        precedes = self._precedes
        parent_pos = (pos - 1) >> 1
        child_pos = 2*pos + 1
        if parent_pos > -1 and precedes(heap[pos].prio, heap[parent_pos].prio):
            self._swim(pos)
        elif child_pos < len(heap):
            other_pos = child_pos + 1
            if other_pos < len(heap) and not precedes(
                    heap[child_pos].prio, heap[other_pos].prio):
                child_pos = other_pos
            if precedes(heap[child_pos].prio, heap[pos].prio):
                self._sink(pos)

    def _sink(self, top=0):
        # "Sink-to-the-bottom-then-swim" algorithm (Floyd, 1964)
        # Tends to reduce the number of comparisons when inserting "heavy"
        # items at the top, e.g. during a heap pop. See heapq for more details.
        heap = self._heap
        position = self._position
        precedes = self._precedes
        endpos = len(heap)
        # Grab the top node
        pos = top
        node = heap[pos]
        # Sift up a chain of child nodes
        child_pos = 2*pos + 1
        while child_pos < endpos:
            # Choose the smaller child.
            other_pos = child_pos + 1
            if other_pos < endpos and not precedes(
                    heap[child_pos].prio, heap[other_pos].prio):
                child_pos = other_pos
            child_node = heap[child_pos]
            # Move it up one level.
            heap[pos] = child_node
            position[child_node.key] = pos
            # Next level
            pos = child_pos
            child_pos = 2*pos + 1
        # We are left with a "vacant" leaf. Put our node there and let it swim
        # until it reaches its new resting place.
        heap[pos] = node
        position[node.key] = pos
        self._swim(pos, top)

    def _swim(self, pos, top=0):
        heap = self._heap
        position = self._position
        precedes = self._precedes
        # Grab the node from its place
        node = heap[pos]
        # Sift parents down until we find a place where the node fits.
        while pos > top:
            parent_pos = (pos - 1) >> 1
            parent_node = heap[parent_pos]
            if precedes(node.prio, parent_node.prio):
                heap[pos] = parent_node
                position[parent_node.key] = pos
                pos = parent_pos
                continue
            break
        # Put node in its new place
        heap[pos] = node
        position[node.key] = pos
