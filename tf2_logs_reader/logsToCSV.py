#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.7
# Author :  - https://github.com/sia-coco
########################

# IMPORTS
import sys
import os
import json
import csv
import importlib


# CUSTOM IMPORTS
import config as cfg
import generic_functions

# workspace config
sys.path.insert(0, os.path.abspath("./")) #
wscfg = importlib.import_module(".".join([cfg.WORKSPACES, cfg.WORKSPACE_NAME, "wsconfig"]))

''' TO DO LIST
'''


''' NOTES
File to handle converting logs to csv lines for data science.

Some logs reference the "unknown" class.
ex:
https://logs.tf/json/2731991
https://logs.tf/json/2715078
Mystery to solve.

OH, some news, an "undefined" class exists too...
https://logs.tf/json/2779696
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
                ignored if use_index is set to True
            option : uses the index of the element in the list as a key
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
    """ Removes keys (and elements they link to) from the data (nested dicts) according to
    given rules.

    A rule is a list of paths + the keys to remove at the end of these paths.

    A path is a list of path segments. A path segment is a dict key in the data.

    A path segment can be replaced by None as a wildcard to generate new paths
    with all of the possible sub path segments accessible from it.

    TODO: can't access lists, for example class stats for each player.

    INPUTS:
            logs data (mostly nested dicts)
            rules for the removal:
                [[["path_segment1", ..], ..], ["key_to_remove1", ..]]
    OUTPUT:
            the logs data with keys deleted
    """

    # Making a copy of the rule list
    rules = [rule for rule in rules]

    for rule in rules:

        # Making a copy of the path list
        paths = [path for path in rule[0]]

        # Path finding
        for path in paths:

            head = data
            del_mode = True

            for i, path_segment in enumerate(path):

                # If a None wildcard has been used, generates the new paths
                if path_segment is None:
                    del_mode = False

                    if isinstance(head, list):
                        for key in range(len(head)):
                            paths.append(path[:i]+[key]+path[i+1:])

                    elif isinstance(head, dict):
                        for key in head:
                            # Yup, modifying the list being explored :) Woohoo!
                            paths.append(path[:i]+[key]+path[i+1:])

                    # breaking since the current path is only a scheme for actual paths
                    # and shouldn't be used to delete keys direcly
                    break

                # Going to next segment
                if isinstance(head, dict):
                    if path_segment in head:
                        head = head[path_segment]
                elif isinstance(head, list):
                    head = head[path_segment]
                else:
                    continue

            # Deletion
            if del_mode:
                for key in rule[1]:
                    if key in head:
                        del head[key]
                    elif cfg.DEBUG_MODE:
                        print(f" > WARNING: logsToCSV.py, removeKeys, key {key} doesn't exist in {head} and can't be removed.")

    return data

def dirtyFixKeys(data):
    """ Ehhhh removes keys we don't want, add some we want to guarantee. This function
    is not generic, just a placeholder until I find better functions.

    INPUTS:
            logs data
    OUTPUT:
            modified logs data
    """

    # remove the "drops" stat from classes that aren't medic
    for player_id in data["players"]:

        if "medic" not in player_id.lower():

            for med_stat in ["drops", "heal", "ubertypes"]:

                if med_stat in data["players"][player_id]:
                    del data["players"][player_id][med_stat]

            if "medicstats" in data["players"][player_id]:
                del data["players"][player_id]["medicstats"]

            if player_id in data["healspread"]:
                del data["healspread"][player_id]

        else:
            if not "ubertypes" in data["players"][player_id]:
                data["players"][player_id]["ubertypes"] = {}

            for medigun in ["medigun", "kritzkrieg", "unknown"]:
                if not medigun in data["players"][player_id]["ubertypes"]:
                    data["players"][player_id]["ubertypes"][medigun] = 0

            if not "medicstats" in data["players"][player_id]:
                data["players"][player_id]["medicstats"] = {}

            for med_stat in ["deaths_with_95_99_uber", "deaths_within_20s_after_uber"]:
                if not med_stat in data["players"][player_id]["medicstats"]:
                    data["players"][player_id]["medicstats"][med_stat] = 0

            for med_stat in ["avg_time_to_build", "avg_time_before_using", "avg_uber_length"]:
                if not med_stat in data["players"][player_id]["medicstats"]:
                    data["players"][player_id]["medicstats"][med_stat] = None


    return data


# MAINCLASSES / MAIN ROLES

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
    class_names = ["scout", "soldier", "pyro", "demoman", "heavyweapons", "engineer", "medic", "sniper", "spy", "unknown", "undefined"]
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

def idsToClass(data, players_roles):
    """ Renames the id's from the log to the role of the player.

    INPUTS:
            logs data
            class based roles dict, sorted in order (first = meets the criteria the most):
                {"Blue": {"class1": ["player_id1", ..], ..}, "Red": {..}}

    OUTPUT:
            modified logs data
    """

    # Call dictKeyRename for each player
    for team in players_roles:
        for class_played in players_roles[team]:
            for i in range(len(players_roles[team][class_played])):
                dictKeyRename(data, players_roles[team][class_played][i], team+class_played.capitalize()+str(i+1))

    return data

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
def filterOffclassGames(player_based_playtimes, mainclasses, criterias, response=False):
    """  If a game has too much offclass (variety, amout, time) it's not counted.

    criterias:
        offclass_blacklist : list of offclasses not accepted : list of str

        offclass_limits : max threshold for each offclass : dict {class: int}
        offclass_quotas : max limit percentage of the total playtime spent offclassing

        total_offclass_limit : max threshold of summed offclasses
        total_offclass_quota : max limit percentage of summed offclasses


    INPUTS:
            list of the classes considered main classes : list of str
            playtimes for each player on each of their played classes
            criterias : dict of criterias
                program handles known criterias
            the response the function has to give if the criterias aren't met
    OUTPUT:
            response (bool) if the criterias aren't met, !response otherwise
    """

    # Simplifying the structure
    playtimes = [player_based_playtimes[team][player_id] for team in player_based_playtimes for player_id in player_based_playtimes[team]]

    for criteria in criterias:

        if criteria == "offclass_blacklist":
            for player in playtimes:
                for class_played in player:
                    if class_played[0] in criterias[criteria]:
                        return response

        elif criteria == "offclass_limits":
            for player in playtimes:
                for class_played in player:
                    if class_played[0] in criterias[criteria]:
                        if class_played[1] > criterias[criteria][class_played[0]]:
                            return response

        elif criteria == "offclass_quotas":
            for player in playtimes:
                total_playtime = sum([class_played[1] for class_played in player])
                for class_played in player:
                    if class_played[0] in criterias[criteria]:
                        if class_played[1]/total_playtime > criterias[criteria][class_played[0]]:
                            return response


        elif criteria == "total_offclass_limit":
            for player in playtimes:
                total_offclass_time = sum([class_played[1] for class_played in player if class_played[0] not in mainclasses])
                if total_offclass_time > criterias[criteria]:
                    return response

        elif criteria == "total_offclass_quota":
            for player in playtimes:
                total_playtime = sum([class_played[1] for class_played in player])
                total_offclass_time = sum([class_played[1] for class_played in player if class_played[0] not in mainclasses])
                if total_offclass_time/total_playtime > criterias[criteria]:
                    return response

        else:
            print(f" > ERROR: logsToCSV.py, filterOffclassGames, criteria {criteria} isn't known.")

    return not response

# CLASS LIMIT
def filterClassLimit(players_roles, criterias, response=False):
    """  If a game has unwanted mainclasses (type, amount) it's not counted.

    criterias:
        classlimit_ranges : range of the amount of players
            that can main a certain class for each team

    INPUTS:

            criterias : dict of criterias
                program handles known criterias
            the response the function has to give if the criterias aren't met

    OUTPUT:
            response (bool) if the criterias aren't met, !response otherwise
    """

    for criteria in criterias:

        if criteria == "classlimit_ranges":
            for team in players_roles:
                for class_played in criterias[criteria]:
                    if class_played in players_roles[team]:
                        amount_of_players = len(players_roles[team][class_played])
                        if amount_of_players < criterias[criteria][class_played][0] or amount_of_players > criterias[criteria][class_played][1]:
                            return response
                    elif criterias[criteria][class_played][0] > 0:
                        return response

        else:
            print(f" > ERROR: logsToCSV.py, filterOffclassGames, criteria {criteria} isn't known.")


    return not response

# LOGS TO CSV
def workspaceLogsToCSV(ids_to_class, filter_class_limit):
    """ Goes through all the logs of the workspace and stores their data
    in a csv file. Useful for easier data science investigation.

    INPUTS:
            option: True if steam id's in the logs should e converted into the roles played
            option: True if the logs should be filtered according to classes played

    """
    # Getting all the files from the logs folder
    log_files = [log for log in os.listdir(cfg.LOGS_DIR) if os.path.isfile(os.path.join(cfg.LOGS_DIR, log))]

    # List to store the log dicts
    dicts_list = []

    # # FOR DEV
    # CSV_dict = logToCSVDict(log_files[143], ids_to_class=True, filter_class_limit=True)
    # dicts_list.append(CSV_dict)
    # print(log_files[143])

    # For tests
    if cfg.DEV_MODE:
        i = 0

    # For each log
    for j, log in enumerate(log_files):

        # Taking a log and applying multiple cleaning operations to prepare for the CSV
        CSV_dict = logToCSVDict(log, ids_to_class=ids_to_class, filter_class_limit=filter_class_limit)

        # Filtering logs that aren't acceptable
        if not CSV_dict is None:
            dicts_list.append(CSV_dict)

        # For tests
        elif cfg.DEV_MODE:
            i+=1
            print(f"log n°{j+1}, {log} denied")

    # Exports to a CSV file with each log dict as a line
    dictsToCSV(dicts_list, cfg.CSV_LOGS)

    # For tests
    if cfg.DEV_MODE:

        print(f"{i} logs denied")

        with open("tests/flat.json", "w") as test_file:
            test_file.write(json.dumps(CSV_dict))

def logToCSVDict(log_file, ids_to_class=False, filter_class_limit=False):
    """  Reads a log file and prepares the dict so it is ready to be added to a CSV file.

    INPUTS:
            name of the log file (str)
            option: True if steam id's in the logs should e converted into the roles played
            option: True if the logs should be filtered according to classes played
    OUTPUT:
            A flat dict, pre processed
    """

    with open(os.path.join(cfg.LOGS_DIR, log_file)) as json_file:

        # Converting json data into python dict
        dict_data = json.load(json_file)

    # Removing keys we don't want to reduce data early
    dict_data = removeKeys(dict_data, wscfg.CSV_KEY_REMOVAL_RULES_PRE)

    # Getting player class playtimes
    class_based_playtimes, player_based_playtimes = getPlaytimes(dict_data)

    # If the offclassing criterias aren't met log is ignored
    if not filterOffclassGames(player_based_playtimes, wscfg.CSV_MAINCLASSES, wscfg.CSV_OFFCLASS_CRITERIAS, response=False):
        return None

    # Classify players to their class if needed
    if ids_to_class or filter_class_limit:
        players_roles = solveRolesFromPlaytimes(player_based_playtimes, class_based_playtimes, dict_data)

    # If the mainclasses criterias aren't met log is ignored
    if filter_class_limit:
        if not filterClassLimit(players_roles, wscfg.CSV_CLASSLIMIT_CRITERIAS):
            return None

    # Deducing main classes and roles
    if ids_to_class:
        dict_data = idsToClass(dict_data, players_roles)

    dict_data = dirtyFixKeys(dict_data)

    # Removing keys we don't need anymore for the processing
    dict_data = removeKeys(dict_data, wscfg.CSV_KEY_REMOVAL_RULES_POST)

    # Flattening the structure
    flat = flattenDict(dict_data)

    return flat

def dictsToCSV(dicts_list, filename):
    """
    Takes a list of dictionaries as input and outputs a CSV file.

    INPUTS:
            list of csv ready dicts
            filename to store the csv data in
    """

    fieldnames = list(dicts_list[0].keys())

    with open(filename, 'w') as csv_file:

        csvwriter = csv.DictWriter(csv_file, delimiter=',', fieldnames=fieldnames)

        header = dict((fn, fn) for fn in fieldnames)
        csvwriter.writerow(header)

        for i, row in enumerate(dicts_list):
            if cfg.DEBUG_MODE:
                print(f"log n°{i+1}")
                csvwriter.writerow(row)
            else:
                try:
                    csvwriter.writerow(row)
                except:
                    pass


####################################################
###################| CONSTANTS |####################
####################################################


####################################################
####################| PROGRAM |#####################
####################################################

if __name__ == '__main__':

    pass
