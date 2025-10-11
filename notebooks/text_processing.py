"""Text Processing for Reddit Comments Analysis
====================================================

This module provides reusable functions for cleaning, analyzing,
and extracting insights from Reddit comment data.

Author: ADS 509 Team"""

import re
import string
from collections import Counter

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download("stopwords")


# =============================================================================
# CLEANING PIPELINE FUNCTIONS
# =============================================================================
def clean_text(text, remove_stopwords=True, lowercase=True):
    """
    Clean a single comment by removing noise and formatting.

    Args:
        text: The comment text to clean
        remove_stopwords: Remove common words
        lowercase: Convert everything to lowercase

    Returns:
        Cleaned text as a string

    """
    if not isinstance(text, str):
        return ""

    # Lowercase
    if lowercase:
        text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove mentions and hashtags
    text = re.sub(r"@\w+|#\w+", "", text)

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove extra whitespace
    text = " ".join(text.split())

    # Remove stopwords
    if remove_stopwords:
        stop_words = set(stopwords.words("english"))
        words = text.split()
        text = " ".join([w for w in words if w not in stop_words])

    return text


def clean_corpus(comments, remove_stopwords=True, lowercase=True):
    """
    Clean a list of comments.

     Args:
         comments: List of comment texts
         remove_stopwords: Remove common words like 'the', 'is', 'and'
         lowercase: Convert everything to lowercase

     Returns:
         List of cleaned comments
    """
    return [clean_text(c, remove_stopwords, lowercase) for c in comments]


def clean_dataframe_column(
    df,
    column="comments_flat",
    new_column="cleaned_comments",
    remove_stopwords=True,
    lowercase=True,
):
    """
    Clean comments in a DataFrame column.

    Args:
        df: DataFrame containing Reddit posts
        column: Column name with comments (default: 'comments_flat')
        new_column: Name for the new cleaned column (default: 'cleaned_comments')
        remove_stopwords: Remove common words
        lowercase: Convert everything to lowercase

    Returns:
        DataFrame with a new cleaned comments column

    """
    df = df.copy()
    df[new_column] = df[column].apply(
        lambda comments: clean_corpus(comments, remove_stopwords, lowercase)
    )
    return df


# =============================================================================
# EDA FUNCTIONS
# =============================================================================


def get_word_counts(comments, top_n=20):
    """
    Get most common words from a list of comments.

    Args:
    ----------
    comments : list of str
        List of comment texts
    top_n : int, default=20
        Number of top words to return

    Returns:
    -------
    pandas.DataFrame
        DataFrame with columns: word, count

    """
    # Combine all comments into one string
    all_text = " ".join(comments)
    words = all_text.split()

    # Count words
    word_freq = Counter(words)

    # Convert to DataFrame
    df = pd.DataFrame(word_freq.most_common(top_n), columns=["word", "count"])
    return df


def get_bigram_counts(comments, top_n=20):
    """
    Get the most common two-word phrases.

    Args:
        comments: List of cleaned comments
        top_n: How many top phrases to return (default: 20)

    Returns:
        DataFrame with columns: bigram, count
    """
    bigram_list = []

    for comment in comments:
        words = comment.split()
        # Create bigrams
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]
        bigram_list.extend(bigrams)

    # Count bigrams
    bigram_freq = Counter(bigram_list)

    # Convert to DataFrame
    df = pd.DataFrame(bigram_freq.most_common(top_n), columns=["bigram", "count"])
    return df


def get_comment_lengths(comments):
    """
    Count the number of words in each comment.

    Args:
        comments: List of comment texts

    Returns:
        List of word counts (one number per comment)
    """
    return [len(comment.split()) for comment in comments]


def get_post_statistics(df, comments_col="cleaned_comments"):
    """
    Add statistics columns for each post's comments.

    Args:
        df: DataFrame with your posts
        comments_col: Column with cleaned comments (default: 'cleaned_comments')

    Returns:
        DataFrame with new columns: avg_comment_length, total_tokens, unique_words
    """
    df = df.copy()

    # Calculate statistics for each post
    df["avg_comment_length"] = df[comments_col].apply(
        lambda comments: np.mean(get_comment_lengths(comments)) if comments else 0
    )

    df["total_tokens"] = df[comments_col].apply(
        lambda comments: sum(get_comment_lengths(comments))
    )

    df["unique_words"] = df[comments_col].apply(
        lambda comments: len(set(" ".join(comments).split()))
    )

    return df


# =============================================================================
# UTILITIES
# =============================================================================


def save_pickle_file(dataframe, filename, dataset_folder):
    # Handle datset_folder
    if not dataset_folder:
        dataset_folder = Path.cwd()
    else:
        dataset_folder = Path(dataset_folder)

    # remove spaces in filename
    filename = filename.replace(" ", "_")

    # ensure folder exists
    dataset_folder.mkdir(parents=True, exist_ok=True)

    # create timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # full path
    full_path = dataset_folder / f"{filename}_{timestamp}_reddit.pkl"

    dataframe.to_pickle(full_path)
    print(f"Saved as {filename}. ")

    return full_path
