
import time
import logging
import pymongo
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine

#If you run it for the first time, the Postgres DB may lag behind,
#in which case half of the pipeline fails. Stop and Start everything again.
#this might help:
time.sleep(10) 


client = pymongo.MongoClient("mongodb://mongo_container:27017/")
db = client.tweets

pg = create_engine('postgresql://postgres:1234@pg_container:5432')
pg.execute('''CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(1000),
    sentiment NUMERIC
);
''')

def read_tweet_from_mongo():
    """gets a random tweet"""
    tweets = list(db.collections.data_science.find())
    if tweets:
        t = random.choice(tweets)
        logging.critical("random tweet: " + t['text'])
        return t

def calc_sentiment(tweet):
    s  = SentimentIntensityAnalyzer()
    sentiment = s.polarity_scores(tweet['text'])
    logging.critical("sentiment: " + str(sentiment))
    return sentiment['compound']


def write_tweet_to_postgres(tweet, sentiment):
    pg.execute(f"""INSERT INTO tweets VALUES ('{tweet["text"]}', {sentiment});""")
    logging.critical("tweet + sentiment written to pg")


logging.critical("Hello from the ETL job")

while True:
    tweet = read_tweet_from_mongo()
    if tweet:
        sent = calc_sentiment(tweet)
        write_tweet_to_postgres(tweet, sent)
    time.sleep(10)
