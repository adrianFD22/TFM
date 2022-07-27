import sys
sys.path.insert(1, '/home/adrian/Documentos/Python')
#-------------------------------------------------------------


# Ejemplo de uso de test_battery(): cálculo en paralelo de los primeros 10
#                                   números.

import testbattery as tb
import multiprocessing as mp


# instance_test(): Generador de instacias a probar sobre las que realizar las
# pruebas. Debe ser un generador definido con los mismos parámetros del ejemplo.
# El generador que definamos será proporcionado como parámetro para la función
# test_battery(). Explicamos el significado que tiene cada parámetro del
# generador:
#
#   samples:    número de pruebas totales a realizar.
#
#   batch:      número de pruebas que realizará el proceso actual.
#
#   pid:        identificador númerico entre 0 y el número de procesos usados
#               (se puede calcular como samples//numcores - 1) que señala al
#               proceso actual.
#
#   num_cores:  número de procesos que se usarán. Se define en la llamada a
#               test_battery().
#
#   params:     parámetros opcionales para el generador en caso de que los
#               requiera.

def instance_test(samples, batch, pid, num_cores, *params):
    before_samples = pid*(samples//num_cores) + min(pid, samples%num_cores)

    for i in range(batch):
        yield i+before_samples


# test(): prueba a realizar. Es proporcionado como parámetro a test_battery().
# Los resultados de las pruebas deben ser impresos por salida estándar (usar la
# usar la función print()). Debe estar definida con el parámetro
#
#   prueba:     instancia sobre la que se realiza la prueba. Vendrá generada a
#               través de la función test_battery() por la función
#               instance_test().

def test(prueba):
    print(prueba)


# test_battery():   función para poner en marcha las pruebas. Divide la carga
# de trabajo en lotes entre el número de procesos indicado por el parámetro
# num_cores. El resultado de las pruebas viene dado en el fichero
# path/prueba.txt, siendo path y prueba .parámetros de la función. Sus
# parámetros son
#
#   test:           pruebas a realizar. Definida previamente.
#
#   instance_test:  generador de pruebas. Definido previamente.
#
#   samples:        número de pruebas totales a realizar.
#
#   path:           ruta en la que almacenar los ficheros auxiliares y el
#                   resultado final.
#
#   out_file:       fichero en el que almacenar el resultado final.
#
#   params:         lista con los argumentos opcionales para la función
#                   instance_test(). Por defecto es [] en caso de no necesitar
#                   argumentos.
#
#   num_cores:      número de procesos a utilizar (núcleos a ocupar). Por
#                   defecto es el número de núcleos de la máquina menos 1.
#                   Puede usarse la librería multiprocessing para calcular el
#                   el número de núcleos del que disponemos.

tb.test_battery(
        test,
        instance_test,
        20,
        "/home/adrian/Documentos",
        "demo_test_battery"
)
