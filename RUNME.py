import os
import sys
import json
import datetime
from MattLAB import MattLOG, MattSQL, MattMATH, MattMAIL

def main():
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

    # Assert if debug mode or team mode
    # debug -> enums: None or any string except "team"
    # team -> email is sent to entire team, rather than current developer
    try:
        mode = sys.argv[1]
        log.info("Running as {}".foramt(mode))
    except IndexError as e:
        mode = "developer_mode"
        log.info("Running as Developer")

    # Obtain All Quarterly Data
    with open("experiment_details.json", "r") as f:
            experiement = json.load(f)

    # Obtain All Quarterly Data
    data_sql = MattSQL.MattSQL(log, experiement["Term Start Date"])
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
            if death_date:
                #stuart_little = MattMATH.MattMOUSE(log, data_table, start_date, cage_num, mouse, feature, end_date=death_date)
            	log.info("Skipping mouse {} since it is DEAD".format(mouse))
            else:
                stuart_little = MattMATH.MattMATH(log, data_table, start_date, cage_num, mouse, feature)
            stuart_little.collect_plot_datapoints()

            # Generate Plot
            mickey_mouse = MattMATH.MattPLOT(log, stuart_little)
            mickey_mouse.make_plot()

    # Create Email
    snail_mail = MattMAIL.MattMAIL(log)
    snail_mail.snail_mail(mode)
    mickey_mouse.remove_plots()
    # Remove tmp log
    tree.remove_emailed_log(log)

if __name__=="__main__":
    main()
