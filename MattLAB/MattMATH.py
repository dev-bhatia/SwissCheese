"""
ABOUT: Contains all analytics and plotting libraries (MattMOUSE, MattPLOT)
AUTHOR: djbhatia@ucsd.edu

Jan. 2020
"""
# System Python
import os
import sys
import csv
import pylab
import logging
import datetime
import numpy as np
import matplotlib.pyplot as plt
from itertools import zip_longest

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
        """
        Loop through dates and append datapoints to proper list
        Also, write datapoints to csv file
        """
        self.identify_dates()
        # Gather Datapoints into Lists
        day = []
        attempts = []
        no_licks = []
        corrects = []
        incorrects = []
        templates = []
        non_templates = []
        right_bias = []
        left_bias = []
        right_incorrect = []
        left_incorrect = []
        bias = []
        count = 0
        for date in self._dates:
            day.append(count)
            self._log.info("Evaluating Mouse {} on {}...".format(self._mouse, date))
            table = self.construct_singular_date_table(date)
            self._phases.append(self.identify_phase(table, date))

            # Get % No Lick, # Attempts, # No Licks
            no_lick_percent, attempt, no_licks_num = self.identify_no_lick(table, date)
            self._no_lick.append(no_lick_percent)
            attempts.append(attempt)
            no_licks.append(no_licks_num)

            # Get % Overall Correct, Correct Licks, Incorrect Licks
            overall_correct, correct, incorrect = self.identify_overall_corrert(table, date)
            self._overall_correct.append(overall_correct)
            corrects.append(correct)
            incorrects.append(incorrect)

            # Get Songs (T, NT), Percents (R, RI, L, LI), Biases (B, +/-B, ABS-B)
            songs, percents, biases = self.identify_absolute_bias(table, date)
            templates.append(songs[0])
            non_templates.append(songs[1])

            right_bias.append(percents[0])
            right_incorrect.append(percents[1])
            left_bias.append(percents[2])
            left_incorrect.append(percents[3])

            bias.append(biases[0])
            self._plus_minus_bias.append(biases[1])
            self._absolute_bias.append(biases[2])
            count += 1

        # Write list in to CSV file for mouse
        # data = [self._dates, day, self._phases, self._no_lick, self._plus_minus_bias, self._absolute_bias, self._overall_correct, ]
        data = [self._dates, day, self._phases, attempts, no_licks, self._no_lick, corrects, incorrects, self._overall_correct,
                templates, non_templates, right_bias, right_incorrect, left_bias, left_incorrect, bias, self._plus_minus_bias, self._absolute_bias]

        export_data = zip_longest(*data, fillvalue = '')
        filename = "sheets/C{}_M{}.csv".format(self._cage, self._mouse)
        with open(filename, 'w', encoding="ISO-8859-1", newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(("Date", "Day", "Phase", "Total Attempts", "No Licks", "% No Lick", "Correct Licks", "Incorrect Licks", "% Overall Corr",
                         "Template Songs", "Non-Template Songs", "Right Bias", "Right Incorrect", "Left Bias", "Left Incorrect", "Bias", "+/- Bias", "ABS Bias"))
            wr.writerows(export_data)
        myfile.close()

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
            return (no_lick, attempts, no_licks)
        except Exception as e:
            self._log.warning("Mouse {} on {} had INVALID No Lick!".format(self._mouse, date))
            return (None, None, None)

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
            return (overall_correct, correct, incorrect)
        except Exception as e:
            self._log.warning("Mouse {} on {} had INVALID Overall Correct!".format(self._mouse, date))
            return (None, None, None)

    def identify_absolute_bias(self, table, date):
        """Identify the % Absolute Bias with data from a single date"""
        # Count Number of Template and Non-Template Songs
        template, non_template = 0, 0
        right, left = 0, 0
        right_incorrect, left_incorrect = 0, 0
        if (date == self._start_date):
            for row in table:
                if (row[6] != 0):
                    # Count Number of Template and Non-Template Songs
                    if (row[3] == 0):
                        template += 1
                        # Count Number of Right Side Licks
                        if (row[4] == 0 and row[5] == 1):
                            right += 1
                        if (row[4] != 0 and row[5] == -1):
                            right_incorrect += 1
                    else:
                        non_template += 1
                        # Count Number of Left Side Licks
                        if (row[4] == 0 and row[5] == -1):
                            left += 1
                        if (row[4] != 0 and row[5] == 1):
                            left_incorrect += 1
        else:
            for row in table:
                if (row[6] == 0):
                    # Count Number of Template and Non-Template Songs
                    if (row[3] == 0):
                        template += 1
                        # Count Number of Right Side Licks
                        if (row[4] == 0 and row[5] == 1):
                            right += 1
                        if (row[4] != 0 and row[5] == -1):
                            right_incorrect += 1
                    else:
                        non_template += 1
                        # Count Number of Left Side Licks
                        if (row[4] == 0 and row[5] == -1):
                            left += 1
                        if (row[4] != 0 and row[5] == 1):
                            left_incorrect += 1
        try:
            # NOTE: Are my trials over or under the recoreded amount in the journal
            # NOTE: Correlation between diff. types of errors on certain days

            # Correlations between lick times and correctness
                # Licking during songs better than licking at end of song
                # What's correlating for a mouse to become an expert mouse!
                # Start with expert mice and see what they have in common? (Take all expert mice)
                # HYPOTHESIS:
                    # 5 expert mice, (CCC) & (next song) [Get to P4 = Expert], maybe 5 mice to P4 on 3 songs (super expert)
                    # 5 mice train for same amt of days on avg, but did not reach P4 on 2nd song
                # Make sure mice did not have headbar problems
                # 1. Expert Mice have low No-Lick % during P1, P2.
                # 2. Expert Mice learn to lick after the song is over, rather than during song (Listen to whole song)
                # 3. Expert Mice not only lick after, but % Baseline Weight hovers at intermediate weight (~85-90%)
                # 4. Expert Mice, before becomeing experts have bias go to 0.

            # Identify Bias
            percent_right = round((right / template) * 100, 2)
            percent_left = round((left / non_template) * 100, 2)
            percent_right_incorrect = round((right_incorrect / template) * 100, 2)
            percent_left_incorrect = round((left_incorrect / template) * 100, 2)

            # NOTE: Right Bias = Percent Correct on Right Side
            # 1. % Incorrect Right -> Left Lick during template song
            # 2. % Incorrect Left -> Right Lick during non-template song

            # bias = (round(percent_right * 100, 2) / (round(percent_right * 100, 2) + round(percent_left * 100, 2)))
            bias = round((percent_right / (percent_right + percent_left)) * 100, 2)

            # Identify +/- and ABS Bias
            plus_minus_bias = round(bias - 50, 4)
            absolute_bias = abs(plus_minus_bias)

            if (bias - 50) > 0:
                self._bias_side = "RIGHT"
            elif (bias - 50) < 0:
                self._bias_side = "LEFT"
            else:
                self._bias_side = "NONE"

            # Log Song Stats
            self._log.info("Mouse {} on {} had {} Template Songs".format(self._mouse, date, template))
            self._log.info("Mouse {} on {} had {} Non Template Songs".format(self._mouse, date, non_template))
            # Log Lick Side Stats
            self._log.info("Mouse {} on {} had Right Bias of {}".format(self._mouse, date, percent_right))
            self._log.info("Mouse {} on {} had Right Incorrect of {}".format(self._mouse, date, percent_right_incorrect))
            self._log.info("Mouse {} on {} had Left Bias of {}".format(self._mouse, date, percent_left))
            self._log.info("Mouse {} on {} had Left Incorrect of {}".format(self._mouse, date, percent_left_incorrect))
            # Log Bias Stats
            self._log.info("Mouse {} on {} had Bias of {}".format(self._mouse, date, bias))
            self._log.info("Mouse {} on {} had +/- Bias of {}".format(self._mouse, date, plus_minus_bias))
            self._log.info("Mouse {} on {} had ABS Bias of {}".format(self._mouse, date, absolute_bias))

            songs = (template, non_template)
            percents = (percent_right, percent_right_incorrect, percent_left, percent_left_incorrect)
            biases = (bias, plus_minus_bias, absolute_bias)

        except ZeroDivisionError as e:
            self._log.warning("Mouse {} on {} had INVALID Bias!".format(self._mouse, date))
            songs = (None, None)
            percents = (None, None, None, None)
            biases = (None, None, None)

        return (songs, percents, biases)
