import os

########################
# PROJECT LEVEL CONFIG #
########################

###### DEV CONFIG
DEBUG_MODE = False
DEV_MODE = DEBUG_MODE or False


###### FOLDER/FILE CONFIG

#---------------------------------
WORKSPACE_NAME = "test_data" 
#---------------------------------

RESSOURCES_FOLDER = "ressources"
WORKSPACE_CONFIG_SKELETON = os.path.join(RESSOURCES_FOLDER, "wsconfig.py")

WORKSPACES = "workspaces"

WORKSPACE_FOLDER = os.path.join(WORKSPACES, WORKSPACE_NAME) 

SQL_DB      = os.path.join(WORKSPACE_FOLDER, "logs_data.db")
LOGS_DIR    = os.path.join(WORKSPACE_FOLDER, "stock_logs")
PLAYERS_DIR = os.path.join(WORKSPACE_FOLDER, "players_data")
WORKSPACE_CONFIG = os.path.join(WORKSPACE_FOLDER, "wsconfig.py")
MATCHES_FILE     = os.path.join(WORKSPACE_FOLDER, "matches_data.json")
MATCHES_RECORD   = os.path.join(WORKSPACE_FOLDER, "matches_record.txt")
PLAYER_NAMES     = os.path.join(WORKSPACE_FOLDER, "player_names.json")
CSV_LOGS = os.path.join(WORKSPACE_FOLDER, "logs.csv")






###### LOGS RETRIEVER

TIMEOUT_DELAY = 4
DOWNLOAD_SLEEP_DELAY = 0.1

LOGS_LIST_URL = "http://logs.tf/api/v1/log"
LOGS_URL = "http://logs.tf/json"

URL64_TF2C    = "76561197964045534"
URL64_SERVEME = "76561197960497430"

TRUSTED_UPLOADERS = [URL64_TF2C, URL64_SERVEME]

MIN_MAX_6S = (12, 14)

CP_MAPS   = ["cp_process_final", "cp_process_f5", "cp_process_f6", "cp_snakewater_final1", "cp_gullywash_final1", "cp_sunshine", "cp_granary_pro_rc8", "cp_metalworks", "cp_metalworks_rc7"]
KOTH_MAPS = ["koth_product_rcx", "koth_product_rc9"]
SIXIES_MAPS = CP_MAPS + KOTH_MAPS


###### LOGS TO CSV

# PRE
csv_top_keys_removal_rule_pre = [[[]], ["version", "names", "chat", "info", "killstreaks", "success", "rounds", "classkills", 'classdeaths', 'classkillassists']]
csv_teams_keys_removal_rule_pre = [[["teams", None]], ["kills", "deaths", "dmg", "charges", "drops", "caps"]]
csv_player_keys_removal_rule_pre = [[["players", None]], ['suicides', 'kapd', 'kpd', 'dmg_real', 'dt_real', 'hr', 'lks', 'as', 'dapd', 'dapm', 'ubers', 'medkits_hp', 'backstabs', 'headshots', 'headshots_hit', 'sentries', 'ic']]
csv_medicstats_keys_removal_rule_pre = [[["players", None, "medicstats"]], ['advantages_lost', 'biggest_advantage_lost', 'avg_time_before_healing']]
csv_class_keys_removal_rule_pre = [[["players", None, "class_stats", None]], ['kills', 'assists', 'deaths', 'dmg', 'weapon']]
CSV_KEY_REMOVAL_RULES_PRE = [csv_top_keys_removal_rule_pre, 
                        csv_teams_keys_removal_rule_pre,
                        csv_medicstats_keys_removal_rule_pre,
                        csv_player_keys_removal_rule_pre,
                        csv_class_keys_removal_rule_pre]

# POST
csv_player_keys_removal_rule_post = [[["players", None]], ["class_stats", "team"]]
CSV_KEY_REMOVAL_RULES_POST = [csv_player_keys_removal_rule_post, 
                              ]

CSV_MAINCLASSES = ["scout", "soldier", "demoman", "medic"] # list of class names
CSV_OFFCLASS_BLACKLIST = ["unknown", "undefined"]  # list of class names
CSV_OFFCLASS_LIMITS_CRITERIA = {"heavyweapons": 2000} # Dict of {classname : int}
CSV_OFFCLASS_QUOTAS_CRITERIA = {"heavyweapons": 1, "sniper": 1} # Dict of {classname : float [0-1]}
CSV_TOTAL_OFFCLASS_LIMIT = 2000 # int
CSV_TOTAL_OFFCLASS_QUOTA = 1 # float [0-1]
CSV_OFFCLASS_CRITERIAS = {"offclass_blacklist": CSV_OFFCLASS_BLACKLIST,
                        "offclass_limits": CSV_OFFCLASS_LIMITS_CRITERIA,
                        "offclass_quotas": CSV_OFFCLASS_QUOTAS_CRITERIA, 
                        "total_offclass_limit": CSV_TOTAL_OFFCLASS_LIMIT,
                        "total_offclass_quota": CSV_TOTAL_OFFCLASS_QUOTA} # Selection of pre established criterias

