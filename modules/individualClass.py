#!/usr/local/bin/python
# -*-coding:Utf-8 -*

from abc import ABCMeta, abstractmethod
import random


class Individual(object):
    """Individual Class: abstract class, standardising the population individuals

    Properties:
    key : standardized representation of the problem: [[x1, 'type']...[xn, 'type']]
    fitness
    xi
    sigmas
    average_sigma

    Methods:
    __init__()
    _random_initialisation(), abstract
    get_binary_standard(), abstract
    get_binary_unstandardized(), abstract
    get_real_standard(), abstract
    get_real_unstandardized(), abstract
    _binarize()
    _realize
    uniformise_sigma()
    sigma_boost()
    """
    __metaclass__ = ABCMeta

    def __init__(self, key=None):
        """Class constructor"""
        super(Individual, self).__init__()
        if key is not None:
            self.key = key
        else:
            self.key = self._random_initialisation()
        self._fitness = float(self._calcul_fitness())

    @abstractmethod
    def _random_initialisation(self):
        """Randomly initialises the individual (abstract method)"""
        pass

    @property
    def key(self):
        """Returns the individual's key"""
        return self._key

    @key.setter
    def key(self, value):
        """key setter"""
        self._key = value
        self._fitness = self._calcul_fitness()

    @property
    def fitness(self):
        """Returns the individual's fitness"""
        return self._fitness

    @property
    def dimension(self):
        """Returns the dimension parameter of the Ackley function"""
        return self._dimension

    @fitness.setter
    def fitness(self, value):
        """Setter for the fitness"""
        self._fitness = self._calcul_fitness()

    @abstractmethod
    def get_binary_standard(self):
        """Returns the individual's key standardised for binary manipulations"""
        pass

    @abstractmethod
    def get_binary_unstandardized(self):
        """Returns the unstandardisation of a standardised binary representation of a key"""
        pass

    @abstractmethod
    def get_real_standard(self):
        """Returns the individual's key standardised for real manipulations"""
        pass

    @abstractmethod
    def get_real_unstandardized(self):
        """Returns the unstandardisation of a standardised real representation of a key"""
        pass

    @abstractmethod
    def _calcul_fitness(self):
        pass

    @property
    def xi(self):
        """Returns the elements of a key until an index corresponding to the dimension property"""
        dimension = self.dimension
        return self.key[0:dimension]

    @property
    def sigmas(self):
        """Returns the elements of a key from an index corresponding to the dimension property to the end"""
        dimension = self.dimension
        return self.key[dimension:]

    @property
    def average_sigma(self):
        """Returns the average of the values of elements returned by the sigmas property (Ackley-useful)"""
        dimension = self.dimension
        sigmas = self.sigmas
        sigmas = [x for (x, y) in sigmas]
        sum_sigmas = sum(sigmas)
        return (float(sum_sigmas) / float(dimension))

    def _binarize(self, a, size):
        """Standardises a string of fixed size into binary representation"""
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
        """Standardises a string of fixed size into real representation"""
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
        """Set every value of the elements from the second half of the key to the same value (Ackley-useful)"""
        length = len(self.key)
        for i in range(length / 2, length):
            if i == length / 2:
                sigma = self._key[i][0]
            else:
                self._key[i] = (sigma, 'ackley_sigma')

    def sigma_boost(self):
        """Re-initialise values of elements from the second half of the key (Ackley-useful)"""
        dimension = self.dimension
        new_key = self.xi
        for i in range(0, dimension):
            random_real = random.uniform(0, 1)
            new_key.append((random_real, 'sigma'))
        self._key = new_key
