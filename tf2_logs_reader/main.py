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
import Player
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

    # print(jsonDB.profilePlayerClasses("[U:1:417187459]", ["soldier"]))

    # classes_for_analysis = ["demoman", "scout", "soldier"]
    classes_for_analysis = ["sniper"]

    # sort_keys = ["dpm", "kd", "kPerHH"]
    sort_keys = ["dpm"]

    players_interresting_stats = jsonDB.quickRecap(players_id, classes_for_analysis)
    jsonDB.recapDisplay(players_interresting_stats, sort_keys, 30)




    # profile = jsonDB.profilePlayerClasses("[U:1:114893365]", ["scout"], True)
    # for key in profile:
    #     for k in profile[key]:
    #         print(k, profile[key][k])






    # # "[U:1:69056566]": "Qc - Tammrock",
    # # "[U:1:417187459]": "> GUCCI - sia",
    
    # # Log files
    # log_files = [log for log in os.listdir(cfg.LOGS_DIR) if os.path.isfile(os.path.join(cfg.LOGS_DIR, log))]

    # # Result dict
    # scrim_results = {"[U:1:69056566]": {}, "[U:1:184671077]": {}}

    # for log_file in log_files:
    #     with open(os.path.join(cfg.LOGS_DIR, log_file)) as json_file:

    #         # Converting json data into python dict
    #         dict_data = json.load(json_file)


    #     for player_id in ["[U:1:69056566]", "[U:1:184671077]"]:

    #         if player_id in dict_data["players"]:
                
    #             team_colour = dict_data["players"][player_id]["team"]
    #             enemy_team="Red"
    #             if team_colour == "Red":
    #                 enemy_team="Blue"
    #             team_score, enemy_score = dict_data["teams"][team_colour]["score"], dict_data["teams"][enemy_team]["score"]
    #             # print(team_colour, team_score, enemy_team, enemy_score)
                
    #             map_played  = dict_data["info"]["map"]
                
    #             if not map_played in scrim_results[player_id]:
    #                 scrim_results[player_id][map_played]={label: 0 for label in ["played", "won", "tie", "lost"]}

    #             # Played
    #             scrim_results[player_id][map_played]["played"] += 1
    #             if team_score > enemy_score:
    #                 scrim_results[player_id][map_played]["won"] += 1
    #             elif team_score == enemy_score:
    #                 scrim_results[player_id][map_played]["tie"] += 1
    #             else:
    #                 scrim_results[player_id][map_played]["lost"] += 1
                    

    # for player_id in scrim_results:
    #     print(player_id)
    #     print(f'{"map":30} {"played":8} {"won":8} {"tie":8} {"lost":8}')
    #     print()

    #     p_d = scrim_results[player_id]

    #     for m in p_d:
            
    #         print(f'{m:25} {p_d[m]["played"]:8} {p_d[m]["won"]:8} {p_d[m]["tie"]:8} {p_d[m]["lost"]:8}')

    #     print()
