import os
import sys
import json
from MattLAB import MattLOG, MattSQL, MattMATH, MattMAIL

def main():
    # Create Logging Object
    tree = MattLOG.MattLOG()
    log = tree.create_log("MouseBehavior")

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
                stuart_little = MattMATH.MattMOUSE(log, data_table, start_date, cage_num, mouse, feature, end_date=death_date)
            else:
                stuart_little = MattMATH.MattMOUSE(log, data_table, start_date, cage_num, mouse, feature)
            stuart_little.collect_plot_datapoints()

            # Generate Plot
            mickey_mouse = MattMATH.MattPLOT(log, stuart_little)
            mickey_mouse.make_plot()

    # Create Email
    snail_mail = MattMAIL.MattMAIL(log)
    # TODO: try using the -- ting
    try:
        mode = sys.argv[1]
    except IndexError as e:
        mode = "developer_mode"
    snail_mail.snail_mail(mode)

if __name__=="__main__":
    main()
