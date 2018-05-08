import json
import tweepy
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def lambda_handler(event, context):
    #opens and reads sckey.json
    a1key={}
    with open("a1keys/a1key.json") as file:
        a1key = json.loads(file.read())
  
    # Consumer keys and access tokens, used for OAuth
    consumer_key = a1key["consumer_key"]
    consumer_secret = a1key["consumer_secret"]
    access_token = a1key["access_token"]
    access_token_secret = a1key["access_token_secret"]

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Store access keys in a way to send to Twitter
    api = tweepy.API(auth)

    def buildTweet(argument1, argument2):
        tweet = "The Court of Appeals for the Fourth Circuit released an opinion on " + argument1 + " that relates to the First Amendment. To read the full text, visit " + argument2 + "."   
        sendTweet(tweet)

    def sendTweet(content):
        api.update_status(content)
    
    #opens and reads a1apikey.json
    a1apikey={}
    with open("a1keys/a1apikey.json") as file:
        a1apikey = json.loads(file.read())
    #authenticate and calls api to print text
    a1_api_key = a1apikey["a1_api_key"]

    #calls court listener api and puts results into json and dataframe
    urlcourt = 'https://www.courtlistener.com/api/rest/v3/opinions/?cluster__docket__court__id=ca4&order_by=-date_modified'
    headers = {'A1-API-KEY': a1_api_key}
    responsecourt = requests.get(urlcourt, headers=headers)
    jsoncourt = responsecourt.json()
    datacourt = jsoncourt.get('results')
    courtdf = pd.DataFrame(datacourt)

    #import yesterday's date
    def getDate():
        yesterday = datetime.now() - timedelta(days=1)
        date = yesterday.strftime('%Y-%m-%d')
        return date

    #import list of Maryland terms
    a1terms = []
    with open('a1terms.txt', 'r') as s:
        a1terms = s.read().splitlines()
    
    #search for md locations only for today
    date = getDate()
    courtdf = courtdf.replace(np.nan, '', regex=True)
    a1date = courtdf[courtdf['date_created'].str.contains(date)]
    if (len(a1date) > 0):
        irow = a1date.iterrows()
        for a in irow:
            print(a[1]['date_created'])

    for t in a1terms:
        search = a1date[a1date['plain_text'].str.contains(t)]
        if (len(search) > 0):
            irow = search.iterrows()
            for r in irow:
                print(r[1]['absolute_url'])
                buildTweet(date, r[1]['download_url'])
    return 'Hello from Lambda'