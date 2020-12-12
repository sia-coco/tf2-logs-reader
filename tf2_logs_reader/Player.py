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
import generic_functions

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

class Player():
    """ Represents a player

    INPUTS:
    """

    def __init__(self, steam_id):

        self.steam_id = steam_id
        self.name = ""

        # Dict of all games played
        self.matches = {}

    def __repr__(self):
        line = f"name: {self.name}\nid: {self.steam_id}\n{len(self.matches.keys())} matches."
        return line

    def addMatch(self, match_id, stats, classkills, classdeaths):
        """ Add stats from one match to the player's match database.

        INPUTS:
                ID of the match (str)
                Individual player data from the log (dict)
                Kills on each class (dict)
                Deaths from each class (dict)
        OUTPUT:
                False if the match was already found in the player's database
                True otherwise
        """

        # If the match wasn't previously saved
        if match_id not in self.matches.keys():
            # Merge class kills and class deaths to the stats dict
            stats["classkills"]  = classkills
            stats["classdeaths"] = classdeaths
            # Add the match data to the player's matches data
            self.matches[match_id] = stats
            return True
        else:
            print(f"Match {match_id} already exists for player {self.steam_id}")
            return False

    def findName(self, names_file):
        """ Assigns a name to the player according to its steam_id 
        and the player_names file.
        """

        # Opens the name file
        with open(names_file) as name_file:
            names_dict = json.load(name_file)

        # If the name exists inside
        if self.steam_id in names_dict:
            # Sets the name of the player
            self.name = names_dict[self.steam_id]

        elif cfg.DEBUG_MODE:
            print(f"player {self.steam_id} has no name in the name table.")

    def cleanMatch(self, match_id, keys_toRemove):
        """ Clears data from the match data according to keys given.
        Usually for clearing redundant or unecessary data.

        INPUTS:
                ID from the match (str)
                The keys to remove in the match dict (dict of lists of str)
                    needs the keys "match", "class", "weapon"
                    {"match": ["", ...], "class": [], "weapon": []}
        """

        match = self.matches[match_id]
        match_keys = match.keys()

        # Removes match keys
        for key in keys_toRemove["match"]:
            if key in match_keys:
                del match[key]

        # If class_stats is a list, transforms it into a dict of dicts where classes are the keys.
        if type(match["class_stats"]) == list:
            new_dict = {class_dict["type"]: class_dict for class_dict in match["class_stats"]}
            match["class_stats"] = new_dict

        classes_dict = match["class_stats"]

        # Goes in each class stats
        for class_k in classes_dict:

            class_dict = classes_dict[class_k]
            class_keys = class_dict.keys()

            # Removes class keys
            for key in keys_toRemove["class"]:
                if key in class_keys:
                    del class_dict[key]

            weapons_dict = class_dict["weapon"]

            # Goes into each weapon stats
            for weapon in weapons_dict.keys():

                weapon_keys = weapons_dict[weapon].keys()

                # Removes weapons stats
                for key in keys_toRemove["weapon"]:
                    if key in weapon_keys:
                        del weapons_dict[weapon][key]

    def cleanAllMatches(self, keys_toRemove):
        """ Clears data from all the matches according to keys given.

        INPUTS:
                The keys to remove in the match dict (dict of lists of str)
                    needs the keys "match", "class", "weapon"
                    {"match": ["", ...], "class": [], "weapon": []}
        """

        for match in self.matches.keys():
            self.cleanMatch(match, keys_toRemove)

    def toJSON(self):
        """ Converts the player object to a json string.

        OUTPUT: 
                player data written in a json string
        """
        return json.dumps(self.__dict__)

    def fromJSON(json_data):
        """ Creates a Player object from json data.

        INPUTS:
                json data
        OUTPUT:
                A Player object
        """

        # Converting to dict
        dict_data = json.load(json_data)

        # Initializing a Player object
        player = Player(dict_data["steam_id"])

        # Setting attributes
        if "name" in dict_data:
            player.name = dict_data["name"] # name

        player.matches = dict_data["matches"] # matches data

        return player

    def save(self, dir):
        """ Saves the data into the player's json file.

        INPUTS:
                Name of the player directory (str)
        """
        player_json = self.toJSON()
        player_file = open(os.path.join(dir, self.steam_id + ".json"), 'w')
        player_file.write(player_json)
        player_file.close()

    def sumMatchData(self, keys):
        """ #TODO

        INPUTS:
        OUTPUT:
        """

        query = {key: 0 for key in keys}

        for match_id in self.matches:
            match = self.matches[match_id]

            for field in keys:
                if field in match:
                    query[field] += match[field]

        return query

    def sumClassData(self, classes, keys):
        """ Gets the data that is specific to the classes requested. Some data from logs
        are for the player as a whole, like suicides or scout kills for example. The data
        retrieved here are per class, not player, which is a good thing.

        Possible classes are : "scout", "pyro", "soldier", "demoman", "heavyweapons",
                               "engineer", "medic", "sniper", "spy"

        Possible keys in the list are : "deaths", "assists", "total_time", "weapon"

        INPUTS:
                list of the class names we want data from ([str, ...])
                list of the attribute names we want data from ([str, ...])
        OUTPUT:
        """

        # Takes note of the matches played
        keys += ["matches_played"]

        query = {c:{key: 0 for key in keys} for c in classes}
        if "weapon" in keys:
            for c in query:
                query[c]["weapon"] = {}

        # For each match
        for match_id in self.matches:
            match = self.matches[match_id]

            # For each requested class
            for class_k in classes:
                # If it exists in that match
                if class_k in match["class_stats"]:
                    query[class_k]["matches_played"] += 1 # Counts the amount of matches played with a given class
                    class_dict = match["class_stats"][class_k]

                    # For each requested stats
                    for field in keys:
                        if field in class_dict:
                            if field == "weapon":
                                query[class_k]["weapon"] = generic_functions.sumDictsOfDicts(query[class_k]["weapon"], class_dict["weapon"])
                            else:
                                query[class_k][field] += class_dict[field]

        return query

    def mergeWeaponData(weapon_data, keys):
        """ Takes weapon data and sums up general data about the class like total of kills, damage etc.
        # TODO
        INPUTS:
        OUTPUT:
        """

        merged = {key:0 for key in keys}

        for weapon in weapon_data:
            for field in keys:
                merged[field] += weapon_data[weapon][field]

        return merged


####################################################
##################| FUNCTIONS |#####################
####################################################


####################################################
##################| VARIABLES |#####################
####################################################


####################################################
###################| CONSTANTS |####################
####################################################


####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :
    pass
