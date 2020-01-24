import os
import json
from MattLAB import MattLOG, MattSQL, MattMATH

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
            death_date = cage[mouse][1]
            # Iterate thorugh data table and generate Mouse Objects
            if death_date:
                stuart_little = MattMATH.MattMouse(log, data_table, cage["Day 0"], cage_num, mouse, end_date=death_date)
            else:
                stuart_little = MattMATH.MattMouse(log, data_table, cage["Day 0"], cage_num, mouse)
            stuart_little.collect_plot_datapoints()
            print("Phases ", stuart_little._phases)
            print("% No Lick ", stuart_little._no_lick)
            print("% ABS Bias ", stuart_little._absolute_bias)
            print("% Overall Correct ", stuart_little._overall_correct)

            # Generate Plot
if __name__=="__main__":
    main()
