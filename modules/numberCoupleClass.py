#!/usr/local/bin/python
# -*-coding:Utf-8 -*

from modules.individualClass import Individual
import random


class NumberCouple(Individual):
    """NumberCouple class: represent one couple of real individual, inherits from the Individual class

    Properties:
    key : standardized representation of the problem [[x1, 'real'][x2, 'real']]
    fitness : = 1/1+f(x) with f(x) = 100(x2 - x1^2)^2 + (x1 - 1)^2
    + every property from the Individual class

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
        """Class constuctor"""
        super(NumberCouple, self).__init__(key)

    def _random_initialisation(self):
        """Randomly initialises an individual, Returns  a random key"""
        key = list()
        for i in range(0, 2):
            x = random.uniform(-2.048, 2.048)
            key.append((x, 'real'))
        return key

    def _calcul_fitness(self):
        """Calculates the individuals fitness"""
        x1, x2 = self._key
        x1 = x1[0]
        x2 = x2[0]
        functionResult = 100 * pow((x2 - pow(x1, 2)), 2) + pow((x1 - 1), 2)
        fitness = 1.0 / (1 + functionResult)
        return fitness

    def get_binary_standard(self):
        """Returns the standardised representation of the key for binary manipulations"""
        x1, x2 = self.key
        x1 = 1000 * x1[0]
        x2 = 1000 * x2[0]
        result = list()
        result.append((self._binarize(x1, 12), 15, 3, 14))
        result.append((self._binarize(x2, 12), 15, 3, 14))
        return result

    def get_real_standard(self):
        """Returns the standardised representation of the key for real manipulations"""
        x1, x2 = self.key
        x1 = 1000 * x1[0]
        x2 = 1000 * x2[0]
        result = list()
        result.append((self._realize(x1, 12), 13, 9, 12))
        result.append((self._realize(x2, 12), 13, 9, 12))
        return result

    @staticmethod
    def get_binary_unstandardized(l):
        """Returns the unstandardisation of a standardised binary representation of the key"""
        key = list()
        for element in l:
            a = int(element, 2)
            a = a / 1000.0
            key.append((a, 'real'))
        return key

    @staticmethod
    def get_real_unstandardized(l):
        """Returns the unstandardisation of a real binary representation of the key"""
        key = list()
        for element in l:
            a = int(element)
            a = a / 1000.0
            key.append((a, 'real'))
        return key
