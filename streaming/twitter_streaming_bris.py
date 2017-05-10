from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import couchdb
import json
import jsonpickle
import sys,os

consumer_key="KuzAGiFtOlmYSbPVr1rBHgHL6"
consumer_secret="BHX5PJvjm1tx318ovvs65gAWeZoZARXwV9BZn2OAJwq4UPeo64"
access_token="839300214410207232-SJlWiB6lgyqF3kvyAoHdPvfa7dCPLpf"
access_token_secret="mX2lJ9lSViNvMw7ydSaLYZT9jT8YtfIxhW5j5cbQAF4Yj"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))

print "Connect to socket"
print s.recv(1024)

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        tweet = json.loads(data)
        #pprint (tweet)
        _id = tweet['id']
        text = str(tweet['text'].encode('ascii','ignore'))
        print text
        lang = str(tweet['lang'].encode('ascii'))
        created_at = str(tweet['created_at'].encode('ascii'))
        coordinates = "null"
        if tweet['coordinates'] != None:
            coordinates = tweet['coordinates']['coordinates']
        else:
            print "No coordinate"
        place = str(tweet['place']['full_name'].encode('ascii'))
        is_finance = 'false'

        send_data = {'id':_id, 'text':text, 'lang':lang, 'created_at':created_at, 'coordinates':coordinates, 'place':place, 'is_finance':is_finance}
        send_date_string = json.dumps(send_data)
        print "send data"

        s.send(send_date_string)
        print " Send data success"

    def on_status(self, status):
        print (status.next)
    def on_error(self, status):
        print (status)
    def on_timeout(self):
        print('Timeout...')
        return True   
if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    l = StdOutListener()
    stream = Stream(auth, l)
    stream.filter(locations=[152.7,-27.69,153.3,-27.06],async=True)
