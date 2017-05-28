# To generate a random seed for the rand c function
import random
import logging


logger_file = 'skiplist.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

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

class _Node:
    #Height start counting by 1
    def __init__(self, key, value = 0, height = 0):
        logger.debug("Creating node with height " + str(height))
        self.key     = key
        self.value   = value
        self.forward = [0] * height
        logger.debug("Printing forward" + str(self.forward))

    def node_to_string(self):
        logger.debug("Converting node to string")
        s = "--- Node ---  k:" + str(self.key)+ ", v:" + str(self.value)
        return s

    def node_with_adjacents_to_string(self):
        s = self.node_to_string()
        logger.debug("Adjacent element, level 0 to (excluded): " + str(len(self.forward)))
        s += "\n\t --- Adjacents ---"
        for n in self.forward:
            s += "\n\t" + n.node_to_string()
        return s

class SkipList:
    #Note: level assumes counting notation starts from 0, maxLevel from 1
    def __init__(self, p, maxLevel = 1):
        logger.debug("Initializing skip list")
        if maxLevel < 1 or p < 0:
            s = ("Illegal values passed to constructor: maxLevel = "
                 + str(maxLevel)
                 + ", p = "
                 + str(p))
            logger.error(s)
            raise ValueError(s)

        self.p        = p
        self.maxLevel = maxLevel
        self.level    = 0
        self.MAX_KEY_VALUE = 429496729333
        self.MIN_KEY_VALUE = 1
        self.HEADER   = _Node(self.MIN_KEY_VALUE - 1, 0, 0)
        self.NIL      = _Node(self.MAX_KEY_VALUE + 1, 100, 0)

        # Note: we start from level 0 (not 1 as in the paper)
        for i in range(maxLevel):
            self.HEADER.forward.append(self.NIL)
        logger.debug(self.list_to_string())


    # Bugged: it always return 0
    # Note: must use C random for performance. However, even using python
    # random nothing changes
    def list_to_string(self):
        logger.debug("Converting list to string")
        s = "--- Skiplist --- \n" + "Max level = " + str(self.maxLevel) \
                + ", Level = " + str(self.level) + ", p = " + str(self.p)
        for i in range(self.maxLevel):
            s += "\n\t" +  self.level_to_string(i)
        logger.debug("Ending conversion")
        return s

    def level_to_string(self, l):
        if l >= self.maxLevel:
            raise ValueError("Level greater than MaxValue")

        logger.debug("Printing Level = " + str(l))
        s = "--- Level " + str(l) + " ---"
        y = self.HEADER
        s += "\n\t" + y.node_to_string()
        i = 1
        while y.forward[l] != self.NIL:
            s += "\n\t" + y.forward[l].node_to_string()
            y = y.forward[l]
            i += 1
        s += "\n\t" + y.forward[l].node_to_string()
        s += "\n--- End of level, " + str(i + 1) + " node present, including \
                HEADER and NIL ---"
        return s

    def _random_level(self):
        level = 0
        rand = random.random()
        logger.debug("p="        + str(self.p))
        logger.debug("maxLevel=" + str(self.maxLevel))

        logger.debug("r="        + str(rand))
        while rand < self.p and level < self.maxLevel - 1:
            level += 1
            rand = random.random()
            logger.debug("r="        + str(rand))
        logger.debug("Random level generated " + str(level))
        return level

    def _update_list(self, key):
        update = [None] * (self.level + 1)
        x     = self.HEADER

        for i in range(self.level, -1, -1):
            while x.forward[i].key < key:
                x = x.forward[i]
            update[i] = x

        logger.debug("Printing update list")
        for n in update:
            logger.debug(n.node_with_adjacents_to_string())
        logger.debug("End update list")

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
        logger.debug("Trying to insert new node, k %s, v %s", key, value)
        if key <= 0 or key >= self.MAX_KEY_VALUE:
            logger.error("Illegal key value passed to insert " + str(key))
            raise ValueError("Illegal key value " + str(key))
         

        update = self._update_list(key)
        x     = update[0].forward[0]
        logger.debug("Candidate: " + x.node_to_string())

        lvl = self._random_level()

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
                for i in range(self.level + 1, lvl + 1):
                    update.append(self.HEADER)
                self.level = lvl
                logger.debug("Printing update list")
                for n in update:
                    logger.debug(n.node_with_adjacents_to_string())
                logger.debug("End update list")

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

