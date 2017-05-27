import logging
import skiplist
import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('Creating an instance of skiplist.Skiplist')
l = skiplist.SkipList(0.5, 8)
n_of_nodes = random.randint(5, 6)
logger.info('Creating ' + str(n_of_nodes) + ' nodes')

for i in range(n_of_nodes):
    key = random.randint(0, 999)
    value = random.randint(0, 99999)
    logger.info('Creating node with k = %d and v = %d', key, value)
    l.insert(key, value)

