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
    ["🏠 Home", "📝 Classifier", "🔍 Topics", "📊 Data Explorer", "🔎 Query Builder", "ℹ️ About"]
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
    - Query Builder for Reddit/Twitter/Yelp data
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
# Query Builder Page (NEW)
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

    if st.button("Run Query"):
        st.success("Query executed successfully! (demo mode)")
        demo_results = pd.DataFrame({
            "post": ["Great teachers at Palo Alto", "Too much homework", "School lacks resources"],
            "score": [25, 12, 8],
            "words": [50, 20, 15]
        })
        st.write(demo_results.head(10))

# -----------------------------
# About Page
# -----------------------------
elif page == "ℹ️ About":
    st.title("About This Project")
    st.write("""
    **ADS-509 Final Project**  
    - Dataset: School Reviews (Yelp, Reddit, Twitter)  
    - Focus: Comparing high-performing Palo Alto schools with low-performing Oklahoma City schools  
    - Methods: Sentiment Classification + Topic Modeling  
    - App: Built with Streamlit  
    
    **Team Members**  
    - Tanya Ortega  
    - Jun Clemente  
    - Amayrani Balbuena
    """)




