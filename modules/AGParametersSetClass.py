#!/usr/local/bin/python
# -*-coding:Utf-8 -*

from modules.individualClass import Individual

class AGParametersSet(Individual):
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