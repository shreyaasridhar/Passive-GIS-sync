from pymongo import MongoClient
from nltk import FreqDist
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import re, string
import nltk
import pandas as pd
client = MongoClient('127.0.0.1', 27017)#('localhost', 27017)
db = client['twitter_db']
collection = db['curtweets']
#print collection.count()
df=pd.DataFrame(list(collection.find()))
hashtags = []
tweets_texts = df["text"].tolist()
stopwords=stopwords.words('english')
english_vocab = set(w.lower() for w in nltk.corpus.words.words())
def process_tweet_text(tweet):
   if tweet.startswith('@null'):
       return "[Tweet not available]"
   tweet = re.sub(r'\$\w*','',tweet) # RE to remove tickers
   tweet = re.sub(r'https?:\/\/.*\/\w*','',tweet) # RE to remove hyperlinks
   tweet = re.sub(r'['+string.punctuation+']+', ' ',tweet) # RE to remove puncutations like 's
   twtok = TweetTokenizer(strip_handles=True, reduce_len=True)
   tokens = twtok.tokenize(tweet)
   tokens = [i.lower() for i in tokens if i not in stopwords and len(i) > 2] #and i in english_vocab]
   return tokens
words = []
for tw in tweets_texts:
    words += process_tweet_text(tw)
disaster=[]
dis= tuple(open("disaster.txt", 'r'))
for i in dis:
    ct=len(i)
    x=i[:ct-1]
    x=x.lower()
    x=re.sub("\s","",x)
    disaster.append(x)
print disaster
disasters=[]
for i in words:
    #print i
    if i in disaster:
        disasters.append(i)
print disasters
fdist2 = FreqDist(disasters)
fdist2.plot(10)