CSV_CLASSLIMIT_RANGES = {"scout": [2,2], "soldier": [2,2], "medic": [1,1], "demoman": [1,1]} # Dict of {classname : range[int, int]}
CSV_CLASSLIMIT_CRITERIAS = {"classlimit_ranges": CSV_CLASSLIMIT_RANGES} # Selection of pre established criterias



# MODULE CONFIG

TOREMOVE_IN_PLAYER_MATCH_STATS  = ['kills', 'deaths', 'assists',
                                  'kapd', 'kpd', 'dmg', 'dmg_real', 'dt_real',
                                  'lks', 'dapd', 'dapm', 'ubers']
TOREMOVE_IN_PLAYER_CLASS_STATS  = ['type', 'kills', 'dmg']
TOREMOVE_IN_PLAYER_WEAPON_STATS = ['shots', 'hits']

TOREMOVE_IN_PLAYER_DICT = {"match": TOREMOVE_IN_PLAYER_MATCH_STATS,
                           "class": TOREMOVE_IN_PLAYER_CLASS_STATS,
                           "weapon": TOREMOVE_IN_PLAYER_WEAPON_STATS}

# SQL
MATCH_TABLE_CREATION_SQL = """  CREATE TABLE IF NOT EXISTS matches (
                                id PRIMARY KEY,
                                match_id integer NOT NULL,
                                game_mode text NOT NULL,
                                map text NOT NULL,
                                length integer NOT NULL,
                                supplemental text NOT NULL,
                                total_length integer NOT NULL,
                                hasRealDamage text NOT NULL,
                                hasWeaponDamage text NOT NULL,
                                hasAccuracy text NOT NULL,
                                hasHP text NOT NULL,
                                hasHP_real text NOT NULL,
                                hasHS text NOT NULL,
                                hasHS_hit text NOT NULL,
                                hasBS text NOT NULL,
                                hasCP text NOT NULL,
                                hasSB text NOT NULL,
                                hasDT text NOT NULL,
                                hasAS text NOT NULL,
                                hasHR text NOT NULL,
                                hasIntel text NOT NULL,
                                AD_scoring text NOT NULL,
                                title text NOT NULL,
                                date integer NOT NULL,
                                uploader_id integer NOT NULL,
                                uploader_name text NOT NULL,
                                uploader_info text NOT NULL
                                );
                                """

PLAYER_TABLE_CREATION_SQL = """  CREATE TABLE IF NOT EXISTS players (
                                 id PRIMARY KEY,
                                 steam_id integer NOT NULL,
                                 team text NOT NULL,
                                 suicides integer NOT NULL,
                                 dmg_real integer NOT NULL,
                                 dt integer NOT NULL,
                                 dt_real integer NOT NULL,
                                 hr integer NOT NULL,
                                 lks integer NOT NULL,
                                 airshots integer NOT NULL,
                                 uber_medigun integer NOT NULL,
                                 uber_kritzkrieg integer NOT NULL,
                                 uber_unknown integer NOT NULL,
                                 drops integer NOT NULL,
                                 medkits integer NOT NULL,
                                 medkits_hp integer NOT NULL,
                                 backstabs integer NOT NULL,
                                 headshots integer NOT NULL,
                                 headshots_hit integer NOT NULL,
                                 sentries integer NOT NULL,
                                 heal integer NOT NULL,
                                 cpc integer NOT NULL,
                                 ic integer NOT NULL,
                                 advantages_lost integer NOT NULL,
                                 biggest_advantage_lost integer NOT NULL,
                                 deaths_with_95_99_uber integer NOT NULL,
                                 deaths_within_20s_after_uber integer NOT NULL,
                                 avg_time_before_healing real NOT NULL,
                                 avg_time_to_build real NOT NULL,
                                 avg_time_before_using real NOT NULL,
                                 avg_uber_length real NOT NULL

                           );
                           """

MATCH_PLAYER_ASSOCIATION_SQL = """ CREATE TABLE IF NOT EXISTS matches_players (
                                match_id INTEGER NOT NULL,
                                player_id INTEGER NOT NULL,
                                PRIMARY KEY (match_id, player_id),
                                FOREIGN KEY (match_id) REFERENCES matches (id),
                                FOREIGN KEY (player_id) REFERENCES players (id)
                           );
                           """
