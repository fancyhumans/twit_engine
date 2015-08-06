# -*- coding: utf-8 -*-

import tweepy
import schedule
import random
import time
import ConfigParser
from datetime import datetime

config = ConfigParser.RawConfigParser()
config.read('settings.cfg')


CONSUMER_KEY = config.get('Twitter OAuth', 'CONSUMER_KEY')
CONSUMER_SECRET = config.get('Twitter OAuth', 'CONSUMER_SECRET')
ACCESS_TOKEN_KEY = config.get('Twitter OAuth', 'ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = config.get('Twitter OAuth', 'ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def main():
    user_list = ['inspire_us','wisdomsquote', 'GreatestQuotes', 'alphabetsuccess', 'InspowerMinds', 'DavidRoads']
    fr = open('posted_twts.txt', 'rb')
    tweet_list = list(eval(fr.read()))
    flag = 1
    count = 0
    while flag:
        user = random.choice(user_list) or False
        last_id = random.choice(tweet_list) or False
        tw_res = api.user_timeline(user, since_id=last_id, count=1, include_rts=False)
        for t_res in tw_res:
            new_status = str(t_res.text)
            if t_res.id in tweet_list:
                flag = 1
            elif 'http' in new_status:
                flag = 1
            elif '@' in new_status:
                flag = 1
            else:
                print new_status
                fl = open('log.txt', 'a')
                api.update_status(status = new_status)
                line = str(datetime.now())+ ','+t_res.id+','+ user +','+ new_status + '\n'
                fl.write(line)
                fl.close()
                fw = open('posted_twts.txt', 'a')
                fw.write(str(t_res.id) + ',')
                fw.close()
                flag = 0
        count += 1
        if count == 10:
            flag = 0

if __name__ == '__main__':
    schedule.every(1).minutes.do(main)
    while 1:
        schedule.run_pending()
        time.sleep(1)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: