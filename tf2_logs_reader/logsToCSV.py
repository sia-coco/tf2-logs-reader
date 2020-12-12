#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.7
# Author :  - https://github.com/sia-coco
########################

# IMPORTS
import os
import json
import csv


# CUSTOM IMPORTS
import config as cfg
import generic_functions


''' TO DO LIST
'''


''' NOTES
File to handle converting logs to csv lines for data science.

Some logs reference the "unknown" class.
ex:
https://logs.tf/json/2731991
https://logs.tf/json/2715078
Mystery to solve.
'''

####################################################
###################| CLASSES |######################
####################################################


####################################################
##################| FUNCTIONS |#####################
####################################################

# STRUCTURE CONVERSION
def flattenDict(d, parent_key='', sep='_'):
    """ Takes a nested dict and flattens it. Handles list values and converts 
    them into dicts according to rules. 

    INPUTS: 
            a dict
            a prefix for the naming
            separator for the naming

    OUTPUT:
            the flat dict

    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k

        if isinstance(v, dict):
            items.extend(flattenDict(v, new_key, sep=sep).items())

        elif isinstance(v, list):

            if k == "class_stats":
                v = listToDict(v, "type")
            elif k in ["rounds", "events", "killstreaks", "chat"]:
                v = listToDict(v, use_index=True)
            elif cfg.DEBUG_MODE:
                print(f" > WARNING: logsToCSV, flattenDict, key '{k}' unkown and needs to be added to the function")

            items.extend(flattenDict(v, new_key, sep=sep).items())
            
        else:
            items.append((new_key, v))

    return dict(items)

def listToDict(dict_list, name_field=None, use_index=False):
    """  Converts a list of dicts into a dict of dicts. It uses values of the sub dicts 
    as keys for these sub dicts or simply uses their index.

    INPUTS: 
            the list of dicts
            name of the key in sub dicts from which to use the value as a key for the sub dicts
                example: using key "class" in [{'class': 'soldier', ...}] 
                            gives {'soldier': {'class': 'soldier, ...}}
    OUTPUT:
    """ 

    new_dict = None

    if use_index:
        new_dict = {str(i):item for i, item in enumerate(dict_list)}

    elif name_field in dict_list[0]:
        new_dict = {item[name_field]:item for item in dict_list}

    elif cfg.DEBUG_MODE:
        print(f" > ERROR: in logsToCSV.py -> listToDict, name '{name_field}' isn't in the dict {dict_list[0]}")

    return new_dict


###### PRE PROCESSING ######

# KEY REMOVAL
def removeKeys(data, rules):
    """  TODO

    A rule is a list of paths + the keys to remove at the end of these paths.

    TODO: can't access lists, for example class stats for each player.

    INPUTS: 
    OUTPUT:
    """ 
    # print(data["players"]["[U:1:57669738]"]["medicstats"].keys())

    rules = [rule for rule in rules]

    for rule in rules:

        paths = [path for path in rule[0]]

        # Path finding
        for path in paths:
            
            head = data
            del_mode = True
            for i, path_segment in enumerate(path):

                if path_segment is None:
                    del_mode = False

                    if isinstance(head, list):
                        # print(path[i-2])
                        for key in range(len(head)):
                            paths.append(path[:i]+[key]+path[i+1:])
                        # if path[i-2] == '[U:1:60940235]':
                        #     print(head)
                        #     print(len(head))
                        #     print(paths[-1])

                    elif isinstance(head, dict):
                        for key in head:
                            # Yup, modifying the list being explored :) Woohoo!
                            paths.append(path[:i]+[key]+path[i+1:])

                    break
                
                if isinstance(head, dict):
                    if path_segment in head:
                        head = head[path_segment]
                elif isinstance(head, list):
                    # print(head)
                    # print(len(head), path)
                    head = head[path_segment]
                else:
                    continue
            
            # Deletion
            if del_mode:
                for key in rule[1]:
                    if key in head:
                        del head[key]
                    elif cfg.DEBUG_MODE:
                        print(f" > ERROR: logsToCSV.py, removeKeysPreProcess, key {key} doesn't exist in {head} and can't be removed.")

    return data

def dirtyFixKeys(data):
    """ Ehhhh removes keys we don't want, add some we want to guarantee. This function is not generic, just a placeholder
    until i find a better function.

    INPUTS: 
    OUTPUT:
    """ 
    
    # remove the "drops" stat from classes that aren't medic
    for player_id in data["players"]:

        if "medic" not in player_id.lower():

            for med_stat in ["drops", "heal", "ubertypes"]:

                if med_stat in data["players"][player_id]:
                    del data["players"][player_id][med_stat]

            if "medicstats" in data["players"][player_id]:
                del data["players"][player_id]["medicstats"]
        
        else:
            if not "ubertypes" in data["players"][player_id]:
                data["players"][player_id]["ubertypes"] = {}
            for medigun in ["medigun", "kritzkrieg"]:
                if not medigun in data["players"][player_id]["ubertypes"]:
                    data["players"][player_id]["ubertypes"][medigun] = 0


    return data


# MAIN CLASSES / MAIN ROLES

def getPlaytimes(data):
    """  Extract the playtime of each player for each classes they played. 
    Separated into their respective teams.

    INPUTS: 
            logs data

    OUTPUT:
            dict (teams) of dicts (classes) of lists (players and playtimes): 
                {"Blue": {"scout": [["PLAYER_ID_1", int], ..], ..}, "Red": {..}}
    """ 

    # Creates the return dict
    class_names = ["scout", "soldier", "pyro", "demoman", "heavyweapons", "engineer", "medic", "sniper", "spy", "unknown"]
    class_based = {colour: {class_name:[] for class_name in class_names} for colour in ["Red", "Blue"]}

    id_list = list(data["players"].keys())

    player_based = {colour: {} for colour in ["Red", "Blue"]}

    # For each id, stores the playtimes of each played class
    for id in id_list:
        
        player_classes_data = data["players"][id]["class_stats"]
        player_team = data["players"][id]["team"]

        player_class_playtimes = []

        for class_data in player_classes_data:
            # Fill the class based structure
            class_based[player_team][class_data["type"]].append([id, class_data["total_time"]])

            # Fill the player based structure
            player_class_playtimes.append([class_data["type"], class_data["total_time"]])
        
        player_based[player_team][id] = player_class_playtimes


    return class_based, player_based

def solveRolesFromPlaytimes(player_based_playtimes, class_based_playtimes, data):
    """  Takes the playtimes of players for each team plus and deduces their role in the team according to some criterias.
    (For 6s: scout1, scout2, soldier1, soldier2, demoman, medic)

    rules for classification:
        1) Find the main class of each player (class they have the most time on)
            this solves people offclassing to important classes, like medic for 1 min.
            Also should a soldier player, offclassing to scout for 20 mins (let's say 
            viaduct) really be considered a soldier in that game? Here, he'll be counted as
            scout.

        2) To differentiate players from the same team with the same main class, we decide to use
            criterias, default one will be the amount of health received by the med.

        # TODO: add criteria system? with ability to chose criterias

    INPUTS: 
            players based playtimes: 
                {"Blue": {"player1_id": [["class1", int], ..], ..}, "Red": {..}}
            class based playtimes: 
                {"Blue": {"scout": [["player1_id", int], ..], ..}, "Red": {..}}
            logs data

    OUTPUT:
            class based roles dict, sorted in order (first = meets the criteria the most):
                {"Blue": {"class1": ["player_id1", ..], ..}, "Red": {..}}

    """ 

    ### Using heals ###
    
    # Getting the summed heals of each player
    heals = {}
    for medic in data["healspread"]:
        generic_functions.sumDicts(heals, data["healspread"][medic])


    ### Solving main classes ###

    players_mainclasses = {colour: {} for colour in ["Red", "Blue"]}

    for team in player_based_playtimes:
        for player in player_based_playtimes[team]:
            player_based_playtimes[team][player].sort(key=lambda class_elt: class_elt[1], reverse=True)
            players_mainclasses[team][player] = player_based_playtimes[team][player][0][0]


    ### Solving role in the team. ###
    # Sorts players in a team in case they main the same class

    players_roles = {team: {class_played: [player for player in players_mainclasses[team] if players_mainclasses[team][player] == class_played] for class_played in {elt[1] for elt in players_mainclasses[team].items()}} for team in ["Red", "Blue"]}

    for team in players_roles:
        for class_played in players_roles[team]:
            if len(players_roles[team][class_played]) > 1:
                players_roles[team][class_played].sort(key=lambda player_id: heals.get(player_id, 0), reverse=True)

    # for team in players_roles:
    #     print(team)
    #     for class_played in players_roles[team]:
    #         print(class_played, players_roles[team][class_played])
    #     print()

    return players_roles

def idsToClass(data):
    """ Renames the id's from the log to the role of the player.
    
    INPUTS: 
    OUTPUT:
    """ 

    # TODO

    # Getting player class playtimes
    class_based_playtimes, player_based_playtimes = getPlaytimes(data)

    # Classify players to their class
    players_roles = solveRolesFromPlaytimes(player_based_playtimes, class_based_playtimes, data)

    # Call dictKeyRename for each player
    for team in players_roles:
        for class_played in players_roles[team]:
            for i in range(len(players_roles[team][class_played])):
                dictKeyRename(data, players_roles[team][class_played][i], team+class_played.capitalize()+str(i+1))

    return data, players_roles
    
def dictKeyRename(iterable, old_key, new_key):
    """ Renames a key in a dict, recursively.

    INPUTS:
        an iterable
        old_key (string)
        new_key (string)

    OUTPUT:
        a dict with renamed keys
    """

    if isinstance(iterable, dict):

        for key in list(iterable.keys()):
            if key == old_key:
                iterable[new_key] = iterable.pop(old_key)
                if type(iterable[new_key]) in [dict, list]:
                    iterable[new_key] = dictKeyRename(iterable[new_key], old_key, new_key)

            elif type(iterable[key]) in [dict, list]:
                iterable[key] = dictKeyRename(iterable[key], old_key, new_key)

    elif isinstance(iterable, list):
        for item in iterable:
            item = dictKeyRename(item, old_key, new_key)

    return iterable

# OFFCLASSES

def filterOffclassGames():
    """  If a game has too much offclass (variety, amout, time) it's not counted.

    TODO

    INPUTS: 
    OUTPUT:
    """ 
    pass

# LOGS TO CSV
def logToCSVDict(log_file, ids_to_class=False):
    """  Reads a log file and makes a csv file out of it.

    INPUTS: 
            name of the log file (str)
    OUTPUT:
    """ 

    with open(os.path.join(cfg.LOGS_DIR, log_file)) as json_file:

        # Converting json data into python dict
        dict_data = json.load(json_file)

        # Removing keys we don't want to reduce data early
        dict_data = removeKeys(dict_data, cfg.CSV_KEY_REMOVAL_RULES_PRE)

        # Deducing main classes and roles
        if ids_to_class:
            dict_data, players_roles = idsToClass(dict_data)

        dict_data = dirtyFixKeys(dict_data)

        # Removing keys we don't need anymore for the processing
        dict_data = removeKeys(dict_data, cfg.CSV_KEY_REMOVAL_RULES_POST)

        # Flattening the structure
        flat = flattenDict(dict_data)

    return flat

def dictsToCSV(dicts_list, filename):
    """
    Takes a list of dictionaries as input and outputs a CSV file.
    """

    fieldnames = list(dicts_list[0].keys())
    # print(fieldnames)
    
    with open(filename, 'w') as csv_file:

        csvwriter = csv.DictWriter(csv_file, delimiter=',', fieldnames=fieldnames)
        
        header = dict((fn, fn) for fn in fieldnames)
        csvwriter.writerow(header)
        
        for row in dicts_list:
            csvwriter.writerow(row)

####################################################
###################| CONSTANTS |####################
####################################################


####################################################
####################| PROGRAM |#####################
####################################################

if __name__ == '__main__':

    # Getting all the files from the logs folder
    log_files = [log for log in os.listdir(cfg.LOGS_DIR) if os.path.isfile(os.path.join(cfg.LOGS_DIR, log))]
    
    dicts_list = []

    # CSV_dict = logToCSVDict("2733105.json", ids_to_class=True)
    # dicts_list.append(CSV_dict)

    # for log in ["2733009.json", "2733105.json"]:
    #     print(log)
    #     CSV_dict = logToCSVDict(log, ids_to_class=True)
    #     dicts_list.append(CSV_dict)

    i=1
    for log in log_files:
        if log in ["2752628.json", "2755434.json", "2759352.json", "2755330.json", "2761066.json", "2760231.json", "2755351.json", "2752576.json", "2760289.json", "2772057.json", "2768327.json", "2769247.json", "2769189.json", "2768424.json", "2769280.json"]:
            continue
        print(i, log)
        i+=1
        CSV_dict = logToCSVDict(log, ids_to_class=True)
        dicts_list.append(CSV_dict)

    dictsToCSV(dicts_list, cfg.CSV_LOGS)


    # print(csv)

    with open("flat.json", "w") as test_file:
        test_file.write(json.dumps(CSV_dict))



    # with open(os.path.join(cfg.LOGS_DIR, "2704470.json")) as json_file:

    #     # Converting json data into python dict
    #     data = json.load(json_file)

    #     data = dictKeyRename(data, "[U:1:85086904]", "medic69")

    # with open("test.json", "w") as test_file:
    #     test_file.write(json.dumps(data))