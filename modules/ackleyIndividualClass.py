#!/usr/local/bin/python
# -*-coding:Utf-8 -*

from modules.individualClass import Individual
import math
import random


class AckleyIndividual(Individual):
    """Ackley Individual class
    Inherits from Individual class

    Attributes:
    _key : is a list(x1, x2)
    _fitness : = 1/1+f(x) with f(x) = 100(x2 - x1^2)^2 + (x1 - 1)^2

    """
    def __init__(self, key=None):
        self._c1 = float(20)
        self._c2 = float(0.2)
        self._c3 = float(2.0 * 3.14159)
        self._dimension = int(30)
        super(AckleyIndividual, self).__init__(key)

    @property
    def c3(self):
        return self._c3

    @property
    def c1(self):
        return self._c1

    @property
    def c2(self):
        return self._c2

    @property
    def dimension(self):
        return self._dimension

    def get_binary_standard(self):
        return None

    def get_real_standard(self):
        return None

    @staticmethod
    def get_binary_unstandardized(l):
        return None

    @staticmethod
    def get_real_unstandardized(l):
        return None

    def _random_initialisation(self):
        key = list()
        for i in range(0, self.dimension):
            random_real = random.uniform(-15.0, 15.0)
            key.append((random_real, 'ackley_x'))

        for i in range(0, self.dimension):
            random_real = random.uniform(0, 1)
            key.append((random_real, 'ackley_sigma'))
        return key

    def _calcul_fitness(self):
        calcul = 0.0
        calcul2 = 0.0
        agregat = 0.0
        c1 = self.c1
        c2 = self.c2
        c3 = self.c3
        dimension = self.dimension

        for i in range(0, dimension):
            agregat += pow(self.key[i][0], 2)
        calcul += float(1.0 / float(dimension)) * float(agregat)
        calcul = float(math.sqrt(calcul))
        calcul = float(-c2 * calcul)
        calcul = float(math.exp(calcul))
        calcul = float(-c1 * calcul)

        agregat = 0.0
        for i in range(0, dimension):
            a = float(c3 * self.key[i][0])
            agregat += float(math.cos(a))
        calcul2 = float((1.0 / float(dimension)) * agregat)
        calcul2 = float(-1 * math.exp(calcul2))

        agregat = float(calcul) + float(calcul2) + float(c1) + float(math.exp(1))
        fitness = 1.0/(1.0 + float(agregat))

        return float(fitness)
