# cython: profile=True
from libc.limits cimport UINT_MAX
from libc.stdlib cimport srand, rand, RAND_MAX
# To generate a random seed for the rand c function
from random import randint
# Used for fast string concatenation
from io import StringIO
#import logging

#logger_file = 'skiplist.log'
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.ERROR)

#WARN: it overwrites the file every time
#fh = logging.FileHandler(logger_file, 'w')
#fh.setLevel(logging.DEBUG)
#ch = logging.StreamHandler()
#ch.setLevel(logging.ERROR)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#fh.setFormatter(formatter)
#ch.setFormatter(formatter)
#logger.addHandler(fh)
#logger.addHandler(ch)

#logger.disabled = True

srand(randint(0, RAND_MAX))


cdef class _Node:
    cdef public unsigned int value
    cdef public unsigned int key
    cdef public list forward

    #Height start counting by 1
    def __cinit__(self, unsigned int key, int value = 0, unsigned short height = 0):
#        logger.debug("Creating node with height %d", height)
        self.key     = key
        self.value   = value
        self.forward = [0] * height
#        logger.debug("Printing forward %s ", self.forward)

    cpdef node_to_string(self):
#        logger.debug("Converting node to string")
        s = "--- Node ---  k: {}, v: {}".format(self.key, self.value)
        return s

    cpdef node_with_adjacents_to_string(self):
        s_list = []
        s_list.append(self.node_to_string())
#        logger.debug("Adjacent element, level 0 to (excluded): %d ", len(self.forward))

        s_list.append ("\n\t --- Adjacents ---")
        for n in self.forward:
            s_list.append("\n\t")
            s_list.append(n.node_to_string())
        return ''.join(s_list)

cdef class SkipList:
    cdef public unsigned short maxLevel, level
    cdef readonly float p
    cdef readonly _Node HEADER, NIL
    cpdef readonly unsigned int MIN_KEY_VALUE
    cpdef readonly unsigned MAX_KEY_VALUE

    #Note: level assumes counting notation starts from 0, maxLevel from 1
    def __cinit__(self, float p, unsigned short maxLevel = 1):
#        logger.debug("Initializing skip list")
        if maxLevel < 1 or p < 0:
#            logger.error("Illegal values passed to constructor, maxL=%d, p=%f", maxLevel, p)
            raise ValueError("Illegal constructor value")

        self.p        = p
        self.maxLevel = maxLevel
        self.level    = 0
        self.MIN_KEY_VALUE = 1
        self.MAX_KEY_VALUE = UINT_MAX - 2
        self.HEADER   = _Node(self.MIN_KEY_VALUE, 0, 0)
        self.NIL      = _Node(self.MAX_KEY_VALUE, 100, 0)

        # Note: we start from level 0 (not 1 as in the paper)
        cdef unsigned short i
        for i in range(maxLevel):
            self.HEADER.forward.append(self.NIL)
#        logger.debug("%s", self.list_to_string())


    # Bugged: it always return 0
    # Note: must use C random for performance. However, even using python
    # random nothing changes
    cpdef list_to_string(self):
#        logger.debug("Converting list to string")
        s_list = []
        s_list.append("--- Skiplist --- \nMaxL = {}, L = {}, p = {} "
                      .format(self.maxLevel, self.level, self.p))
        cdef unsigned short i
        for i in range(self.maxLevel):
            s_list.append("\n\t")
            s_list.append(self.level_to_string(i))
#        logger.debug("Ending conversion")
        return ''.join(s_list)

    cpdef level_to_string(self, int l):
        if l >= self.maxLevel:
            raise ValueError("Level greater than MaxValue")

#        logger.debug("Printing Level = %d", l)
        s_list = []
        s_list.append("--- Level {} ---".format(l))
        cdef _Node y = self.HEADER
        s_list.append("\n\t")
        s_list.append(y.node_to_string())
        cdef int i = 1
        while y.forward[l] != self.NIL:
            s_list.append("\n\t")
            s_list.append(y.forward[l].node_to_string())
            y = y.forward[l]
            i += 1
        s_list.append("\n\t")
        s_list.append(y.forward[l].node_to_string())
        s_list.append("\n--- End of level, {} node present, including HEADER and NIL ---"
                      .format(i+1))
        return ''.join(s_list)

    cdef unsigned short _random_level(self):
        cdef unsigned short level = 0
        cdef float random = int(rand()) / int(RAND_MAX)
#        logger.debug("p= %f", self.p)
#        logger.debug("maxLevel= %d", self.maxLevel)

