#!/usr/local/bin/python
# -*-coding:Utf-8 -*

from abc import ABCMeta, abstractmethod


class Individual(object):
    """Individual Class

    Abstract class representing an individual
    """
    __metaclass__ = ABCMeta

    def __init__(self, key):
        """
        initialise with "Individual(key)"
        """
        super(Individual, self).__init__()
        self.key = key
        self._fitness = float(self._calculFitness())

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value
        self._fitness = self._calculFitness()

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        self._fitness = self._calculFitness()

    @abstractmethod
    def getBinaryStandard(self):
        pass

    @abstractmethod
    def getBinaryUnstandardized(self):
        pass

    @abstractmethod
    def getRealStandard(self):
        pass

    @abstractmethod
    def getRealUnstandardized(self):
        pass

    @abstractmethod
    def _calculFitness(self):
        pass

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
