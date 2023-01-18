import requests
import random
import pandas as pd 
from sqlalchemy import create_engine
import time
import logging

time.sleep(45)

webhook_url = "https://hooks.slack.com/services/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"

pg = create_engine('postgresql://postgres:1234@pg_container:5432')

while True:
    df = pd.read_sql_query("SELECT * FROM tweets", pg)
    n = random.randint(0,len(df)-1)
    tweet_text = df['text'][n]
    tweet_sent = df['sentiment'][n]
    data = {'text': "Neuer Tweet: {} - Sentiment: {}".format(tweet_text,tweet_sent)}
    requests.post(url=webhook_url, json = data)
    logging.critical("New tweet sent to slack!")
    time.sleep(30)