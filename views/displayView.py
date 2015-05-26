#!/usr/local/bin/python
# -*-coding:Utf-8 -*

import os
import operator as op


def display(element, verbose=1, iteration_info=0):
    if verbose == 1 and type(element) == dict:
        print("=== {} ===\n\n".format(element['title']))
        for (key, value) in sorted(element.items(), key=op.itemgetter(0)):
            if not key == 'title':
                print("- {} : {}".format(key, value))
        raw_input()
        os.system('clear')
    else:
        print("Iteration : {} / {}".format(iteration_info[0], iteration_info[1]))