#        logger.debug("r=%f", random)
        while random < self.p and level < self.maxLevel - 1:
            level += 1
            random = int(rand()) / int(RAND_MAX)
#            logger.debug("r= %f", random)
#        logger.debug("Random level generated %d ", level)
        return level

    cdef list _update_list(self, unsigned int key):
        cdef list update = [None] * (self.level + 1)
        cdef _Node x     = self.HEADER
        cdef unsigned short i

        for i in range(self.level, -1, -1):
            while x.forward[i].key < key:
                x = x.forward[i]
            update[i] = x

#        logger.debug("Printing update list")

#        if logger.getEffectiveLevel() <= logging.DEBUG:
#            for n in update:
#                logger.debug("%s", n.node_with_adjacents_to_string())
#        logger.debug("End update list")

        return update

    cpdef list get_nodes_of_level(self, unsigned short l):
        if l >= self.maxLevel:
            raise ValueError("Level greater than MaxValue")

        cdef list nodes = []
        cdef _Node y    = self.HEADER

        while y.forward[l] != self.NIL:
            nodes.append(y)
            y = y.forward[l]
        nodes.append(y)
        nodes.append(self.NIL)
        return nodes

    cpdef bint insert(self, unsigned int key, int value):
#        logger.debug("Inserting new node, k %s, v %s", key, value)
        if key < self.MIN_KEY_VALUE  or key > self.MAX_KEY_VALUE:
#            logger.error("Illegal key value passed to insert, key = %s", key)
            raise ValueError("Illegal key value")

        cdef list update = self._update_list(key)
        cdef _Node x     = update[0].forward[0]
#        if logger.getEffectiveLevel() <= logging.DEBUG:
#            logger.debug("Candidate: %s", x.node_to_string())

        cdef unsigned short lvl = self._random_level()
        cdef unsigned short i

        if x.key == key:
#            logger.debug("Key already present, updating value")
            x.value = value
            return False
        else:
#            logger.debug("Random level selected %d", lvl)
            x = _Node(key, value, lvl + 1)
#            if logger.getEffectiveLevel() <= logging.DEBUG:
#                logger.debug("%s", x.node_to_string())

            if lvl > self.level:
#                logger.debug("Level > current level")
                i = 0
                for i in range(self.level + 1, lvl + 1):
                    update.append(self.HEADER)
                self.level = lvl
#                logger.debug("Printing update list")
#                if logger.getEffectiveLevel() <= logging.DEBUG:
#                    for n in update:
#                        logger.debug("%s", n.node_with_adjacents_to_string())
#                logger.debug("End update list")
            i = 0
            for i in range (lvl + 1):
#                    logger.debug("Iteration %d", i)
                    x.forward[i] = update[i].forward[i]
                    update[i].forward[i] = x

#            if logger.getEffectiveLevel() <= logging.DEBUG:
#                logger.debug(self.list_to_string())
            return True

    cpdef int search(self, unsigned int key):
#        logger.debug("Searching node with key %s", key)
        if key < self.MIN_KEY_VALUE  or key > self.MAX_KEY_VALUE:
#            logger.error("Illegal key value passed to insert, k= %d", key)
            raise ValueError("Illegal key value")

        cdef _Node x = self.HEADER

        cdef unsigned short i = self.level
        for i in range(self.level, -1, -1):
#            logger.debug("Searching at level %s", i)
            while x.forward[i].key < key:
#                logger.debug("Next key is %s, traversing", x.forward[i].key)
                x = x.forward[i]
        x = x.forward[0]
        if x.key == key:
#            logger.debug("Node found, value = %s", x.value)
            return x.value
        else:
#            logger.debug("Node not found")
            return -1

    cpdef bint delete(self, unsigned int key):
#            logger.debug("Deleting node with key %s", key)
            if key < self.MIN_KEY_VALUE  or key > self.MAX_KEY_VALUE:
#                logger.error("Illegal key value passed to insert, key = %s", key)
                raise ValueError("Illegal key value")

            cdef list update = self._update_list(key)
            cdef _Node x     = update[0].forward[0]
#            if logger.getEffectiveLevel() <= logging.DEBUG:
#                logger.debug("Candidate: %s", x.node_to_string())

#            logger.debug(x.node_to_string())
            cdef unsigned short i = 1

            if x.key == key:
#                logger.debug("Key present, deleting it")
                for i in range(0, self.level):
                    if update[i].forward[i] != x: break
                    update[i].forward[i] = x.forward[i]
                while self.level > 0 and self.HEADER.forward[self.level] == self.NIL:
                    self.level -=1
                return True
            else:
                return False
