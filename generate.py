# generate.py
import streamlit as st
import json
from few_shot import FewShotPosts
from post_generator import generate_post
import os

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]
if not os.path.exists("data/processed_posts.json"):
    from preprocess import process_posts
    process_posts("data/rawpost.json", "data/processed_posts.json")

def main(json_file="data/rawpost.json"):
    st.subheader("LinkedIn Post Generator")

    # Load scraped posts
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            scraped_posts = json.load(f)
        st.write(f"✅ Loaded {len(scraped_posts)} posts from LinkedIn.")
    except Exception:
        scraped_posts = []
        st.warning("⚠️ No posts loaded. Please scrape posts first.")

    # Dropdowns
    col1, col2, col3 = st.columns(3)
    fs = FewShotPosts()
    tags = fs.get_tags()

    with col1:
        selected_tag = st.selectbox("Topic", options=tags)
    with col2:
        selected_length = st.selectbox("Length", options=length_options)
    with col3:
        selected_language = st.selectbox("Language", options=language_options)

    # Generate Button
    if st.button("Generate"):
        post = generate_post(selected_length, selected_language, selected_tag)
        st.write(post)

if __name__ == "__main__":
    main()
