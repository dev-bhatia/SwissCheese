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

    def plot_debugger(self):
        """Print Data Lists we are plotting"""
        self._log.debug(self._subject._phases)
        self._log.debug(self._subject._overall_correct)
        self._log.debug(self._subject._absolute_bias)
        self._log.debug(self._subject._plus_minus_bias)
        self._log.debug(self._subject._no_lick)

    def remove_plots(self):
        """Remove All Plots saved in Plots dir"""
        self._log.info("Deleting plots...")
        if (('win32' or 'win64') in sys.platform): # If this runs on Windows OS
            os.system("ECHO Y | del .\\plots\\*")
        else: # UNIX System
            os.system("rm plots/*")
        self._log.info("Done deleting plots...")
        self._log.info("Compeleted Behavior Email Automation - EOF")

    def list_min(input_list):
        """Find the min of a list with None types"""
        min = 0
        for element in input_list:
            if (element != None):
                if element < min:
                    min = element
        return min

    def phase_changes(self):
        """Return indicies where phase first change"""
        phase_1 = None
        phase_2 = None
        phase_3 = None
        phase_4 = None

        # First we error correct phases
        # TODO: Make sure this correction works (ie. are there phases that just last one day?)
        for index in range(len(self._subject._phases)):
            try:
                if not (self._subject._phases[index] == self._subject._phases[index - 1]):
                    if not (self._subject._phases[index] == self._subject._phases[index + 1]):
                        if (self._subject._phases[index - 1] == self._subject._phases[index + 1]):
                            self._subject._phases[index] = self._subject._phases[index - 1]
                            self._log.critical("PHASE CORRECTION on Day {} for Mouse {}, now Phase is {}".format(
                                index, self._subject._mouse, self._subject._phases[index - 1]))
            except:
                continue

        for index in range(len(self._subject._phases)):
            if self._subject._phases[index] == 1 and phase_1 is None:
                phase_1 = index
            if self._subject._phases[index] == 2 and phase_2 is None:
                phase_2 = index
            if self._subject._phases[index] == 3 and phase_3 is None:
                phase_3 = index
            if self._subject._phases[index] == 4 and phase_4 is None:
                phase_4 = index

        return [phase_1, phase_2, phase_3, phase_4]

    def make_plot(self):
        """Generate and Save a Behavior Performance Plot"""
        # Config Figure
        plt.figure(figsize=(8,5))
        pylab.rcParams['xtick.major.pad']='8'
        pylab.rcParams['xtick.minor.pad']='8'
        plt.rcParams['axes.xmargin'] = 0

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

        # Obtain Data Labels
        try:
            oc_label = "OvAll Corr: {}%".format(round(self._subject._overall_correct[len(self._subject._overall_correct) - 1], 4))
        except TypeError as e:
            oc_label = ""
        try:
            nl_label = "No Lick: {}%".format(round(self._subject._no_lick[len(self._subject._no_lick) - 1], 4))
        except TypeError as e:
            nl_label = ""
        # No Longer Plotting ABS Bias
        # try:
        #     ab_label = "ABS Bias: {}%".format(round(self._subject._absolute_bias[len(self._subject._absolute_bias) - 1], 4))
        # except TypeError as e:
        #     ab_label = ""
        try:
            pm_label = "+/- Bias: {}%".format(round(self._subject._plus_minus_bias[len(self._subject._plus_minus_bias) - 1], 4))
        except TypeError as e:
            pm_label = ""

        # Plot Data
        x_count = range(0, len(self._subject._phases))
        plt.plot(x_count, self._subject._overall_correct, color="g",
                 label=oc_label, lw=1.0, marker="o")
        plt.plot(x_count, self._subject._no_lick, color="r",
                 label=nl_label, lw=1.0, marker="o")
        # No Longer Plotting ABS Bias
        # plt.plot(x_count, self._subject._absolute_bias, color="b",
        #         label=ab_label, lw=1.0, marker="o")
        plt.plot(x_count, self._subject._plus_minus_bias, color="b",
                 label=pm_label, lw=1.0, marker="o")

        # Color Phase regions & Bounds
        phase_indicies = self.phase_changes()
        plt.axvspan(0, phase_indicies[0], facecolor='#FFFFFF', alpha=1) # PHASE 0 - GRAY
        plt.axvspan(phase_indicies[0], len(x_count), facecolor='#ffedc9', alpha=1) # PHASE 1 - YELLOW
        plt.axvspan(phase_indicies[1], len(x_count), facecolor='#c9ffe0', alpha=1) # PHASE 2 - GREEN
        plt.axvspan(phase_indicies[2], len(x_count), facecolor='#c9e2ff', alpha=1) # PHASE 3 - BLUE
        plt.axvspan(phase_indicies[3], len(x_count), facecolor='#ffc9cf', alpha=1) # PHASE 4 - RED
        plt.hlines(0, 0, len(x_count), linestyles="dashed", colors="#000000", lw=2)

        # Format x and y ticks
        plt.xticks(x_count, fontsize='small', rotation='-22.5')
        # for ticklabel, tickcolor in zip(plt.gca().get_xticklabels(), days_colors):
        #     ticklabel.set_color(tickcolor)
        y_axis_lower_threshold = MattPLOT.list_min(self._subject._plus_minus_bias)
        if (y_axis_lower_threshold < -31.0):
            plt.yticks(np.arange(-50, 101, step=10))
        elif (y_axis_lower_threshold < 0.0):
            plt.yticks(np.arange(-30, 101, step=10))
        else:
            plt.yticks(np.arange(0, 101, step=10))

        # Color negative yticks
        count = len(plt.gca().get_yticklabels())
        if (len(plt.gca().get_yticklabels()) > 11):
            for ticklabel in plt.gca().get_yticklabels():
                if (len(plt.gca().get_yticklabels()) - count < len(plt.gca().get_yticklabels()) - 11):
                    ticklabel.set_color("#616161") # Grayscale negative y-axis ticks
                count -= 1

        # Set Labels & Titles
        plt.grid(axis="x")
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
