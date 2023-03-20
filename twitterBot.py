import tweepy
import time
from decouple import config

CONSUMER_KEY = config('CONSUMER_KEY')
CONSUMER_SECRET = config('CONSUMER_SECRET')
ACCESS_TOKEN = config('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = config('BEARER_TOKEN')

# ID of @devopswithkunal account
BOT_ID = 1460548132870111233
# Time between retweeting a tweet again. Set to 120 in accordance with the twitter api requests limits
SLEEP_TIME = 120

# Twitter authentication
# auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

client = tweepy.Client(
    BEARER_TOKEN,
    CONSUMER_KEY, CONSUMER_SECRET,
    ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

try:
    client.get_user(id=BOT_ID)
    print('🟢Authentication OK')
except:
    print('🔴Error in authentication')


def retweeted(tweet):
    if tweet.author_id == BOT_ID:
        try:
            if tweet.referenced_tweet.type == "retweet" and tweet.referenced_tweet.id == tweet.id:
                return True
        except:
            return False
    return False

class StreamListener(tweepy.StreamingClient):

    def on_connect(self):
        print('Connected to stream. Listening to tweets')

    def on_tweet(self, tweet):
        print(f" Tweet by @{tweet.author_id}")
        # Check if the tweet's author is not us and if the tweet is not a reply and Check if tweet is not already retweeted.
        if tweet.in_reply_to_user_id is None and int(tweet.author_id) != int(BOT_ID) and not retweeted(tweet):
            blocked_ids = client.get_blocked()
            # Check if the tweet author is not blocked by us
            if str(tweet.author_id) not in blocked_ids:
                # If a blocked tweet was retweeted by someone else who is not blocked, then check the original tweet's ID
                try:                    
                    print('Attempting retweet ........ 🟡')
                    client.retweet(tweet.id)
                    print('Tweet succesfully retweeted ✅')
                    time.sleep(int(SLEEP_TIME))
                except Exception as err:
                    print(err)
            else:
                print('🛑Blocked tweet by: ', tweet.author_id)
                time.sleep(int(SLEEP_TIME))

    def on_error(self, status):
        print(f"🔴 Error while retweeting: {status}")

    def on_closed(self, response):
        print(f'🔴 Stream closed! {response}')


stream = StreamListener(
    BEARER_TOKEN,
    wait_on_rate_limit=True
)

# Look for tweets with the below mentioned words/tags only
stream.add_rules(add=tweepy.StreamRule(value="#DevOpsWithKunal OR #devopswithkunal OR #DevOpswithKunal OR #DevOpswithkunal OR \
#devopsWithKunal OR #Devopswithkunal"))

stream.filter(tweet_fields=["created_at", "in_reply_to_user_id", "author_id", "referenced_tweets"])
