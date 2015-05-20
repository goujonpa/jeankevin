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

choice = int(raw_input("1 OU 2 ?"))
if choice == 1:
    population = Population('NumberCouple')
    population.run_GA()
