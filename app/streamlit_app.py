import streamlit as st
import pandas as pd

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
        "source": ["Niche", "Yelp", "Website", "Niche", "Yelp"],
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
    ["🏠 Home", "📝 Classifier", "🔍 Topics", "📊 Data Explorer", "ℹ️ About"]
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
# About Page
# -----------------------------
elif page == "ℹ️ About":
    st.title("About This Project")
    st.write("""
    **ADS-509 Final Project**  
    - Dataset: School Reviews (Niche, Yelp, School Websites, Articles)  
    - Focus: Comparing high-performing Palo Alto schools with low-performing Oklahoma City schools  
    - Methods: Sentiment Classification + Topic Modeling  
    - App: Built with Streamlit  
    
    **Team Members**  
    - Tanya Ortega  
    - Jun Clemente  
    - Amayrani Balbuena
    """)



