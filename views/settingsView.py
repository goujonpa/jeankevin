#!/usr/local/bin/python
# -*-coding:Utf-8 -*

import os
import math


def set_NCpl_settings():

    os.system("clear")

    print(
        "\n---> NumberCouple Individual\n"
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
        options["iterations"] = int(5000)
        options["stopFitness"] = float(1)
        options["crosspoint"] = int(111)
        options["crossmode"] = int(0)
        options["maximalPopulation"] = int(20)
        options["mutationMode"] = int(1)
        options["mutationProbability"] = float(2)
        options["verbose"] = int(0)
        options["initialPopulation"] = int(1000)

    elif preset == 2:
        print("\nBASICS")
        x = int(raw_input("Stop Iterations Number:\n"))
        options["iterations"] = int(x) - 1

        options['stopFitness'] = float(raw_input("\nStop Fitness:\n"))
        os.system("clear")

        print("\nCROSSOVER")

        options["crossmode"] = int(raw_input(
            "Crossover Mode:\n"
            "-> 0: Binary mode\n"
            "-> 1: Real mode\n"
        ))

        options["crosspoint"] = int(raw_input(
            "Crosspoint Mode:\n"
            "-> 0 <= n <= 11: Fixed to position n\n"
            "-> Other: Random movement\n"
        ))
        os.system("clear")

        print("\nPOPULATION")
        options["maximalPopulation"] = int(raw_input(
            "Maximal Population:\n"
            "-> n > 2: elitist insertion, just keep n best individuals\n"
            "-> Other: every individual is kept (can slow down the algorythm for several iterations)\n"
        ))
        os.system("clear")

        print("\nMUTATIONS")

        options["mutationMode"] = int(raw_input(
            "Mutation Mode:\n"
            "-> 0: Swap mode (only for real mode)\n"
            "-> 1: Each nucleotid has a chance to be muted, one by one\n"
            "-> 2: 1 mutation maximum by child\n"
        ))

        options["mutationProbability"] = float(raw_input(
            "Mutation Probability Mode:\n"
            "-> 0 < n < 1: Fixed Probability\n"
            "-> 2: Random Probability, basically between 1/BitArraySize and 1/PopulationSize\n"
        ))
        os.system("clear")

        print("\nVERBOSE")
        options["verbose"] = int(raw_input(
            "Verbose Mode\n"
            "-> 1: Enabled\n"
            "-> 0: Disabled\n"
        ))
        os.system("clear")

        print("\n===== POPULATION INITIALISATION =====\n")
        options["initialPopulation"] = int(raw_input("\nInitialise with how much individuals ?\n"))
        os.system("clear")

    return options


def set_AklI_settings():

    os.system("clear")

    print(
        "\n---> Ackley Function Individual\n"
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
        options["iterations"] = int(50)
        options["stopFitness"] = float(0.80)
        options["base"] = int(8)
        options['verbose'] = int(1)

    elif preset == 2:
        print("\nBASICS")
        x = int(raw_input("Stop Iterations Number:\n"))
        options["iterations"] = int(x) - 1

        options['stopFitness'] = float(raw_input("\nStop Fitness:\n"))

        print("\nGENERATIONS")

        options["base"] = int(raw_input(
            "n setting:\n"
            "lambda (number of child from the father) = 8 * n\n"
            "mu (number of best child selected to make new father) = lambda / 4\n"
            "t (global step size) = 1 / (n)^(1/2)\n"
            "ti (component step size) = 1 / (n)^(1/4)\n"
        ))

        print("\nVERBOSE")
        options["verbose"] = int(raw_input(
            "Verbose Mode\n"
            "-> 1: Enabled\n"
            "-> 0: Disabled\n"
        ))
        os.system("clear")
    options['maximalPopulation'] = 2 * options['base']
    options['childNumber'] = 8 * options['base']
    options['globalLearningTax'] = 1.0 / pow(options['base'], 0.5)
    options['localLearningTax'] = 1.0 / pow(options['base'], 0.25)

    return options
