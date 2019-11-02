import json
import pandas as pd
import matplotlib.pyplot as plt

tweets_data_path = 'sample.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        if "created_at" in tweet.keys():
            tweets_data.append(tweet)
    except:
        continue


print(len(tweets_data))
tweets = pd.DataFrame()

tweets_text = [i["text"] for i in tweets_data]
tweets_lang = [i["lang"] for i in tweets_data]
tweets_country = [i["place"] if i['place'] != None else None for i in tweets_data]

tweets['text'] = tweets_text
tweets['lang'] = tweets_lang
tweets['country'] = tweets_country

tweets_by_lang = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')
plt.show()

print(tweets)