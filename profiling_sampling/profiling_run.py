import my_profile as mp
import numpy as np
import sys
sys.path.insert(0, '../Python')
sys.path.insert(0, '../Cython')
sys.path.insert(0, '../Cython_malloc')
import skiplist_cython as slc
import skiplist as slp
import skiplist_malloc as slm
import random
import time
import cProfile, pstats
import io
import os

"""
Return a list of a specific type.

Keyword arguments:
n -- The type: 0 for python, 1 for cython, 2 for cython_malloc
p -- The skiplist probability (see also skiplist specifications)
max_level -- The max level of the skiplist (see also skiplist specifications)
"""
def _skiplist_implementation_type_build(n, p, max_level):
    if n == 0:
        sl = slp.SkipList(p, max_level)
    elif n == 1:
        sl = slc.SkipList(p, max_level)
    elif n == 2:
        sl = slm.SkipList(p, max_level)
    else:
        raise ValueError("Choice not valid {}".format(n))
    return sl

"""
Generate an array of random nodes keys.

Keyword arguments:
number_of_nodes -- The number of nodes to generate
min_key_value -- The minimum value for each key of a node
max_key_value -- The maximum value for each key of a node
"""
def _generate_random_node_keys(number_of_nodes, min_key_value, max_key_value):
    return np.random.randint(min_key_value, max_key_value, size=number_of_nodes)

"""
Run a basic profile, counting for each basic function of a skiplist (insert, 
delete, search). It counts the execution time of each of the functions and 
then write the result in a file under basic_profile/n/p/ and using as filename
max_level, number_of_nodes.

Keyword arguments:
number_of_nodes -- The number of nodes to generate
max_level -- The maximum level of the list
p -- The probability of the list
n -- The type of the skiplist
"""
def basic_profile(number_of_nodes, max_level, p, n):
    sl = _skiplist_implementation_type_build(n, p, max_level)
    nodes_keys = _generate_random_node_keys(number_of_nodes, sl.MIN_KEY_VALUE, sl.MAX_KEY_VALUE)

    filename = 'basic_profile/{}/{:1.2f}/ml_{:0>2}_n_{:0>8}.log'.format(n, p, max_level, number_of_nodes)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename, 'w')

    t0 = time.perf_counter()
    mp.vectorized_insert(sl, number_of_nodes, nodes_keys)
    t1 = time.perf_counter()
    f.write('CPU time for Python insert {:4.10f}\n'.format(t1-t0))

    t0 = time.perf_counter()
    mp.search_list(sl, np.random.permutation(nodes_keys))
    t1 = time.perf_counter()
    f.write('CPU time for Python search {:4.10f}\n'.format(t1-t0))

    t0 = time.perf_counter()
    mp.delete_list(sl, np.random.permutation(nodes_keys))
    t1 = time.perf_counter()
    f.write('CPU time for Python delete {:4.10f}\n'.format(t1-t0))
    f.close()

"""
Analogous to basic_profile, but using the cProfile/pstats modules.
It writes the result in a file under deep_profile/n/p/ and using as filename
max_level, number_of_nodes.


Keyword arguments:
number_of_nodes -- The number of nodes to generate
max_level -- The maximum level of the list
p -- The probability of the list
n -- The type of the skiplist
"""
def deep_profile(number_of_nodes, max_level, p, n):
    sl = _skiplist_implementation_type_build(n, p, max_level)
    nodes_keys = _generate_random_node_keys(number_of_nodes, sl.MIN_KEY_VALUE, sl.MAX_KEY_VALUE)

    filename = 'deep_profile/{}/{:1.2f}/ml_{:0>2}_n_{:0>8}.log'.format(n, p, max_level, number_of_nodes)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    stream = io.open(filename, 'w')

    cProfile.runctx('mp.vectorized_insert(sl, number_of_nodes, nodes_keys)', globals(), locals(), '.prof_v_ins')
    s = pstats.Stats('.prof_v_ins', stream=stream)
    s.strip_dirs().sort_stats('time').print_stats(30)
               
    perm = np.random.permutation(nodes_keys)
    cProfile.runctx('mp.search_list(sl, perm)', globals(), locals(), '.prof_perm_search')
    s = pstats.Stats('.prof_perm_search', stream=stream)
    s.strip_dirs().sort_stats('time').print_stats(30)
               
    perm = np.random.permutation(nodes_keys)
    cProfile.runctx('mp.delete_list(sl, perm)', globals(), locals(), '.prof_perm_delete')
    s = pstats.Stats('.prof_perm_delete', stream=stream)
    s.strip_dirs().sort_stats('time').print_stats(30)


