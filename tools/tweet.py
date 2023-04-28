import tweepy
from dotenv import load_dotenv
import os


def tweet(message, reply_to=0):
    """Function to post a tweet
    Args: 
        message: String that is needed to be tweeted. Message must be 280 characters max
    Returns: -
    """
    
    # Load the environment variables from .env file
    load_dotenv()

    # Retrieve the Twitter API keys and access tokens from environment variables
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    bearer_token = os.getenv("TWITTER_BEARER")

    # Authenticate with the Twitter API
    api = tweepy.Client(bearer_token=bearer_token,
                        access_token=access_token,
                        access_token_secret=access_token_secret,
                        consumer_key=consumer_key,
                        consumer_secret=consumer_secret)

    # Post the tweet
    if reply_to==0:
        tweet = api.create_tweet(text=message)
    else:
        tweet = api.create_tweet(text=message, in_reply_to_tweet_id=reply_to)
    
    print("Tweeted: ", message)
    
    return tweet.data['id']

def check_messages(messages):
    """Check the lenght of every messages to be tweeted
    Args:
        messages: List of strings with every message to be tweeted
    Returns:
        Boolean. 
        False if all the messages length are less than 280 characters or not empty.
        True if not.
    """
    for message in messages:
        if len(message) > 280 or len(message)==0:
            return True
    
    return False