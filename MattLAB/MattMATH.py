# System Python
import sys
import logging
import datetime

class MattMouse:
    def __init__(self, log, data, start_date, cage_num, mouse_num, end_date=False):
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
            self._phases.append(self.identify_phase(table))
            self._no_lick.append(self.identify_no_lick(table, date))
            self._overall_correct.append(self.identify_overall_corrert(table, date))
            self._absolute_bias.append(self.identify_absolute_bias(table, date))
            break

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

    def identify_phase(self, table):
        """Return the phase with data from a single date"""
        return int(table[0][9])

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
            return round((no_licks / attempts) * 100, 4)
        except Exception as e:
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
            return round((correct / (correct + incorrect)) * 100, 4)
        except Exception as e:
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
                    if (row[3] == 0 and row[4] == 0 and row[5] != 0):
                        right += 1
                    # Count Number of Left Side Licks
                    if (row[3] != 0 and row[4] == 0 and row[5] != 0):
                        left += 1
        else:
            for row in table:
                if (row[6] != 0):
                    # Count Number of Template and Non-Template Songs
                    if (row[3] == 0):
                        template += 1
                    else:
                        non_template += 1
                    # Count Number of Right Side Licks
                    if (row[3] == 0 and row[4] == 0 and row[5] != 0):
                        right += 1
                    # Count Number of Left Side Licks
                    if (row[3] != 0 and row[4] == 0 and row[5] != 0):
                        left += 1

        percent_right = right / template
        percent_left = left / non_template
        try:
            # Identify Bias
            bias = round((percent_right / (percent_right + percent_left)) * 100, 4)
            # Identify Absolute Bias
            absolute_bias = round(abs(bias - 50), 4)
        except ZeroDivisionError as e:
            self._log.warning("Mouse {} on {} had INVALID Bias...".format(self._mouse, date))
            absolute_bias = None

        return absolute_bias

class MattPLOT:
    def __init__(self, data_tuple):
        
