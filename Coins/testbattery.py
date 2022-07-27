import multiprocessing as mp
import os
import sys
import time
import subprocess


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print("Elapsed time:", end - start, "seconds")

    return wrapper


def func_batch(func_params):
    # Recuperar parámetros
    test, instance_test, params, samples, batch, pid, num_cores, path = func_params

    # Crear fichero
    file_out = path + "aux_func_batch" + str(pid) + ".txt"
    sys.stdout = open(file_out, 'a+')

    generator = instance_test(samples, batch, pid, num_cores, *params)

    for i in range(batch):
        prueba = next(generator)
        test(prueba)

    # Cerrar fichero
    sys.stdout.close()

    return file_out

@timer
def test_battery(
        test: callable,
        instance_test: callable,
        samples: int,
        path: str,
        out_file: str,
        params: list = [],
        num_cores: int = mp.cpu_count() - 1,
) -> None:

    batch = samples // num_cores
    remainder = samples % num_cores

    # Repartir las pruebas en lotes
    batch_list = [[test, instance_test, params, samples, batch + 1, pid, num_cores, path]
                  for pid in range(0, remainder)] +\
                 [[test, instance_test, params, samples, batch, pid, num_cores, path]
                  for pid in range(remainder, num_cores)]

    # Ejecutar pool de procesos en paralelo
    pool = mp.Pool(num_cores)
    filenames = pool.map(func_batch, batch_list)
    pool.close()
    filenames = list(filenames)

    out_file_ext = path + out_file + '.txt'


    # Agrupar los resultados
    with open(out_file_ext, 'w') as outfile:
        for names in filenames:
            with open(names) as infile:
                outfile.write(infile.read())

            if os.path.exists(names):
                os.remove(names)

            outfile.write("\n-------------------------------------------\n")


def func_batch_gap(func_params):
    # Recuperar parámetros
    test, path, pid = func_params

    # Crear fichero
    file_out = path + "aux_func_batch" + str(pid) + ".txt"
    output = open(file_out, 'a+')

    #Ejecutar fichero de gap
    subprocess.run(["/home/adrian/Documentos/Bash/exec_gap_script.sh", test], stdout = output)

    # Cerrar fichero
    sys.stdout.close()

    return file_out


@timer
def test_battery_gap(
        test: str,
        path: str,
        out_file: str,
        num_cores: int = mp.cpu_count() - 1,
) -> None:

    batch_list = [[test, path, pid] for pid in range(num_cores)]

    # Ejecutar pool de procesos en paralelo
    pool = mp.Pool(num_cores)
    filenames = pool.map(func_batch_gap, batch_list)
    pool.close()
    filenames = list(filenames)

    out_file_ext = path + "/"+out_file + ".txt"

    # Agrupar los resultados
    with open(out_file_ext, 'w') as outfile:
        for names in filenames:
            with open(names) as infile:
                outfile.write(infile.read())

            if os.path.exists(names):
                os.remove(names)

            outfile.write("\n-------------------------------------------\n")
