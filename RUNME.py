"""
This program runs on both UNIX & Windows Systems
    shell> python RUNME.py
"""

import os
import sys
import json
import datetime
import random
from MattLAB import MattLOG, MattSQL, MattMATH, MattMAIL, MattPLOT

class Mouse:
    def __init__(self):
        # Range 18
        self._phases = [0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4]
        self._overall_correct = []
        self._absolute_bias = []
        self._plus_minus_bias = []
        self._no_lick = []
        self._cage = 00
        self._mouse = 0
        self._feature = "Test"
        for i in range(len(self._phases)):
            self._overall_correct.append(random.uniform(0, 100))
            self._absolute_bias.append(random.uniform(0, 50))
            self._plus_minus_bias.append(random.uniform(-45, 45))
            self._no_lick.append(random.uniform(0, 100))
        self._bias_side = "No"
        if (self._plus_minus_bias[len(self._plus_minus_bias) - 1] < 0):
            self._bias_side = "LEFT"
        else:
            self._bias_side = "RIGHT"

def main():
    sys.stdout = open("today.log", "w")

    # Create logs and plots directories if they do not already exist
    if not os.path.exists("logs"):
        os.mkdir("logs")
    if not os.path.exists("plots"):
        os.mkdir("plots")

    # Remove all logs from logs dir if Monday (clean logs on weekly basis)
    if not (datetime.datetime.today().weekday()):
        os.system("rm logs/*")

    # Create Logging Object
    tree = MattLOG.MattLOG()
    log = tree.create_log("MouseBehavior")

    # Assert if debug mode or team mode (default: debug mode)
    #   debug -> enums: None or any string except "team"
    #   team -> email is sent to entire team, rather than current developer
    try:
        mode = sys.argv[1]
        log.info("Running as {}".format(mode))
    except IndexError as e:
        mode = "developer_mode"
        log.info("Running as Developer")

    # Obtain All Quarterly Data
    with open("experiment_details.json", "r") as f:
            experiement = json.load(f)

    # Obtain All Quarterly Data
    data_sql = MattSQL.MattSQL(log, start_date=experiement["Term Start Date"])
    data_table = data_sql.execute_querry(data_sql.format_querry())

    cage_nums = [key for key in experiement if "Term" not in key]
    for cage_num in cage_nums:
        log.info("On Cage {}".format(cage_num))
        cage = experiement[cage_num]
        mice = [key for key in cage if "Day" not in key]
        for mouse in mice:
            feature = cage[mouse][0]
            death_date = cage[mouse][1]
            try:
                start_date = cage[mouse][2]
            except Exception as e:
                start_date = cage["Day 0"]
            # Iterate thorugh data table and generate Mouse Objects
            if (death_date):
                if (experiement["Include Term Dead Mice"] == "Yes"):
                    stuart_little = MattMATH.MattMATH(log, data_table, start_date, cage_num, mouse, feature, end_date=death_date)
                else:
                    log.info("Skipping mouse {} since it PASSED on {}".format(mouse, death_date))
            else:
                stuart_little = MattMATH.MattMATH(log, data_table, start_date, cage_num, mouse, feature)
            stuart_little.collect_plot_datapoints()

    stuart_little = Mouse()
    # Generate Plot
            mickey_mouse = MattPLOT.MattPLOT(log, stuart_little)
            mickey_mouse.make_plot()

    # Create Email
    snail_mail = MattMAIL.MattMAIL(log)
    snail_mail.snail_mail(mode)
    mickey_mouse.remove_plots()

if __name__=="__main__":
    sys.exit("Lab shutdown") # Stopping all runs for COVID-19
    main()
