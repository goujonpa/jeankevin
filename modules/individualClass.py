#!/usr/local/bin/python
# -*-coding:Utf-8 -*

from abc import ABCMeta, abstractmethod

class Individual(object):
	"""
	docstring for Individual
	abstract class

	attributes:
	_key
	_fitness

	methods:
	getKey()
	getFitness()
	_calculFitness() : abstract method

	"""
	__metaclass__ = ABCMeta

	def __init__(self, key):
		"""
		initialise with "Individual(key)"
		"""
		super(Individual, self).__init__()
		self._key = key
		self._fitness = self._calculFitness()

	def getKey(self):
		return self._key

	def getFitness(self):
		return self._fitness

	@abstractmethod
	def getBinaryStandard(self):
		pass

	@abstractmethod
	def getBinaryParameters(self):
		pass

	@abstractmethod
	def getBinaryUnstandardized(self):
		pass

	@abstractmethod
	def getRealStandard(self):
		pass

	@abstractmethod
	def getRealParameters(self, ):
		pass

	@abstractmethod
	def getRealUnstandardized(self):
		pass

	@abstractmethod
	def _calculFitness(self):
		pass

	def _binarize(a, size):
		b = str(bin(a))
	    if b[0] == '-':
	        b = b[3:]
	        b = b.zfill(size)
	        b = '-0b' + b
	    else:
	        b = b[2:]
	        b = b.zfill(size)
	        b = '+0b' + b
	    return b

	def _realize(a, size):
        b = str(a)
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


class NumberCouple(Individual):
	"""
	docstring for NumberCouple
	inherits from Individual

	Attributes:
	_key : is a list(x1, x2)
	_fitness : = 1/1+f(x) with f(x) = 100(x2 - x1^2)^2 + (x1 - 1)^2
	
	Methods:
	getKey()
	getFitness()
	_calculFitness : calculates the fitness value
	"""
	def __init__(self, key):
		super(NumberCouple, self).__init__(key)

	def _calculFitness(self):
		    x1, x2 = self._key
		    fitness = 1.0 / (1 + (100 * pow((x2 - pow(x1,2)),2) + pow((x1 - 1),2)))
		    return fitness

	def getBinaryStandard(self):
		x1, x2 = self.getKey()
		x1 = 1000 * x1
		x2 = 1000 * x2
		result = []
		result.append((self._binarize(x1, 12), 15, 2, 14))
		result.append((self._binarize(x2, 12), 15, 2, 14))
		return result

	def getRealStandard(self):
		x1, x2 = self.getKey()
		x1 = 1000 * x1
		x2 = 1000 * x2
		result = []
		result.append((self._realize(x1, 12), 13, 9, 12))
		result.append((self._realize(x2, 12), 13, 9, 12))
		return result

	@staticmethod
	def getBinaryUnstandardized(self, list):
		key = list()
		for element in list:
			a = int(element, 2)
			a = a / 1000.0
			key.append(a)
		return key

	@staticmethod
	def getRealUnstandardized(self, list):
		key = list()
		for element in list:
			a = int(element)
			a = a / 1000.0
			key.append(a)
		return key


class FunctionParametersSet(Individual):
	"""
	docstring for FunctionParametersSet
	inherits from Individual

	Attributes:
	_key : is a list(x1, x2)
	_fitness : = 1/1+f(x) with f(x) = 100(x2 - x1^2)^2 + (x1 - 1)^2
	
	Methods:
	getKey()
	getFitness()
	_calculFitness : calculates the fitness value
	"""

	def __init__(self, key):
		super(FunctionParametersSet, self).__init__(key)

	def _calculFitness(self):
		return None
		

