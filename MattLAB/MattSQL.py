"""
ABOUT: Library to access, obtain, and produce datapoints from Team Database
AUTHOR: djbhatia@ucsd.edu

Jan. 2020
"""
# System Python
import os
import sys
import json
import logging
from datetime import datetime

# MySQL Python
import mysql.connector

# TODO: Allow User to fetch data for one mouse

class MattSQL:
    def __init__(self, log, start_date, end_date):
        """Initialize Data Values to use in SQL Querry(ies)"""
        self._log = log
        self._start_date = start_date
        self._end_date = end_date
        try:
            with open("cred_config.json", 'r') as f:
                self._creds = json.load(f)
            self._log.debug("Database credentials file found & loaded")
        except FileNotFoundError as e:
            self._log.critical("Database credentials FILE NOT FOUND")
            sys.exit("Terminating Program...")

    def format_querry():
        """Build querry w/input parameters to obtain table output, shown in README"""
        _selections = ("temporal_trails.timestamp, "
                       "temporal_trails.Session_ID, "
                       "temporal_trails.Song, "
                       "temporal_trails.Difficulty, "
                       "temporal_trails.Correctness, "
                       "temporal_trails.LickResult, "
                       "temporal_trails.AssistDrop, "
                       "temporal_session.id, "
                       "temporal_session.Animal_ID, "
                       "temporal_session.Training")
        _join = ("temporal_session INNER JOIN temporal_trails ON temporal_session.id=temporal_trails.Session_ID")
        _time = "temporal_trails.timestamp between '{} 00:00:00' AND '{} 23:59:59'".format(self.start_date, self.end_date)
        _sort = "ORDER BY temporal_session.id ASC"
        _querry = "SELECT {} FROM {} WHERE ({}) {}".format(selections, _join, _time, _sort)
        self._log.debug("Querry Ready for Start Date: {} & End Date: {}".format(self.start_date, self.end_date))
        self._log.debug('Querry: {}'.format(_querry))
        return _querry

    def execute_querry(self, querry):
        """Execute SQL Querry"""
        db_access = mysql.connector.connect(user=self._creds['user'],
                                            password=self._creds['password'],
                                            host=self._creds['ip_address'],
                                            database=self._creds['name'])
        dbcursor = db_access.cursor()
        dbcursor.execute(querry)
        self._log.debug('Querry executed. Now returning output table')
        _table = dbcursor.fetchall()
        dbcursor.close()
        db_access.close()
        return _table

    
