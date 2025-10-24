import os
import random
import requests
import tweepy

# connect to Twitter v2
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
)

def get_quote():
    r = requests.get("https://api.quotable.io/random")
    data = r.json()
    return f"“{data['content']}”\n— {data['author']}"

def post_text_quote():
    quote = get_quote()
    hashtags = "#Motivation #Inspiration #QuoteOfTheDay"
    tweet = f"{quote}\n\n{hashtags}"
    client.create_tweet(text=tweet)
    print("✅ Posted text quote successfully!")

if __name__ == "__main__":
    post_text_quote()
