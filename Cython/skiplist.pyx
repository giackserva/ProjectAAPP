from libc.limits cimport INT_MAX, INT_MIN
from libc.stdlib cimport srand, rand, RAND_MAX
# To generate a random seed for the rand c function
from random import randint

import logging

logger_file = 'skiplist.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#WARN: it overwrites the file every time
fh = logging.FileHandler(logger_file, 'w')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

srand(randint(0, INT_MAX))

cdef class _Node:
    cdef public int key, value
    cdef public list forward

    #Height start counting by 1
    def __cinit__(self, int key, int value = 0, int height = 0):
        logger.debug("Creating node with height " + str(height))
        self.key     = key
        self.value   = value
        self.forward = [0] * height
        logger.debug("Printing forward" + str(self.forward))

    cpdef node_to_string(self):
        logger.debug("Converting node to string")
        s = "--- Node ---  k:" + str(self.key)+ ", v:" + str(self.value)
        return s

    cpdef node_with_adjacents_to_string(self):
        s = self.node_to_string()
        logger.debug("Adjacent element, level 0 to (excluded): " + str(len(self.forward)))
        s += "\n\t --- Adjacents ---"
        for n in self.forward:
            s += "\n\t" + n.node_to_string()
        return s

cdef class SkipList:
    cdef public int maxLevel, level
    cdef double p
    cdef _Node HEADER, NIL

    #Note: level assumes counting notation starts from 0, maxLevel from 1
    def __cinit__(self, double p, int maxLevel = 1):
        logger.debug("Initializing skip list")
        if maxLevel < 1 or p < 0:
            logger.error("Illegal values passed to constructor")
            raise ValueError("Illegal constructor value")

        self.p        = p
        self.maxLevel = maxLevel
        self.level    = 0
        self.HEADER   = _Node(INT_MIN, 0, 0)
        self.NIL      = _Node(INT_MAX, 100, 0)

        # Note: we start from level 0 (not 1 as in the paper)
        cdef int i
        for i in range(maxLevel):
            self.HEADER.forward.append(self.NIL)
        logger.debug(self.list_to_string())


    # Bugged: it always return 0
    # Note: must use C random for performance. However, even using python
    # random nothing changes
    cpdef list_to_string(self):
        logger.debug("Converting list to string")
        s = "--- Skiplist --- \n" + "Max level = " + str(self.maxLevel) \
                + ", Level = " + str(self.level) + ", p = " + str(self.p)
        cdef int i
        for i in range(self.maxLevel):
            s += "\n\t" +  self.level_to_string(i)
        logger.debug("Ending conversion")
        return s

    cpdef level_to_string(self, int l):
        if l >= self.maxLevel:
            raise ValueError("Level greater than MaxValue")

        logger.debug("Printing Level = " + str(l))
        s = "--- Level " + str(l) + " ---"
        cdef _Node y = self.HEADER
        s += "\n\t" + y.node_to_string()
        while y.forward[l] != self.NIL:
            s += "\n\t" + y.forward[l].node_to_string()
            y = y.forward[l]
        s += "\n\t" + y.forward[l].node_to_string()
        return s

    cdef int _random_level(self):
        cdef int level = 0
        cdef double random = int(rand()) / int(RAND_MAX)
        logger.debug("p="        + str(self.p))
        logger.debug("maxLevel=" + str(self.maxLevel))

        logger.debug("r="        + str(random))
        while random < self.p and level < self.maxLevel - 1:
            level += 1
            random = int(rand()) / int(RAND_MAX)
            logger.debug("r="        + str(random))
        logger.debug("Random level generated " + str(level))
        return level

    cdef list _update_list(self, int key):
        cdef list update = [None] * (self.level + 1)
        cdef _Node x     = self.HEADER
        cdef int i

        for i in range(self.level, -1, -1):
            while x.forward[i].key < key:
                x = x.forward[i]
            update[i] = x

        logger.debug("Printing update list")
        for n in update:
            logger.debug(n.node_with_adjacents_to_string())
        logger.debug("End update list")

        return update

    cpdef list get_nodes_of_level(self, int l):
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

    cpdef bint insert(self, int key, int value):
        logger.debug("Trying to insert new node, k %s, v %s", key, value)
        if key <= INT_MIN or key >= INT_MAX:
            logger.error("Illegal key value passed to insert")
            raise ValueError("Illegal key value")

        cdef list update = self._update_list(key)
        cdef _Node x     = update[0].forward[0]
        logger.debug("Candidate: " + x.node_to_string())

        cdef int lvl = self._random_level()
        cdef int i

        if x.key == key:
            logger.debug("Key already present, updating value")
            x.value = value
            return True
        else:
            logger.debug("Random level selected " + str(lvl))
            x = _Node(key, value, lvl + 1)
            logger.debug(x.node_to_string())

            if lvl > self.level:
                logger.debug("Level > current level")
                i = 0
                for i in range(self.level + 1, lvl + 1):
                    update.append(self.HEADER)
                self.level = lvl
                logger.debug("Printing update list")
                for n in update:
                    logger.debug(n.node_with_adjacents_to_string())
                logger.debug("End update list")
            i = 0
            for i in range (lvl + 1):
                try:
                    logger.debug("Iteration " + str(i))
                    x.forward[i] = update[i].forward[i]
                    logger.debug("Node appended")
                    update[i].forward[i] = x
                    logger.debug("Forward node updated")
                except IndexError as err:
                    logger.error("Error while inserting node at iteration %d", i)
                    logger.error(x.node_with_adjacents_to_string())
                    logger.error(update[i].node_with_adjacents_to_string())
                    logger.error(update[i].forward[i].node_with_adjacents_to_string())
                    return False

            logger.debug(self.list_to_string())
            return True

