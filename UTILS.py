import praw
import sys
import pandas as pd
from get_nba_data import advanced_stats
from get_nba_data import category_leaders
sys.path.append("/Users/junkim/Documents/nba_bot")
import configure
import DICTS

# log in to reddit using your reddit bot credentials
def login_to_reddit():
    r = praw.Reddit(username = configure.username,
                    password = configure.password,
                    client_id = configure.client_id,
                    client_secret = configure.client_secret,
                    user_agent = configure.user_agent)
    return r

# does the comment ask for the nba stat bot?
def it_calls_nba_stat_bot(comment):
    comment = comment.lower()
    if "nba_stat_bot" in comment or \
        "nba stat bot" in comment:
        return True
    else:
        return False

def reply(comment_id, name, stat, num):
    comment = "{} led in {} with {} {}".format(name, stat, num, stat)
    comment_id.reply(comment)

def parse_comment(comment):
    comment = comment.lower()
    stat = comment.split("who led in ",1)[1].split()[0]
    season = comment.split("in season ",1)[1].split()[0]\
                .replace("?", "")
    season_plus_one = str(int(season) + 1)[2:]

    return stat, season + "-" + season_plus_one

def get_leader_stats(stat, season):
    leaders = category_leaders()
    assist_leaders = leaders.get_data(stat_cat=stat, 
                                      season=season)
    stat = DICTS.StatCategory[stat]
    player_name = assist_leaders[:1]["PLAYER"]

    #calculate the per game stat for these stats
    stats_need_div = ["OREB","DREB","REB","AST",
                      "STL","BLK","TOV","PTS"]
    if stat in stats_need_div:
        player_stat = assist_leaders[:1][stat] / \
                        assist_leaders[:1]["GP"]
    else:
        player_stat = assist_leaders[:1][stat]

    return player_name[0], player_stat[0]