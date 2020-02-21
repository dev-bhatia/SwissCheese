"""
ABOUT: Contains all analytics and plotting libraries (MattMOUSE, MattPLOT)
AUTHOR: djbhatia@ucsd.edu

Jan. 2020
"""
# System Python
import os
import sys
import pylab
import logging
import datetime
import numpy as np
import matplotlib.pyplot as plt

class MattMATH:
    def __init__(self, log, data, start_date, cage_num, mouse_num, feature, end_date=False):
        """Library for Gathering Datapoints for one given mouse"""
        self._log = log
        self._data = data
        self._start_date = start_date
        if end_date:
            self._end_date = end_date
        else:
            self._end_date = str(datetime.datetime.now())[:10]
        self._cage = cage_num
        self._mouse = mouse_num
        self._feature = feature
        self._log.info("Mouse Object Initialized for Mouse {}".format(self._mouse))
        self._log.debug("Looping through dates {} to {}".format(self._start_date, self._end_date))

        # Plot Variables
        self._phases = []
        self._no_lick = []
        self._absolute_bias = []
        self._overall_correct = []

    def collect_plot_datapoints(self):
        self.identify_dates()
        for date in self._dates:
            self._log.info("Evaluating Mouse {} on {}...".format(self._mouse, date))
            table = self.construct_singular_date_table(date)
            self._phases.append(self.identify_phase(table, date))
            self._no_lick.append(self.identify_no_lick(table, date))
            self._overall_correct.append(self.identify_overall_corrert(table, date))
            self._absolute_bias.append(self.identify_absolute_bias(table, date))

    def datetime_range(self, start=None, end=None):
        span = end - start
        for i in range(span.days + 1):
            yield start + datetime.timedelta(days=i)

    def identify_dates(self):
        """identify a list of dates to loop over based on start and end dates"""
        self._dates = []
        start_date = datetime.datetime(int(self._start_date[:4]), int(self._start_date[5:7]), int(self._start_date[8:]))
        end_date = datetime.datetime(int(self._end_date[:4]), int(self._end_date[5:7]), int(self._end_date[8:]))
        for date in self.datetime_range(start=start_date, end=end_date):
            if ((date.weekday() != 5) and (date.weekday() != 6)):
                date_str = str(date)[:10]
                self._dates.append(date_str)

    def construct_singular_date_table(self, date):
        """Return a table for a mouse on a specific date"""
        singular_date_table = []
        for row in self._data:
            if (str(row[0])[:10] == date):
                if (str(row[8])[5:] == "{}{}".format(self._cage, self._mouse)):
                    singular_date_table.append(row)
        return singular_date_table

    def identify_phase(self, table, date):
        """Return the phase with data from a single date"""
        try:
            phase = int(table[0][9])
            self._log.info("Mouse {} on {} was on Phase {}".format(self._mouse, date, phase))
            return phase
        except Exception as e:
            self._log.warning("Mouse {} on {} has NO PHASE".format(self._mouse, date))
            return None

    def identify_no_lick(self, table, date):
        """Return the % No Licks with data from a single date"""
        no_licks, attempts = 0, 0
        if (date == self._start_date):
            # We Know we are on Day 0
            for row in table:
                if (row[6] != 0):
                    attempts += 1
                    if (row[5] == 0):
                        no_licks += 1
        else:
            for row in table:
                if (row[6] == 0):
                    attempts += 1
                    if (row[5] == 0):
                        no_licks += 1
        try:
            no_lick = round((no_licks / attempts) * 100, 4)
            self._log.info("Mouse {} on {} had {} Attempts, {} were No Licks".format(self._mouse, date, attempts, no_licks))
            self._log.info("Mouse {} on {} had No Lick of {}".format(self._mouse, date, no_lick))
            return no_lick
        except Exception as e:
            self._log.warning("Mouse {} on {} had INVALID No Lick!".format(self._mouse, date))
            return None

    def identify_overall_corrert(self, table, date):
        """Identify the % Overall Correct with data from a single date"""
        correct, incorrect = 0, 0
        if (date == self._start_date):
            for row in table:
                if (row[6] != 0):
                    if (row[5] != 0 and row[4] == 0):
                        correct += 1
                    if (row[5] != 0 and row[4] == 1):
                        incorrect += 1
        else:
            for row in table:
                if (row[6] == 0):
                    if (row[5] != 0 and row[4] == 0):
                        correct += 1
                    if (row[5] != 0 and row[4] == 1):
                        incorrect += 1
        try:
            overall_correct = round((correct / (correct + incorrect)) * 100, 4)
            self._log.info("Mouse {} on {} had {} Correct Licks".format(self._mouse, date, correct))
            self._log.info("Mouse {} on {} had {} Inorrect Licks".format(self._mouse, date, incorrect))
            self._log.info("Mouse {} on {} had Overall Correct of {}".format(self._mouse, date, overall_correct))
            return overall_correct
        except Exception as e:
            self._log.warning("Mouse {} on {} had INVALID Overall Correct!".format(self._mouse, date))
            return None

    def identify_absolute_bias(self, table, date):
        """Identify the % Absolute Bias with data from a single date"""
        # Count Number of Template and Non-Template Songs
        template, non_template = 0, 0
        right, left = 0, 0
        if (date == self._start_date):
            for row in table:
                if (row[6] != 0):
                    # Count Number of Template and Non-Template Songs
                    if (row[3] == 0):
                        template += 1
                    else:
                        non_template += 1
                    # Count Number of Right Side Licks
                    if (row[3] == 0 and row[4] == 0 and row[5] == 1):
                        right += 1
                    # Count Number of Left Side Licks
                    if (row[3] != 0 and row[4] == 0 and row[5] == -1):
                        left += 1
        else:
            for row in table:
                if (row[6] == 0):
                    # Count Number of Template and Non-Template Songs
                    if (row[3] == 0):
                        template += 1
                    else:
                        non_template += 1
                    # Count Number of Right Side Licks
                    if (row[3] == 0 and row[4] == 0 and row[5] == 1):
                        right += 1
                    # Count Number of Left Side Licks
                    if (row[3] > 0 and row[4] == 0 and row[5] == -1):
                        left += 1
        try:
            # Identify Bias
            percent_right = right / template
            percent_left = left / non_template
            bias = round((percent_right / (percent_right + percent_left)) * 100, 4)
            # Identify Absolute Bias
            absolute_bias = round(abs(bias - 50), 4)
            self._log.info("Mouse {} on {} had {} Template Songs".format(self._mouse, date, template))
            self._log.info("Mouse {} on {} had {} Non Template Songs".format(self._mouse, date, non_template))
            self._log.info("Mouse {} on {} had Right Bias of {}".format(self._mouse, date, round(percent_right * 100, 4)))
            self._log.info("Mouse {} on {} had Left Bias of {}".format(self._mouse, date, round(percent_left * 100, 4)))
            self._log.info("Mouse {} on {} had Bias of {}".format(self._mouse, date, bias))
            self._log.info("Mouse {} on {} had ABS Bias of {}".format(self._mouse, date, absolute_bias))
        except ZeroDivisionError as e:
            self._log.warning("Mouse {} on {} had INVALID Bias!".format(self._mouse, date))
            absolute_bias = None

        return absolute_bias

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
            # if (phase != None):
            #     days.append(phase)
            # else:
            #     days.append(None)
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

        # Plot Data
        try:
            oc_label = "OvAll Corr: {}%".format(round(self._subject._overall_correct[len(self._subject._overall_correct) - 1], 2))
        except TypeError as e:
            oc_label = ""
        try:
            nl_label = "No Lick: {}%".format(round(self._subject._no_lick[len(self._subject._no_lick) - 1], 2))
        except TypeError as e:
            nl_label = ""
        try:
            ab_label = "ABS Bias: {}%".format(round(self._subject._absolute_bias[len(self._subject._absolute_bias) - 1], 2))
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
        plt_title = "Cage {} Mouse {} - {} - Phase {} - Bias".format(
                        self._subject._cage, self._subject._mouse,
                        self._subject._feature,
                        self._subject._phases[len(self._subject._phases) - 1])
        plt.legend(title=plt_title, title_fontsize="large", fontsize="medium",
                   loc="upper center", bbox_to_anchor=(0.5, 1.15),
                   ncol=3, fancybox=True)
        plt.xlabel('Day')
        plt.ylabel('Performance')
        plt.savefig("plots/m{}.png".format(self._subject._mouse))

    def remove_plots(self):
        """Remove All Plots saved in Plots dir"""
        self._log.info("Deleting plots...")
        os.system("rm -rf plots/*")
        self._log.info("Done deleting plots...")
