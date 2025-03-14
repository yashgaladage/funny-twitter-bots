import tweepy
import openai
import os
import random
from dotenv import load_dotenv

# Load API keys
load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Authenticate Twitter API
auth = tweepy.OAuth1UserHandler(TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)

# Humor styles
HUMOR_STYLES = ["sarcastic", "pun-based", "dark humor", "meme-style"]

# Function to fetch viral tweets
def fetch_viral_tweets():
    tweets = api.search_tweets(q="trending", result_type="popular", lang="en", count=5)
    return tweets

# Function to generate funny replies using OpenAI
def generate_funny_reply(tweet_text):
    openai.api_key = OPENAI_API_KEY
    humor_type = random.choice(HUMOR_STYLES)
    
    prompt = f"Make a {humor_type} reply to this viral tweet:\n'{tweet_text}'\nReply with creativity."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=0.9
    )
    
    return response["choices"][0]["message"]["content"].strip()

# Function to post reply
def reply_to_tweets():
    viral_tweets = fetch_viral_tweets()
    
    for tweet in viral_tweets:
        tweet_text = tweet.text
        tweet_id = tweet.id
        funny_reply = generate_funny_reply(tweet_text)
        
        # Post reply
        api.update_status(status=f"@{tweet.user.screen_name} {funny_reply}", in_reply_to_status_id=tweet_id)
        print(f"Replied to: {tweet_text}\nWith: {funny_reply}\n")

# Run the bot
if __name__ == "__main__":
    reply_to_tweets()
