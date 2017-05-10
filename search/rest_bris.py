import tweepy
import json
import couchdb
import jsonpickle
import sys,os
import time
from textblob import TextBlob
import requests 
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.path as mplPath
import numpy as np
import socket



maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
tweetCount = 0
#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))

print "Connect to socket"
print s.recv(1024)

oauth_keys = [["eNaOt7MW9SUk7zuPQpCrbXTBC", "agxEVyN5z6HtIv9LAK6CNmSU3dH194BMkuALb5oI9PU4Ui5dzK", "855999502255247360-Re3ewycQBkVi08w0rb1sp9bB40cLouA", "nisiRGg3tO50EMmbaU6MvAhnXYXe3FcQ0sjzkolDEPTyV"],
              ["ahAzM3Wvh4YITVM60G65ZuOpP", "NbWxlbuBsoDA4HELYWlyylY0RASjm0Gtbmsn9Vzbx10ZFXDAGv", "855999502255247360-BjSm0tFrw3v3um0QTRJ0wAvmhiy7cme", "kRUY3kM5MbBNryRDMA20EN7CNE7lSdJEg3FO3z7Omm1BH"],
              ["YFwd6NZlPBEm2Nu7VUs7eOXva", "ACa2A3C4RrV2TaSa9v1KF3ruO0zSZBC91RPYDh6K1XzYDY8rry", "855999502255247360-p93VgBZJIdb9254jAiCWzxCJ6RFJsLE", "Yrp1QszXQ2NUXJExQC4NR42ew4t7FpHKVD6EpJK8PBFZL"],
              ["ZQGDhawy20pPmyQmKQ79CtVNu", "Y1goSHJTe70CalKKBhT7EnGgkmiffnevmEvwG34z7IRjVVbBfb", "855999502255247360-wcivhMiEXhZHw5zyDJe0QhulwLaPFUW", "pvWGE9jNQyeHLnnMFkTbXniorXIjlDKuTDBxEPQRkLfXH"],
              ["ibSGx30BljiLofBRtS77AFETt", "4g2H14S8ugsPme1jELA6Y4O9RR5Sf8EElPLH96F5A8XFarl8VM", "855999502255247360-mwwO3oTq9TKhixLA8Exke4vgV1CnyfD", "med3gQXEWkKQtyC84zSDPIgCH3o2WrHGIx7fliTk6sJEf"]]


auths = []  
for consumer_key, consumer_secret, access_key, access_secret in oauth_keys:  
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
    auth.set_access_token(access_key, access_secret)  
    auths.append(auth)

#Pass our consumer key and consumer secret to Tweepy's user authentication handler

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

#Pass our access token and access secret to Tweepy's user authentication handler
#auth.set_access_token(access_token, access_secret)

#Creating a twitter API wrapper using tweepy

# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1L
switch = 0
while tweetCount < maxTweets:
    

    api = tweepy.API(auths[switch], #monitor_rate_limit=True, 

        #retry_count=10000, retry_delay=5, 
         #   retry_errors=set([401, 404, 500, 503]),
                #wait_on_rate_limit=True,
                    wait_on_rate_limit_notify=True)
    
    #Error handling
    if (not api):
        print ("Problem connecting to API")

    

    try:
        if max_id <= 0:
            if (not sinceId):
                new_tweets = api.search(q="place:004ec16c62325149", count=tweetsPerQry)
            else:
                new_tweets = api.search(q="place:004ec16c62325149", count=tweetsPerQry,
                                            since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q="place:004ec16c62325149", count=tweetsPerQry,
                                            max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q="place:004ec16c62325149", count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
        
        if not new_tweets:
            print "No more tweets found"
            time.sleep(180)
        


        for tweet in new_tweets:
            #Load tweets and send to analysis server

            data = json.loads(jsonpickle.encode(tweet._json))
            _id = data['id']
            text = str(data['text'].encode('ascii','ignore'))
            lang = str(data['lang'].encode('ascii'))
            created_at = str(data['created_at'].encode('ascii'))
            coordinates = "null"
            if data['coordinates'] != None:
                coordinates = data['coordinates']['coordinates']
            else:
                print "No coordinate"
            place = str(data['place']['full_name'].encode('ascii'))
            is_finance = 'false'

            send_data = {'id':_id, 'text':text, 'lang':lang, 'created_at':created_at, 'coordinates':coordinates, 'place':place, 'is_finance':is_finance}
            send_date_string = json.dumps(send_data)
            print "send data"

            s.send(send_date_string)
            print " Send data success"  

        tweetCount += len(new_tweets)
        
        try:
            max_id = new_tweets[-1].id
        except :
            continue

        print("Downloaded {0} tweets in Brisbane".format(tweetCount))   

    except tweepy.TweepError as e:
        print "switching keys...bris"
        switch += 1
        if switch > 4:
            print "Limit reached"
            switch = 0
            time.sleep(180)
         
        continue
    except StopIteration:
        break
