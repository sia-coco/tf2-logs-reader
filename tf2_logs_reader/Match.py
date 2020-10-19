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

class Match():
    """ Represents a match

    INPUTS:
    """

    def __init__(self, id, length, teams_stats, rounds_stats, healspread_stats):

        self.id = id
        self.length = length

        self.team_stats = teams_stats
        self.rounds_stats = rounds_stats
        self.healspread_stats = healspread_stats

        # team_stats contains ['score', 'kills', 'deaths', 'dmg', 'charges', 'drops', 'firstcaps', 'caps']
        # Taking only team exclusive stats
        # self.score     = team_stats["score"]
        # self.firstcaps = team_stats["firstcaps"]
        # self.caps      = team_stats["caps"]

        # self.players = players # might add?

    def __repr__(self):
        line = f"Match '{self.id}'\nlength: {self.length}"
        return line

    def toJSON(self):
        """ Translates the match object to a json string.

        INPUTS:
        OUTPUT:
        """
        return json.dumps(self.__dict__)


####################################################
##################| FONCTIONS |#####################
####################################################


####################################################
##################| VARIABLES |#####################
####################################################


####################################################
##################| CONSTANTES |####################
####################################################


####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :
    pass
    