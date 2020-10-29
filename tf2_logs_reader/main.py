#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.6
# Author :  - https://github.com/sia-coco
########################

# IMPORTS
import sys
import os

import json
import sqlite3

# FILE IMPORTS
import config as cfg
from Player import *
from Match import *

import jsonDB

# Sub-modules


##########################################
############| TF2 LOG READER |############
##########################################

""" TO DO LIST ✔✘
"""

""" PROBLEMS
"""

""" NOTES
Logs.tf API documentation:
https://docs.google.com/document/d/1AMu7iY0VBXkfSu3Mua0zbEwhFf8uC2POKNhb3PydBg4/edit
"""

####################################################
###################| CLASSES |######################
####################################################


####################################################
##################| FUNCTIONS |#####################
####################################################






##################################################
##################| PROGRAM |#####################
##################################################

if __name__ == "__main__" :

    # jsonDB.clearDatabase(True, True)

    # # Gets data from all the logs in the logs folder
    jsonDB.saveAllLogs()

    players_id = [log.split(".")[0] for log in os.listdir(cfg.PLAYERS_DIR) if os.path.isfile(os.path.join(cfg.PLAYERS_DIR, log))]
    # print(players_id[0])

    # print(jsonDB.profilePlayerClasses(players_id[0], ["soldier"]))

    # classes_for_analysis = ["demoman", "scout", "soldier"]
    classes_for_analysis = ["demoman"]

    # sort_keys = ["dpm", "kd", "kPerHH"]
    sort_keys = ["dpm", "kd", "kPerHH"]

    players_interresting_stats = jsonDB.quickRecap(players_id, classes_for_analysis)
    jsonDB.recapDisplay(players_interresting_stats, sort_keys, 70)

