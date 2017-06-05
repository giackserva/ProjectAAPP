import sys
sys.path.insert(0, '../Python')
sys.path.insert(0, '../Cython')
sys.path.insert(0, '../Cython_malloc')
import skiplist_cython as slc
import skiplist as slp
import skiplist_malloc as slm
import my_profile as mp
import numpy as np
import math
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
append_to_path -- A string to append to the path
"""
def basic_profile(number_of_nodes, max_level, p, n, append_to_path = ''):
    sl = _skiplist_implementation_type_build(n, p, max_level)
    nodes_keys = _generate_random_node_keys(number_of_nodes, sl.MIN_KEY_VALUE,
            sl.MAX_KEY_VALUE)

    filename = 'data/basic_profile/{}/{:1.2f}/ml_{:0>2}_n_{:0>8}{}.log'.format(n, p,
            max_level, number_of_nodes, append_to_path)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = io.open(filename, 'w')

    t0 = time.perf_counter()
    mp.vectorized_insert(sl, nodes_keys)
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
append_to_path -- A string to append to the path
"""
def deep_profile(number_of_nodes, max_level, p, n, append_to_path = ''):
    sl = _skiplist_implementation_type_build(n, p, max_level)
    nodes_keys = _generate_random_node_keys(number_of_nodes,
            sl.MIN_KEY_VALUE, sl.MAX_KEY_VALUE)

    filename = 'data/deep_profile/{}/{:1.2f}/ml_{:0>2}_n_{:0>8}{}.log'.format(n, p,
            max_level, number_of_nodes, append_to_path)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    stream = io.open(filename, 'w')

    cProfile.runctx('mp.vectorized_insert(sl, nodes_keys)',
            globals(), locals(), '.prof_v_ins')
    s = pstats.Stats('.prof_v_ins', stream=stream)
    s.strip_dirs().sort_stats('time').print_stats(30)

    perm = np.random.permutation(nodes_keys)
    cProfile.runctx('mp.search_list(sl, perm)', globals(), locals(),
            '.prof_perm_search')
    s = pstats.Stats('.prof_perm_search', stream=stream)
    s.strip_dirs().sort_stats('time').print_stats(30)

    perm = np.random.permutation(nodes_keys)
    cProfile.runctx('mp.delete_list(sl, perm)', globals(), locals(),
            '.prof_perm_delete')
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
append_to_path -- A string to append to the path
"""
def sampling(number_of_nodes, max_level, p, n, append_to_path = ''):
    filename_for_insert_samples = 'data/samples/{}/{:1.2f}/insert{}.csv'.format(n,
            p, append_to_path)
    filename_for_search_samples = 'data/samples/{}/{:1.2f}/search{}.csv'.format(n,
            p, append_to_path)
    filename_for_delete_samples = 'data/samples/{}/{:1.2f}/delete{}.csv'.format(n,
            p, append_to_path)
    os.makedirs(os.path.dirname(filename_for_insert_samples), exist_ok=True)
    os.makedirs(os.path.dirname(filename_for_search_samples), exist_ok=True)
    os.makedirs(os.path.dirname(filename_for_delete_samples), exist_ok=True)

    sl = _skiplist_implementation_type_build(n, p, max_level)
    nodes_keys = _generate_random_node_keys(number_of_nodes, sl.MIN_KEY_VALUE,
            sl.MAX_KEY_VALUE)

    f1 = io.open(filename_for_insert_samples, 'a')
    t0 = time.perf_counter()
    mp.vectorized_insert(sl, nodes_keys)
    t1 = time.perf_counter()
    f1.write('{}, {}, {:4.10f}\n'.format(number_of_nodes, max_level, t1-t0))
    f1.close
    f2 = io.open(filename_for_search_samples, 'a')
    perm = np.random.permutation(nodes_keys)
    t0 = time.perf_counter()
    mp.search_list(sl, perm)
    t1 = time.perf_counter()
    f2.write('{}, {}, {:4.10f}\n'.format(number_of_nodes, max_level, t1-t0))
    f2.close()

    f3 = io.open(filename_for_delete_samples, 'a')
    perm = np.random.permutation(nodes_keys)
    t0 = time.perf_counter()
    mp.delete_list(sl, perm)
    t1 = time.perf_counter()
    f3.write('{}, {}, {:4.10f}\n'.format(number_of_nodes, max_level, t1-t0))
    f3.close()

"""
Keyword arguments:
n -- The type of the skiplist
"""
def performance_test(n, maxZeros):
    for zeros in  range(1, maxZeros + 1):
        sl = _skiplist_implementation_type_build(n, 0.5,
                math.floor(math.log(10**zeros, 2)))
        nodes_keys = _generate_random_node_keys(10**zeros, 
                sl.MIN_KEY_VALUE, sl.MAX_KEY_VALUE)

        for el in np.nditer(nodes_keys):
            sl.insert(el, 0)

        insert_time = 0
        search_time = 0
        delete_time = 0

        for i in range(100):
            ins = nodes_keys[0]
            while ins in nodes_keys:
                ins = np.random.randint(sl.MIN_KEY_VALUE, sl.MAX_KEY_VALUE)
            t0 = time.perf_counter()
            sl.insert(ins, 0)
            insert_time += time.perf_counter() - t0
            t0 = time.perf_counter()
            sl.delete(ins)
            delete_time += time.perf_counter() - t0
            ins = np.random.choice(nodes_keys)
            t0 = time.perf_counter()
            sl.search(ins)
            search_time += time.perf_counter() - t0

        #function,order of magnitude, avg time
        print('insert,{},{:.6f}'.format(zeros, insert_time / 100 * 1000))
        print('delete,{},{:.6f}'.format(zeros, delete_time / 100 * 1000))
        print('search,{},{:.6f}'.format(zeros, search_time / 100 * 1000))


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
        # i = current level
        for i in range(max_max_level, min_min_level - 1, -1):
            #j = n of nodes
            #The idea is to have a sampling on 10% of the range
            for j in range(max_n_of_nodes, min_n_of_nodes - 1,
                    int(max_n_of_nodes / -10) - 1):
                basic_profile(j, i, p, n, "_mp")
    elif t == 1:
        print('Deep profile starting')
        for i in range(max_max_level, min_min_level - 1, -1):
            #n of nodes
            #The idea is to have a sampling on 10% of the range
            for j in range(max_n_of_nodes, min_n_of_nodes - 1,
                    int(max_n_of_nodes / -10) - 1):
                deep_profile(j, i, p, n, "_dp")
    elif t == 2:
        print('Sampling enabled')
        for i in range(max_max_level, min_min_level - 1, -1):
            #n of nodes
            #The idea is to have a sampling on 10% of the range
            for j in range(max_n_of_nodes, min_n_of_nodes - 1,
                    int(max_n_of_nodes / -10) - 1):
                sampling(j, i, p, n, "_s")
    else:
        print('error, illegal value {}'.format(n))

"""
Run the multiple_profiling function for 3 varying parameters:
    - The different type of skiplist implementation
    - The different kind of profiles to run
    - The probability of the skiplist

