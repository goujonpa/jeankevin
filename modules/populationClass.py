#!/usr/local/bin/python
# -*-coding:Utf-8 -*

import views.displayView as v
import views.saveFigure as vSave
import views.settingsView as vSet
from modules.numberCoupleClass import NumberCouple
from modules.ackleyIndividualClass import AckleyIndividual
import operator
import random
import math
import os


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

    @property
    def crosstype(self):
        return self._settings['crossType']

    @property
    def selection_mode(self):
        return self._settings['selectionMode']

    def enable_verbose(self):
        self._settings['verbose'] = int(1)

    def disable_verbose(self):
        self._settings['verbose'] = int(0)

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
        self.disable_verbose()
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
        self.enable_verbose()
        os.system('clear')

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
        vSave.save_figure(self._save_iterations, self._save_fitness_sums, self._save_maximums, 'simuES')

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

            result1 = self._store(result[0])
            result2 = self._store(result[1])
            result = (result1, result2)
# ============= cacacacacacaca
        childString1 = self._mutation(childString1, size1, minCrossPosition1, maxCrossPosition1)
        childString2 = self._mutation(childString2, size2, minCrossPosition2, maxCrossPosition2)

        text = '5- Child #1 - Key[' + str(i) + '] - After mutation'
        self.addview(str(text), childString1)
        text = '5- Child #2 - Key[' + str(i) + '] - After mutation'
        self.addview(str(text), childString2)
#   ------------

            i = i + 1
            self._save_iterations.append(i)
            self._save_fitness_sums.append(self.fitness_sums)
            self._save_maximums.append(self.best.fitness)

        best = self.best
        print("\n\nBest:\n{} : fitness = {}".format(best.key, best.fitness))
        vSave.save_figure(self._save_iterations, self._save_fitness_sums, self._save_maximums, 'simuGA')

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
        self.empty_view()
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

    def _crossover(self, parent1, parent2):
        self.empty_view()
        self.addview('title', 'CROSSOVER & MUTATIONS RESUME')

        self.addview('0- Parent #1', parent1.key)
        self.addview('0- Parent #2', parent2.key)

        crossmode = self.crossmode
        if crossmode == 'binary':
            standard_parent1 = parent1.get_binary_standard()
            standard_parent2 = parent2.get_binary_standard()
        elif crossmode == 'real':
            standard_parent1 = parent1.get_real_standard()
            standard_parent2 = parent2.get_real_standard()

        self.addview('1- Standardized parent #1', standard_string1)
        self.addview('1- Standardized parent #2', standard_string2)

        crossover_type = self.crosstype
        if crossover_type == 'randomOnePoint':
            childs = self._cross_random_one_point(standard_parent1, standard_parent2)

        if crossmode == 'binary':
            child1 = parent1.get_binary_unstandardized(childs[0])
            child2 = parent1.get_binary_unstandardized(childs[1])
        elif crossmode == 'real':
            child1 = parent1.get_binary_unstandardized(childs[0])
            child2 = parent1.get_binary_unstandardized(childs[1])

        self.addview('6- Unstandardized Child #1', child1)
        self.addview('6- Unstandardized Child #2', child2)

        if self.individuals_type == 'NumberCouple':
            child1 = NumberCouple(child1)
            child2 = NumberCouple(child2)

        return (child1, child2)

    def _cross_random_one_point(standard_parent1, standard_parent2):
        length1 = len(standard_parent1)
        length2 = len(standard_parent2)  # if difference, exception

        crosspoint = random.randint(min_position, max_position)
        text = '3- Keys[' + str(i) + '] - CROSSPOINT'
        self.addview(str(text), crosspoint)

        child1 = list()
        child2 = list()

        for i in range(0, length1):
            string1, size1, min_position1, max_position1 = standard_parent1[i]
            string2, size2, min_position2, max_position2 = standard_parent2[i]

            string1 = string1[0:crosspoint] + string2[crosspoint:]
            string2 = string2[0:crosspoint] + string1[crosspoint:]
            child1.append(string1)
            child2.append(string2)

            text = '4- Child #1 - Key[' + str(i) + '] - After crossover'
            self.addview(str(text), string1)
            text = '4- Child #2 - Key[' + str(i) + '] - After crossover'
            self.addview(str(text), string2)

        return (string1, string2)


    def _mutation(self, string, size, min_position, max_position):  # Add display !!!
        crossmode = self.crossmode
        mutation_mode = self.mutation_mode
        probability = self.mutation_probability

        if probability > 1:
            min_probability = 1.0 / max(size, self.population_size)
            max_probability = 1.0 / min(size, self.population_size)
            probability = random.uniform(min_probability, max_probability)

        if mutation_mode == 'swap':   # swap mode
            string = self._mutation_GA_swap(string, size, min_position, max_position, probability)
        elif mutation_mode == 'everyNucleotid':    # all nucleotid mode
            string = self._mutation_GA_every_nucleotid(string, size, min_position, max_position, probability, crossmode)
        elif mutation_mode == 'oneNucleotid':    # max 1 nucleotid mode
            string = self._mutation_GA_one_nucleotid(string, size, min_position, max_position, probability, crossmode)

        return string

    def _mutation_GA_swap(self, string, size, min_position, max_position, mutation_probability):
        a = 0
        b = 0
        while a == b and b < a:
            a = random.randint(min_position, max_position)
            b = random.randint(min_position, max_position)
        string = string[0:a] + string[b] + string[a+1:b] + string[a] + string[b+1:]
        return string

    def _mutation_GA_every_nucleotid(self, string, size, min_position, max_position, mutation_probability, crossmode):
        for i in range(min_position, max_position):
            pick = random.uniform(0, 1)
            if pick < mutation_probability:
                if crossmode == 'binary':
                    if string[i] == '1':
                        char = '0'
                    elif string[i] == '0':
                        char = '1'
                elif crossmode == 'real':
                    char = str(random.randint(0, 9))
                string = string[0:i] + char + string[i+1:]
        return string

    def _mutation_GA_one_nucleotid(self, string, s_type, size, min_position, max_position, mutation_probability, crossmode):
        pick = random.uniform(0, 1)
        if pick < mutation_probability:
            i = random.randint(min_position, max_position)
            if crossmode == 'binary':
                if string[i] == '1':
                    char = '0'
                elif string[i] == '0':
                    char = '1'
            elif crossmode == 'real':
                char = str(random.randint(0, 9))
            string = string[0:i] + char + string[i+1:]
            return string

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
