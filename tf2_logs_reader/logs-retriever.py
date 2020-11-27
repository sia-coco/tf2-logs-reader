#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.7
# Author :  - https://github.com/sia-coco
########################

# IMPORTS
import os
import requests
from requests.exceptions import HTTPError
import json
import time
import itertools

# CUSTOM IMPORTS
import config as cfg


''' TO DO LIST
'''


''' NOTES
'''

####################################################
###################| CLASSES |######################
####################################################

class LogsRetriever():
    """ 

    uploaders:
        76561197964045534 : TF2C
        76561197960497430 : serveme

    request_args = {"title":X, "uploader":Y, "player": Z, "limit": N, "offset": N}

    INPUTS:
            dict or arguments for the api request (see above)
    """

    def __init__(self, request_args):
        
        self.request_args = request_args

        # The response of logs.tf api for list of logs
        self.logs_tf_response = None

        # The list of logs we are going to work on
        self.log_list         = None


    def main(self, clean_params):
        """ 
        """ 

        self.logs_tf_response = getLogsList(self.request_args)
        self.log_list = self.logs_tf_response["logs"]

        self.cleanLogList(**clean_params)

        if cfg.DEBUG_MODE:
            self.profilePlayersLogs()


    ###### CLEAN LOG LIST ######

    def cleanLogList(self, split_trusted=False, time_frame=[None, None], player_frame=[None, None], map_frame=None):
        """  Cleans the log list according to given criterias
            
    
        INPUTS: 
                (option) keep logs from trusted uploaders
        """ 

        if split_trusted:
            self.log_list, untrusted_logs = self.splitLogsTrustedUntrusted()
        
        # Selects logs from a certain time frame
        self.log_list = selectLogsListFrame(self.log_list, "date", frame=time_frame)

        # Select logs with certain amounts of players (to get games from particular formats)
        self.log_list = selectLogsListFrame(self.log_list, "players", frame=player_frame)

        # Select logs of particular maps
        self.log_list = selectLogsListFrame(self.log_list, "map", str_frame=map_frame)


    def splitLogsTrustedUntrusted(self):
        """  takes a list of logs and discriminates the ones from trusted 
        sources from the others.
    

        OUTPUT: 
                a list of "trusted" logs
                a list of the remaining logs
        """ 

        # The list of arguments can't specify uploaders. Since the goal is 
        #     to compare the whole group of uploaders with the trusted ones.
        if "uploader" in self.request_args:
            if self.request_args["uploader"] is not None:
                print(f" > ERROR : request_args{self.request_args} should not contain key 'uploader'.")
        
        # Getting every log id
        full_id_list = [k["id"] for k in self.log_list]
        

        ### Getting trusted sources logs
        trusted_uploaders_log_list = []
        trusted_uploaders_id_list = []

        for trusted_uploader in cfg.TRUSTED_UPLOADERS:

            # log list
            trusted_uploader_log_list = getLogsList({**self.request_args, **{"uploader": trusted_uploader}})["logs"]
            trusted_uploaders_log_list += trusted_uploader_log_list

            # log id list
            trusted_uploader_id_list = [k["id"] for k in trusted_uploader_log_list]
            trusted_uploaders_id_list += trusted_uploader_id_list

        ### Getting untrusted logs
        other_ids = set(full_id_list).symmetric_difference(set(trusted_uploaders_id_list))
        other_log_list = [log for log in self.log_list if log["id"] in other_ids]
        

        return (trusted_uploaders_log_list, other_log_list)
    


    ###### DOWNLOAD LOGS ######

    def downloadLogsFromList(self):
        """ Downloads logs from the list to the local directory.
        """ 
        
        # Getting the list of all the id's from the logs we want to download
        logs_ids_list = [str(log["id"]) for log in self.log_list]
        old_size = len(logs_ids_list)

        # Getting the list of all the id's from already downloaded logs
        already_dowloaded_logs = [log.split(".")[0] for log in os.listdir(cfg.LOGS_DIR) if os.path.isfile(os.path.join(cfg.LOGS_DIR, log))]

        logs_ids_list = [log_id for log_id in logs_ids_list if log_id not in already_dowloaded_logs]
        new_size = len(logs_ids_list)

        print(f"{old_size - new_size} logs already downloaded. Remaining amount to download: {new_size}")


        dl_count = 0
        for log_id in logs_ids_list:


            downloaded = False

            while not downloaded:

                # Sleeps to avoid downloding to quickly and getting denied by server
                time.sleep(cfg.DOWNLOAD_SLEEP_DELAY)

                # Downloading
                json_log = getResponse(cfg.LOGS_URL+"/"+log_id)

                if json_log is not None:
                    downloaded = True

                    # Converting to string
                    json_string = json.dumps(json_log)

                    # Saving in a corresponding file
                    log_file = open(os.path.join(cfg.LOGS_DIR, log_id + ".json"), 'w')
                    log_file.write(json_string)
                    log_file.close()
                
                else:

                    print(f" > ERROR in logs-retriever : log {log_id} didn't get downloaded. Retrying.")

            dl_count += 1
            print(f"{dl_count}/{new_size}")

        print(" > Done downloading")



    ###### USER UTILITY/PRINTS ######

    def profilePlayersLogs(self):
        """  Prints a recap of the logs.

        """ 
        
        result = obj.splitLogsTrustedUntrusted()

        print(f"total logs: {len(result[0])+len(result[1])}")
        print(f"trusted uploaders logs: {len(result[0])}")
        print(f"other logs: {len(result[1])}")



