import Coins.custom_tools
from Coins.coins import *
import sys
import Coins.testbattery as tb
import multiprocessing as mp


def instance_test(samples, batch, pid, num_cores, *params):
    before_samples = pid*(samples//num_cores) + min(pid, samples%num_cores)

    for i in range(batch):
        yield CoinSystem.randomCoinsNonTrivial(*params)


def test(E):
    # Dado un sistema de monedas e no canónico, devolver:
    #  0 si no se han encontrado snitches
    #  1 si el menor snitch es pequeño
    #  2 si el menor snitch es grande

    # Si el generador no ha encontrado un sistema de monedas
    e = E.getCoins()

    # Encontrar el menor snitch
    s = E.getLowestSnitch()

    small = 2 * e[-1]

    if s >= small:
        print("Encontrado menor snitch grande")
        print("\te =", e)


# -------------------------------------------------------------------------------
if __name__ == '__main__':
    from time import time

    # Abrir fichero salida
    path = r'C:\Users\adria\PycharmProjects\coinExchange'

    # sys.stdout = open(r'C:\Users\adria\PycharmProjects\coinExchange\console_menorSnitchRandom', 'a')
    # print()
    # print("---------------------------------------------------------------------")

    # Ejecutar banco de pruebas
    samples = 100000
    randomParams = [50,6,30]

    start_time = time()

    tb.test_battery(
        test,
        instance_test,
        20,
        "",
        "demo_test_battery",
        params=randomParams
    )

    finish_time = time()
    print(f"Program finished in {finish_time - start_time} seconds\n")

    # Borrar memoria
    globals().clear()
