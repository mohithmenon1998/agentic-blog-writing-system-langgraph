import streamlit as st
import requests

API_URL = "https://agentic-blog-writing-system-langgraph.onrender.com"  # change when deployed

st.set_page_config(page_title="Blog Generator", layout="wide")

# -----------------------------
# Session state
# -----------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "blogs" not in st.session_state:
    st.session_state.blogs = []

if "current_blog" not in st.session_state:
    st.session_state.current_blog = None


# -----------------------------
# Helper functions
# -----------------------------
def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}


def fetch_blogs():
    res = requests.get(f"{API_URL}/blogs", headers=get_headers())
    if res.status_code == 200:
        st.session_state.blogs = res.json()
    else:
        st.error("Failed to fetch blogs")


# -----------------------------
# Auth UI
# -----------------------------
if not st.session_state.token:
    st.title("🔐 Login / Signup")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    # LOGIN
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            res = requests.post(
                f"{API_URL}/login",
                json={"email": email, "password": password},
            )

            if res.status_code == 200:
                st.session_state.token = res.json()["token"]
                fetch_blogs()
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # SIGNUP
    with tab2:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")

        if st.button("Signup"):
            res = requests.post(
                f"{API_URL}/signup",
                json={"email": email, "password": password},
            )

            if res.status_code == 200:
                st.success("Account created! Please login.")
            else:
                st.error(res.text)

    st.stop()


# -----------------------------
# Sidebar (Past blogs)
# -----------------------------
st.sidebar.title("📚 Past Blogs")

if st.button("🔄 Refresh"):
    fetch_blogs()

for blog in st.session_state.blogs:
    if st.sidebar.button(blog["topic"]):
        st.session_state.current_blog = blog["content"]


# -----------------------------
# Main UI
# -----------------------------
st.title("🧠 AI Blog Generator")

topic = st.text_input("Enter blog topic")

if st.button("🚀 Generate"):
    if not topic.strip():
        st.warning("Enter a topic")
    else:
        with st.spinner("Generating blog..."):
            res = requests.post(
                f"{API_URL}/generate",
                json={"topic": topic},
                headers=get_headers(),
            )

            if res.status_code == 200:
                data = res.json()
                st.session_state.current_blog = data.get("final", "")
                fetch_blogs()
            else:
                st.error("Generation failed")


# -----------------------------
# Display blog
# -----------------------------
if st.session_state.current_blog:
    st.markdown("---")
    st.markdown(st.session_state.current_blog)

    st.download_button(
        "⬇️ Download Markdown",
        st.session_state.current_blog,
        file_name="blog.md",
    )


# -----------------------------
# Logout
# -----------------------------
st.sidebar.divider()
if st.sidebar.button("🚪 Logout"):
    st.session_state.token = None
    st.session_state.blogs = []
    st.session_state.current_blog = None
    st.rerun()