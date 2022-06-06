import tweepy
import time
from decouple import config

CONSUMER_KEY = config('CONSUMER_KEY')
CONSUMER_SECRET = config('CONSUMER_SECRET')
ACCESS_TOKEN = config('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')

# ID of @devopswithkunal account
BOT_ID = 1460548132870111233
# Time between retweeting a tweet again. Set to 120 in accordance with the twitter api requests limits
SLEEP_TIME = 120

# Twitter authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print('🟢Authentication OK')
except:
    print('🔴Error in authentication')


class StreamListener(tweepy.Stream):

    def on_status(self, tweet):
        print(f" Tweet by @{tweet.author.screen_name}")
        # Check if the tweet's author is not us and if the tweet is not a reply and if tweet is not already retweeted
        if tweet.in_reply_to_status_id is None and int(tweet.author.id) != int(BOT_ID) and not tweet.retweeted:
            # Check if the tweet author is not blocked by us
            if str(tweet.author.id) not in api.get_blocked_ids(stringify_ids = True):
                try:                    
                    print('Attempting retweet ........ 🟡')
                    api.retweet(tweet.id)
                    print('Tweet succesfully retweeted ✅')
                    time.sleep(int(SLEEP_TIME))
                except Exception as err:
                    print(err)
            else:
                time.sleep(int(SLEEP_TIME))

    def on_error(self, status):
        print(f"🔴 Error while retweeting: {status}")


stream = StreamListener(
  CONSUMER_KEY, CONSUMER_SECRET,
  ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
# Look for tweets with the below mentioned words/tags only
stream.filter(track=['#DevOpsWithKunal', "#devopswithkunal", "DevOpswithKunal", "#DevOpswithkunal", "#devopsWithKunal", "#Devopswithkunal"])