"""
A function to take samples of the execution time of insert, search and delete.
Samples are under the directory samples/n/p and are kept into 3 different csv files
(one for insert, one for search and one for delete).
Each csv file has 3 columns: number of nodes, max level and execution time

Keyword arguments:
number_of_nodes -- The number of nodes to generate
max_level -- The maximum level of the list
p -- The probability of the list
n -- The type of the skiplist
"""
def sampling(number_of_nodes, max_level, p, n):
    filename_for_insert_samples = 'samples/{}/{:1.2f}/insert.csv'.format(n, p)
    filename_for_search_samples = 'samples/{}/{:1.2f}/search.csv'.format(n, p)
    filename_for_delete_samples = 'samples/{}/{:1.2f}/delete.csv'.format(n, p)
    os.makedirs(os.path.dirname(filename_for_insert_samples), exist_ok=True)
    os.makedirs(os.path.dirname(filename_for_search_samples), exist_ok=True)
    os.makedirs(os.path.dirname(filename_for_delete_samples), exist_ok=True)
    
    sl = _skiplist_implementation_type_build(n, p, max_level)
    nodes_keys = np.random.randint(sl.MIN_KEY_VALUE,
                sl.MAX_KEY_VALUE,
                size=number_of_nodes)

    f1 = open(filename_for_insert_samples, 'a')
    t0 = time.perf_counter()
    mp.vectorized_insert(sl, number_of_nodes, nodes_keys)
    t1 = time.perf_counter()
    f1.write('{}, {}, {:4.10f}\n'.format(number_of_nodes, max_level, t1-t0))
    f1.close()

    f2 = open(filename_for_search_samples, 'a')
    perm = np.random.permutation(nodes_keys)
    t0 = time.perf_counter()
    mp.search_list(sl, perm)
    t1 = time.perf_counter()
    f2.write('{}, {}, {:4.10f}\n'.format(number_of_nodes, max_level, t1-t0))
    f2.close()

    f3 = open(filename_for_delete_samples, 'a')
    perm = np.random.permutation(nodes_keys)
    t0 = time.perf_counter()
    mp.delete_list(sl, perm)
    t1 = time.perf_counter()
    f3.write('{}, {}, {:4.10f}\n'.format(number_of_nodes, max_level, t1-t0))
    f3.close()

# t = 0 for basic_profile, 1 for deep_profile
# n = 0, 1, 2 for python, cython, cython_malloc
"""
It run one type of profiling function for an adequate number of nodes.


Keyword arguments:
t -- The type of the profile function to run: 0 for basic_profile, 1 for 
deep_profile and 2 for sampling.
max_max_level -- The maximum among all maximum levels that you want the profile 
to run. Note that the number of nodes that will be generated depends on this
parameter.
min_min_level -- The minimum among all minimum levels that you want the profile 
to run (minimum 1)
F.e. If min_min_level = 1 and max_max_level = 4 the function will run for all 
the levels in the range [1, 4].
p -- The probability of the list
n -- The type of the skiplist
"""
def multiple_profiling(t, max_max_level, min_min_level, p, n):
    min_n_of_nodes = max_max_level
    max_n_of_nodes = 2**max_max_level

    if t == 0:
        print('Basic profile starting')
        for i in range(max_max_level, min_min_level - 1, -1):
            #n of nodes
            #The idea is to have a sampling on 10% of the range
            for j in range(max_n_of_nodes, min_n_of_nodes - 1, int(max_n_of_nodes / -10)):
                basic_profile(j, i, p, n)
    elif t == 1:
        print('Deep profile starting')
        for i in range(max_max_level, min_min_level - 1, -1):
            #n of nodes
            #The idea is to have a sampling on 10% of the range
            for j in range(max_n_of_nodes, min_n_of_nodes - 1, int(max_n_of_nodes / -10)):
                deep_profile(j, i, p, n)
    elif t == 2:
        print('Sampling enabled')
        for i in range(max_max_level, min_min_level - 1, -1):
            #n of nodes
            #The idea is to have a sampling on 10% of the range
            for j in range(max_n_of_nodes, min_n_of_nodes - 1, int(max_n_of_nodes / -10)):
                sampling(j, i, p, n)
    else:
        print('error, illegal value {}'.format(n))
"""
Run the multiple_profiling function for 3 varying parameters:
    - The different type of skiplist implementation
    - The different kind of profiles to run
    - The probability of the skiplist

See also multiple_profiling
"""
def all_night_long(min_min_level, max_max_level):
    ps = np.linspace(0.1, 0.9, num=5, endpoint=True)
    for t in range(2, -1, -1):
        for n in range(3):
            for i in range(len(ps)):
                multiple_profiling(t, max_max_level, min_min_level, ps[i], n)
