import random
import  numpy as np
import time
import skiplist_no_log as skiplist
import cProfile, pstats
import logging
import io
import os

MAX_LEVEL      = 10
MIN_N_OF_NODES = 50
MAX_N_OF_NODES = 2**MAX_LEVEL

def vectorized_insert(skiplist, n_of_nodes, nodes_keys):
    #n_of_nodes = random.randint(MIN_N_OF_NODES, MAX_N_OF_NODES)
    t0 = time.time()
    for k in np.nditer(nodes_keys):
        skiplist.insert(k, 0)
    t1 = time.time()
    logging.info('CPU time for Cython insert: %.3fs', t1-t0)

def search_list(skiplist, keys):
    t0 = time.time()
    for k in np.nditer(keys):
        skiplist.search(k)
    t1 = time.time()
    logging.info('CPU time for Cython search: %.3fs', t1-t0)

def delete_list(skiplist, keys):
    t0 = time.time()
    for k in np.nditer(keys):
        skiplist.delete(k)
    t1 = time.time()
    logging.info('CPU time for Cython delete: %.3fs', t1-t0)
    
def start(number_of_nodes, max_level, p):
    logging.basicConfig(filename='profile.log', filemode='w', level=logging.INFO)
    sl = skiplist.SkipList(p, max_level)
    n_of_nodes = number_of_nodes
    logging.debug("Trying insert with n of nodes = %d ", n_of_nodes)
    nodes_keys = np.random.randint(sl.MIN_KEY_VALUE,
                                   sl.MAX_KEY_VALUE, 
                                   size=n_of_nodes)
    vectorized_insert(sl, n_of_nodes, nodes_keys)
    
    # we want to search for 10% of all keys in the ndarray of keys
    #step = n_of_nodes / 10
    #search_list(sl, nodes_keys[0:n_of_nodes:int(step)])
    search_list(sl, np.random.permutation(nodes_keys))

    delete_list(sl, np.random.permutation(nodes_keys))

def deep_profile(number_of_nodes, max_level, p):
    stream = io.open('profile.log', 'w')
    # cProfile.run('start()')
    cProfile.runctx('start(number_of_nodes, max_level, p)', globals(), locals(), '.prof')
    s = pstats.Stats('.prof', stream=stream)
    s.strip_dirs().sort_stats('time').print_stats(30)
    os.system('espeak "your program has finished"')
