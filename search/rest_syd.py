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

oauth_keys = [["k687eBqLZnS6UOtx6etDg2UnX", "aDbBWi9hAG703xNFXCTIEG6pB2qGsHLoUvvhIpnIjJZVbL4dBe", "762662430-VfMM4zSLxQBtYNInjvwqaYbVKbOxfna5faf3u8J2", "ZaJZzWt1zcwPd9yh4F64aLnfzg0PyJHUE0T8iXgU2yjce"],
              ["wEkdhaqWDQNZQVY3E0YD1fler", "2w0bhxYGBDIHcERBewYi5Ykv497NilJ27UV6S1tsEEq9u5NmAo", "762662430-bjXItOt3fEE8R9mBlD9Be1x70uRmeFbNWh2g0NNV", "gcvMWQkl8zLUW0eQuFgtacrD5ByghJlq226ewzdfbL9Pj"],
              ["KuzAGiFtOlmYSbPVr1rBHgHL6", "BHX5PJvjm1tx318ovvs65gAWeZoZARXwV9BZn2OAJwq4UPeo64", "839300214410207232-SJlWiB6lgyqF3kvyAoHdPvfa7dCPLpf", "mX2lJ9lSViNvMw7ydSaLYZT9jT8YtfIxhW5j5cbQAF4Yj"],
              ["4reQgCnnupSfb91YRh2b0Z3es", "J0DleKwUVRFdMLDX2tKgvKQAKmmZBXWEI7ID0QlDyWVySb30ql", "839300214410207232-Uesl5uOmzHZsgRQSK9MLcZESihTnlyF", "uOozVm23tG4228c5oVfk82EMTPDaCw5XaokqnKQK4wGj9"],              
              ["d6o4P8YbmQxoypzjbTqRE44m3", "kriQg5h3RPz9eQMZqlYGDSjCRDczRXG3P06NXBcF0oJDvCuaGk", "762662430-NSeAkrU4wHTTNgcaLx7EyqwHpBUSTzh5Hu0xM9Gj", "xO1QXw1FcbEZ72AyQZ8JhMA5PDKjnTPwZVCTIocMFEt9F"]]


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
                new_tweets = api.search(q="place:0073b76548e5984f", count=tweetsPerQry)
            else:
                new_tweets = api.search(q="place:0073b76548e5984f", count=tweetsPerQry,
                                            since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q="place:0073b76548e5984f", count=tweetsPerQry,
                                            max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q="place:0073b76548e5984f", count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
        
        if not new_tweets:
            print "No more tweets found"
            time.sleep(240)

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

        print("Downloaded {0} tweets in Sydney".format(tweetCount))   

    except tweepy.TweepError as e:
            
        print "switching keys...syd"
        switch += 1
        if switch > 4:
            print "Limit reached"
            switch = 0
            time.sleep(180)

        continue
    except StopIteration:
        break
