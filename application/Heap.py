__author__ = 'Acko'


class HeapError(Exception):
    """ Exception derived class for heap errors """

    pass


class HeapNode(object):
    """
        Class which represents wrapper class for each item stored inside heap.

        It contains two properties, key and value. Has methods for comparing it self with
        other HeapNode instances (overloading operator<() and operator>()). Also has
        method which returns its content in tuple like form (used for returning data from heap).
    """

    def __init__(self, key, value):
        """
            Constructor of class, sets values sent as parameters to its properties.

            :param key: (object - must have overloaded operator>() and operator<()) key on which items are
                sorted inside heap
            :param value: (object) value, any type of object which will be stored inside heap
        """

        self.__key = key
        self.__value = value

    def for_return(self):
        """
            Method which creates tuple representation of node data.

            :return: (tuple) tuple wrapped instance properties
        """

        return self.__key, self.__value

    def __lt__(self, other):
        """ Overloading operator < () """

        return self.__key < other.__key

    def __gt__(self, other):
        """ Overloading operator > () """

        return self.__key > other.__key

    def __str__(self):
        """ Overriding __str__ from object """

        return '(' + str(self.__key) + ', ' + str(self.__value) + ')'


class Heap(object):
    """
        Class which represents Heap implemented by balanced, binary tree, represented as a list.

        This class is Heap implementation using balanced, binary tree, which is "default" presentation
        of heaps. Tree is represented as a list of elements, default 0-th element is None only for simplification
        of left/right child positioning.
    """

    """ Enumeration describing direction of heap (min or max key element to top) """
    HEAP_UP, HEAP_DOWN = 0, 1

    def __init__(self, direction=HEAP_DOWN):
        """
            Constructor, initializes internal list (tree) and sets __compare__ property to appropriate function
            based on direction parameter.

            :param direction: (Heap.HEAP_UP or Heap.HEAP_DOWN) shows direction in which elements should be ordered.
        """

        self.__data = [None]
        self.__compare__ = lambda a, b: (a < b if direction == self.HEAP_UP else a > b)

    def __len__(self):
        """ Overriding __len__ """

        return len(self.__data)

    def __str__(self):
        """ Overriding __str__ """

        ret_val = ''
        for el in self.__data:
            ret_val += str(el) + ', '
        return ret_val

    def __has_left_child(self, pos):
        """ Method which tells us if element on current position has left child """

        return pos * 2 < len(self.__data)

    def __has_right_child(self, pos):
        """ Method which tells us if element on current position has right child """

        return pos * 2 + 1 < len(self.__data)

    def __get_left_child(self, pos):
        """
            Method which returns left child (HeapNode instance) of element on sent position.

            :param pos: (int) position of element whose child we're looking for.
            :return: (HeapNode) left child (if exists)

            :raises: (HeapError) if element doesn't have left child
        """

        if not self.__has_left_child(pos):
            raise HeapError('Reaching out of range')
        return self.__data[pos * 2]

    def __get_right_child(self, pos):
        """
            Method which returns right child (HeapNode instance) of element on sent position.

            :param pos: (int) position of element whose child we're looking for.
            :return: (HeapNode) right child (if exists)

            :raises: (HeapError) if element doesn't have right child
        """

        if not self.__has_right_child(pos):
            raise HeapError('Reaching out of range')
        return self.__data[pos * 2 + 1]

    def __get_parent(self, pos):
        """
            Method which returns parent (HeapNode instance) of element on sent position.

            :param pos: (int) position of element whose parent we're looking for.
            :return: (HeapNode) parent (if exists)

            :raises: (HeapError) if element doesn't have parent (root node)
        """

        if pos <= 1:
            raise HeapError('Reaching out of range')
        return self.__data[pos // 2]

    def __swap(self, pos_a, pos_b):
        """ Simple helper method, swaps two elements, placed on positions sent as parameters """

        self.__data[pos_a], self.__data[pos_b] = self.__data[pos_b], self.__data[pos_a]

    def __up_heap(self, pos):
        """
            Method for sorting data when new element is inserted into structure.

            It goes from given position up to top (parent by parent) checking if child element should be
            before parent, and if true, swaps them, and checks next parent. It stops when finds parent
            which should be before given element, or when given element becomes root node.

            :param pos: (int) position of element which should be checked for going "up" on tree
        """

        while pos > 1 and self.__compare__(self.__get_parent(pos), self.__data[pos]):
            self.__swap(pos, pos // 2)
            pos //= 2

    def __down_heap(self, pos=1):
        """
            Method for sorting data when element is removed from structure.

            It goes from position (usually root node), checks for left and right children, if both exists
            then checks which should go before other one, and that one swaps with position from where started,
            if right doesn't exist, then just swaps it with left, and if neither child exists, then it stops.

            When start position is put down as far as it should go (it will always go to the bottom because
            its value (key) doesn't matter, it implies that start position should be removed), then it is
            swapped with last filled position, and after that, last filled position is freed, and up_heap is
            called with position on which initially node was dropped.

            :param pos: (int) position from which to start (default = root node)
        """

        while True:
            left = self.__get_left_child(pos) if self.__has_left_child(pos) else None
            right = self.__get_right_child(pos) if self.__has_right_child(pos) else None

            if right and left and self.__compare__(left, right):
                self.__swap(pos, pos * 2 + 1)
                pos = pos * 2 + 1
            elif left:
                self.__swap(pos, pos * 2)
                pos *= 2
            else:
                if pos != len(self.__data) - 1:
                    self.__swap(pos, len(self.__data) - 1)
                    self.__up_heap(pos)
                self.__data.pop()
                return

    def is_empty(self):
        """ Checks if heap is empty """

        return len(self.__data) == 1

    def add(self, key, value):
        """
            Public interface, method for adding new key, value pair into heap.

            :param key: (object - must have overloaded operator>() and operator<()) key, based on which objects
                are sorted.
            :param value: (object) value, any object type which should be stored in heap
        """

        self.__data.append(HeapNode(key, value))
        self.__up_heap(len(self.__data) - 1)

    def top(self):
        """ Returns first key, value pair in heap """

        if self.is_empty():
            raise HeapError("Heap empty!")
        return self.__data[1].for_return()

    def pop(self):
        """
            Public interface, method which returns first key, value pair in heap, and reorganizes other nodes.

            :return: (tuple (key, value)) first key, value pair in heap.
        """

        if self.is_empty():
            raise HeapError("Heap empty!")

        item, self.__data[1] = self.__data[1], None
        self.__down_heap()
        return item.for_return()