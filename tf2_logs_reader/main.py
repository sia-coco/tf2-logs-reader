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
from typing import Tuple, List, Optional
from enum import Enum

import typer # https://typer.tiangolo.com/
app = typer.Typer()


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

class ClearOptionEnum(str, Enum):
    none = "none"
    players = "players"
    All = "all"

class ClassesEnum(str, Enum):
    scout = "scout"
    soldier = "soldier"
    pyro = "pyro"
    demoman = "demoman"
    heavyweapons = "heavyweapons"
    engineer = "engineer"
    medic = "medic"
    sniper = "sniper"
    spy = "spy"
    unknown = "unknown"
    undefined = "undefined"

class RecapSortByEnum(str, Enum):
    dpm = "dpm"
    kd = "kd"
    kPerHH = "kPerHH"



####################################################
##################| FUNCTIONS |#####################
####################################################


@app.command()
def retriever():
    """ Logs retriever tool.

    INPUTS: 

    OUTPUT:
    """ 
    typer.echo("|  >  Logs Retriever CLI")


@app.command()
def tocsv():
    """ Logs to csv converter tool.

    INPUTS: 

    OUTPUT:
    """ 
    pass


@app.command()
def clearjsondb(mode: ClearOptionEnum):
    """ Clears workspace's json database.

    INPUTS: 
    OUTPUT:
    """ 

    if mode != ClearOptionEnum.none.value:

        typer.secho(f"Clearing logs JSON database.", fg=typer.colors.CYAN, bold=True)
    
        if mode == ClearOptionEnum.All.value and typer.confirm("Confirm you want to clear all data ?", abort=True):
            jsonDB.clearDatabase(True, True)

        elif mode == ClearOptionEnum.players.value and typer.confirm("Confirm you want to clear players data ?", abort=True):
            jsonDB.clearDatabase(False, True)

        typer.secho(f"Done.", fg=typer.colors.CYAN, bold=True)

@app.command()
def parselogs():
    """ Parses logs in the json database.

    INPUTS: 
    OUTPUT:
    """ 

    typer.secho(f"Parsing logs ...", fg=typer.colors.CYAN, bold=True)
    
    jsonDB.parseAllLogs()

    typer.secho(f"Done.", fg=typer.colors.CYAN, bold=True)

@app.command()
def recap(classes: List[ClassesEnum],
          mintime: int,
          sortby: List[RecapSortByEnum] = typer.Option(default=[RecapSortByEnum.dpm.value], case_sensitive=True)
        ):
    """ Json logs database tool.

    INPUTS: 
            List of class names
            minimum playtime on a class for a player to be in the recap for that class
            list of sorting options
    """ 

    # Getting the players ids, corresponding to each player file saved in players DB
    players_id = [log.split(".")[0] for log in os.listdir(cfg.PLAYERS_DIR) if os.path.isfile(os.path.join(cfg.PLAYERS_DIR, log))]

    # Convert class options into str
    classes_for_analysis = [class_option.value for class_option in classes]

    # Convert sort options into str
    sort_keys = [key.value for key in sortby]

    # API recap functions
    players_interresting_stats = jsonDB.quickRecap(players_id, classes_for_analysis)
    jsonDB.recapDisplay(players_interresting_stats, sort_keys, mintime)

@app.command()
def profile(player_id: str,
            classes: List[ClassesEnum],
            detail_weps: bool = typer.Option(False)
            ):
    """  Prints a small recap of a player's stats.

    INPUTS: 
            player id
            list of classes
            option, True to detail weapon stats, False otherwise
            
    """ 

    # Convert class options into str
    classes = [class_option.value for class_option in classes]

    profile = jsonDB.profilePlayerClasses(player_id, classes, detail_weps)

    for key in profile:
        typer.secho(key, fg="cyan", bold=True)
        for k in profile[key]:
            print(k, profile[key][k])
        print()

@app.command()
def recapMaps():
    """  TODO

    INPUTS: 
    OUTPUT:
    """ 
    pass


##################################################
##################| PROGRAM |#####################
##################################################

if __name__ == "__main__" :

    app()



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
    #     print(f'{"map":30} {"played":8} {"won":8} {"tie":8} {"lost":8} {"winrate":10}')
    #     print()

    #     p_d = scrim_results[player_id]

    #     for m in p_d:
            
    #         print(f'{m:25} {p_d[m]["played"]:8} {p_d[m]["won"]:8} {p_d[m]["tie"]:8} {p_d[m]["lost"]:8} {int(round((p_d[m]["won"]+p_d[m]["tie"])/p_d[m]["played"]*100, 0)):10} %')

    #     print()
