#!/usr/local/bin/python
# -*-coding:Utf-8 -*

from abc import ABCMeta, abstractmethod
import random


class Individual(object):
    """Individual Class

    Abstract class representing an individual
    """
    __metaclass__ = ABCMeta

    def __init__(self, key=None):
        """
        initialise with "Individual(key)"
        """
        super(Individual, self).__init__()
        if key is not None:
            self.key = key
        else:
            self.key = self._random_initialisation()
        self._fitness = float(self._calcul_fitness())

    @abstractmethod
    def _random_initialisation(self):
        pass

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value
        self._fitness = self._calcul_fitness()

    @property
    def vector_size(self):
        return (len(self.key)/2)

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        self._fitness = self._calcul_fitness()

    @abstractmethod
    def get_binary_standard(self):
        pass

    @abstractmethod
    def get_binary_unstandardized(self):
        pass

    @abstractmethod
    def get_real_standard(self):
        pass

    @abstractmethod
    def get_real_unstandardized(self):
        pass

    @abstractmethod
    def _calcul_fitness(self):
        pass

    @property
    def xi(self):
        size = self.vector_size
        return self.key[0:size]

    @property
    def sigmas(self):
        size = self.vector_size
        return self.key[size:]

    @property
    def average_sigma(self):
        size = self.vector_size
        sigmas = self.sigmas
        sigmas = [x for (x, y) in sigmas]
        sum_sigmas = sum(sigmas)
        return (float(sum_sigmas) / float(size))

    def _binarize(self, a, size):
        b = str(bin(int(a)))
        if b[0] == '-':
            b = b[3:]
            b = b.zfill(size)
            b = '-0b' + b
        else:
            b = b[2:]
            b = b.zfill(size)
            b = '+0b' + b
        return b

    def _realize(self, a, size):
        b = str(int(a))
        if b[0] == '-':
            b = b[1:]
            while len(b) != size:
                b = '0' + b
            b = '-' + b
        else:
            while len(b) != size:
                b = '0' + b
            b = '+' + b
        return b

    def uniformise_sigma(self):
        length = len(self.key)
        for i in range(length / 2, length):
            if i == length / 2:
                sigma = self._key[i][0]
            else:
                self._key[i] = (sigma, 'ackley_sigma')

    def sigma_boost(self):
        size = self.vector_size
        new_key = self.key[0:size]
        for i in range(0, size):
            random_real = random.uniform(0, 1)
            new_key.append((random_real, 'sigma'))
        self._key = new_key
