import pandas as pd
import streamlit as st


# -----------------------------
# Load Data (placeholder until scraping is complete)
# -----------------------------
@st.cache_data
def load_demo_data():
    data = {
        "school": ["Henry M. Gunn HS", "Palo Alto HS", "Hope Tech (Private)",
                   "Boulevard Academy", "Memorial HS"],
        "city": ["Palo Alto, CA", "Palo Alto, CA", "Palo Alto, CA",
                 "Oklahoma City, OK", "Oklahoma City, OK"],
        "source": ["Yelp", "Twitter", "Reddit", "Yelp", "Twitter"],
        "review_text": [
            "The teachers are amazing and offer lots of support.",
            "Great academics but a bit competitive.",
            "Strong extracurriculars and technology programs.",
            "The school lacks resources and feels unsafe.",
            "Administration doesn’t listen to parents."
        ],
        "rating": [5, 4, 5, 2, 1]
    }
    return pd.DataFrame(data)

df = load_demo_data()

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("📚 ADS-509 School Reviews App")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📝 Classifier", "🔍 Topics", "📊 Data Explorer", "🔎 Query Builder", "🏫 District Comparison", "ℹ️ About"]
)

# -----------------------------
# Home Page
# -----------------------------
if page == "🏠 Home":
    st.title("School Reviews Analysis")
    st.subheader("Comparing High vs Low Performing Districts")
    st.write("""
    This app explores how parent and student reviews differ between
    **high-performing schools in Palo Alto, CA** and
    **low-performing schools in Oklahoma City, OK**.

    Features:
    - Sentiment Classification
    - Topic Modeling
    - Descriptive Statistics
    - Query Builder for Reddit data
    """)

# -----------------------------
# Classifier Page
# -----------------------------
elif page == "📝 Classifier":
    st.title("Text Classifier")
    st.write("Paste a review below to see if it’s predicted as Positive or Negative.")

    user_input = st.text_area("Review text:", "")
    if st.button("Classify"):
        if user_input.strip():
            # Placeholder prediction
            st.success("Prediction: Positive (demo) with 85% confidence")
        else:
            st.warning("Please enter a review first.")

# -----------------------------
# Topics Page
# -----------------------------
elif page == "🔍 Topics":
    st.title("Topic Modeling")
    st.write("Explore the main themes found in reviews.")

    # Demo topics (replace later with LDA/NMF results)
    demo_topics = {
        1: ["teachers", "academics", "support"],
        2: ["safety", "resources", "facilities"],
        3: ["extracurriculars", "sports", "clubs"]
    }
    for tid, words in demo_topics.items():
        st.write(f"**Topic {tid}:** {', '.join(words)}")

# -----------------------------
# Data Explorer Page
# -----------------------------
elif page == "📊 Data Explorer":
    st.title("Descriptive Statistics")
    st.write("Overview of the dataset: number of reviews, average rating, sentiment distribution.")

    # Summary metrics
    st.metric("Total Reviews", len(df))
    st.metric("Avg Rating (Palo Alto)", df[df["city"]=="Palo Alto, CA"]["rating"].mean())
    st.metric("Avg Rating (OKC)", df[df["city"]=="Oklahoma City, OK"]["rating"].mean())

    # Show reviews
    st.subheader("Sample Reviews")
    st.dataframe(df[["school", "city", "source", "rating", "review_text"]])

