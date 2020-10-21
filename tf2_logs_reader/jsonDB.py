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

# FILE IMPORTS
import config as cfg
import Player
import Match

# Sub-modules


####################################################
############| LIBRARY ... |############
####################################################

""" TO DO LIST ✔✘
"""

""" PROBLEMS
"""

""" NOTES
"""

####################################################
###################| CLASSES |######################
####################################################


####################################################
##################| FUNCTIONS |#####################
####################################################

### JSON DATABASE ###

# CLEAR DATABASE
def clearDatabase(clear_logs=False, clear_players=True):
    """ Clears all previous data.
    """

    dirs_to_clear = []

    if clear_logs:
        dirs_to_clear.append(cfg.LOGS_DIR)
    if clear_players:
        dirs_to_clear.append(cfg.PLAYERS_DIR)


    for dir in dirs_to_clear:
        filelist = [ f for f in os.listdir(dir) if f.endswith(".json") ]
        for f in filelist:
            os.remove(os.path.join(dir, f))

    with open(cfg.MATCHES_FILE, "w") as file:
        file.write("{}")

    with open(cfg.MATCHES_RECORD, "w") as file:
        pass

# PROCESS LOGS FROM THE LOGS FOLDER TO DATABASE
def saveAllLogs(save_players=True, save_match=True):
    """ Gets all the logs from the logs folder and processes them.
    If they have already been processed they won't be processed again.
    Each processed log has its ID saved in the matches record file.

    INPUTS:
            option: if True, saves to player database
            option: if True, saves to the match database
    """
    # Getting all the files from the logs folder
    log_files = [log for log in os.listdir(cfg.LOGS_DIR) if os.path.isfile(os.path.join(cfg.LOGS_DIR, log))]

    # Opening the file that stores all processed logs id
    matches_record = open(cfg.MATCHES_RECORD, 'r+')
    matches_list = [match[:-1] for match in list(matches_record)] # [-1] to remove '\n'

    # Saving all of them
    for log_file in log_files:

        # Checking if it has been saved already
        if not log_file.split(".")[0] in matches_list:

            # Adding match to the saved match list
            matches_record.write(log_file.split(".")[0]+"\n")

            # Saving match
            saveLog(log_file, save_players, save_match)

        else:
            print(f"log file {log_file} already anaysed")

    matches_record.close()

def saveLog(log_file, save_players=True, save_match=True):
    """ Saves data from a an individual logs file in the database.
    If it has already been processed it won't be processed again.
    Else its ID saved in the matches record file.

    # top_keys  = ['version', 'teams', 'length', 'players', 'names', 'rounds', 'healspread', 'classkills', 'classdeaths', 'classkillassists', 'chat', 'info', 'killstreaks', 'success']
    # sub_dicts = ['teams', 'players', 'names', 'healspread', 'classkills', 'classdeaths', 'classkillassists', 'info']

    INPUTS:
            name of the logs file (str)
            option: if True, saves to player database
            option: if True, saves to the match database
    """

    with open(cfg.MATCHES_RECORD) as matches_record:
        matches_list = [match[:-1] for match in list(matches_record)] # [-1] to remove '\n'

    # Getting match id
    match_id = log_file.split('.')[0]

    # Checks that the log file hasn't been processed already
    if not match_id in matches_list:

        with open(os.path.join(cfg.LOGS_DIR, log_file)) as json_file:

            # Converting json data into python dict
            dict_data = json.load(json_file)

            # Saves the match data
            if save_match:
                saveToMatch(match_id, dict_data)

            # Saves the player data
            if save_players:
                saveToPlayer(match_id, dict_data)

            matches_record = open(cfg.MATCHES_RECORD, 'a')
            matches_record.write(log_file.split(".")[0]+"\n")
            matches_record.close()

    else:
        print(f"log file {log_file} already anaysed")

def saveToPlayer(match_id, log):
    """ Saves the corresponding match data into a player database.

    INPUTS:
            ID of the match (str)
            data from the log (dict)
    """

    # Dict with all player data
    players_data = log["players"]

    # List of all player ID's from the log data
    player_ids = list(players_data.keys())

    # List all existing players already registered in the database
    registered_players = [player.split(".")[0] for player in os.listdir(cfg.PLAYERS_DIR) if os.path.isfile(os.path.join(cfg.PLAYERS_DIR, player))]

    # For each player in the log data
    for player_id in player_ids:

        # Get the already existing data if there is some
        if player_id in registered_players:
            # Loads the existing player data file
            with open(os.path.join(cfg.PLAYERS_DIR, player_id + ".json")) as player_json:
                player = Player.Player.fromJSON(player_json)

        # Create a new player object if there is no pre-existing data for that player
        else:
            # Creates the player object for the first time
            player = Player.Player(player_id)

        # In the log, class kills and class deaths data are stored individually
        # and not in each player's data so we get it separately.
        if player_id in log["classkills"].keys():
            classkills = log["classkills"][player_id]
        else:
            classkills  = {}
        if player_id in log["classdeaths"].keys():
            classdeaths = log["classdeaths"][player_id]
        else:
            classdeaths = {}

        # Adds the math data to the player's data.
        if player.addMatch(match_id, players_data[player_id], classkills, classdeaths):
            # Writes data in the player file if the match is new to the player database.
            player.save(cfg.PLAYERS_DIR)
            print(f"match {match_id} added to player {player_id}")

