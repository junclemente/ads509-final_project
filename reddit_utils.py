import configparser
import os
from pathlib import Path

import nltk
import pandas as pd
import praw
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download VADER lexicon (only once)
nltk.download("vader_lexicon", quiet=True)


# --------------------------------------------
# ✅ Reddit API Connection
# --------------------------------------------
# def connect_local_reddit():
#     """Connect to Reddit using praw.ini credentials."""
#     import configparser
#     import os

#     import praw

#     # Locate praw.ini one level up
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     praw_path = os.path.join(current_dir, "praw.ini")

#     if not os.path.exists(praw_path):
#         raise FileNotFoundError(f"❌ praw.ini not found at: {praw_path}")

#     # Manually load config and feed credentials to PRAW
#     config = configparser.ConfigParser()
#     config.read(praw_path)
#     creds = config["default"]

#     reddit = praw.Reddit(
#         client_id=creds["client_id"],
#         client_secret=creds["client_secret"],
#         user_agent=creds["user_agent"],
#     )

#     return reddit


def _build_reddit(client_id: str, client_secret: str, user_agent: str) -> praw.Reddit:
    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )


def connect_reddit() -> praw.Reddit:
    """
    Create a Reddit client with the following precedence:
      1) Streamlit secrets: st.secrets['praw'] = { client_id, client_secret, user_agent }
      2) Local praw.ini (searched in CWD and alongside this file)
      3) Environment variables: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

    Returns
    -------
    praw.Reddit

    Raises
    ------
    RuntimeError
        If no valid credentials can be found.
    """
    # ---- 1) Streamlit secrets (Streamlit Cloud / local Streamlit)
    try:
        import streamlit as st  # imported lazily so non-Streamlit runs don't need it

        if hasattr(st, "secrets") and "praw" in st.secrets:
            s = st.secrets["praw"]
            for k in ("client_id", "client_secret", "user_agent"):
                if k not in s or not s[k]:
                    raise RuntimeError(f"Streamlit secrets 'praw' is missing '{k}'.")
            return _build_reddit(s["client_id"], s["client_secret"], s["user_agent"])
    except Exception:
        # swallow import/lookup issues and fall through to next method
        pass

    # ---- 2) Local praw.ini (INI format)
    # Search a few sensible spots: CWD, file's dir, and parent of file's dir
    # connect_local_reddit()
    candidate_dirs = [
        Path.cwd(),
        Path(__file__).resolve().parent,
        Path(__file__).resolve().parent.parent,
    ]
    for d in candidate_dirs:
        ini_path = d / "praw.ini"
        if ini_path.exists():
            cfg = configparser.ConfigParser()
            cfg.read(ini_path)
            section = (
                "default"
                if "default" in cfg
                else (cfg.sections()[0] if cfg.sections() else None)
            )
            if not section:
                raise RuntimeError(f"Found {ini_path} but it has no sections.")
            creds = cfg[section]
            for k in ("client_id", "client_secret", "user_agent"):
                if k not in creds or not creds[k]:
                    raise RuntimeError(
                        f"{ini_path} section [{section}] is missing '{k}'."
                    )
            return _build_reddit(
                creds["client_id"], creds["client_secret"], creds["user_agent"]
            )

    # ---- 3) Environment variables
    cid = os.getenv("REDDIT_CLIENT_ID")
    csec = os.getenv("REDDIT_CLIENT_SECRET")
    ua = os.getenv("REDDIT_USER_AGENT")
    if cid and csec and ua:
        return _build_reddit(cid, csec, ua)

    # ---- No creds found
    raise RuntimeError(
        "No Reddit credentials found. Provide one of:\n"
        "  • Streamlit secrets:\n"
        "      [praw]\n"
        '      client_id = "..." \n'
        '      client_secret = "..." \n'
        '      user_agent = "app/0.1 by u/yourname"\n'
        "  • A local praw.ini with [default] section\n"
        "  • Environment vars: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT"
    )


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
        posts.append(
            {
                "source": "reddit",
                "district": district_name,
                "query": query,
                "title": submission.title,
                "score": submission.score,
                "url": submission.url,
                "comments": submission.num_comments,
                "sentiment_score": sentiment_score,
                "sentiment_label": sentiment_label,
            }
        )

    df = pd.DataFrame(posts)

    if not df.empty:
        df["sentiment_score"] = df["sentiment_score"].astype(float)

    return df
    return df
