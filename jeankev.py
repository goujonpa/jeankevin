#!/usr/local/bin/python
# -*-coding:Utf-8 -*

######################################################
# Jean Kevin                                         #
# Python application                                 #
# Conformance to PEP 8 !                             #
# Implementation proposition for Genetic Algorithms  #
# School Project developped by Paul GOUJON, 2015     #
#                                                    #
# Documentation can be found in the "Report" folder  #
######################################################

from modules.populationClass import *
import os

os.system('clear')

choice = int(raw_input(
    'GA or ES\n'
    '--> 1: GA\n'
    '--> 2: ES\n'
))
if choice == 1:
    population = Population('NumberCouple')
    population.run_GA()
elif choice == 2:
    population = Population('AckleyIndividual')
    population.run_ES()
