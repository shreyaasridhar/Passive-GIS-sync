import got, codecs
from pymongo import MongoClient
#import numpy
import pandas as pd
from datetime import datetime, timedelta

client = MongoClient('localhost', 27017)
db = client['twitter_db']
collection = db['curtweets']
now = datetime.now()
d = datetime.today() - timedelta(days=1)
tweetCriteria = got.manager.TweetCriteria().setSince(str(d)[:10]).setUntil(str(now)[:10]).setMaxTweets(6000).setQuerySearch('india flood OR earthquake OR rains OR landslide')
#tweetCriteria = got.manager.TweetCriteria().setSince("2017-08-27").setUntil("2017-08-30").setMaxTweets(6000).setQuerySearch('flood india OR earthquake OR rains OR landslide')
def streamTweets(tweets):
   for t in tweets:
      obj = {"user": t.username, "retweets": t.retweets, "favorites":
            t.favorites, "text":t.text,"geo": t.geo,"mentions":
            t.mentions, "hashtags": t.hashtags,"id": t.id,
            "permalink": t.permalink,}
      tweetind = collection.insert_one(obj).inserted_id
got.manager.TweetManager.getTweets(tweetCriteria, streamTweets)
