
#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.6
# Author :  - https://github.com/sia-coco
########################

# IMPORTS
import sys
import os

# FILE IMPORTS
import tf2_logs_reader.config as cfg

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
##################| FUNCTIONS |#####################
####################################################

# SETUP FOLDER
def setup():
    """ Create different files and folders for storage. Needs to be used first
    in order to use the rest of the functions properly.
    """

    # Data dir
    if not os.path.exists(cfg.DATA_FOLDER):
        os.makedirs(cfg.DATA_FOLDER)
        print(f"# Created folder {cfg.DATA_FOLDER} to store the logs.")
    else:
        print(f"# Folder {cfg.DATA_FOLDER} already exists.")

    # Sub dirs
    if not os.path.exists(cfg.LOGS_DIR):
        os.makedirs(cfg.LOGS_DIR)
        print(f"# Created folder {cfg.LOGS_DIR} to store the logs.")
    else:
        print(f"# Folder {cfg.LOGS_DIR} already exists.")

    if not os.path.exists(cfg.PLAYERS_DIR):
        os.makedirs(cfg.PLAYERS_DIR)
        print(f"# Created folder {cfg.PLAYERS_DIR} to store the logs.")
    else:
        print(f"# Folder {cfg.PLAYERS_DIR} already exists.")


    # Files
    for json_file in [cfg.MATCHES_FILE, cfg.PLAYER_NAMES]:
        if not os.path.exists(json_file):
            with open(json_file, "w") as file:
                file.write("{}")
        else:
            print(f"# File {json_file} already exists.")

    if not os.path.exists(cfg.MATCHES_RECORD):
        with open(cfg.MATCHES_RECORD, "w") as file:
            pass
    else:
        print(f"# File {cfg.PLAYERS_DIR} already exists.")

def setupSQL():
    """ Sets up the sqlite database.
    TODO: Unfinished, WIP
    """

    conn = connectToSQL(cfg.SQL_DB)

    if conn is not None:

        # Creates the match table
        execSQL(conn, "DROP TABLE IF EXISTS matches;")
        execSQL(conn, cfg.MATCH_TABLE_CREATION_SQL)

        # Creates the players table
        execSQL(conn, "DROP TABLE IF EXISTS players;")
        execSQL(conn, cfg.PLAYER_TABLE_CREATION_SQL)

        # Creates the matches players association table
        execSQL(conn, "DROP TABLE IF EXISTS matches_players;")
        execSQL(conn, cfg.MATCH_PLAYER_ASSOCIATION_SQL)

        
        
    
        conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__" :

    q = input("Do you want to setup the folder? (y/n): ")
    if q == "y":
        setup()

    # q = input("Do you want to setup the sql database? (y/n): ")
    # if q == "y":
    #     setupSQL()