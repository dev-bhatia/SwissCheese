"""
Library to generate plots for each mouse
"""
# System Python
import os
import sys
import pylab
import logging
import datetime
import numpy as np
import matplotlib.pyplot as plt

class MattPLOT:
    def __init__(self, log, mouse_object):
        """Library for Plotting and Saving datapoints of a MattMOUSE Object"""
        self._log = log
        self._subject = mouse_object

    def debug(self):
        print(self._subject._overall_correct)
        print(self._subject._absolute_bias)
        print(self._subject._no_lick)

    def make_plot(self):
        plt.figure(figsize=(8,5))
        pylab.rcParams['xtick.major.pad']='8'
        pylab.rcParams['xtick.minor.pad']='8'
        plt.rcParams['axes.xmargin'] = 0

        # Plot x-axis Phases and Colors
        # TODO: Fix up this sloppy implementation
        index = 0
        # days = []
        x_count = []
        for phase in self._subject._phases:
            x_count.append(index)
            index += 1

        # Set x-axis phase colors
        days_colors = []
        for mouse_phase in self._subject._phases:
            if (mouse_phase == 0):
                days_colors.append('#000000') # BLACK
            elif (mouse_phase == 1):
                days_colors.append('#D3200C') # RED
            elif (mouse_phase == 2):
                days_colors.append('#134DD6') # BLUE
            elif (mouse_phase == 3):
                days_colors.append('#009607') # GREEN
            elif (mouse_phase == 4):
                days_colors.append('#AF288B') # PURPLE
            else:
                days_colors.append('#FFFFFF') # WHITE

        # Identify Phase regions
        # phase_zero = [0, 1]
        # try:
        #     phase_one = []
        #     phase_one.append(self._subject._phases.index(1))
        #     try:
        #         phase_one.append(self._subject._phases.index(2))
        #     except ValueError as e:
        #         phase_one.append(len(self._subject._phases) - 1)
        # except ValueError as e:
        #     # Mouse is only on Previous Phase
        #     continue

        #
        # # Plot Translucesnt Phase Blocks
        # plt.axvspan(1.25, 1.55, facecolor='g', alpha=0.5)
        # plt.axvspan(1.25, 1.55, facecolor='g', alpha=0.5)
        # plt.axvspan(1.25, 1.55, facecolor='g', alpha=0.5)
        # plt.axvspan(1.25, 1.55, facecolor='g', alpha=0.5)
        # plt.axvspan(1.25, 1.55, facecolor='g', alpha=0.5)

        # Plot Data
        try:
            oc_label = "OvAll Corr: {}%".format(round(self._subject._overall_correct[len(self._subject._overall_correct) - 1], 4))
        except TypeError as e:
            oc_label = ""
        try:
            nl_label = "No Lick: {}%".format(round(self._subject._no_lick[len(self._subject._no_lick) - 1], 4))
        except TypeError as e:
            nl_label = ""
        try:
            ab_label = "ABS Bias: {}%".format(round(self._subject._absolute_bias[len(self._subject._absolute_bias) - 1], 4))
        except TypeError as e:
            ab_label = ""
        plt.plot(x_count, self._subject._overall_correct, color="g",
                 label=oc_label, lw=1.0, marker="o")
        plt.plot(x_count, self._subject._no_lick, color="r",
                 label=nl_label, lw=1.0, marker="o")
        plt.plot(x_count, self._subject._absolute_bias, color="b",
                 label=ab_label, lw=1.0, marker="o")

        # Format titles
        plt.yticks(np.arange(0, 101, step=10))
        plt.xticks(x_count, fontsize='small', rotation='-22.5')
        for ticklabel, tickcolor in zip(plt.gca().get_xticklabels(), days_colors):
            ticklabel.set_color(tickcolor)

        plt.grid()
        plt_title = "Cage {} Mouse {} - {} - Phase {} - {} Bias".format(
                        self._subject._cage,
                        self._subject._mouse,
                        self._subject._feature,
                        self._subject._phases[len(self._subject._phases) - 1],
                        self._subject._bias_side)
        plt.legend(title=plt_title, title_fontsize="large", fontsize="medium",
                   loc="upper center", bbox_to_anchor=(0.5, 1.15),
                   ncol=3, fancybox=True)
        plt.xlabel('Day')
        plt.ylabel('Performance')
        plt.savefig("plots/m{}.png".format(self._subject._mouse))

    def remove_plots(self):
        """Remove All Plots saved in Plots dir"""
        self._log.info("Deleting plots...")
        if (('win32' or 'win64') in sys.platform): # If this runs on Windows OS
            os.system("ECHO Y | del .\\plots\\*")
        else: # UNIX System
            os.system("rm plots/*")
        self._log.info("Done deleting plots...")
        self._log.info("Compeleted Behavior Email Automation - EOF")
