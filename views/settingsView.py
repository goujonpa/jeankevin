#!/usr/local/bin/python
# -*-coding:Utf-8 -*

import os
import math


def set_NCpl_settings():

    os.system("clear")

    print(
        "---> NumberCouple Individual\n"
        "\n===== OPTIONS =====\n"
    )

    options = {}

    preset = int(raw_input(
        "PRESET\n"
        "Use preset ?\n"
        "\n\n-> 1: Source based preset\n"
        "\n-> 2: I WANT TO SET BY MYSELF\n"
    ))

    os.system("clear")

    if preset == 1:
        options["iterations"] = int(1000000)
        options["stopFitness"] = float(1)
        options["mode"] = 'binary'
        options['crossMode'] = 'randomOnePoint'
        options["maximalPopulation"] = int(50)
        options["mutationMode"] = 'everyNucleotid'
        options["mutationProbability"] = float(2)
        options["verbose"] = False
        options["initialPopulation"] = int(100)
        options['selectionMode'] = 'roulette'

    elif preset == 2:
        print('BASICS')
        x = int(raw_input('Stop Iterations Number:\n'))
        options['iterations'] = int(x)

        options['stopFitness'] = float(raw_input('\nStop Fitness:\n'))
        os.system('clear')

        print('SELECTION')

        options['selectionMode'] = int(raw_input(
            '\nSelection Method:\n'
            '--> 1: Roulette method\n'
        ))
        if options['selectionMode'] == 1:
            options['selectionMode'] = 'roulette'

        os.system('clear')

        print('CROSSOVER & MUTATIONS')

        options['mode'] = int(raw_input(
            'Mode:\n'
            '-> 1: Binary mode\n'
            '-> 2: Real mode\n'
        ))
        if options['mode'] == 1:
            options['mode'] = 'binary'
        elif options['mode'] == 2:
            options['mode'] = 'real'

        options['crossMode'] = int(raw_input(
            'Crossover Mode:\n'
            '--> 1: One random one point\n'
        ))
        if options['crossMode'] == 1:
            options['crossMode'] = 'randomOnePoint'

        options['mutationMode'] = int(raw_input(
            'Mutation Mode:\n'
            '-> 0: Swap mode (only for real mode)\n'
            '-> 1: Each nucleotid has a chance to be muted, one by one\n'
            '-> 2: 1 mutation maximum by child\n'
        ))
        if options['mutationMode'] == 0:
            options['mutationMode'] = 'swap'
        elif options['mutationMode'] == 1:
            options['mutationMode'] = 'everyNucleotid'
        elif options['mutationMode'] == 2:
            options['mutationMode'] = 'oneNucleotid'

        options['mutationProbability'] = float(raw_input(
            'Mutation Probability Mode:\n'
            '-> 0 < n < 1: Fixed Probability\n'
            '-> 2: Random Probability, basically between 1/BitArraySize and 1/PopulationSize\n'
        ))

        os.system('clear')

        print("\nPOPULATION")
        options["maximalPopulation"] = int(raw_input(
            "Maximal Population:\n"
            "-> n > 0: elitist insertion, just keep n best individuals\n"
            "-> Other: every individual is kept (can slow down the algorythm for several iterations)\n"
        ))

        options["initialPopulation"] = int(raw_input("\nInitialise with how much individuals ?\n"))
        os.system("clear")

        print("\nVERBOSE")
        options["verbose"] = int(raw_input(
            "Verbose Mode\n"
            "-> 1: Enabled\n"
            "-> 0: Disabled\n"
        ))
        if options['verbose'] == 0:
            options['verbose'] = False
        elif options['verbose'] == 1:
            options['verbose'] = True

        os.system("clear")
    return options


def set_AklI_settings():
    os.system("clear")
    print(
        "---> Ackley Function Individual\n"
        "\n===== OPTIONS =====\n"
    )

    options = {}

    preset = int(raw_input(
        "PRESET\n"
        "Use preset ?\n"
        "\n\n-> 1: Source based preset\n"
        "\n-> 2: I WANT TO SET BY MYSELF\n"
    ))

    os.system("clear")

    if preset == 1:
        options["iterations"] = int(1000)
        options["stopFitness"] = float(0.99)
        options["base"] = int(10)
        options['verbose'] = False
        options['selectionMode'] = int(1)
        options['mutationMode'] = '2LRNS'
        options['recombinationMode'] = 'intermediate'
        options['sigmaBoost'] = True

    elif preset == 2:
        print('\nBASICS')
        x = int(raw_input('Stop Iterations Number:\n'))
        options["iterations"] = int(x) - 1

        options['stopFitness'] = float(raw_input('\nStop Fitness:\n'))

        print("\nGENERATIONS")

        options["base"] = int(raw_input(
            'n setting:\n'
            'lambda (number of child from the father) = 8 * n\n'
            'mu (number of best child selected to make new father) = lambda / 4\n'
            't (global step size) = 1 / (n)^(1/2)\n'
            'ti (component step size) = 1 / (n)^(1/4)\n'
        ))

        print('RECOMBINATION')
        options['recombinationMode'] = int(raw_input(
           'Recombination mode:\n'
           '1- Intermediate\n'
           '2- Select Best\n'
           '3- Weighted\n'
        ))
        if options['recombinationMode'] == 1:
            options['recombinationMode'] = 'intermediate'
        elif options['recombinationMode'] == 2:
            options['recombinationMode'] = 'best'
        elif options['recombinationMode'] == 3:
            options['recombinationMode'] = 'weighted'

        print('MUTATION')
        options['mutationMode'] = int(raw_input(
           'Mutation mode:\n'
           '1- 2 Learning Rates, N Sigmas\n'
           '2- 1 Learning Rate, 1 Sigma\n'
        ))
        if options['mutationMode'] == 1:
            options['mutationMode'] = '2LRNS'
        elif options['mutationMode'] == 2:
            options['mutationMode'] = '1LR1S'

        print('SIGMA BOOST')
        options['sigmaBoost'] = int(raw_input(
           'Allow sigma boost YOLO special feature ?\n'
           '1- sigma nitro enabled\n'
           '2- sigma nitro disabled\n'
        ))
        if options['sigmaBoost'] == 1:
            options['sigmaBoost'] = True
        elif options['sigmaBoost'] == 2:
            options['sigmaBoost'] = False


        print("\nVERBOSE")
        options["verbose"] = int(raw_input(
            "Verbose Mode\n"
            "-> 1: Enabled\n"
            "-> 0: Disabled\n"
        ))
        os.system("clear")
    options['maximalPopulation'] = 2 * options['base']
    options['childNumber'] = 8 * options['base']
    options['globalLearningRate'] = 1.0 / pow(options['base'], 0.5)
    options['localLearningRate'] = 1.0 / pow(options['base'], 0.25)

    return options
