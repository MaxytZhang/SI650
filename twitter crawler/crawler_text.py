from requests_oauthlib import OAuth1
import sys
import requests
import api_key
import json

consumer_key = api_key.CONSUMER_KEY
consumer_secret = api_key.CONSUMER_SECRET
access_token = api_key.ACCESS_KEY
access_secret = api_key.ACCESS_SECRET

url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)



'''
q: query

result_type: what type of search results you would prefer to receive
            mixed(default): Include both popular and real time results in the response
            recent: return only the most recent results in the response
            popular: return only the most popular results in the response

count: The number of tweets to return per page, up to a maximum of 100
       15(default)

 

'''

base_url = "https://api.twitter.com/1.1/search/tweets.json"
pd = {
    "q": "Andrew Yang",
    "result_type": "mixed",
    "count": 1
}

r = requests.get(base_url, pd, auth=auth)

r_body = r.json()

twitter_str = json.dumps(r_body, indent=2)
print(twitter_str)