See also multiple_profiling
"""
def variating_multiple_profiling(min_min_level, max_max_level):
    ps = np.linspace(0.1, 0.9, num=5, endpoint=True)
    for t in range(2, -1, -1):
        for n in range(3):
            for i in range(len(ps)):
                multiple_profiling(t, max_max_level, min_min_level, ps[i], n)

"""
Keyword arguments:
n -- The type of the skiplist
number_of_nodes -- The number of nodes to generate in the original list
of insert/search/delete in the original list
max_level -- The maximum level of the list
p -- The probability of the list

Return:
    The populated skiplist
"""
def create_and_populate_a_skiplist(n, max_level, p, number_of_nodes):
    sl = _skiplist_implementation_type_build(n, p, max_level)
    nodes_keys = _generate_random_node_keys(number_of_nodes, sl.MIN_KEY_VALUE,
            sl.MAX_KEY_VALUE)
    for k in np.nditer(nodes_keys):
        sl.insert(k, 1)
    return sl

"""
Take an already existing skiplist and populate it with new nodes
"""
def add_nodes_to_skiplist(sl, number_of_nodes):
    nodes_keys = _generate_random_node_keys(number_of_nodes, sl.MIN_KEY_VALUE,
            sl.MAX_KEY_VALUE)
    for k in np.nditer(nodes_keys):
        sl.insert(k, 0)
    return sl

"""
A function to take samples of the execution time of insert, search and delete.
Basically, it operates on a skiplist you provide and then it measure the 
average time to insert a node, iterating from 0 to number_of_samples - 1

Samples are under the directory samples/n/p/number_of_nodes and are kept into 3
different csv files (one for insert, one for search and one for delete).
Each csv file has 3 columns: number of nodes, max level and execution time



Keyword arguments:
number_of_samples -- The number of nodes using to take the average time


Return:
    A list containing the samples in the following order: insert, search
    and delete
