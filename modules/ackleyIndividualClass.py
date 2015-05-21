#!/usr/local/bin/python
# -*-coding:Utf-8 -*

from modules.individualClass import Individual


class AckleyIndividual(Individual):
    """Ackley Individual class
    Inherits from Individual class

    Attributes:
    _key : is a list(x1, x2)
    _fitness : = 1/1+f(x) with f(x) = 100(x2 - x1^2)^2 + (x1 - 1)^2

    """
    def __init__(self, key):
        super(NumberCouple, self).__init__(key)

    def _calcul_fitness(self):
            x1, x2 = self._key
            functionResult = 100 * pow((x2 - pow(x1, 2)), 2) + pow((x1 - 1), 2)
            fitness = 1.0 / (1 + functionResult)
            return fitness

    def get_binary_standard(self):
        x1, x2 = self.getKey()
        x1 = 1000 * x1
        x2 = 1000 * x2
        result = []
        result.append((self._binarize(x1, 12), 15, 3, 14))
        result.append((self._binarize(x2, 12), 15, 3, 14))
        return result

    def get_real_standard(self):
        x1, x2 = self.getKey()
        x1 = 1000 * x1
        x2 = 1000 * x2
        result = []
        result.append((self._realize(x1, 12), 13, 9, 12))
        result.append((self._realize(x2, 12), 13, 9, 12))
        return result

    @staticmethod
    def get_binary_unstandardized(l):
        key = list()
        for element in l:
            a = int(element, 2)
            a = a / 1000.0
            key.append(a)
        return key

    @staticmethod
    def get_real_unstandardized(l):
        key = list()
        for element in l:
            a = int(element)
            a = a / 1000.0
            key.append(a)
        return key
