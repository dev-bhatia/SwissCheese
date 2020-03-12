"""
A quick script executed before RUNME.py on our automation host to ensure
we are running the most up-to-date stable build.
"""
import os
import sys

def execute_command(cmd):
    

# Update branch to latest version
try:
    cmd = "git fetch"
    print("Updating branch to latest version if necessary...")
    os.system(cmd)
    print("Completed Fetch. Attempting Reset...")
except Exception as e:
    print("Error in git fetch: {}".format(e))
    sys.exit(1)

try:
    print("Attempting Hard Reset")
    os.system("git reset --hard origin/master")
    print("Completed Reset. Program Updated")
except Exception as e:
    print("Error in git reset --hard origin/master: {}".format(e))
    sys.exit(1)
