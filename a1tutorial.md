## 1st Amendment
**Problem:** At the Court of Appeals for the Fourth Circuit, what cases are related to the first amendment?
**Solution:** Search opinions for the first amendment.

#### Version 1
Sends out a tweet when the program runs to a Twitter account.
* Create a gmail account for bot
  - firstamendmentcns@gmail.com
* Create a Twitter account using gmail account
  - @1st_amendment_4
* Get keys for Twitter account at apps.twitter.com
* Create GitHub repo with 4 files: sctutorial.md, sckey.json, readme.md, GitIgnore, & sccode.py
* Write the following code in pskey.json:
  - consumer key, consumer key secret, access token, & access token secret
* Write the following code in pscode.py:
  - Import Json & Tweepy
  - Call in authentication information from pskey.json
  - Store them so they can be passed into Twitter
  - Create keyword to tweet out
  - Tweet out keyword with authentication to test
```
import json
import tweepy

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
```
#### Version 2 
Put all recent opinions of the Supreme Court in a dataframe
* Get Court Listener API key
* Store in a1apikey.json file
* Call in authentication information from a1apikey.json
* Import requests
* Use requests.get to call URL: https://www.courtlistener.com/api/rest/v3/clusters/?court_id=ca4 
* Headers for authenticating a1apikey.json
* Put results of json into dataframe
```
import requests
import pandas as pd
import numpy as np

#opens and reads a1apikey.json
a1apikey={}
with open("a1keys/a1apikey.json") as file:
    a1apikey = json.loads(file.read())
#authenticate and calls api to print text
a1_api_key = a1apikey["a1_api_key"]

#calls court listener api and puts results into json and dataframe
urlcourt = 'https://www.courtlistener.com/api/rest/v3/opinions/?cluster_docket_court__id=ca4'
headers = {'A1-API-KEY': a1_api_key}
responsecourt = requests.get(urlcourt, headers=headers)
jsoncourt = responsecourt.json()
datacourt = jsoncourt.get('results')
courtdf = pd.DataFrame(datacourt)
```
#### Version 3
* Get yesterday's date
* Search for date in data frame under date_created by iterating over rows
* If found, print out event in console
```
from datetime import datetime, timedelta

#import yesterday's date
def getDate():
    yesterday = datetime.now() - timedelta(days=1)
    date = yesterday.strftime('%Y-%m-%d')
    return date
    
#search for md locations only for today
date = getDate()
courtdf = courtdf.replace(np.nan, '', regex=True)
a1date = courtdf[courtdf['date_created'].str.contains(date)]
if (len(a1date) > 0):
    irow = a1date.iterrows()
    for a in irow:
        print(a[1]['date_created'])
```
#### Version 4
* Create text file of list of terms related to Maryland
* Search for list of terms in recent opinions in plain_text by iterating over rows
* If found, tweet out date
```
#import list of Maryland terms
a1terms = []
with open('a1terms.txt', 'r') as s:
    a1terms = s.read().splitlines()
    
for t in a1terms:
    search = a1date[a1date['plain_text'].str.contains(t)]
    if (len(search) > 0):
        irow = search.iterrows()
        for r in irow:
            print(r[1]['absolute_url'])
            buildTweet(date, r[1]['download_url'])
```