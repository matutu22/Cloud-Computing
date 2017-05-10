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
language_client = language.Client()

couch = couchdb.Server('http://127.0.0.1:5984')
data_db = couch['twitter_data']
result_db = couch['suburb_data']
count = 0
num = 0
fitness=['fitness','gym','workout', 'push up', 'deadlift','bench press', 'squat','crunch','diets','weight loss','body building','yoga']
sports=['football','basketball','soccer','cricket','baseball','tennis','rugby','golf','badminton','table tennis']
outdoor=['outdoor', 'camping','trekking','swimming','surfing','running','cycling','climbing','hiking','fishing']
keywords={'fitness':fitness,'sports':sports,'outdoor':outdoor}

nlp = StanfordCoreNLP('http://localhost:9000')
print ' Connect to NLP server '
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

                try:
                    json_data = json.loads(queue_data)
                    print " Load data"
                except:
                    print " Fail load data"
                    continue
                postcode = 0
                text = json_data['text']
                coordinates = json_data['coordinates']
                print coordinates
                _id = json_data['id']
                lang = json_data['lang']
                if lang!= "en":
                    print "Not english"
                    continue
                place = json_data['place']
                is_finance = json_data['is_finance']
                created_at = json_data['created_at']
    
                encodetext=text.encode("ascii","ignore")
                plaintext = re.sub('http.*', '', encodetext) + '.'

                # Get postcode
                if coordinates!= 'null':
                    for a in polygon['features']:
                        bbPath = mplPath.Path(np.array(a['geometry']['coordinates'][0][0]))
            #print ("%s in %s" %(bbPath.contains_point(coordinates),a['properties']['postcode']))

                
                        if bbPath.contains_point(coordinates):
                            print "Contains point"
                            postcode = str(a['properties']['postcode'].encode('ascii'))
                            print ("%s in %s" %(bbPath.contains_point(coordinates),a['properties']['postcode']))
                            break
                    
                    for k in keywords:
                        for b in keywords.get(k):
                            if b in text.lower():             
                                for suburbs in result_db:
                                    doc = result_db.get(suburbs)
                                    if postcode == doc['postcode']:
                                        doc[k] += 1
                                        result_db.save(doc)
                                        searched_for_brunch = 'true'

                                        print " Found one %s result in %s" %(k, postcode)
                                        break
                            else:
                                searched_for_brunch = 'false'
                                       
                print "Finish postcode and keywords"


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

                google_score=0
                magnitude = 0
    
            # Google nature language API
            
                document = language_client.document_from_text(plaintext)
                sentiment = document.analyze_sentiment().sentiment
                google_score = sentiment.score
                magnitude = sentiment.magnitude
                print "%s has google score of %s" % (plaintext, str(google_score))
            

             # Textblob
                b=TextBlob(plaintext)
                polarity = b.sentiment[0]
                subjectivity = b.sentiment[1]
                print "Save textblob data"

                tweet_data = {'id':_id, 'text':plaintext, 'coordinates':coordinates, 'postcode':postcode, 'lang':lang,'city':place, 'is_finance':is_finance, 'created_at':created_at, 
                  'searched_for_brunch':searched_for_brunch, 'sentiment_value':average_sentiment_value, 'sentiment':sentiment_desc, 'sentiment_score_google':google_score, 
                  'magnitude':magnitude, 'polarity':polarity, 'subjectivity':subjectivity}
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
s.bind(('0.0.0.0',9999))
s.listen(15)

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

while True:
    sock, addr = s.accept()
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
