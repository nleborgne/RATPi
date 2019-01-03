# -*- coding: utf-8 -*-
import tweepy
from secrets import *
import requests
import logging


# create OauthHandler instance
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
# API instance
api = tweepy.API(auth)

#logging
logging.basicConfig(filename='general.log',level=logging.DEBUG)


def show_tweets(api):
    # show public tweets
    # problem : can't have emojis yet
    public_tweets = api.home_timeline()
    for tweet in public_tweets :
        logging.info(tweet.text.encode('utf-8',errors='ignore'))

def get_followers(api):
    # get followers
    user = api.get_user('ratpidf')
    for friend in user.friends():
        logging.info(friend.screen_name)


def getTraffic(train,line):
    if(train.lower() == 'rer'):
        train1 = 'rers'
    elif(train.lower() == 'metro' or train.lower() == 'métro'):
        train1 = 'metros'
    
    url = ('https://api-ratp.pierre-grimaud.fr/v3/traffic/{}/{}'.format(train1.lower(),line.lower()))
    resp = requests.get(url=url)
    title = resp.json()['result']['title']
    message = resp.json()['result']['message']
    return ('{} {} : {} - {}'.format(train.upper(),line.upper(),title,message))

class BotStreamer(tweepy.StreamListener):

    def on_status(self,status):
        username = status.user.screen_name
        status_id = status.id

        logging.info('{} : {}'.format(username,status.text).encode('utf-8',errors='ignore'))
        string = status.text.split()
        try :
            traffic = getTraffic(string[1],string[2])
            api.update_status(status='@{} {}'.format(username,traffic),in_reply_to_status_id=status.id)
        except Exception as e:
            logging.warning(e)

myStreamListener = BotStreamer()
stream = tweepy.Stream(auth,myStreamListener)
stream.filter(track=['@ratpidf'])