"""
def sampling2(skiplist, number_of_samples):
    insert_time = 0
    search_time = 0
    delete_time = 0
    result_list = []

    # Node that the idea is to maintain the size of the list consant, while
    # measuring the average time for insert, search and delete
    for i in range(number_of_samples):
        ins = np.random.randint(skiplist.MIN_KEY_VALUE, skiplist.MAX_KEY_VALUE)
        t0 = time.perf_counter()
        inserted = skiplist.insert(ins, 0)
        insert_time += time.perf_counter() - t0
        if inserted:
            skiplist.delete(ins)
        # Otherwise the node was not inserted, only replaced with a new value

        ins = np.random.randint(skiplist.MIN_KEY_VALUE, skiplist.MAX_KEY_VALUE)
        t0 = time.perf_counter()
        skiplist.search(ins)
        search_time += time.perf_counter() - t0

        ins = np.random.randint(skiplist.MIN_KEY_VALUE, skiplist.MAX_KEY_VALUE)
        t0 = time.perf_counter()
        deleted = skiplist.delete(ins)
        delete_time += time.perf_counter() - t0
        if deleted:
            skiplist.insert(ins, 0)
        # Otherwise the node that we wanted to delete wasn't in the list

    result_list.append(insert_time / number_of_samples * 1000)
    result_list.append(search_time / number_of_samples * 1000)
    result_list.append(delete_time / number_of_samples * 1000)
    return result_list

"""
Launch multiple time sampling2 with variating parameters
    - The probability of the skip list (0.1, 0.9, step=0.2)
    - The max level of the list (min_max_level, max_max_level)
    - The number of nodes that the skiplist has

It basically generates multiple lists basing with different probabilities and
max levels. Then, add the provided number of nodes to the skiplist. Lastly, it
samples the insertion/searching/deletion time for each generated skiplist.

Argument keys:
    - The kind of skiplist (0 python, 1 cython, 2 cython malloc)
    - The max_max_level and min_max_level associated  
      [> 0 and min_max_level <= max_max_level]
    - The max_number_of_nodes for the generated skiplist [> 0]
    - The step between the number of nodes. F.e. if you select a
      max_number_of_nodes = 1000 and a step = 100, it will generate skiplist
      with a number of nodes = [1, 101, 201, 301, ..., 901]
      [> 0 and < max_number_of_nodes]
    - The minimum probability level
    - The maximum probability level
    - The step between probabilities. All these probabilities are integer.
        E.g. min_p=1, max_p=9, step=1 means [0.1, 0.2, 0.3, ..., 0.9]
    - The number_of_samples, i.e. the number of nodes for which to take
      the average performance basing on operations on the generated list 
      [> 0]

"""
def variating_sampling2(n, max_number_of_nodes, min_p, max_p, step_bw_ps,
        number_of_samples, append_to_path = '_vs2'):

    filename_samples = 'data/samples2/n_{}/p_{:1.2f}/'
    last_part_of_files = ['insert{}.csv'.format(append_to_path),
            'search{}.csv'.format(append_to_path), 
            'delete{}.csv'.format(append_to_path)] 
            
    " Variating probabilities"
    for i in range(min_p, max_p + 1, step_bw_ps):
        p = i / 10

        tmp = filename_samples.format(n, p)
        os.makedirs(os.path.dirname(tmp), exist_ok=True)

        filename_for_insert_samples = tmp + last_part_of_files[0]
        filename_for_search_samples = tmp + last_part_of_files[1]
        filename_for_delete_samples = tmp + last_part_of_files[2]
        
        with io.open(filename_for_insert_samples, 'a') as f1, \
            io.open(filename_for_search_samples, 'a') as f2, \
            io.open(filename_for_delete_samples, 'a') as f3: 
        
            k = 1
            j = 1
            while k * 10 ** j <= max_number_of_nodes:
                nd = k * 10 ** j
                ml = math.floor(math.log(nd, 1/p))
                sl = create_and_populate_a_skiplist(n, ml, p, nd)

                print("Sampling with ml={}, p={:.2f}, n={}".format(ml, p, nd))
                
                result_list = sampling2(sl, number_of_samples)
                f1.write('{}, {:4.10f}\n'.format(nd, result_list[0]))
                f2.write('{}, {:4.10f}\n'.format(nd, result_list[1]))
                f3.write('{}, {:4.10f}\n'.format(nd, result_list[2]))    

                k += 1
                if k == 10:
                    k = 1
                    j += 1

"""
Same arguments as variating_sampling2
"""
def vs2_test(n, max_number_of_nodes, min_p, max_p, step_bw_ps, number_of_samples):
    filename = 'data/tst/n_{}/minp_{}_maxp_{}.cprof'.format(
            n, min_p, max_p)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    function_call = 'variating_sampling2({}, {}, {}, {}, {}, {})'.format(
            n, max_number_of_nodes, min_p, max_p, step_bw_ps, number_of_samples)
    cProfile.runctx(function_call, globals(), locals(), '.prof')
    with io.open(filename, 'w') as stream:
        s = pstats.Stats('.prof', stream=stream)
        s.strip_dirs().sort_stats('time').print_stats(30)
