#!/usr/local/bin/python
# -*-coding:Utf-8 -*

from os import system

def setNumberCoupleSettings():
    """
    set every useful options for the execution
    """

    os.system("clear")

    print(
        "\n---> NumberCouple Individual\n"
        "\n===== OPTIONS =====\n"
    )
    
    options = {}

    preset = int(raw_input("PRESET\n"
        "Use preset ?\n"
        "\n\n-> 1: Source based preset\n"
        "\n-> 2: I WANT TO SET BY MYSELF\n"
        ))
    
    os.system("clear")

    if preset == 1:
        options["iterations"] = int(1000)
        options["stopFitness"] = float(0.98)
        options["crosspoint"] = int(111)
        options["crossmode"] = int(0)
        options["maximalPopulation"] = int(20)
        options["mutationMode"] = int(2)
        options["mutationProbability"] = float(0.01)
        options["verbose"] = int(0)
        options["initialPopulation"] = int(50)

    elif preset == 2:
        print("\nBASICS")
        x = int(raw_input("Stop Iterations Number:\n"))
        options["iterations"] = int(x) - 1

        options['stopFitness'] = float(raw_input("\nStop Fitness:\n"))
        os.system("clear")

        print("\nCROSSOVER")

        options["crossmode"] = int(raw_input("Crossover Mode:\n"
            "-> 0: Binary mode\n"
            "-> 1: Real mode\n"
            ))

        options["crosspoint"] = int(raw_input("Crosspoint Mode:\n"
            "-> 0 <= n <= 11: Fixed to position n\n"
            "-> Other: Random movement\n"
            ))
        os.system("clear")

        print("\nPOPULATION")
        options["maximalPopulation"] = int(raw_input("Maximal Population:\n"
            "-> n > 2: elitist insertion, just keep n best individuals\n"
            "-> Other: every individual is kept (can slow down the algorythm for several iterations)\n"
            ))
        os.system("clear")

        print("\nMUTATIONS")

        options["mutationMode"] = int(raw_input("Mutation Mode:\n"
            "-> 0: Swap mode (only for real mode)\n"
            "-> 1: Each nucleotid has a chance to be muted, one by one\n"
            "-> 2: 1 mutation maximum by child\n"
        ))

        options["mutationProbability"] = float(raw_input("Mutation Probability Mode:\n"
            "-> 0 < n < 1: Fixed Probability\n"
            "-> 2: Random Probability, basically between 1/BitArraySize and 1/PopulationSize\n"
            ))
        os.system("clear")

        print("\nVERBOSE")
        options["verbose"] = int(raw_input("Verbose Mode\n"
            "-> 1: Enabled\n"
            "-> 0: Disabled\n"
            ))
        os.system("clear")

        print("\n===== POPULATION INITIALISATION =====\n")
        options["initialPopulation"] = int(raw_input("\nInitialise with how much individuals ?\n"))
        os.system("clear")

    return options