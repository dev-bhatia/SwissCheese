"""
Library to generate plots for each mouse
"""
# System Python
import os
import sys
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

        # Subtract index by 0.5 to phase shift by half a day (asthetic change)
        for index in range(len(self._subject._phases)):
            if self._subject._phases[index] == 1 and phase_1 is None:
                phase_1 = index - 0.5
            if self._subject._phases[index] == 2 and phase_2 is None:
                phase_2 = index - 0.5
            if self._subject._phases[index] == 3 and phase_3 is None:
                phase_3 = index - 0.5
            if self._subject._phases[index] == 4 and phase_4 is None:
                phase_4 = index - 0.5

        return [phase_1, phase_2, phase_3, phase_4]

    def make_plot(self):
        """Generate and Save a Behavior Performance Plot"""
        self._log.info("Creating Plot for Mouse {}".format(self._subject._mouse))
        # Obtain Data Labels # TODO: Syntax for try/except
        try: oc_label = "OvAll Corr: {}%".format(round(self._subject._overall_correct[len(self._subject._overall_correct) - 1], 4))
        except TypeError as e: oc_label = ""

        try: nl_label = "No Lick: {}%".format(round(self._subject._no_lick[len(self._subject._no_lick) - 1], 4))
        except TypeError as e: nl_label = ""

        try: pm_label = "+/- Bias: {}%".format(round(self._subject._plus_minus_bias[len(self._subject._plus_minus_bias) - 1], 4))
        except TypeError as e: pm_label = ""

        # Create figure - # NOTE: Bias is Plotted on Axis 2
        fig, ax1 = plt.subplots(figsize=(8,5))
        ax2 = ax1.twinx()
        x_count = range(0, len(self._subject._phases))
        ovCorr_line = ax1.plot(x_count, self._subject._overall_correct, color="g", label=oc_label, lw=1.75, marker="o")
        noLick_line = ax1.plot(x_count, self._subject._no_lick, color="r", label=nl_label, lw=1.75, marker="o")
        pmBias_line = ax2.plot(x_count, self._subject._plus_minus_bias, color="b", label=pm_label, lw=1.75, marker="o")
        center_format_space = "                             "
        ax1.set_xlabel("Day")
        ax1.set_ylabel(center_format_space + "Performance")
        ax2.set_ylabel("Bias" + center_format_space, color="b")
        lines = ovCorr_line + noLick_line + pmBias_line

        plt.xticks(x_count, fontsize='small', rotation='-22.5')

        # Color Phase Regions on Plot
        phase_indicies = self.phase_changes()
        ax1.axvspan(0, phase_indicies[0], facecolor='#feffba', alpha=1)               # PHASE 0
        ax1.axvspan(phase_indicies[0], len(x_count), facecolor='#9effc0', alpha=0.5)  # PHASE 1
        ax1.axvspan(phase_indicies[1], len(x_count), facecolor='#a1dcff', alpha=0.5)  # PHASE 2
        ax1.axvspan(phase_indicies[2], len(x_count), facecolor='#ca9eff', alpha=0.25) # PHASE 3
        ax1.axvspan(phase_indicies[3], len(x_count), facecolor='#ffe0e0', alpha=1)    # PHASE 4
        ax2.hlines(0, 0, len(x_count), linestyles="solid", colors="#000000", lw=1)    # 0 line

        # Add Legend, Title, Most Recent Values, & SAVE Plot
        ax1.grid(axis="x")
        ax1.autoscale(axis="both", tight=True)
        ax2.set_yticks(np.arange(-50, 101, step=10))
        ax2.use_sticky_edges=True
        ax1.set_yticks(np.arange(-50, 101, step=10))

        # Set Tick Colors for Bias Axis
        count = 0
        for ticklabel in ax2.get_yticklabels():
            if (count > 10):
                ticklabel.set_color('#FFFFFF')
            else:
                ticklabel.set_color('b')
            count +=1

        # Set Tick Colors for Performance Axis
        count = 0
        for ticklabel in ax1.get_yticklabels():
            if (count >= 5):
                continue # Change tickcolor in future here
            else:
                ticklabel.set_color('#FFFFFF')
            count += 1

        plt_title = "Cage {} Mouse {} - {} - Phase {} - {} Bias".format(
                        self._subject._cage,
                        self._subject._mouse,
                        self._subject._feature,
                        self._subject._phases[len(self._subject._phases) - 1],
                        self._subject._bias_side)
        ax1.legend(lines, [line.get_label() for line in lines],
                   title=plt_title, title_fontsize="large", fontsize="medium",
                   loc="upper center", bbox_to_anchor=(0.5, 1.15),
                   ncol=3, fancybox=True, frameon=False)

        plt.savefig("plots/m{}.png".format(self._subject._mouse))
