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
        self._plus_minus_bias = []
        self._overall_correct = []

    def collect_plot_datapoints(self):
        """Loop through dates and append datapoints to proper list"""
        self.identify_dates()
        for date in self._dates:
            self._log.info("Evaluating Mouse {} on {}...".format(self._mouse, date))
            table = self.construct_singular_date_table(date)
            self._phases.append(self.identify_phase(table, date))
            self._no_lick.append(self.identify_no_lick(table, date))
            self._overall_correct.append(self.identify_overall_corrert(table, date))
            plus_minus_bias, absolute_bias = self.identify_absolute_bias(table, date)
            self._plus_minus_bias.append(plus_minus_bias)
            self._absolute_bias.append(absolute_bias)

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
            percent_right = round((right / template) * 100, 2)
            percent_left = round((left / non_template) * 100, 2)
            # percent_right = round(percent_right * 100, 2)
            # percent_left = round(percent_left * 100, 2)
            # bias = (round(percent_right * 100, 2) / (round(percent_right * 100, 2) + round(percent_left * 100, 2)))
            bias = round((percent_right / (percent_right + percent_left)) * 100, 2)

            # Format Rounding
            # percent_right = round(percent_right * 100, 2)
            # percent_left = round(percent_left * 100, 2)
            # bias = round(bias * 100, 2)

            # Identify Absolute Bias
            plus_minus_bias = round(bias - 50, 4)
            absolute_bias = abs(plus_minus_bias)

            if (bias - 50) > 0:
                self._bias_side = "RIGHT"
            elif (bias - 50) < 0:
                self._bias_side = "LEFT"
            else:
                self._bias_side = "NONE"

            # Log Stats
            self._log.info("Mouse {} on {} had {} Template Songs".format(self._mouse, date, template))
            self._log.info("Mouse {} on {} had {} Non Template Songs".format(self._mouse, date, non_template))
            self._log.info("Mouse {} on {} had Right Bias of {}".format(self._mouse, date, percent_right))
            self._log.info("Mouse {} on {} had Left Bias of {}".format(self._mouse, date, percent_left))
            self._log.info("Mouse {} on {} had Bias of {}".format(self._mouse, date, bias))
            self._log.info("Mouse {} on {} had +/- Bias of {}".format(self._mouse, date, plus_minus_bias))
            self._log.info("Mouse {} on {} had ABS Bias of {}".format(self._mouse, date, absolute_bias))

        except ZeroDivisionError as e:
            self._log.warning("Mouse {} on {} had INVALID Bias!".format(self._mouse, date))
            plus_minus_bias, absolute_bias = None, None

        return plus_minus_bias, absolute_bias