def saveToMatch(match_id, log):
    """ Saves match data into the match record file.

    TODO: Check up and continue the match analysis part

    INPUTS:
            ID of the match (str)
            data from the log (dict)
    """

    with open(cfg.MATCHES_FILE) as matches_file:
        # Loads stored matches file as a dict
        matches_dict = json.load(matches_file)

    if match_id not in matches_dict.keys():
        # Creates a new match object
        match = Match.Match(match_id, log["length"], log["teams"], log["rounds"], log["healspread"])
        # Appends the match to the matches dict
        matches_dict[match_id] = match.__dict__

        # Converts back to json
        matches_json = json.dumps(matches_dict)

        # Writes in the file
        matches_file = open(cfg.MATCHES_FILE, 'w')
        matches_file.write(matches_json)
        matches_file.close()
        print(f"match {match_id} added to the match database")

    else:
        print(f"match {match_id} already exists in match database")

# DATA PRE-PROCESSING
def preprocessingPlayer(player):
    """ Pre-processes the players object.

    INPUTS:
            a player object (Player)
    """

    # Normalizes Matches from the player
    player.cleanAllMatches(cfg.TOREMOVE_IN_PLAYER_DICT)

    # Adds a name to the player if there is a corresponding one in the name database
    player.findName(cfg.PLAYER_NAMES)

    # Saves all data to the player file
    player.save(cfg.PLAYERS_DIR)

# DATA PROCESSING/EXTRACTING
def profilePlayerClasses(player_id, classe_names):
    """ #TODO

    INPUTS:
    OUTPUT:
    """

    class_fields = ["deaths", "assists", "total_time", "weapon"]
    weapon_fields = ["kills", "dmg"]

    # Reading from the player file to create the player object.
    with open(os.path.join(cfg.PLAYERS_DIR, player_id + ".json")) as player_json:
        player = Player.Player.fromJSON(player_json)

    # Getting class stats
    class_data = player.sumClassData(classe_names, class_fields)

    # Merging stats from class weapons
    for class_name in classe_names:
        weapon_merged_data = Player.Player.mergeWeaponData(class_data[class_name]["weapon"], weapon_fields)

        del class_data[class_name]["weapon"]
        for key in weapon_merged_data:
            class_data[class_name][key] = weapon_merged_data[key]

    return class_data


def quickRecap(players_id, classes):
    """ Quickly shows important data.

    INPUTS:
    OUTPUT:
    """
    
    players_interresting_stats = []
    
    for player_id in players_id:

        with open(os.path.join(cfg.PLAYERS_DIR, player_id) + ".json") as player_json:
            player = Player.Player.fromJSON(player_json)

        # Pre-processes the player object
        preprocessingPlayer(player)

        class_data = profilePlayerClasses(player_id, classes)
        for ligne in class_data:

            matches = class_data[ligne]["matches_played"]
            mins    = class_data[ligne]["total_time"]/60
            kills   = class_data[ligne]["kills"]
            dam     = class_data[ligne]["dmg"]
            deaths  = class_data[ligne]["deaths"]

            if matches != 0:
                kPerMatch = round(kills/matches, 2)
                kPerHH = round(kills/(mins/30), 2)
            else:
                kPerMatch = 0
                kPerHH = 0

            if deaths != 0:
                kd = round(kills/deaths, 2)
            else:
                kd = kills

            if mins != 0:
                dpm = round(dam/mins, 2)
            else:
                dpm = dam

            player_interresting_stats = {"id": player.steam_id, "name": player.name, "class": ligne, "dpm": dpm, "kd": kd, "mins": int(mins), "kPerHH": kPerHH}
            players_interresting_stats.append(player_interresting_stats)

    return players_interresting_stats

def recapDisplay(recap_stats, sort_keys):
    """ #TODO

    INPUTS:
    OUTPUT:
    """

    for sort_key in sort_keys:
        print()
        print(sort_key)
        players_interresting_stats = [p for p in recap_stats if p["mins"] != 0]
        players_interresting_stats.sort(key=lambda l: l[sort_key], reverse=True)

        print(f'{"name":29} {"mins":8} {"dpm":8} {"kd":8}  {"kPerHH":8}')
        print()

        for l in players_interresting_stats:
            # Only takes plqyers that have a certain time (in minutes) on the class
            if l["mins"] > 150:
                print(f'{l["name"]:25} {l["mins"]:8} {l["dpm"]:8} {l["kd"]:8}  {l["kPerHH"]:8} {l["id"]:15} {l["class"]:15}')

####################################################
####################| PROGRAM |#####################
####################################################

if __name__ == "__main__" :

    pass
    
    # clearDatabase()

    # Gets data from all the logs in the logs folder
    # saveAllLogs()

    # players_id = [log.split(".")[0] for log in os.listdir(cfg.PLAYERS_DIR) if os.path.isfile(os.path.join(cfg.PLAYERS_DIR, log))]


    # classes_for_analysis = ["demoman", "scout", "soldier"]
    # classes_for_analysis = ["demoman"]

    # players_interresting_stats = quickRecap(players_id, classes_for_analysis)
    
    # recapDisplay(players_interresting_stats)


    