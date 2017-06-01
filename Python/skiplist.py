from random import random
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

UINT_MAX = 4294967295

class _Node:
    #Height start counting by 1
    def __init__(self, key, value = 0, height = 0):
#        logger.debug("Creating node with height %d", height)
        self.key     = key
        self.value   = value
        self.forward = [0] * height
#        logger.debug("Printing forward %s ", self.forward)

    def node_to_string(self):
#        logger.debug("Converting node to string")
        s = "--- Node ---  k: {}, v: {}".format(self.key, self.value)
        return s

    def node_with_adjacents_to_string(self):
        s_list = []
        s_list.append(self.node_to_string())
#        logger.debug("Adjacent element, level 0 to (excluded): %d ", len(self.forward))

        s_list.append ("\n\t --- Adjacents ---")
        for n in self.forward:
            s_list.append("\n\t")
            s_list.append(n.node_to_string())
        return ''.join(s_list)

class SkipList:
    #Note: level assumes counting notation starts from 0, maxLevel from 1
    def __init__(self, p, maxLevel = 1):
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
        for i in range(maxLevel):
            self.HEADER.forward.append(self.NIL)
#        logger.debug("%s", self.list_to_string())


    # Bugged: it always return 0
    # Note: must use C random for performance. However, even using python
    # random nothing changes
    def list_to_string(self):
#        logger.debug("Converting list to string")
        s_list = []
        s_list.append("--- Skiplist --- \nMaxL = {}, L = {}, p = {} "
                      .format(self.maxLevel, self.level, self.p))
        for i in range(self.maxLevel):
            s_list.append("\n\t")
            s_list.append(self.level_to_string(i))
#        logger.debug("Ending conversion")
        return ''.join(s_list)

    def level_to_string(self, l):
        if l >= self.maxLevel:
            raise ValueError("Level greater than MaxValue")

#        logger.debug("Printing Level = %d", l)
        s_list = []
        s_list.append("--- Level {} ---".format(l))
        y = self.HEADER
        s_list.append("\n\t")
        s_list.append(y.node_to_string())
        i = 0
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

    def _random_level(self):
        rand = random()
#        logger.debug("p= %f", self.p)
#        logger.debug("maxLevel= %d", self.maxLevel)

#        logger.debug("r=%f", rand)
        level = 0
        while rand < self.p and level < self.maxLevel - 1:
            level += 1
            rand = random()
#            logger.debug("r= %f", rand)
#        logger.debug("Random level generated %d ", level)
        return level

    def _update_list(self, key):
        update = [None] * (self.level + 1)
        x     = self.HEADER

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

    def get_nodes_of_level(self, l):
        if l >= self.maxLevel:
            raise ValueError("Level greater than MaxValue")

        nodes = []
        y    = self.HEADER

        while y.forward[l] != self.NIL:
            nodes.append(y)
            y = y.forward[l]
        nodes.append(y)
        nodes.append(self.NIL)
        return nodes

    def insert(self, key, value):
#        logger.debug("Inserting new node, k %s, v %s", key, value)
        if key < self.MIN_KEY_VALUE  or key > self.MAX_KEY_VALUE:
#            logger.error("Illegal key value passed to insert, key = %s", key)
            raise ValueError("Illegal key value")

        update = self._update_list(key)
        x     = update[0].forward[0]
#        if logger.getEffectiveLevel() <= logging.DEBUG:
#            logger.debug("Candidate: %s", x.node_to_string())

        lvl = self._random_level()

        if x.key == key:
#            logger.debug("Key already present, updating value")
            x.value = value
            return True
        else:
#            logger.debug("Random level selected %d", lvl)
            x = _Node(key, value, lvl + 1)
#            if logger.getEffectiveLevel() <= logging.DEBUG:
#                logger.debug("%s", x.node_to_string())

            if lvl > self.level:
#                logger.debug("Level > current level")
                for i in range(self.level + 1, lvl + 1):
                    update.append(self.HEADER)
                self.level = lvl
#                logger.debug("Printing update list")
#                if logger.getEffectiveLevel() <= logging.DEBUG:
#                    for n in update:
#                        logger.debug("%s", n.node_with_adjacents_to_string())
#                logger.debug("End update list")
            for i in range (lvl + 1):
#                    logger.debug("Iteration %d", i)
                    x.forward[i] = update[i].forward[i]
                    update[i].forward[i] = x

#            if logger.getEffectiveLevel() <= logging.DEBUG:
#                logger.debug(self.list_to_string())
            return True

    def search(self, key):
#        logger.debug("Searching node with key %s", key)
        if key < self.MIN_KEY_VALUE  or key > self.MAX_KEY_VALUE:
#            logger.error("Illegal key value passed to insert, k= %d", key)
            raise ValueError("Illegal key value")

        x = self.HEADER

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

    def delete(self, key):
#            logger.debug("Deleting node with key %s", key)
            if key < self.MIN_KEY_VALUE  or key > self.MAX_KEY_VALUE:
#                logger.error("Illegal key value passed to insert, key = %s", key)
                raise ValueError("Illegal key value")

            update = self._update_list(key)
            x     = update[0].forward[0]
#            if logger.getEffectiveLevel() <= logging.DEBUG:
#                logger.debug("Candidate: %s", x.node_to_string())

#            logger.debug(x.node_to_string())

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
