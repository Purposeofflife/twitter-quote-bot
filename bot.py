import os
import requests
import tweepy
from dotenv import load_dotenv

# Load environment variables (GitHub Secrets)
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate with Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def get_quote():
    try:
        response = requests.get("https://api.quotable.io/random", timeout=10)
        data = response.json()
        return f"{data['content']} — {data['author']}"
    except Exception as e:
        return "Keep going, the best is yet to come! — Unknown"

def post_quote():
    quote = get_quote()
    try:
        api.update_status(quote)
        print("Tweet posted successfully!")
    except Exception as e:
        print("Error posting tweet:", e)

if __name__ == "__main__":
    post_quote()