# -----------------------------
# Query Builder Page (with Reddit API)
# -----------------------------
elif page == "🔎 Query Builder":
    st.title("Query Builder")

    st.sidebar.header("Search Parameters")
    district_name = st.sidebar.text_input("District Name", "Palo Alto")

    terms = {
        "schools": st.sidebar.checkbox("schools", value=True),
        "district": st.sidebar.checkbox("district", value=True),
        "education": st.sidebar.checkbox("education", value=True),
        "homework": st.sidebar.checkbox("homework", value=True),
        "teachers": st.sidebar.checkbox("teachers", value=True),
        "students": st.sidebar.checkbox("students", value=True)
    }

    selected_terms = [term for term, checked in terms.items() if checked]

    if selected_terms:
        terms_str = " OR ".join(selected_terms)
        query = f'{district_name} ({terms_str})'
    else:
        query = district_name

    MIN_WORD = st.sidebar.number_input("Minimum Words", min_value=5, value=10)
    MIN_SCORE = st.sidebar.number_input("Minimum Score", min_value=1, value=5)
    LIMIT = st.sidebar.number_input("Number of Posts (Limit)", min_value=50, max_value=500, value=150)

    st.write("### Query Preview")
    st.code(query, language="text")
    st.write(f"Min Words: {MIN_WORD}, Min Score: {MIN_SCORE}, Limit: {LIMIT}")

    # ✅ Correct import path to reddit_utils.py (same folder)
    if st.button("Run Query"):
        import importlib.util
        import os

        project_root = os.path.abspath(os.path.dirname(__file__))
        reddit_utils_path = os.path.join(project_root, "reddit_utils.py")

        if not os.path.exists(reddit_utils_path):
            st.error(f"❌ reddit_utils.py not found at: {reddit_utils_path}")
        else:
            spec = importlib.util.spec_from_file_location("reddit_utils", reddit_utils_path)
            reddit_utils = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(reddit_utils)

            with st.spinner("Fetching Reddit posts..."):
                try:
                    df_results = reddit_utils.fetch_reddit_posts(district_name, selected_terms, limit=LIMIT)
                    st.success(f"✅ Found {len(df_results)} Reddit posts for '{district_name}'")

                    st.subheader("Sample Results")
                    st.dataframe(df_results.head(10))
                except Exception as e:
                    st.error(f"⚠️ Error fetching Reddit posts: {e}")

