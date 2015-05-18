#!/usr/local/bin/python
# -*-coding:Utf-8 -*

import views.populationViews as view
from individualClass import *
import operator
import random

class Population(object):
    """
    docstring for Population
    """

    def __init__(self, individualsType):
        super(Population, self).__init__()
        self._individualsType = individualsType
        self._settings = {}
        self._population = []
        self._minFitness = None
        self._maxFitness = None
        self._settings = self.initSettings()
        self._initialise()

    def getIndividualsType(self):
        return self._individualsType

    def getBest(self):
        sortedPopulation = sorted(self.getPopulation(), key = operator.itemgetter(1))
        return sortedPopulation[len(sortedPopulation)-1]

    def initSettings(self):
        if self.getIndividualsType() == 'NumberCouple':
            return view.setNumberCoupleSettings()

    def getSettings(self):
        return self._settings

    def getPopulation(self):
        return self._population

    def getPopulationSize(self):
        return len(self._population)

    def getStopIterationNumber(self):
        return self._settings['iterations']

    def getInitialPopulation(self):
        return self._settings['initialPopulation']

    def getStopFitness(self):
        return self._settings['stopFitness']

    def getMinFitness(self):
        return self._minFitness

    def getMaxFitness(self):
        return self._maxFitness

    def getMutationMode(self):
        return self._settings['mutationMode']

    def getMutationProbability(self):
        return self._settings['mutationProbability']

    def getCrossMode(self):
        return self._settings['crossmode']

    def _initialise(self): # could be more generic
        if self.getIndividualsType() == 'NumberCouple':
            for i in range(0, self.getInitialPopulation()):
                x1 = random.uniform(-2.048, 2.048)
                x2 = random.uniform(-2.048, 2.048)
                newIndividual = NumberCouple((x1, x2))
                if newIndividual.getFitness() < self.getStopFitness():
                    self._store(newIndividual)
                else:
                    i = i - 1

    def _store(self, newIndividual):
        if self.getMaxFitness() == None:
            self._maxFitness = newIndividual.getFitness()
        if self.getMinFitness() == None:
            self._minFitness = newIndividual.getFitness()
        if newIndividual.getFitness() > self.getMaxFitness():
            self._maxFitness = newIndividual.getFitness()
        if newIndividual.getFitness() < self.getMinFitness():
            self._minFitness = newIndividual.getFitness()

        self._population.append((newIndividual, newIndividual.getFitness()))

        maximalPopulation = self._settings['maximalPopulation']
        if maximalPopulation > 1:
            while (len(self._population) > maximalPopulation): # pops tuple with minimal fitness
                self._population = sorted(self._population, key = operator.itemgetter(1))
                self._population.pop(0)
                self._minFitness = self._population[0][1]

        if newIndividual.getFitness() > self._settings['stopFitness']:
            return newIndividual
        else:
            return 1


    def runAG(self):
        stopIteration = self.getStopIterationNumber()
        result = (1,1)
        i = 0

        while result == (1,1) and i < stopIteration:
            parent1 = self._selectOne()
            parent2 = self._selectOne()
            result = self._cross(parent1, parent2)
            i = i + 1

        best = self.getBest()
        print("\n\nBest:\n{} : fitness = {}".format(best.getKey(), best.getFitness()))

    def _selectOne(self):
        positionList = list()
        aggregation = 0
        individuals, fitnesses = zip(*self._population)
        sumFitnesses = sum(fitnesses)

        for (individual, fitness) in self._population:
            aggregation += fitness / sumFitnesses
            positionList.append((individual, aggregation))

        pick = random.uniform(0,1)
        for (individual, position) in sorted(positionList, key = operator.itemgetter(1)):
            if position > pick:
                return individual


    def _cross(self, parent1, parent2):
        crossmode = self.getCrossMode()
        if crossmode == 0:
            standardParent1 = parent1.getBinaryStandard()
            standardParent2 = parent2.getBinaryStandard()
        elif crossmode == 1:
            standardParent1 = parent1.getRealStandard()
            standardParent2 = parent2.getRealStandard()

        lengths1 = len(parent1.getKey())
        lengths2 = len(parent2.getKey()) # if not == raise exception
        child1 = list()
        child2 = list()
        for i in range(0, lengths1 - 1):
            string1, size1, minCrossPosition1, maxCrossPosition1 = standardParent1[i]
            string2, size2, minCrossPosition2, maxCrossPosition2 = standardParent2[i]
            # if parameters not ==, raise exception
            crosspoint = random.randint(minCrossPosition1, maxCrossPosition1)
            childString1 = string1[0:crosspoint] + string2[crosspoint:]
            childString2 = string2[0:crosspoint] + string1[crosspoint:]
            childString1 = self._mutate(childString1, size1, minCrossPosition1, maxCrossPosition1)
            childString2 = self._mutate(childString2, size2, minCrossPosition2, maxCrossPosition2)
            child1.append(childString1)
            child2.append(childString2)

        if self.getIndividualsType() == 'NumberCouple' and crossmode == 0:
            newChild1 = NumberCouple(NumberCouple.getBinaryUnstandardized(child1))
            result1 = self._store(newChild1)
            newChild2 = NumberCouple(NumberCouple.getBinaryUnstandardized(child2))
            result2 = self._store(newChild2)
        elif self.getIndividualsType() == 'NumberCouple' and crossmode == 1:
            newChild1 = NumberCouple(NumberCouple.getRealUnstandardized(child1))
            result1 = self._store(newChild1)
            newChild2 = NumberCouple(NumberCouple.getRealUnstandardized(child2))
            result2 = self._store(newChild2)

        return (result1, result2)

    def _mutate(self, childString, size, minCrossPosition, maxCrossPosition):
        mutationMode = self.getMutationMode()
        mutationProbability = self.getMutationProbability()
        stringType = self.getIndividualsType()
        crossmode = self.getCrossMode()

        if mutationProbability > 1:
            mutationProbability = random.uniform( (1.0 / max(size, self.getPopulationSize()) ), 1.0 / min(size, self.getPopulationSize()) )

        if mutationMode == 0: # swap mode
            a = 0
            b = 0
            while a == b and b < a :
                a = random.randint(minCrossPosition, maxCrossPosition)
                b = random.randint(minCrossPosition, maxCrossPosition)
            childString = childString[0:a] + childString[b] + childString[a+1:b] + childString[a] + ChildString[b+1:]
        elif mutationMode == 1: # all nucleotid mode
            for i in range(minCrossPosition, maxCrossPosition):
                pick = random.uniform(0,1)
                if pick < mutationProbability:
                    if crossmode == 0:
                        #print(childString)
                        #print("\n")
                        #print(i)
                        raw_input()
                        if childString[i] == '1':
                            char = '0'
                        elif childString[i] == '0':
                            char = '1'
                    elif crossmode == 1:
                        char = str(random.randint(0,9))
                    childString = childString[0:i] + char + childString[i+1:]
        elif mutationMode == 2: # max 1 nucleotid mode
            pick = random.uniform(0,1)
            if pick < mutationProbability:
                i = random.randint(minCrossPosition, maxCrossPosition)
                if crossmode == 0:
                    if childString[i] == '1':
                        char = '0'
                    elif childString[i] == '0':
                        char = '1'
                elif crossmode == 1:
                    char = str(random.randint(0,9))
                childString = childString[0:i] + char + childString[i+1:]

        return childString








