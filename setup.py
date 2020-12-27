
#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.6
# Author :  - https://github.com/sia-coco
########################

# IMPORTS
import sys
import os

from shutil import copyfile

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

    # Worspaces dir
    if not os.path.exists(cfg.WORKSPACES):
        os.makedirs(cfg.WORKSPACES)
        print(f"# + Created folder {cfg.WORKSPACES} to store the workspaces.")
    else:
        print(f"# Folder {cfg.WORKSPACES} already exists.")
    if not os.path.exists(os.path.join(cfg.WORKSPACES, "__init__.py")):
        with open(os.path.join(cfg.WORKSPACES, "__init__.py"), "w") as file:
            pass

    # Ressoures dir
    if not os.path.exists(cfg.RESSOURCES_FOLDER):
        os.makedirs(cfg.RESSOURCES_FOLDER)
        print(f"# + Created folder {cfg.RESSOURCES_FOLDER} to store the ressource files.")
    else:
        print(f"# Folder {cfg.RESSOURCES_FOLDER} already exists.")


    # Workspace dir
    if not os.path.exists(cfg.WORKSPACE_FOLDER):
        os.makedirs(cfg.WORKSPACE_FOLDER)
        print(f"# + Created folder {cfg.WORKSPACE_FOLDER} to store the logs.")
    else:
        print(f"# Folder {cfg.WORKSPACE_FOLDER} already exists.")

    # Sub dirs
    if not os.path.exists(cfg.LOGS_DIR):
        os.makedirs(cfg.LOGS_DIR)
        print(f"# + Created folder {cfg.LOGS_DIR} to store the logs.")
    else:
        print(f"# Folder {cfg.LOGS_DIR} already exists.")

    if not os.path.exists(cfg.PLAYERS_DIR):
        os.makedirs(cfg.PLAYERS_DIR)
        print(f"# + Created folder {cfg.PLAYERS_DIR} to store the logs.")
    else:
        print(f"# Folder {cfg.PLAYERS_DIR} already exists.")


    # Files
    for json_file in [cfg.MATCHES_FILE, cfg.PLAYER_NAMES, cfg.TEAMS_FILE]:
        if not os.path.exists(json_file):
            with open(json_file, "w") as file:
                file.write("{}")
            print(f"# + File {json_file} created.")
        else:
            print(f"# File {json_file} already exists.")

    for text_file in [cfg.MATCHES_RECORD, os.path.join(cfg.WORKSPACE_FOLDER, "__init__.py")]:
        if not os.path.exists(text_file):
            with open(text_file, "w") as file:
                pass
            print(f"# + File {text_file} created.")
        else:
            print(f"# File {text_file} already exists.")

    # Workspace config file
    if not os.path.exists(cfg.WORKSPACE_CONFIG):
        copyfile(cfg.WORKSPACE_CONFIG_SKELETON, cfg.WORKSPACE_CONFIG)
        print(f"# + File {cfg.WORKSPACE_CONFIG} created.")
    else:
        print(f"# File {cfg.WORKSPACE_CONFIG} already exists.")



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

    q = input("Do you want to setup the folder workspace? (y/n): ")
    if q == "y":
        setup()

    # q = input("Do you want to setup the sql database? (y/n): ")
    # if q == "y":
    #     setupSQL()
    