# -----------------------------------
# 🏫 District Comparison (Reddit Posts + Sentiment + Visualization)
# -----------------------------------
elif page == "🏫 District Comparison":
    import importlib.util
    import os
    import sys

    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    from wordcloud import WordCloud

    st.title("🏫 District Comparison (Reddit Posts)")
    st.subheader("Query Preview")

    # Input fields for two districts
    district1 = st.text_input("District 1", "Palo Alto")
    district2 = st.text_input("District 2", "Oklahoma City")

    # Default search terms
    selected_terms = ["schools", "district", "education", "homework", "teachers", "students"]
    query1 = f'{district1} ({ " OR ".join(selected_terms) })'
    query2 = f'{district2} ({ " OR ".join(selected_terms) })'

    st.code(f"District 1: {query1}\nDistrict 2: {query2}", language="text")

    # ✅ Load reddit_utils dynamically (same folder as this script)
    project_root = os.path.abspath(os.path.dirname(__file__))
    reddit_utils_path = os.path.join(project_root, "reddit_utils.py")

    if not os.path.exists(reddit_utils_path):
        st.error(f"❌ reddit_utils.py not found at: {reddit_utils_path}")
    else:
        spec = importlib.util.spec_from_file_location("reddit_utils", reddit_utils_path)
        reddit_utils = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(reddit_utils)

        if st.button("Run Comparison"):
            with st.spinner("Fetching Reddit posts and analyzing sentiment..."):
                try:
                    # Fetch posts for each district
                    df1 = reddit_utils.fetch_reddit_posts(district1, selected_terms, limit=50)
                    df2 = reddit_utils.fetch_reddit_posts(district2, selected_terms, limit=50)

                    if df1.empty or df2.empty:
                        st.warning("⚠️ One or both districts returned no Reddit results.")
                    else:
                        # Add district labels
                        df1["district"] = district1
                        df2["district"] = district2
                        combined_df = pd.concat([df1, df2], ignore_index=True)

                        # Display metrics
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(label=f"{district1} - Avg Sentiment", value=round(df1['sentiment_score'].mean(), 2))
                        with col2:
                            st.metric(label=f"{district2} - Avg Sentiment", value=round(df2['sentiment_score'].mean(), 2))

                        # 🎨 Color-coded sentiment labels
                        def color_sentiment(val):
                            if val == "Positive":
                                color = "lightgreen"
                            elif val == "Negative":
                                color = "salmon"
                            else:
                                color = "lightgray"
                            return f"background-color: {color}"

                        st.subheader(f"📘 {district1} Reddit Posts")
                        st.dataframe(df1[["title", "score", "sentiment_label"]].style.applymap(color_sentiment, subset=["sentiment_label"]))

                        st.subheader(f"📗 {district2} Reddit Posts")
                        st.dataframe(df2[["title", "score", "sentiment_label"]].style.applymap(color_sentiment, subset=["sentiment_label"]))

                        # 📊 Sentiment Distribution Chart
                        st.subheader("📊 Sentiment Distribution by District")
                        sentiment_counts = combined_df.groupby(["district", "sentiment_label"]).size().unstack(fill_value=0)
                        st.bar_chart(sentiment_counts)

                        # ☁️ Word Clouds
                        st.subheader("☁️ Word Clouds by District")
                        col_wc1, col_wc2 = st.columns(2)

                        with col_wc1:
                            st.markdown(f"### {district1}")
                            text1 = " ".join(df1["title"])
                            if text1.strip():
                                wc1 = WordCloud(width=500, height=300, background_color="black", colormap="cool").generate(text1)
                                st.image(wc1.to_array(), use_container_width=True)
                            else:
                                st.write("No text available.")

                        with col_wc2:
                            st.markdown(f"### {district2}")
                            text2 = " ".join(df2["title"])
                            if text2.strip():
                                wc2 = WordCloud(width=500, height=300, background_color="black", colormap="plasma").generate(text2)
                                st.image(wc2.to_array(), use_container_width=True)
                            else:
                                st.write("No text available.")

                        # 📋 Summary Table
                        st.subheader("📋 Sentiment Summary Table")
                        summary_data = []
                        for df, name in [(df1, district1), (df2, district2)]:
                            summary_data.append({
                                "District": name,
                                "# Posts": len(df),
                                "Avg Sentiment": round(df["sentiment_score"].mean(), 2),
                                "% Positive": round((df["sentiment_label"] == "Positive").mean() * 100, 1),
                                "% Negative": round((df["sentiment_label"] == "Negative").mean() * 100, 1),
                            })
                        summary_df = pd.DataFrame(summary_data)
                        st.table(summary_df)

                        # 💬 Insights
                        st.subheader("💬 Key Insights")
                        avg1 = df1["sentiment_score"].mean()
                        avg2 = df2["sentiment_score"].mean()

                        if avg1 > avg2:
                            st.markdown(f"✨ **{district1}** discussions appear slightly more positive overall compared to **{district2}**.")
                        elif avg2 > avg1:
                            st.markdown(f"✨ **{district2}** discussions appear slightly more positive overall compared to **{district1}**.")
                        else:
                            st.markdown("😐 Both districts show a similar overall sentiment tone.")

                        st.markdown("_These insights reflect the tone of recent Reddit discussions related to school topics._")

                except Exception as e:
                    st.error(f"⚠️ Error fetching Reddit posts: {e}")

# -----------------------------
# About Page
# -----------------------------
elif page == "ℹ️ About":
    st.title("About This Project")
    st.write("""
    **ADS-509 Final Project**  
    - Dataset: School Reviews (Reddit)  
    - Focus: Comparing high-performing Palo Alto schools with low-performing Oklahoma City schools  
    - Methods: Sentiment Classification + Topic Modeling  
    - App: Built with Streamlit  
    
    **Team Members**  
    - Tanya Ortega  
    - Jun Clemente  
    - Amayrani Balbuena
    """)




    """)




