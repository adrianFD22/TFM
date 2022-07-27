from Coins.custom_tools import *
from random import randint


class CoinSystem:

    # Dar un sistema de monedas e y opcionalmente el número de monedas a calcular
    # las representaciones óptimas y voraz
    def __init__(self, e, n=1100):
        coins = e[:]

        # Comprobar que sean todo números
        if not all(isinstance(x, int) for x in coins):
            raise Exception("Coin system must be formed by integers")

        # Comprobar que no hayan repetidos
        coinsSet = set(coins)
        if len(coinsSet) != len(coins):
            raise Exception("Coin system can't contain repeated elements")

        # Comprobar que la primera moneda es 1
        coins.sort()

        if coins[0] != 1:
            raise Exception("Coin system must start at 1")

        # Inicializar variables locales
        self.__e = coins
        self.__n = 1
        self.__greed = [-1]
        self.__opt = [-1]
        self.__lowestWit = -1
        self.__lowestSni = -1

        # Calcular los primeros números
        n_init = self.__e[-1] + self.__e[-2] if len(self.__e) > 1 else 2;
        self.__calculate(n_init)

        # Comprobar si el sistema es canónico y Cohen-Macaulay hallando el menor witness y el menor snitch

        # Menor witness
        if len(self.__e) >= 3:
            for b in range(self.__e[2] + 2, self.__e[-1] + self.__e[-2]):
                if self.isWitness(b):
                    self.__lowestWit = b
                    break

        # Menor snitch
        if self.__lowestWit != -1:
            for b in range(self.__e[-1] + 2, self.__e[-1] + self.__e[-2]):
                if self.isSnitch(b):
                    self.__lowestSni = b
                    break

    # Dar un sistema de monedas aleatorio cuyo menor contraejemplo sea menor que la
    # moneda más grande
    @classmethod
    def randomCoinsNonTrivial(cls, max_coin=1000, min_n_coins=7, max_n_coins=30):
        # Número de pruebas
        samples = 10000

        for i in range(samples):
            h = randint(min_n_coins, max_n_coins)
            e = random_combination(range(2, max_coin), h)
            e = [1] + list(e)

            E = CoinSystem(e)
            w = E.getLowestWitness()

            if w != -1:
                if w < e[-1]:
                    return E

        return -1

    # Obtener e
    def getCoins(self):
        return self.__e

    # Obtener M(b)
    def getOptimal(self, b):
        self.__calculate(b)

        return self.__opt[b - 1]

    # Obtener G(b)
    def getGreedy(self, b):
        self.__calculate(b)

        return self.__greed[b - 1]

    # Obtener el menor witness
    def getLowestWitness(self):
        return self.__lowestWit

    # Obtener el menor witness
    def getLowestSnitch(self):
        return self.__lowestSni

    # Calcular representaciones voraces y óptimas (función interna de la clase)
    def __calculate(self, n):
        if self.__n >= n:
            return

        if self.__n == 1:
            self.__n = n
            old_n = 1

        else:
            old_n = self.__n

        # Aumentar el tamaño de las listas que contienen las representaciones
        while n > self.__n:
            self.__n = self.__n + self.__n // 2 + 1

        self.__greed = self.__greed + [-1] * (self.__n - old_n)
        self.__opt = self.__opt + [-1] * (self.__n - old_n)

        # Calcular los valores que no han sido previamente calculados
        max_coin_lower = 0
        for b in range(old_n, self.__n + 1):

            # Optimal
            min_rep = b
            for i in self.__e:
                if i > b:
                    break
                if i == b:
                    min_rep = 1
                    break
                if i < b:
                    res = self.__opt[b - i - 1] + 1
                    min_rep = res if res < min_rep else min_rep

            self.__opt[b - 1] = min_rep

            # Greedy
            if max_coin_lower < len(self.__e) and b == self.__e[max_coin_lower]:
                self.__greed[b - 1] = 1
                max_coin_lower = max_coin_lower + 1
            else:
                act_coin = self.__e[max_coin_lower-1]
                self.__greed[b - 1] = self.__greed[b - act_coin - 1] + 1

    # Comprobar si b es witness de e[i]
    def isWitnessCoin(self, b, i):
        self.__calculate(b)

        c_i = self.__e[i]
        if c_i >= b:
            return False

        return self.__greed[b - 1] > self.__greed[b - c_i - 1] + 1

    # Comprobar si b es un witness
    def isWitness(self, b):
        for i in range(0, len(self.__e)):
            if self.isWitnessCoin(b, i):
                return True

        return False

    # Comprobar si b es un contraejemplo
    def isCounterEx(self, b):
        self.__calculate(b)

        return self.__greed[b - 1] != self.__opt[b - 1]

    # Comprobar si b es un snitch
    def isSnitch(self, b):
        self.__calculate(b)

        if b <= self.__e[-1]:
            return False

        return self.__opt[b - 1] != self.__opt[b - self.__e[-1] - 1] + 1