####################################################
##################| FUNCTIONS |#####################
####################################################

def getResponse(url, request_args={}):
    """ Gets the json response from a query.

    INPUTS:
            the url to query
            args for the query

    OUTPUT:
            json response
    """

    try:
        # Sends request
        response = requests.get(url, timeout=cfg.TIMEOUT_DELAY, params=request_args)

        # Check validity
        response.raise_for_status()


    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

    except Exception as err:
        print(f'Other error occurred: {err}')

    else:
        return response.json()

def getLogsList(request_args):
    """ Retrieves json list of logs answer from logs.tf using search parameters.

    request_args = {"title":X, "uploader":Y, "player": Z, "limit": N, "offset": N}

    INPUTS:
            dict or arguments for the api request (see above)

    OUTPUT:
            the response of logs.tf api for list of logs
    """ 
    
    url = cfg.LOGS_LIST_URL

    return getResponse(url, request_args)

def selectLogsListFrame(log_list, field, frame=(None, None), str_frame=None):
    """ Only keeps logs in the log list that are within a given value frame.

    frame (min,max) values are included in the output

    fields: ["id", "title", "map", "date", "views", "players"]

    frame values:
        - "id" is the log id on logs.tf
        - "title" is the log title on logs.tf
        - "map" is the exact name of the map desired
        - "date" is the date of submission of the log in seconds from epoch
            https://www.epochconverter.com/
        - "views" the amount of times the log has been viewed on logs.tf
        - "players" the amount of players who participated in the game

    INPUTS: 
            the log list [{field1, field2, ..}, ..]
            the field we want to use as filter
            a couple of (min,max) value for the given field

    OUTPUT:
            list of the logs remaining after filtering
    """ 
    if cfg.DEBUG_MODE:
        print(f"size of list before {field} filter : {len(log_list)}")

    if field in ["id", "date", "views", "players"]:
        
        if frame[0] is not None:
            log_list = [log for log in log_list if log[field]>= frame[0]]
        if frame[1] is not None:
            log_list = [log for log in log_list if log[field]<= frame[1]]

    elif field in ["title", "map"]:
        if str_frame is not None:
            log_list = [log for log in log_list if log[field] in str_frame]

    else :
        print(f" > ERROR: logs-retriever.py, selectLogsListFrame, field '{field}' unknown.")

    if cfg.DEBUG_MODE:
        print(f"size of list after {field} filter : {len(log_list)}")

    return log_list

def removeDuplicates():
    """  Detects and removes logs that got sent twice to logs.tf through 
    multiple uploaders.

    INPUTS: 
    OUTPUT:
    """ 
    pass

def kPlayersFromTeam(team, k, team_name):
    """  Generates combinations of k players from a team

    INPUTS: 
            a team dict: {"team name": {"player 1": id_1, ...}}
            amount of players for each sub group
            team name: str
    OUTPUT:
            a player dict: {"team - player1, player2, ...": "id1, id2, ..."}
    """ 
    
    combs = [comb for comb in itertools.combinations(team, k)]

    players = {}

    for comb in combs:
            
        players[team_name+" - "+", ".join(comb)] = ", ".join([team[player_name] for player_name in comb])

    return players  

