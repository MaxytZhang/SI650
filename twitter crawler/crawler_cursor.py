import tweepy as tw
import pandas as pd
import api_key

consumer_key = api_key.CONSUMER_KEY
consumer_secret = api_key.CONSUMER_SECRET
access_token = api_key.ACCESS_KEY
access_secret = api_key.ACCESS_SECRET

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_words = "Andrew+Yang"
date_since = "2019-10-15"
tweets = tw.Cursor(api.search, q=f"{search_words}-filter:retweets", lang="en", since=date_since).items(10000)

df = pd.DataFrame()
df["text"] = [t.text for t in tweets]
df.to_csv("yang10000.csv", index = False)
print(df)