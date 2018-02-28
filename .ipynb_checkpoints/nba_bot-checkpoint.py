import praw
import sys
import pandas as pd
import time
from get_nba_data import advanced_stats
from get_nba_data import category_leaders
sys.path.append("/Users/junkim/Documents/nba_bot")
import configure
import DICTS
import UTILS

class nba_stat_bot(object):
    def __init__(self, test_run=True, run_time=1, num_posts=50):
        self.test_run = test_run
        if self.test_run:
            self.run_time = 1*60
        else:
            self.run_time = run_time*60
        self.num_posts = num_posts
        
    def run(self):
        r = UTILS.login_to_reddit()
        t_end = time.time() + 60 * self.run_time
        while time.time() < t_end:      
            # go through every submission on /r/nba
            for comment in r.subreddit('nba').stream.comments():
                # if it has any mentions of nba_stat_bot
                if UTILS.it_calls_nba_stat_bot(comment.body):
                    stat, season = UTILS.parse_comment(comment.body)
                    player, num = UTILS.get_leader_stats(stat, season)
                    UTILS.reply(comment, player, stat, num)
                    
        print("done with one iteration")