import os
import random
import textwrap
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import tweepy

# --- Step 1: Connect to Twitter using your secret keys ---
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)

# --- Step 2: Get a random motivational quote ---
def get_quote():
    try:
        response = requests.get("https://api.quotable.io/random")
        data = response.json()
        return f"“{data['content']}”\n— {data['author']}"
    except:
        # backup quotes if the website doesn’t work
        backup_quotes = [
            "Believe in yourself.",
            "Every day is a new beginning.",
            "Stay positive, work hard, make it happen.",
            "Dream big and dare to fail.",
            "Be the reason someone smiles today."
        ]
        return random.choice(backup_quotes)

# --- Step 3: Get a random background image from Unsplash ---
def get_background():
    topics = ["nature", "sky", "mountains", "forest", "sunset", "inspiration"]
    topic = random.choice(topics)
    url = f"https://source.unsplash.com/800x400/?{topic}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # check for bad response
        img = Image.open(BytesIO(response.content)).convert("RGB")
        return img
    except Exception as e:
        print(f"⚠️ Could not load background image: {e}")
        # Fallback: create a simple solid background
        img = Image.new("RGB", (800, 400), color=(40, 40, 40))
        return img

# --- Step 4: Create the final image with the quote ---
def create_quote_image(quote):
    img = get_background().filter(ImageFilter.GaussianBlur(2))
    draw = ImageDraw.Draw(img)

    # Load a simple, readable font
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = ImageFont.truetype(font_path, 28)

    # Wrap text neatly
    wrapped_text = textwrap.fill(quote, width=40)

    # ✅ FIXED text size calculation
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (img.width - text_w) / 2
    y = (img.height - text_h) / 2

    # Add dark overlay for readability
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 120))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)

    # Draw text with shadow
    shadow_color = "black"
    text_color = "white"
    for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
        draw.text((x + offset[0], y + offset[1]), wrapped_text, font=font, fill=shadow_color)
    draw.text((x, y), wrapped_text, font=font, fill=text_color)

    img.convert("RGB").save("quote.jpg")

def post_quote():
    quote = get_quote()
    create_quote_image(quote)
    hashtags = "#Motivation #Inspiration #QuoteOfTheDay"
    api.update_status_with_media(status=hashtags, filename="quote.jpg")
    print("✅ Successfully posted a beautiful quote image!")

if __name__ == "__main__":
    post_quote()
