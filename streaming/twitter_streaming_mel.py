from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import couchdb
import json
import jsonpickle
import sys,os
import socket
from pprint import pprint

consumer_key="TcHoempgSuQkcbeIcBQPzLMqi"
consumer_secret="VqNr0PugcJqHhwR8cHcI7ocRVDTcA5UAQGGpEoWHZJsIrY9Xuz"
access_token="839300214410207232-Jia98vmQtOIQaHhDDNCiJxtoJ9m35Hc"
access_token_secret="qCGLAhGLqO58bkSOxymqP7v2fI6ISbBqlK2r39Emy2QhD"

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
    stream.filter(locations=[144,-38.03,146,-37] ,async=True)
