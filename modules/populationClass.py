#!/usr/local/bin/python
# -*-coding:Utf-8 -*

from views import displayView as vDisp
from views import clearView as vClr
from views import settingsView as vSet
from modules.numberCoupleClass import NumberCouple
from modules.AGParametersSetClass import AGParametersSet
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
        self._worst = None
        self._best = None
        self._settings = self.initSettings()
        self._initialise()
        raw_input()

    def getIndividualsType(self):
        return self._individualsType

    def getBest(self):
        return self._best

    def initSettings(self):
        if self.getIndividualsType() == 'NumberCouple':
            return vSet.setSettings()

    def getSettings(self):
        return self._settings

    def getVerbose(self):
        return self._settings['verbose']

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
        if self._worst is None:
            return None
        return self._worst.getFitness()

    def getMaxFitness(self):
        if self._best is None:
            return None
        return self._best.getFitness()

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
        view = dict()
        view['title'] = "INDIVIDUAL STORAGE"
        if self.getMaxFitness() == None:
            self._best = newIndividual
        if self.getMinFitness() == None:
            self._worst = newIndividual
        if newIndividual.getFitness() > self.getMaxFitness():
            view['MAX'] = "is new max fitness"
            self._best = newIndividual
        if newIndividual.getFitness() < self.getMinFitness():
            view['MIN'] = "is new min storage"
            self._worst = newIndividual

        self._population.append((newIndividual, newIndividual.getFitness()))
        view["ADDED"] = "{} added, fitness = {}".format(newIndividual.getKey(), newIndividual.getFitness())

        maximalPopulation = self._settings['maximalPopulation']
        if maximalPopulation > 1:
            while (len(self._population) > maximalPopulation): # pops tuple with minimal fitness
                self._population = sorted(self._population, key = operator.itemgetter(1))
                poped = self._population.pop(0)
                self._worst = self._population[0][0]
                view['POP'] = "{} is poped".format(poped[0].getKey())

        vDisp.dDisplay(view, self.getVerbose())

        if newIndividual.getFitness() > self._settings['stopFitness']:
            return newIndividual
        else:
            return 1


    def runAG(self):
        stopIteration = self.getStopIterationNumber()
        result = (1,1)
        i = 0

        while result == (1,1) and i < stopIteration:
            vClr.do()
            parent1 = self._selectOne()
            parent2 = self._selectOne()
            raw_input()
            vClr.do()
            result = self._cross(parent1, parent2)
            i = i + 1

        best = self.getBest()
        print("\n\nBest:\n{} : fitness = {}".format(best.getKey(), best.getFitness()))

    def _selectOne(self):
        positionList = list()
        view = dict()
        view['title'] = "SELECTED CHILD"
        aggregation = 0
        individuals, fitnesses = zip(*self._population)
        sumFitnesses = sum(fitnesses)
        view['Fitnesses Sum'] = sumFitnesses

        for (individual, fitness) in self._population:
            aggregation += fitness / sumFitnesses
            positionList.append((individual, aggregation))

        pick = random.uniform(0,1)
        view['Pick'] = pick
        for (individual, position) in sorted(positionList, key = operator.itemgetter(1)):
            if position > pick:
                view['Individual Position'] = position
                view['Individual Fitness'] = individual.getFitness()
                view['Individual Key'] = individual.getKey()
                vDisp.dDisplay(view, self.getVerbose())
                return individual


    def _cross(self, parent1, parent2):
        view = dict()
        view['title'] = "CROSSOVER AND MUTATIONS RESUME"
        crossmode = self.getCrossMode()
        view['0- PARENT 1'] = parent1.getKey()
        view['0- PARENT 2'] = parent2.getKey()
        if crossmode == 0:
            standardParent1 = parent1.getBinaryStandard()
            standardParent2 = parent2.getBinaryStandard()
        elif crossmode == 1:
            standardParent1 = parent1.getRealStandard()
            standardParent2 = parent2.getRealStandard()

        view["1- STANDARDIZED PARENT 1"] = standardParent1
        view["1- STANDARDIZED PARENT 2"] = standardParent2

        lengths1 = len(parent1.getKey())
        lengths2 = len(parent2.getKey()) # if not == raise exception

        view["2- LENGTH 1"] = lengths1
        view["2- LENGTH 2"] = lengths2

        child1 = list()
        child2 = list()

        for i in range(0, lengths1):
            string1, size1, minCrossPosition1, maxCrossPosition1 = standardParent1[i]
            string2, size2, minCrossPosition2, maxCrossPosition2 = standardParent2[i]
            # if parameters not ==, raise exception
            crosspoint = random.randint(minCrossPosition1, maxCrossPosition1)
            view['3- Keys['+ str(i) +'] - CROSSPOINT'] = crosspoint
            childString1 = string1[0:crosspoint] + string2[crosspoint:]
            view['4- Child 1 - Key['+ str(i) +'] - After crossover'] = childString1
            childString2 = string2[0:crosspoint] + string1[crosspoint:]
            view['4- Child 2 - Key['+ str(i) +'] - After crossover'] = childString2
            childString1 = self._mutate(childString1, size1, minCrossPosition1, maxCrossPosition1)
            view['5- Child 1 - Key['+ str(i) +'] - After mutation'] = childString1
            childString2 = self._mutate(childString2, size2, minCrossPosition2, maxCrossPosition2)
            view['5- Child 2 - Key['+ str(i) +'] - After mutation'] = childString2
            child1.append(childString1)
            child2.append(childString2)

        if self.getIndividualsType() == 'NumberCouple' and crossmode == 0:
            child1 = NumberCouple.getBinaryUnstandardized(child1)
            newChild1 = NumberCouple(child1)
            result1 = self._store(newChild1)
            child2 = NumberCouple.getBinaryUnstandardized(child2)
            newChild2 = NumberCouple(child2)
            result2 = self._store(newChild2)
        elif self.getIndividualsType() == 'NumberCouple' and crossmode == 1:
            newChild1 = NumberCouple(NumberCouple.getRealUnstandardized(child1))
            result1 = self._store(newChild1)
            newChild2 = NumberCouple(NumberCouple.getRealUnstandardized(child2))
            result2 = self._store(newChild2)

        view['6- UNSTANDARDIZED CHILD 1'] = child1
        view['6- UNSTANDARDIZED CHILD 2'] = child2
        vDisp.dDisplay(view, self.getVerbose())
        raw_input()

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
                    print("MUTATION MGGGG")
                    if crossmode == 0:
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








