import unittest
import logging
import random
from skiplist_no_log import SkipList

 
class SkipListTestCase(unittest.TestCase):
    MIN_NODES_TO_INSERT = 5
    MAX_NODES_TO_INSERT = 20
    MAX_LEVEL           = 5
    P                   = 0.5

    def setUp(self):
        self.sl = SkipList(self.P, self.MAX_LEVEL)


    def test_init(self):
        log = logging.getLogger("SkipListTestCase.test_init" )
        self.assertEqual(self.sl.level, 0)
        self.assertEqual(len(self.sl.HEADER.forward), self.sl.maxLevel)
        self.assertEqual(len(self.sl.NIL.forward), 0)

    #Note: could fail in case 2 nodes with same key will be generated
    def test_first_level_has_all_nodes_after_insert(self):
        log = logging.getLogger("SkipListTestCase.test_first_level_has_all_nodes_after_insert" )
        n_of_nodes = random.randint(self.MIN_NODES_TO_INSERT, self.MAX_NODES_TO_INSERT)
        log.debug("Number of nodes to insert = %s", n_of_nodes)
        for i in range(n_of_nodes):
            key = random.randint(self.sl.MIN_KEY_VALUE, self.sl.MAX_KEY_VALUE)
            value = random.randint(0, 99999)
            self.sl.insert(key, value)
        
        log.debug(self.sl.level_to_string(0))
        for n in self.sl.get_nodes_of_level(0):
            log.debug(n.key)
        # We have to take into account also header and nil node
        self.assertEqual(len(self.sl.get_nodes_of_level(0)), n_of_nodes + 2 )

    def test_search(self):
        log = logging.getLogger("SkipListTestCase.test_search" )
        n_of_nodes = random.randint(5, 6)
        log.debug("Number of nodes to insert = %s", n_of_nodes)
        node_to_search = random.randrange(0, n_of_nodes)
        log.debug("Among all generated nodes, we'll search the %s-th generated",
                  node_to_search)

        for i in range(n_of_nodes):
            key = random.randint(self.sl.MIN_KEY_VALUE, self.sl.MAX_KEY_VALUE)
            value = random.randint(0, 99999)
            self.sl.insert(key, value)
            if i == node_to_search:
                search_key = key
                search_value = value
                log.debug("Node to search has key = %s and value = %s", 
                              key, value )
        log.debug(self.sl.list_to_string())
        found_value = self.sl.search(search_key)
        log.debug("Found value = %s", found_value)
        self.assertEqual(found_value, search_value)

            
        
if __name__ == '__main__':
    logging.basicConfig(filename='testsuite.log', filemode='w', level=logging.DEBUG)
    logging.getLogger("SkipListTestCase.test_init").setLevel(logging.ERROR)
    logging.getLogger("SkipListTestCase.test_first_level_has_all_nodes_after_insert").setLevel(logging.ERROR)
    logging.getLogger("SkipListTestCase.test_search").setLevel(logging.ERROR)
    unittest.main()    
