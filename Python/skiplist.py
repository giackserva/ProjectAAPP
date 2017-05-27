from random import random
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

  
class _Node:
     

    #Height start counting by 1
    def __init__(self, key, value = 0, height = 0):
        logger.debug("Creating node with height " + str(height))
        self.key = key
        self.value = value
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
            logger.error("Illegal values passed to constructor")
            raise ValueError("Illegal constructor value")
         
        self.INT_MIN = -1000
        self.INT_MAX = 1000
        self.p = p
        self.maxLevel = maxLevel
        self.level = 0
        self.HEADER = _Node(self.INT_MIN, 0, 0)
        self.NIL = _Node(self.INT_MAX, 100, 0)
        # Note: we start from level 0 (not 1 as in the paper)
        for i in range(maxLevel):
            self.HEADER.forward.append(self.NIL)
        logger.debug(self.list_to_string())
        

    def list_to_string(self):
        logger.debug("Converting list to string")
        s = "--- Skiplist --- \n" + "Max level = " + str(self.maxLevel) \
            + ", Level = " + str(self.level)
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
        while y.forward[l] != self.NIL:
            s += "\n\t" + y.forward[l].node_to_string()
            y = y.forward[l]
        s += "\n\t" + y.forward[l].node_to_string()
        return s

    def _random_level(self):
        level = 0
        while random() < self.p and level < self.maxLevel - 1:
            level += 1
        return level
             
    def _update_list(self, key):
        update = [None] * (self.level + 1)
        x = self.HEADER
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
        y = self.HEADER
        while y.forward[l] != self.NIL:
            nodes.append(y)
            y = y.forward[l]
        nodes.append(y)
        nodes.append(self.NIL)
        return nodes
         
    def insert(self, key, value):
        logger.debug("Trying to insert new node, k %s, v %s", key, value)
        if key <= self.INT_MIN or key >= self.INT_MAX:
            logger.error("Illegal key value passed to insert")
            raise ValueError("Illegal key value")
        
        update = self._update_list(key)
        x = update[0].forward[0]
        logger.debug("Candidate: " + x.node_to_string())
         
        if x.key == key:
            logger.debug("Key already present, updating value")
            x.value = value
        else:
            lvl = self._random_level()
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
                
            logger.debug(self.list_to_string())
