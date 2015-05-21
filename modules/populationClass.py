#!/usr/local/bin/python
# -*-coding:Utf-8 -*

from views import displayView as vDisp
from views import clearView as vClr
from views import settingsView as vSet
from modules.numberCoupleClass import NumberCouple
import operator
import random


class Population(object):
    """
    docstring for Population
    """

    def __init__(self, individuals_type):
        super(Population, self).__init__()
        self._individuals_type = individuals_type
        self._settings = self._initSettings()
        self._worst = None
        self._best = None
        self._population = self._initialise()
        raw_input()

    @property
    def individuals_type(self):
        return self._individuals_type

    @property
    def settings(self):
        return self._settings

    @property
    def best(self):
        return self._best

    def _initSettings(self):
        if self.individuals_type == 'NumberCouple':
            return vSet.set_NCpl_settings()
        elif self.individuals_type == 'AckleyIndividual':
            return vSet.set_AklI_settings()

    @property
    def verbose(self):
        return self._settings['verbose']

    @property
    def population(self):
        return self._population

    @property
    def population_size(self):
        return len(self._population)

    @property
    def stop_iteration(self):
        return self._settings['iterations']

    @property
    def initial_population(self):
        return self._settings['initialPopulation']

    @property
    def stop_fitness(self):
        return self._settings['stopFitness']

    @property
    def min_fitness(self):
        if self._worst is None:
            return None
        return self._worst.fitness

    @property
    def max_fitness(self):
        if self._best is None:
            return None
        return self._best.fitness

    @property
    def mutation_mode(self):
        return self._settings['mutationMode']

    @property
    def mutation_probability(self):
        return self._settings['mutationProbability']

    @property
    def crossmode(self):
        return self._settings['crossmode']

    def _initialise(self):  # could be more generic
        if self.individuals_type == 'NumberCouple':
            for i in range(0, self.initial_population):
                newIndividual = NumberCouple()
                if newIndividual.fitness < self.stop_fitness:
                    self._store(newIndividual)
                else:
                    i = i - 1
        elif self.individuals_type == 'AckleyIndividual':
            return None

    def _store(self, newIndividual):
        view = dict()
        view['title'] = "INDIVIDUAL STORAGE"

        if self.max_fitness is None:
            self._best = newIndividual
        if self.min_fitness is None:
            self._worst = newIndividual

        if newIndividual.fitness > self.max_fitness:
            view['MAX'] = "is new max fitness"
            self._best = newIndividual
        if newIndividual.fitness < self.min_fitness:
            view['MIN'] = "is new min storage"
            self._worst = newIndividual

        self._population.append((newIndividual, newIndividual.fitness))
        view["ADDED"] = "{} added, fitness = {}".format(newIndividual.key, newIndividual.fitness)

        maximalPopulation = self._settings['maximalPopulation']
        if maximalPopulation > 1:
            while (len(self._population) > maximalPopulation):  # pops tuple with minimal fitness
                self._population = sorted(self._population, key=operator.itemgetter(1))
                poped = self._population.pop(0)
                self._worst = self._population[0][0]
                view['POP'] = "{} is poped".format(poped[0].key)

        vDisp.dDisplay(view, self.verbose)

        if newIndividual.fitness > self._settings['stopFitness']:
            return newIndividual
        else:
            return 1

    def run_GA(self):
        result = (1, 1)
        i = 0

        while result == (1, 1) and i < stop_iteration:
            vClr.do()
            parent1 = self._selectOne()
            parent2 = self._selectOne()
            raw_input()
            vClr.do()
            result = self._cross(parent1, parent2)
            i = i + 1

        best = self.best
        print("\n\nBest:\n{} : fitness = {}".format(best.key, best.fitness))

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

        pick = random.uniform(0, 1)
        view['Pick'] = pick
        for (individual, position) in sorted(positionList, key=operator.itemgetter(1)):
            if position > pick:
                view['Individual Position'] = position
                view['Individual Fitness'] = individual.fitness
                view['Individual Key'] = individual.key
                vDisp.dDisplay(view, self.verbose)
                return individual

    def _cross(self, parent1, parent2):
        view = dict()
        view['title'] = "CROSSOVER AND MUTATIONS RESUME"
        crossmode = self.crossmode
        view['0- PARENT 1'] = parent1.key
        view['0- PARENT 2'] = parent2.key

        if crossmode == 0:
            standardParent1 = parent1.get_binary_standard()
            standardParent2 = parent2.get_binary_standard()
        elif crossmode == 1:
            standardParent1 = parent1.get_real_standard()
            standardParent2 = parent2.get_real_standard()

        view["1- STANDARDIZED PARENT 1"] = standardParent1
        view["1- STANDARDIZED PARENT 2"] = standardParent2

        lengths1 = len(parent1.key)
        lengths2 = len(parent2.key)    # if not == raise exception

        view["2- LENGTH 1"] = lengths1
        view["2- LENGTH 2"] = lengths2

        child1 = list()
        child2 = list()

        for i in range(0, lengths1):
            string1, size1, minCrossPosition1, maxCrossPosition1 = standardParent1[i]
            string2, size2, minCrossPosition2, maxCrossPosition2 = standardParent2[i]
            # if parameters not ==, raise exception
            crosspoint = random.randint(minCrossPosition1, maxCrossPosition1)
            view['3- Keys[' + str(i) + '] - CROSSPOINT'] = crosspoint
            childString1 = string1[0:crosspoint] + string2[crosspoint:]
            view['4- Child 1 - Key[' + str(i) + '] - After crossover'] = childString1
            childString2 = string2[0:crosspoint] + string1[crosspoint:]
            view['4- Child 2 - Key[' + str(i) + '] - After crossover'] = childString2
            childString1 = self._mutate(childString1, size1, minCrossPosition1, maxCrossPosition1)
            view['5- Child 1 - Key[' + str(i) + '] - After mutation'] = childString1
            childString2 = self._mutate(childString2, size2, minCrossPosition2, maxCrossPosition2)
            view['5- Child 2 - Key[' + str(i) + '] - After mutation'] = childString2
            child1.append(childString1)
            child2.append(childString2)

        if self.individuals_type == 'NumberCouple' and crossmode == 0:
            child1 = NumberCouple.get_binary_unstandardized(child1)
            newChild1 = NumberCouple(child1)
            result1 = self._store(newChild1)
            child2 = NumberCouple.get_binary_unstandardized(child2)
            newChild2 = NumberCouple(child2)
            result2 = self._store(newChild2)
        elif self.individuals_type == 'NumberCouple' and crossmode == 1:
            newChild1 = NumberCouple(NumberCouple.get_real_unstandardized(child1))
            result1 = self._store(newChild1)
            newChild2 = NumberCouple(NumberCouple.get_real_unstandardized(child2))
            result2 = self._store(newChild2)

        view['6- UNSTANDARDIZED CHILD 1'] = child1
        view['6- UNSTANDARDIZED CHILD 2'] = child2
        vDisp.dDisplay(view, self.verbose)
        raw_input()

        return (result1, result2)

    def _mutate(self, childString, size, minCrossPosition, maxCrossPosition):
        mutationMode = self.mutation_mode
        mutationProbability = self.mutation_probability
        stringType = self.individuals_type
        crossmode = self.crossmode

        if mutationProbability > 1:
            minMutationProbability = 1.0 / max(size, self.population_size)
            maxMutationProbability = 1.0 / min(size, self.population_size)
            mutationProbability = random.uniform(minMutationProbability, maxMutationProbability)

        if mutationMode == 0:   # swap mode
            a = 0
            b = 0
            while a == b and b < a:
                a = random.randint(minCrossPosition, maxCrossPosition)
                b = random.randint(minCrossPosition, maxCrossPosition)
            childString = childString[0:a] + childString[b] + childString[a+1:b] + childString[a] + ChildString[b+1:]
        elif mutationMode == 1:    # all nucleotid mode
            for i in range(minCrossPosition, maxCrossPosition):
                pick = random.uniform(0, 1)
                if pick < mutationProbability:
                    print("MUTATION MGGGG")
                    if crossmode == 0:
                        if childString[i] == '1':
                            char = '0'
                        elif childString[i] == '0':
                            char = '1'
                    elif crossmode == 1:
                        char = str(random.randint(0, 9))
                    childString = childString[0:i] + char + childString[i+1:]
        elif mutationMode == 2:    # max 1 nucleotid mode
            pick = random.uniform(0, 1)
            if pick < mutationProbability:
                i = random.randint(minCrossPosition, maxCrossPosition)
                if crossmode == 0:
                    if childString[i] == '1':
                        char = '0'
                    elif childString[i] == '0':
                        char = '1'
                elif crossmode == 1:
                    char = str(random.randint(0, 9))
                childString = childString[0:i] + char + childString[i+1:]

        return childString

    def run_ES():
        # given n , p , mu, lambda, appartenant a N+
        # tant que non satisfait
            # pour tout k (individu appartenant a la pop)
                # (xk, sk) vector de solutions = recombination de  (p séléctionnés parmi la population P)
                # sk' paramètre de strategy = mutation du paramètre de strategy sk
                # xk'  = mutation vecteur solution en fonction du paramètre sk
            # P = P + new childs
            # P = select_by_age truc
            # P = select_mu_best

        # given n , lambda, appartenant a N+
        # x appartient a  R(n) , s, P = dict
        # tant que non satisfait
            # pour tout lambda, soit nombre de la pop d'enfant
                # sk paramètre de strategy = mutation du paramètre de strategy s
                # xk  = mutation de x du paramètre sk
                # P = P + new childs
            # P = select_by_age truc
            # (x, s) vector de solutions = recombination de  (p séléctionnés parmi la population P)

        # recombination choisie : discrete... on verra pour la intermediate/weighted plus tard
        return None
