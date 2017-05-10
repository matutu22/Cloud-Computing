import couchdb
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import json
import matplotlib.path as mplPath
import numpy as np
import requests
from textblob import TextBlob
import Queue
import time, socket, threading
import re
from pycorenlp import StanfordCoreNLP
from google.cloud import language
import random

with open ('polygon.json') as data_file:
    polygon=json.load(data_file)

#connect to couchdb
couch = couchdb.Server('http://127.0.0.1:5984')
data_db = couch['twitter_data_fin']


#connect to NLP
nlp = StanfordCoreNLP('http://localhost:9009')
print ' Connect to NLP server '
#make 5 queues for data
q1=Queue.Queue()
q2=Queue.Queue()
q3=Queue.Queue()
q4=Queue.Queue()
q5=Queue.Queue()

def dowork(q):
    while True:
        while not q.empty():
            print "Read from queue"
            try:
                queue_data = q.get()
                # Parse data
                try:
                    json_data = json.loads(queue_data)
                    print " Load data"
                except:
                    print " Fail load data"
                    continue
                text = json_data['text']
                _id = json_data['id']
                lang = json_data['lang']
                if lang!= "en":
                    print "Not english"
                    continue
                created_at = json_data['createdAt']
    
                encodetext=text.encode("ascii","ignore")
                plaintext = re.sub('http.*', '', encodetext) + '.'

                # Stanford NLP
                res = nlp.annotate(plaintext,
                    properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json',
                       'timeout': '1000' })      
                sentiment_value = 0
                tweets = ""
                count_tweet_sentence = 0
                sentiment_desc=""
    
                for s in res["sentences"]:
                    sentiment_value += int(s['sentimentValue'].encode('ascii'))
                    tweets += " ".join([t["word"] for t in s["tokens"]])
                    count_tweet_sentence = s["index"]
                if plaintext != '' and count_tweet_sentence == 0:
                    count_tweet_sentence = 1
                if count_tweet_sentence != 0:

                    average_sentiment_value= sentiment_value/count_tweet_sentence
                if sentiment_value/count_tweet_sentence == 0:
                    sentiment_desc = "Very negative"
                if sentiment_value/count_tweet_sentence ==1:
                    sentiment_desc = "Negative"
                if sentiment_value/count_tweet_sentence ==2:
                    sentiment_desc = "Neutral"
                if sentiment_value/count_tweet_sentence ==3:
                    sentiment_desc = "Positive"
                if sentiment_value/count_tweet_sentence ==4:
                    sentiment_desc = "Very positive"
                print "tweets: %s has sentiment value %d" % (tweets, sentiment_value/count_tweet_sentence)


                 # Textblob
                b=TextBlob(plaintext)
                polarity = b.sentiment[0]
                subjectivity = b.sentiment[1]
                print "Save textblob data"

                tweet_data = {'id':_id, 'text':plaintext,  'lang':lang, 'created_at':created_at, 
                   'sentiment_value':average_sentiment_value, 'sentiment':sentiment_desc,  'polarity':polarity, 'subjectivity':subjectivity}
                print tweet_data
                try:
                    data_db[str(_id)] = tweet_data
                    print ' Analyzed and saved one tweet to database'

                except:
                    print "Skip update duplicate"
            except Exception as e:
                print e
                continue

    print "None in queue"

def tcplink(sock, addr):
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome!')
    while True:
        data = sock.recv(100000)
        if data == 'exit' :
            break
        if data:
            x = random.randint(1,5)
            if x == 1:
                q1.put(data)
                print "Put to queue 1"
            if x == 2:
                q2.put(data) 
                print "Put to queue 2"       
            if x == 3:
                q3.put(data)
                print "Put to queue 3"

            if x == 4:
                q4.put(data)
                print "Put to queue 4"

            if x == 5:
                q5.put(data)
                print "Put to queue 5"
    print "Disconnected"

        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0',9998))
s.listen(15)

#start 5 analysis threads
a=threading.Thread(target=dowork,args=(q1,))
a.start()
print " Start process 1 analyzing message"
b=threading.Thread(target=dowork,args=(q2,))
b.start()
print " Start process 2 analyzing message"
c=threading.Thread(target=dowork,args=(q3,))
c.start()
print " Start process 3 analyzing message"
d=threading.Thread(target=dowork,args=(q4,))
d.start()
print " Start process 4 analyzing message"
e=threading.Thread(target=dowork,args=(q5,))
e.start()
print " Start process 5 analyzing message"

#keep listening for new connections
while True:
    sock, addr = s.accept()
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
