#!/usr/local/bin/python
# -*-coding:Utf-8 -*

from modules.individualClass import Individual
import math
import random


class AckleyIndividual(Individual):
    """Ackley Individual class : represents one ackley individual, inherits from Individual class

    Properties:
    key : standardized representation of the problem [[x1, 'real']...[xn, 'real'], [sig1, 'real']...[sign, 'real']]
    fitness : = 1/1+f(x) with f(x) = result of the ackley function
    c3
    c2
    c1
    dimension
    + every properties from the Individual Class

    Methods:
    __init__()
    get_binary_standard()
    get_real_standard()
    get_binary_unstandardized()
    get_real_unstandardized
    _calcul_fitness()
    _random_initialisation()
    + every method from the Individual Class
    """

    def __init__(self, key=None):
        """Class constructor"""
        self._c1 = float(20)
        self._c2 = float(0.2)
        self._c3 = float(2.0 * 3.14159)
        self._dimension = int(30)
        super(AckleyIndividual, self).__init__(key)

    @property
    def c3(self):
        """Returns the c3 parameter of the Ackley function"""
        return self._c3

    @property
    def c1(self):
        """Returns the c1 parameter of the Ackley function"""
        return self._c1

    @property
    def c2(self):
        """Returns the c2 parameter of the Ackley function"""
        return self._c2

    def get_binary_standard(self):
        """Implemented soon"""
        result = list()
        for i in range(0, self.dimension):
            value = self.key[i][0]
            value = int(1000 * value)
            result.append((self._binarize(value, 16), 19, 3, 18))
        return result

    def get_real_standard(self):
        """Soon"""
        result = list()
        for i in range(0, self.dimension):
            value = self.key[i][0]
            value = int(1000 * value)
            result.append((self._realize(value, 16), 17, 12, 16))
        return result

    @staticmethod
    def get_binary_unstandardized(l):
        """Soon"""
        key = list()
        for element in l:
            a = int(element, 2)
            a = a / 1000.0
            key.append((a, 'x'))
        return key

    @staticmethod
    def get_real_unstandardized(l):
        """Soon"""
        key = list()
        for element in l:
            a = int(element)
            a = a / 1000.0
            key.append((a, 'x'))
        return key

    def _random_initialisation(self):
        """Randomly initialises an AckleyIndividual"""
        key = list()
        for i in range(0, self.dimension):
            random_real = random.uniform(-15.0, 15.0)
            key.append((random_real, 'x'))

        for i in range(0, self.dimension):
            random_real = random.uniform(10, 20)
            key.append((random_real, 'sigma'))
        return key

    def _calcul_fitness(self):
        """Returns the fitness of the individual"""
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
