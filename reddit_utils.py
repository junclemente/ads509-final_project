import praw
import pandas as pd
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon (only once)
nltk.download('vader_lexicon', quiet=True)

# --------------------------------------------
# ✅ Reddit API Connection
# --------------------------------------------
def connect_reddit():
    """Connect to Reddit using praw.ini credentials."""
    import configparser
    import praw
    import os

    # Locate praw.ini one level up
    current_dir = os.path.dirname(os.path.abspath(__file__))
    praw_path = os.path.join(current_dir, "praw.ini")

    if not os.path.exists(praw_path):
        raise FileNotFoundError(f"❌ praw.ini not found at: {praw_path}")

    # Manually load config and feed credentials to PRAW
    config = configparser.ConfigParser()
    config.read(praw_path)
    creds = config["default"]

    reddit = praw.Reddit(
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        user_agent=creds["user_agent"]
    )

    return reddit



# --------------------------------------------
# ✅ Sentiment Analysis Helper
# --------------------------------------------
def analyze_sentiment(text):
    """Return compound sentiment score and label."""
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(text)["compound"]

    if score >= 0.05:
        label = "Positive"
    elif score <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    return score, label


# --------------------------------------------
# ✅ Fetch Reddit Posts for a District
# --------------------------------------------
def fetch_reddit_posts(district_name, terms, limit=50):
    """Fetch Reddit posts and perform sentiment analysis."""
    reddit = connect_reddit()
    subreddit = reddit.subreddit("education")  # You can customize this

    query = f'{district_name} ({ " OR ".join(terms) })'
    posts = []

    for submission in subreddit.search(query, limit=limit):
        sentiment_score, sentiment_label = analyze_sentiment(submission.title)
        posts.append({
            "source": "reddit",
            "district": district_name,
            "query": query,
            "title": submission.title,
            "score": submission.score,
            "url": submission.url,
            "comments": submission.num_comments,
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label
        })

    df = pd.DataFrame(posts)

    if not df.empty:
        df["sentiment_score"] = df["sentiment_score"].astype(float)

    return df


