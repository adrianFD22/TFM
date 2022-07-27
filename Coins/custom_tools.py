import random
import multiprocessing as mp
from itertools import chain, combinations
import math
import sys, os


def random_combination(iterable, r):
    # Random selection from itertools.combinations(iterable, r)
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(range(n), r))
    return tuple(pool[i] for i in indices)


def powerset(iterable):
    # powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


# ------------------------------------------------------------------------------


# Banco de pruebas que realiza sucesivas ejecuciones de la función proof
# tomando como parámetros las sucesivas salidas de la función randomIter

def funcBatch(params):
    # Crear fichero
    current = mp.current_process()
    file_out = r'C:\Users\adria\PycharmProjects\coinExchange\console_func_' + str(current._identity[0]) + ".txt"
    sys.stdout = open(file_out, 'a+')

    proof = params[0]
    randomIter = params[1]
    randomParams = params[2]
    n = params[3]

    # resBatch = []
    generator = (randomIter(**randomParams) for i in range(n))

    for prueba in generator:
        proof(prueba)
        # resBatch.append(res)

    # Cerrar fichero
    sys.stdout.close()

    return file_out


def testBenchFunc(proof, randomFunc, randomParams, samples, out_file):
    num_cores = mp.cpu_count()-1
    batch = samples // num_cores

    # Repartir las pruebas en lotes
    batch_list = [[proof, randomFunc, randomParams, batch]] * num_cores
    batch_list.append([proof, randomFunc, randomParams, samples % num_cores])

    pool = mp.Pool(num_cores)
    filenames = pool.map(funcBatch, batch_list)
    filenames = set(filenames)

    # result = [j for sub in result for j in sub]

    # Open file3 in write mode
    with open(out_file, 'w') as outfile:
        # Iterate through list
        for names in filenames:
            # Open each file in read mode
            with open(names) as infile:
                # read the data from file1 and
                # file2 and write it in file3
                outfile.write(infile.read())

            # Delete file
            if os.path.exists(names):
                os.remove(names)

            # Add '\n' to enter data of file2
            # from next line
            outfile.write("\n-------------------------------------------")


def funcCombi(params):
    # Crear fichero
    current = mp.current_process()
    file_out = r'C:\Users\adria\PycharmProjects\coinExchange\console_Combi_' + str(current._identity[0]) + ".txt"
    sys.stdout = open(file_out, 'a+')

    proof = params[0]
    sub_iterable = params[1]
    suffix = params[2]

    # resBatch = []
    generator = powerset(sub_iterable)

    for prueba in generator:
        act = list(prueba) + list(suffix)
        proof(act)
        # res = proof(act)
        # resBatch.append(res)

    # Cerrar fichero
    sys.stdout.close()

    return file_out


def testBenchCombi(proof, elements, out_file):
    num_cores = mp.cpu_count()-1

    top = math.ceil(math.log(num_cores, 2))

    suffixes = [i for i in powerset(elements[-top:])]
    sub_iterable = elements[:-top]

    # Repartir las pruebas en lotes
    batch_list = [[proof, sub_iterable, s] for s in suffixes]

    pool = mp.Pool(num_cores)
    filenames = pool.map(funcCombi, batch_list)
    filenames = set(filenames)

    # result = [j for sub in result for j in sub]

    # Open file3 in write mode
    with open(out_file, 'w') as outfile:
        # Iterate through list
        for names in filenames:
            # Open each file in read mode
            with open(names) as infile:
                # read the data from file1 and
                # file2 and write it in file3
                outfile.write(infile.read())

            # Delete file
            if os.path.exists(names):
                os.remove(names)

            # Add '\n' to enter data of file2
            # from next line
            outfile.write("\n-------------------------------------------")
