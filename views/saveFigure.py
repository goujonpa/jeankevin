#!/usr/local/bin/python
# -*-coding:Utf-8 -*

import matplotlib.pyplot as plot


def save_figure(iterations, fitness_sums, maximums, file_name):

    plot.plot(iterations, fitness_sums)
    fitness_plot_name = file_name + "_fit.pdf"
    plot.savefig(fitness_plot_name)
    plot.clf()
    plot.plot(iterations, maximums)
    maximum_plot_name = file_name + "_max.pdf"
    plot.savefig(maximum_plot_name)
