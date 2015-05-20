#!/usr/local/bin/python
# -*-coding:Utf-8 -*

import os
import operator as op


def dDisplay(dictionary, verbose):
    if verbose == 1:
        print("\n=== {} ===\n\n".format(dictionary['title']))
        for (key, value) in sorted(dictionary.items(), key=op.itemgetter(0)):
            if not key == 'title':
                print("- {} : {}".format(key, value))
