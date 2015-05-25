#!/usr/local/bin/python
# -*-coding:Utf-8 -*

import matplotlib.pyplot as plot


def save_figure(iterations, mesures, file_name):
    for (key, value) in mesures.items():
        plot.plot(iterations, value)
        name = file_name + '_' + key + '.pdf'
        plot.savefig(name)
        plot.clf()
