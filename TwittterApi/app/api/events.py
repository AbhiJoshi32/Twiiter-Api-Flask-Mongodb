from __future__ import absolute_import
from flask import jsonify
from TwittterApi.app.api.twitter_api import TwitterApiImpl
from TwittterApi.app import socketio
from TwittterApi.app.api import tweet_db

twitter_api_impl = TwitterApiImpl()
from datetime import datetime
col = 'tweets'

class TweetListener(twitter_api_impl.stream_listener):
    def on_status(self, status):
        socketio.emit('streamTweet',status._json)
        metadata = status._json
        metadata['created_at'] = datetime.strptime(metadata['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        doc = {'metadata' : status._json,'text' : status.text}
        db.insertDoc(doc,col)
        return True
 
    def on_error(self, status_code):
        print('error')
        if status_code == 420:
            return False
 
    def on_timeout(self):
        print('timeout')
        socketio.emit('connect','disconnected')
        return False

tweet_listener = TweetListener()
twitter_stream = twitter_api_impl.createTwitterStream(tweet_listener)

@socketio.on('streamTweet')
def streamTweet(json):
    socketio.emit('connect','connected')
    action = json["action"]
    if (action == 'start stream'):
        keywords = json["keywords"]
        twitter_stream.disconnect()
        print('starting stream')
        twitter_stream.filter(track = keywords,async = True)
    else:
        twitter_stream.disconnect()
        socketio.emit('connect','disconnected')