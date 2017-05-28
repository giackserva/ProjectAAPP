import unittest
import logging
import random
from skiplist import SkipList

logging.basicConfig(filename='testsuite.log', level=logging.ERROR)
 
class SkipListTestCase(unittest.TestCase):
     
    def setUp(self):
        maxLevel = random.randint(1, 100)
        p = random.random()
        self.sl = SkipList(p, maxLevel)


    def test_init(self):
        self.assertEqual(self.sl.level, 0)
        self.assertEqual(len(self.sl.HEADER.forward), self.sl.maxLevel)
        self.assertEqual(len(self.sl.NIL.forward), 0)

    #Note: could fail in case 2 nodes with same key will be generated
    def test_first_level_has_all_nodes_after_insert(self):
        n_of_nodes = random.randint(5, 10)
        logging.debug(n_of_nodes)
        for i in range(n_of_nodes):
            key = random.randint(0, 999)
            value = random.randint(0, 99999)
            self.sl.insert(key, value)
        
        logging.debug(self.sl.level_to_string(0))
        for n in self.sl.get_nodes_of_level(0):
            logging.debug(n.key)
        # We have to take into account also header and nil node
        self.assertEqual(len(self.sl.get_nodes_of_level(0)), n_of_nodes + 2 )
        
if __name__ == '__main__':
    unittest.main()    
