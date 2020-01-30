import os
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
            # Iterate thorugh data table and generate Mouse Objects
            if death_date:
                stuart_little = MattMATH.MattMOUSE(log, data_table, cage["Day 0"], cage_num, mouse, feature, end_date=death_date)
            else:
                stuart_little = MattMATH.MattMOUSE(log, data_table, cage["Day 0"], cage_num, mouse, feature)
            stuart_little.collect_plot_datapoints()

            # Generate Plot
            mickey_mouse = MattMATH.MattPLOT(log, stuart_little)
            mickey_mouse.make_plot()

    # Create Email
    snail_mail = MattMAIL.MattMAIL(log)
    snail_mail.snail_mail()

if __name__=="__main__":
    main()
