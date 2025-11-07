import streamlit as st
from scrape_linkedin import scrape_linkedin
import generate

st.set_page_config(page_title="LinkedIn Scraper & Post Generator", page_icon="💬")
st.title("💬 LinkedIn Post Generator")
st.write("Log in securely to LinkedIn, scrape recent posts, and generate LinkedIn posts.")

# Initialize session state
if "scraped" not in st.session_state:
    st.session_state.scraped = False
    st.session_state.json_file = None

# --- Login form ---
if not st.session_state.scraped:
    with st.form("login_form"):
        email = st.text_input("LinkedIn Email")
        password = st.text_input("LinkedIn Password", type="password")
        profile_url = st.text_input("LinkedIn Profile URL", placeholder="https://www.linkedin.com/in/example/")
        submitted = st.form_submit_button("Login and Proceed")

    if submitted:
        if not email or not password or not profile_url:
            st.error("⚠️ Please fill in all fields.")
        else:
            with st.spinner("🔄 Logging in..."):
                try:
                    json_file, count = scrape_linkedin(email, password, profile_url)
                    st.success(f"✅ Scraped {count} posts successfully!")
                    # Save to session_state
                    st.session_state.scraped = True
                    st.session_state.json_file = json_file
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# --- Show generate.py functionality ---
if st.session_state.scraped:
    generate.main(json_file=st.session_state.json_file)
