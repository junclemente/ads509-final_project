import praw

# Load Reddit instance using your praw.ini file
reddit = praw.Reddit("default")

# Print connection info
print("Authenticated as:", reddit.user.me())

# Quick test: check a subreddit
subreddit = reddit.subreddit("education")
print("Subreddit title:", subreddit.title)
print("Description (first 200 chars):", subreddit.public_description[:200])