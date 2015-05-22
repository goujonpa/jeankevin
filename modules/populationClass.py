#!/usr/local/bin/python
# -*-coding:Utf-8 -*

import views as v
from modules.numberCoupleClass import NumberCouple
from modules.ackleyIndividualClass import AckleyIndividual
import operator
import random
import math


class Population(object):
    """
    docstring for Population
    """

    # ========== CONSTRUCTOR ==========

    def __init__(self, individuals_type):
        super(Population, self).__init__()
        self._individuals_type = individuals_type
        self._settings = self._initSettings()
        self._worst = None
        self._best = None
        self._current_iteration = 0
        self._save_iterations = list()
        self._save_maximums = list()
        self._save_fitness_sums = list()
        self._population = list()
        self._view = dict()
        self._initialise()

    # ========== PROPERTIES & BASIC METHODS ==========

    # ----- Population

    @property
    def maximal_population(self):
        return self._settings['maximalPopulation']

    def _empty_population(self):
        self._population = list()

    @property
    def best(self):
        return self._best

    @property
    def population(self):
        return self._population

    @property
    def population_size(self):
        return len(self._population)

    # ----- Fitness

    @property
    def fitness_sums(self):
        population = self.population
        sums = 0.0
        individuals, values = zip(*self.population)
        sums = sum(values)
        return sums

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

    def _empty_extrems(self):
        self._best = None
        self._worst = None

    # ----- Learning rates

    @property
    def global_learning_rate(self):
        return self._settings['globalLearningRate']

    @property
    def local_learning_rate(self):
        return self._settings['localLearningRate']

    # ----- Settings

    @property
    def settings(self):
        return self._settings

    def _initSettings(self):
        if self.individuals_type == 'NumberCouple':
            return vSet.set_NCpl_settings()
        elif self.individuals_type == 'AckleyIndividual':
            return vSet.set_AklI_settings()

    @property  # Could be incorporated to settings
    def individuals_type(self):
        return self._individuals_type

    @property
    def child_number(self):
        return self._settings['childNumber']

    @property
    def verbose(self):
        return self._settings['verbose']

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
    def mutation_mode(self):
        return self._settings['mutationMode']

    @property
    def mutation_probability(self):
        return self._settings['mutationProbability']

    @property
    def crossmode(self):
        return self._settings['crossmode']

    # ----- View

    @property
    def view(self):
        return self._view

    def addview(self, key, value):
        self._view[key] = value

    def empty_view(self):
        self._view = dict()

    def display(self, element=0, verbose=1):
        if element == 0:
            v.display(self._view, self.verbose, (self.current_iteration, self.stop_iteration))
        else:
            v.display(element, verbose, (self.current_iteration, self.stop_iteration))

    # ----- Others

    @property
    def current_iteration(self):
        return self._current_iteration

    # ========== GA & ES Algorithms ==========

    def _initialise(self):  # could be more generic
        if self.individuals_type == 'NumberCouple':
            for i in range(0, self.initial_population):
                newIndividual = NumberCouple()
                if newIndividual.fitness < self.stop_fitness:
                    self._store(newIndividual)
                else:
                    i = i - 1
        elif self.individuals_type == 'AckleyIndividual':
            adam = AckleyIndividual()
            result = self._store(adam)

    def run_ES(self):
        # Initialisation done by initialise()
        i = 0
        while i < self.stop_iteration and self.population[0][1] < self.stop_fitness:
            self._current_iteration = i
            self._save_iterations.append(i)
            self._save_fitness_sums.append(self.fitness_sums)
            self._save_maximums.append(self.best.fitness)
            self._mutation_ES_Nx_Nsigma_gauss_2LR()  # Self-adapted
            j = i + 0.5

            self._save_iterations.append(j)
            self._save_fitness_sums.append(self.fitness_sums)
            self._save_maximums.append(self.best.fitness)
            self._recombination_ES_Nx_Nsigma_inter()
            i += 1

        best = self.best
        print("\n\nBest:\n{} : fitness = {}".format(best.key, best.fitness))
        vSv.save_figure(self._save_iterations, self._save_fitness_sums, self._save_maximums, 'simuES')

        return 1

    def run_GA(self):
        result = (1, 1)
        i = 0
        self._save_iterations.append(i)
        self._save_fitness_sums.append(self.fitness_sums)
        self._save_maximums.append(self.best.fitness)

        while result == (1, 1) and i < self.stop_iteration:
            self._current_iteration = i
            parent1 = self._selectOne()
            parent2 = self._selectOne()
            result = self._cross(parent1, parent2)
            i = i + 1
            self._save_iterations.append(i)
            self._save_fitness_sums.append(self.fitness_sums)
            self._save_maximums.append(self.best.fitness)

        best = self.best
        print("\n\nBest:\n{} : fitness = {}".format(best.key, best.fitness))
        vSv.save_figure(self._save_iterations, self._save_fitness_sums, self._save_maximums, 'simuGA')

        return 1

    def _store(self, newIndividual):
        self.empty_view()
        self.addview('title', 'INDIVIDUAL STORAGE')

        if self.max_fitness is None:
            self._best = newIndividual
        if self.min_fitness is None:
            self._worst = newIndividual

        if newIndividual.fitness > self.max_fitness:
            self.addview('MAX', 'is new max fitness')
            self._best = newIndividual
        if newIndividual.fitness < self.min_fitness:
            self.addview('MIN', 'is new min fitness')
            self._worst = newIndividual

        self._population.append((newIndividual, newIndividual.fitness))
        text = '{} added, fitness = {}'.format(newIndividual.key, newIndividual.fitness)
        self.addview('ADDED', text)

        if self.maximal_population >= 1:
            while (self.population_size > self.maximal_population):  # pops tuple with minimal fitness
                self._population = sorted(self.population, key=operator.itemgetter(1))
                poped = self._population.pop(0)
                self._worst = self._population[0][0]
                text = '{} is poped'.format(poped[0].key)
                self.addview('POP', text)

        self.display()

        if newIndividual.fitness > self.stop_fitness:
            return newIndividual
        else:
            return 1

    def _selectOne(self):
        if self.selection_mode == 1:
            return self._roulette_selection()
        elif self.selection_mode == 2:
            return self._tournament_selection()

    def _roulette_selection(self):
        self.empty_view
        self.addview('title', 'SELECTION BY ROULETTE WHEEL')

        positionList = list()
        aggregation = 0
        individuals, fitnesses = zip(*self._population)
        sumFitnesses = sum(fitnesses)

        self.addview('Fitnesses Sum', sumFitnesses)

        for (individual, fitness) in self._population:
            aggregation += fitness / sumFitnesses
            positionList.append((individual, aggregation))

        pick = random.uniform(0, 1)

        self.addview('Pick', pick)

        for (individual, position) in sorted(positionList, key=operator.itemgetter(1)):
            if position > pick:
                self.addview('Individual Position', position)
                self.addview('Individual Fitness', individual.fitness)
                self.addview('Individual Key', individual.key)
                break

        self.display()
        return individual

    def _cross(self, parent1, parent2):
        self.empty_view()
        self.addview('title', 'CROSSOVER & MUTATIONS RESUME')

        self.addview('0- Parent #1', parent1.key)
        self.addview('0- Parent #2', parent2.key)

        crossmode = self.crossmode
        if crossmode == 0:
            standardParent1 = parent1.get_binary_standard()
            standardParent2 = parent2.get_binary_standard()
        elif crossmode == 1:
            standardParent1 = parent1.get_real_standard()
            standardParent2 = parent2.get_real_standard()

        self.addview('1- Standardized parent #1', standardParent1)
        self.addview('1- Standardized parent #2', standardParent2)

        length1 = len(parent1.key)
        length2 = len(parent2.key)    # if not == raise exception

        self.addview('2- Length #1', length1)
        self.addview('2- Length #2', length2)

        view["2- LENGTH 1"] = length1
        view["2- LENGTH 2"] = length2

        child1 = list()
        child2 = list()

        for i in range(0, lengths1):
            string1, size1, minCrossPosition1, maxCrossPosition1 = standardParent1[i]
            string2, size2, minCrossPosition2, maxCrossPosition2 = standardParent2[i]  # if not equals, exception

            crosspoint = random.randint(minCrossPosition1, maxCrossPosition1)
            text = '3- Keys[' + str(i) + '] - CROSSPOINT'
            self.addview(str(text), crosspoint)

            childString1 = string1[0:crosspoint] + string2[crosspoint:]
            childString2 = string2[0:crosspoint] + string1[crosspoint:]

            text = '4- Child #1 - Key[' + str(i) + '] - After crossover'
            self.addview(str(text), childString1)
            text = '4- Child #2 - Key[' + str(i) + '] - After crossover'
            self.addview(str(text), childString2)

            childString1 = self._mutate(childString1, size1, minCrossPosition1, maxCrossPosition1)
            childString2 = self._mutate(childString2, size2, minCrossPosition2, maxCrossPosition2)

            text = '5- Child #1 - Key[' + str(i) + '] - After mutation'
            self.addview(str(text), childString1)
            text = '5- Child #2 - Key[' + str(i) + '] - After mutation'
            self.addview(str(text), childString2)

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

        self.addview('6- Unstandardized Child #1', child1)
        self.addview('6- Unstandardized Child #2', child2)

        self.display()

        return (result1, result2)

    def _mutate(self, childString, size, minCrossPosition, maxCrossPosition):  # Add display !!!
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

    def _recombination_ES_Nx_Nsigma_inter(self):
        population = self.population
        population_size = self.population_size
        key_length = len(population[0][0].key)
        new_key = list()
        for (individual, fitness) in population:
            for i in range(0, key_length):
                if len(new_key) <= i and i < (key_length / 2):
                    new_key.append([individual.key[i][0], 'ackley_x'])
                elif len(new_key) <= i:
                    new_key.append([individual.key[i][0], 'ackley_sigma'])
                else:
                    new_key[i][0] += individual.key[i][0]
        new_key = [(x / population_size, y) for x, y in new_key]
        new_father = AckleyIndividual(new_key)
        self._empty_population()
        self._empty_extrems()
        result = self._store(new_father)
        return result

    def _mutation_ES_Nx_Nsigma_gauss_2LR(self):
        individual = self.population[0][0]
        vector_size = len(individual.key)/2

        for i in range(0, self.child_number):
            global_step_size = float(self.global_learning_rate * random.gauss(0, 1))
            list_sigma = list()
            list_xi = list()

            for j in range(0, vector_size):
                local_step_size = float(self.local_learning_rate * random.gauss(0, 1))
                zk = float(random.gauss(0, 1))
                sigma = float(individual.key[30+j][0])
                sigma = float(sigma) * float(math.exp(local_step_size + global_step_size))
                list_sigma.append((sigma, 'ackley_sigma'))
                xi = individual.key[j][0] + float(sigma * zk)
                list_xi.append((xi, 'ackley_x'))
            new_key = list_xi + list_sigma
            new_individual = AckleyIndividual(new_key)
            result = self._store(new_individual)
        return result
