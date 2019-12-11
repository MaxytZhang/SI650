from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import api_key

consumer_key = api_key.CONSUMER_KEY
consumer_secret = api_key.CONSUMER_SECRET
access_token = api_key.ACCESS_KEY
access_secret = api_key.ACCESS_SECRET

class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
stream = Stream(auth, l)

stream.filter(track=['Andrew Yang'], languages=["en"], is_async=True)
