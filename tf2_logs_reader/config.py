import os

# WORKSPACE CONFIG
DATA_FOLDER = "data"

SQL_DB      = os.path.join(DATA_FOLDER, "logs_data.db")
LOGS_DIR    = os.path.join(DATA_FOLDER, "stock_logs")
PLAYERS_DIR = os.path.join(DATA_FOLDER, "players_data")

MATCHES_FILE   = os.path.join(DATA_FOLDER, "matches_data.json")
MATCHES_RECORD = os.path.join(DATA_FOLDER, "matches_record.txt")
PLAYER_NAMES   = os.path.join(DATA_FOLDER, "player_names.json")


# QUERY CONFIG

TIMEOUT_DELAY = 4

LOGS_LIST_URL = "http://logs.tf/api/v1/log"
LOGS_URL = "http://logs.tf/json"
DOWNLOAD_SLEEP_DELAY = 0.1

URL64_TF2C    = "76561197964045534"
URL64_SERVEME = "76561197960497430"

TRUSTED_UPLOADERS = [URL64_TF2C, URL64_SERVEME]

MIN_MAX_6S = (12, 14)



# MODULE CONFIG
TOREMOVE_IN_PLAYER_MATCH_STATS = ['kills', 'deaths', 'assists',
                                  'kapd', 'kpd', 'dmg', 'dmg_real', 'dt', 'dt_real',
                                  'lks', 'dapd', 'dapm', 'ubers']
TOREMOVE_IN_PLAYER_CLASS_STATS = ['type', 'kills', 'dmg']
TOREMOVE_IN_PLAYER_WEAPON_STATS = ['shots', 'hits']

TOREMOVE_IN_PLAYER_DICT = {"match": TOREMOVE_IN_PLAYER_MATCH_STATS,
                           "class": TOREMOVE_IN_PLAYER_CLASS_STATS,
                           "weapon": TOREMOVE_IN_PLAYER_WEAPON_STATS}


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