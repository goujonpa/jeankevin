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
        self._save_sigma_value = list()
        self._population = list()
        self._view = dict()
        self._sigma_count = 0
        self._initialise()

    # ========== PROPERTIES & BASIC METHODS ==========

    # ----- Population

    @property
    def maximal_population(self):
        return self._settings['maximalPopulation']

    def _empty_population(self):
        self._empty_extrems()
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

    @property
    def parent(self):
        return self.population[0][0]

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
    def mode(self):
        return self._settings['mode']

    @property
    def crossmode(self):
        return self._settings['crossMode']

    @property
    def selection_mode(self):
        return self._settings['selectionMode']

    @property
    def recombination_mode(self):
        return self._settings['recombinationMode']

    @property
    def sigma_boost(self):
        return self._settings['sigmaBoost']

    @property
    def sigma_count(self):
        return self._sigma_count

    def enable_verbose(self):
        self._settings['verbose'] = True

    def disable_verbose(self):
        self._settings['verbose'] = False

    # ----- View

    @property
    def view(self):
        return self._view

    def addview(self, key, value):
        self._view[key] = value

    def empty_view(self):
        self._view = dict()

    def display(self, element=None, verbose=True):
        if element is None:
            v.display(self._view, self.verbose, (self.current_iteration, self.stop_iteration))
        else:
            v.display(element, verbose, (self.current_iteration, self.stop_iteration))

    # ----- Others

    @property
    def current_iteration(self):
        return self._current_iteration

    # ========== GA & ES Algorithms ==========

    def _initialise(self):  # could be more generic
        verbose = False
        if self.verbose is True:
            self.disable_verbose()
            verbose = True
        if self.individuals_type == 'NumberCouple':
            for i in range(0, self.initial_population):
                newIndividual = NumberCouple()
                if newIndividual.fitness < self.stop_fitness:
                    self._store(newIndividual)
                else:
                    i -= 1
        elif self.individuals_type == 'AckleyIndividual':
            adam = AckleyIndividual()
            result = self._store(adam)
        if verbose is True:
            self.enable_verbose()
        os.system('clear')

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
            result = self._crossover(parent1, parent2)
            result1 = self._store(self._mutation_GA(result[0]))
            result2 = self._store(self._mutation_GA(result[1]))
            result = (result1, result2)

            i += 1
            self._save_iterations.append(i)
            self._save_fitness_sums.append(self.fitness_sums)
            self._save_maximums.append(self.best.fitness)

        best = self.best
        print("\n\nBest:\n{} : fitness = {}".format(best.key, best.fitness))
        mesures['max'] = self._save_maximums
        mesures['fitness'] = self._save_fitness_sums
        vSave.save_figure(self._save_iterations, mesures, 'simuGA')

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

        if self.maximal_population > 0:
            while (self.population_size > self.maximal_population):  # pops tuple with minimal fitness
                self._population = sorted(self.population, key=operator.itemgetter(1))
                poped = self._population.pop(0)
                self._worst = self._population[0][0]
                text = '{} is poped'.format(poped[0].key)
                self.addview('POP', text)

        self.display()

        if newIndividual.fitness >= self.stop_fitness:
            return newIndividual
        else:
            return 1

    def _selectOne(self):
        if self.selection_mode == 'roulette':
            return self._roulette_selection()
        elif self.selection_mode == 'turnament':
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
        self.addview('title', 'CROSSOVER')

        self.addview('0- Parent #1', parent1.key)
        self.addview('0- Parent #2', parent2.key)

        mode = self.mode
        if mode == 'binary':
            standard_parent1 = parent1.get_binary_standard()
            standard_parent2 = parent2.get_binary_standard()
        elif mode == 'real':
            standard_parent1 = parent1.get_real_standard()
            standard_parent2 = parent2.get_real_standard()

        self.addview('1- Standardized parent #1', standard_parent1)
        self.addview('1- Standardized parent #2', standard_parent2)

        crossover_mode = self.crossmode
        if crossover_mode == 'randomOnePoint':
            childs = self._cross_random_one_point(standard_parent1, standard_parent2)

        if mode == 'binary':
            child1 = parent1.get_binary_unstandardized(childs[0])
            child2 = parent1.get_binary_unstandardized(childs[1])
        elif mode == 'real':
            child1 = parent1.get_binary_unstandardized(childs[0])
            child2 = parent1.get_binary_unstandardized(childs[1])

        self.addview('5- Unstandardized Child #1', child1)
        self.addview('5- Unstandardized Child #2', child2)

        if self.individuals_type == 'NumberCouple':
            child1 = NumberCouple(child1)
            child2 = NumberCouple(child2)

        self.display()

        return (child1, child2)

    def _cross_random_one_point(self, standard_parent1, standard_parent2):
        length1 = len(standard_parent1)
        length2 = len(standard_parent2)  # if difference, exception

        child1 = list()
        child2 = list()

        for i in range(0, length1):

            string1, size1, min_position1, max_position1 = standard_parent1[i]
            string2, size2, min_position2, max_position2 = standard_parent2[i]  # if not equal raise exception

            crosspoint = random.randint(min_position1, max_position1)
            text = '3- Keys[' + str(i) + '] - CROSSPOINT'
            self.addview(str(text), crosspoint)

            string1 = string1[0:crosspoint] + string2[crosspoint:]
            string2 = string2[0:crosspoint] + string1[crosspoint:]

            text = '4- Child #1 - Key[' + str(i) + '] - After crossover'
            self.addview(str(text), string1)
            text = '4- Child #2 - Key[' + str(i) + '] - After crossover'
            self.addview(str(text), string2)

            child1.append(string1)
            child2.append(string2)

        return (child1, child2)

    def _mutation_GA(self, child):  # Add display !!!
        self.empty_view()
        self.addview('title', 'MUTATION')
        self.addview('0- Individual', child.key)

        mode = self.mode
        mutation_mode = self.mutation_mode
        probability = self.mutation_probability

        if mode == 'binary':
            standard_child = child.get_binary_standard()
        elif mode == 'real':
            standard_child = child.get_real_standard()
        self.addview('1- Standardized', standard_child[0])

        mutated_child = list()
        i = 0
        for (string, size, min_position, max_position) in standard_child:

            if probability > 1:
                min_probability = 1.0 / max(size, self.population_size)
                max_probability = 1.0 / min(size, self.population_size)
                probability = random.uniform(min_probability, max_probability)

            self.addview('2- Mutation Probability', probability)
            text = '3- key[' + str(i) + '] before mutation'
            self.addview(text, string)

            if mutation_mode == 'swap':   # swap mode
                string = self._mutation_GA_swap(string, size, min_position, max_position, probability)
            elif mutation_mode == 'everyNucleotid':    # all nucleotid mode
                string = self._mutation_GA_every_nucleotid(
                    string, size, min_position, max_position, probability, mode
                )
            elif mutation_mode == 'oneNucleotid':    # max 1 nucleotid mode
                string = self._mutation_GA_one_nucleotid(
                    string, size, min_position, max_position, probability, mode
                )

            text = '4- key[' + str(i) + '] after potential mutation'
            self.addview(text, string)
            mutated_child.append(string)
            i += 1

        if mode == 'binary':
            child = child.get_binary_unstandardized(mutated_child)
        elif mode == 'real':
            child = child.get_real_unstandardized(mutated_child)

        if self.individuals_type == 'NumberCouple':
            child = NumberCouple(child)

        self.addview('5- Result', child.key)
        self.display()

        return child

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

    def _mutation_GA_one_nucleotid(self, string, size, min_position, max_position, mutation_probability, crossmode):
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

    def run_ES(self):
        # Initialisation done by initialise()
        i = 0
        mesures = dict()

        while i < self.stop_iteration and self.max_fitness < self.stop_fitness:
            self._current_iteration = i
            self._save_iterations.append(i)
            self._save_fitness_sums.append(self.fitness_sums)
            self._save_maximums.append(self.best.fitness)
            self._save_sigma_value.append(self.best.average_sigma)
            self._mutation_ES()  # Self-adapted
            j = i + 0.5

            self._save_iterations.append(j)
            self._save_fitness_sums.append(self.fitness_sums)
            self._save_maximums.append(self.best.fitness)
            self._save_sigma_value.append(self.best.average_sigma)
            self._recombination_ES()
            if self.sigma_boost is True and not self.best.fitness > self._save_maximums[-1]:
                if self.sigma_count < 5:
                    self._sigma_count += 1
                else:
                    self._sigma_count = 0
                    self._population[0][0].sigma_boost()
            elif self.sigma_boost is True:
                self._sigma_count = 0
            i += 1

        best = self.best
        print("\n\nBest:\n{} : fitness = {}".format(best.key, best.fitness))
        mesures['max'] = self._save_maximums
        mesures['fitness'] = self._save_fitness_sums
        mesures['sigma'] = self._save_sigma_value
        vSave.save_figure(self._save_iterations, mesures, 'simuES')

    def _recombination_ES(self):
        if self.recombination_mode == 'intermediate':
            self._recombination_ES_intermediate()
        elif self.recombination_mode == 'best':
            self._recombination_ES_best()
        elif self.recombination_mode == 'weighted':
            self._recombination_ES_weighted()

    def _recombination_ES_intermediate(self):
        self.empty_view()
        self.addview('title', 'RECOMBINATION INTERMEDIATE')
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

        new_key = [(float(x / population_size), y) for x, y in new_key]
        self.addview('New individual xs', [x for (x, y) in new_key[0:(len(new_key) / 2)]])
        self.addview('New individual sigmas', [x for (x, y) in new_key[(len(new_key) / 2):]])
        new_father = AckleyIndividual(new_key)
        self._empty_population()
        result = self._store(new_father)
        self.display()

    def _recombination_ES_weighted(self):  # TO IMPLEMENT MG
        self.empty_view()
        self.addview('title', 'RECOMBINATION WEIGHTED')
        population = self.population
        key_length = len(population[0][0].key)
        new_key = list()

        for (individual, fitness) in population:
            for i in range(0, key_length):
                if len(new_key) <= i and i < (key_length / 2):
                    new_key.append([(individual.key[i][0] * individual.fitness), 'ackley_x'])
                elif len(new_key) <= i:
                    new_key.append([(individual.key[i][0] * individual.fitness), 'ackley_sigma'])
                else:
                    new_key[i][0] += (individual.key[i][0] * individual.fitness)

        new_key = [(float(x / self.fitness_sums), y) for x, y in new_key]
        self.addview('New individual xs', [x for (x, y) in new_key[0:(len(new_key) / 2)]])
        self.addview('New individual sigmas', [x for (x, y) in new_key[(len(new_key) / 2):]])
        new_father = AckleyIndividual(new_key)
        self._empty_population()
        result = self._store(new_father)
        self.display()

    def _recombination_ES_best(self):
        self.empty_view()
        self.addview('title', 'RECOMBINATION BEST')
        best = self.best
        self.addview('Best', best.key)
        self.addview('Fitness', best.fitness)
        self._empty_population()
        self._store(best)
        self.display()

    def _mutation_ES(self):
        if self.mutation_mode == '1LR1S':
            self._mutation_ES_1LR1S()
        elif self.mutation_mode == '2LRNS':
            self._mutation_ES_2LRNS()

    def _mutation_ES_2LRNS(self):  # pretty weird results....????!
        self.empty_view()
        self.addview('title', 'MUTATION 2LRNS')
        individual = self.parent
        vector_size = individual.vector_size
        self.addview('0- Individual xs before mutation', [x for (x, y) in individual.xi])
        self.addview('0- Individual sigmas before mutation', [x for (x, y) in individual.sigmas])
        self.addview('0- Global learning rate:', self.global_learning_rate)

        for i in range(0, self.child_number):
            global_step_size = float(self.global_learning_rate * random.gauss(0, 1))
            self.addview('1- Global step size', global_step_size)
            list_sigma = list()
            list_xi = list()

            for j in range(0, vector_size):
                local_step_size = float(random.gauss(0, 1) * self.local_learning_rate)
                sigma = float(individual.key[30+j][0])
                sigma = sigma * float(math.exp(global_step_size + local_step_size))
                list_sigma.append((sigma, 'ackley_sigma'))
                xi = float(individual.key[j][0]) + float(sigma * random.gauss(0, 1))
                list_xi.append((xi, 'ackley_x'))

            new_key = list_xi + list_sigma
            self.addview('2- New child xs', [x for (x, y) in list_xi])
            self.addview('3- New child sigmas', [x for (x, y) in list_sigma])
            new_individual = AckleyIndividual(new_key)
            self.addview('4- New fitness', new_individual.fitness)
            self.display()
            self._store(new_individual)
            self.empty_view()
            self.addview('title', 'MUTATION 1LR1S')

    def _mutation_ES_1LR1S(self):
        self.empty_view()
        self.addview('title', 'MUTATION 1LR1S')
        individual = self.parent
        vector_size = individual.vector_size
        individual.uniformise_sigma()
        self.addview('0- Individual xs Before mutation', [x for (x, y) in individual.xi])
        self.addview('0- Individual sigma Before mutation', [x for (x, y) in individual.sigmas[0:1]])
        self.addview('0- Global learning rate:', self.global_learning_rate)

        for i in range(0, self.child_number):
            global_step_size = float(self.global_learning_rate * random.gauss(0, 1))
            self.addview('1- Global step size', global_step_size)
            list_sigma = list()
            list_xi = list()

            for j in range(0, vector_size):
                sigma = float(individual.key[30+j][0])
                sigma = sigma * float(math.exp(global_step_size))
                list_sigma.append((sigma, 'ackley_sigma'))
                xi = float(individual.key[j][0]) + float(sigma * random.gauss(0, 1))
                list_xi.append((xi, 'ackley_x'))

            new_key = list_xi + list_sigma
            self.addview('2- New child xs', [x for (x, y) in list_xi])
            self.addview('3- New child sigma', [x for (x, y) in list_sigma[0:1]])
            new_individual = AckleyIndividual(new_key)
            self.addview('4- New fitness', new_individual.fitness)
            self.display()
            self._store(new_individual)
            self.empty_view()
            self.addview('title', 'MUTATION 1LR1S')
