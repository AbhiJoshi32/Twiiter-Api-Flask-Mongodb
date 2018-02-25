from __future__ import absolute_import

from TwittterApi.app.api.twitter_api import TwitterApiImpl
from flask.json import dumps, request
from TwittterApi.app.api import api
from TwittterApi.app.api import tweet_db
from datetime import datetime

twitter_api_impl = TwitterApiImpl()
twitter_api = twitter_api_impl.twitter_api

col = 'tweets'


@api.route('/trending/places', methods=['GET'])
def get_trending_places():
    return jsonify({'result':twitter_api.trends_available()})

@api.route('/trending/<int:place_id>', methods=['GET'])
def get_trending(place_id):
    return jsonify({'result':twitter_api.trends_place(place_id)})

@api.route('/search/<string:keywords>', methods=['GET'] )
def search_keywords(keywords):
    return jsonify({'result':twitter_api.search(keywords)})

@api.route('/filter', methods=['POST'])
def filter_tweets(): 
    print(request.json)
    query = {}
    res = []
    for key in request.json:
        if (key == 'name'):    
            query['metadata.user.name'] = {}
            query['metadata.user.name'] = request.json['name']
        if (key == 'screen_name'):
            query['metadata.user.screen_name'] = {}
            query['metadata.user.screen_name'] = request.json['screen_name']
        if (key == 'date_low'):
            query['metadata.created_at'] = {}
            query['metadata.created_at']['$gt'] = datetime.strptime(request.json['date_low'], "%d/%m/%y %H:%M")
        if (key == 'date_high'):
            query['metadata']['created_at'] = {}
            query['metadata']['created_at']['$lt'] = datetime.strptime(request.json['date_low'], "%d/%m/%y %H:%M")
        print(query)
        for doc in tweet_db.findDocs(query,col):
            res.append(doc)
    return dumps({'result':res})

    
