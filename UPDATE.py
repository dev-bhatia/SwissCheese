"""
A quick script executed before RUNME.py on our automation host to ensure
    we are running the most up-to-date stable build.
"""
import os
import sys

def execute_command(cmd):
    try:
        print("Attempting to run: {}".format(cmd))
        os.system(cmd)
        print("Completed running: {}".format(cmd))
    except Exception as e:
        print("Encountered Error Running: {}".format(cmd))
        print("Exception: {}".format(e))
        sys.exit(1)

# Update branch to latest version
execute_command("git fetch")
execute_command("git reset --hard origin/master")

# The update worked!