####################################################
###################| CONSTANTS |####################
####################################################


####################################################
####################| PROGRAM |#####################
####################################################

if __name__ == '__main__':
    

    players = {}

    # players = {
    #     "mystt, daga, marv": "76561198114545358, 76561198105323129, 76561198042599456"}


    # players = {
    #     "sia": "76561198377453187"}

    # teams = {
    #     "Weebtech": {"aqua": "76561198800637336", 
    #                 "Frager": "76561198323411853", 
    #                 "strange_magic": "76561197993508562",
    #                 "Houf": "76561198448050535", 
    #                 "Miku": "76561198127793996",},
    # }

    teams = {
        "Gucci": {"smi": "76561198056760624", 
                    "sia": "76561198377453187", 
                    # "hud": "76561198020644759", 
                    "Dying Tom": "76561197975576152",
                    "snb": "76561198021205963", 
                    "neko": "76561198144936805",
                    "b4ro": "76561198041043955"},

        "frenchies": {"rdm": "76561198075159093", 
                    "Reyviix": "76561198268216386",
                    "azitio": "76561198084056439", 
                    "gtlm": "76561198084798301", 
                    "flash": "76561198067379855", 
                    "sun4": "76561197995912889"},
        
        "wall rats": {"legatus": "76561198257342972", 
                    "strife": "76561197972383519", 
                    "black jesus": "76561198261795972", 
                    "zoid": "76561198142074232", 
                    "drozdzers": "76561198000639694", 
                    "nurse": "76561198204505424"},
        
        "russians": {"vorobey": "76561198035711179", 
                    "smd": "76561198373793124", 
                    "x_dias": "76561198857650831", 
                    "1TY3": "76561198821399014", 
                    "pupsik": "76561198419106750", 
                    "uolya": "76561198017935466"},
        
        # "snack": {"Sora": "76561198147190605",
        #             "harbl": "76561198024929695", 
        #             "robin": "76561198041264237", 
        #             "Luna": "76561198420882457", 
        #             "Apolo": "76561198116159344"},
     
        "Vodka": {"tsd": "76561198287797509", 
                    "TendoN": "76561198870764276", 
                    "cherry": "76561198843962495", 
                    "adru": "76561198085230924", 
                    "znach": "76561198173267766", 
                    "laiky": "76561198258487465"},
        
        "GADOU": {"YoungBuck": "76561198000321365",
                    "spolioz": "76561198035671349",
                    "elite": "76561198044201431",
                    "rvn": "76561198044957035",
                    "azer": "76561198196708482",
                    "ympo": "76561198202441870"},

        "Quality Control": {"Munky": "76561198009322855",
                    "Mont": "76561198008462369",
                    "Cak3": "76561198012633295",
                    "Tammrock": "76561198029322294",
                    "Fenrir": "76561198004910829",
                    "SmAsH": "76561197999115826"},

        "Orange": {"Shizuu": "76561198113918934",
            "Dave": "76561198046838348",
            "Sebab": "76561198122706821",
            "CaptainPadux": "76561198303885943",
            "Ryan": "76561198091360047",
            "MindBl4st": "76561198093936708"},

        "Gaeta": {"TBourdon": "76561198105347669",
            "MattJ": "76561198115594594",
            "Ja": "76561198052996870",
            "DeIT": "76561198204007537",
            "Emiel": "76561198063814219",
            "Coca": "76561198077605729"},
    }

    for team in teams:
        player_comb = kPlayersFromTeam(teams[team], 5, team)
        players = {**players, **player_comb}



    # 1601510400: 1 oct 2020
    # 1605355200: 14 nov 2020 before dreamhack
    # 1605394800: 14 nov 2020 after dreamhack
    # clean_params = {"split_trusted":False, "time_frame":[1601510400, 1605355200], "player_frame":[12, 13], "map_frame":cfg.CP_MAPS}
    clean_params = {"split_trusted":False, "time_frame":[1605394800, None], "player_frame":[12, 13], "map_frame":cfg.CP_MAPS}

    for players_id in players: 

        print(players_id)

        args = {"title":None, "uploader":None, "player": players[players_id], "limit": 50, "offset": None}
        obj = LogsRetriever(args)

        obj.main(clean_params)
        obj.downloadLogsFromList()

        print()




    