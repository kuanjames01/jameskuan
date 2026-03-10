import streamlit as st
import random

st.title("pabobohan")

# session states
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = {}
    st.session_state.page = "Home"

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:
    st.subheader("Login")

    name = st.text_input("Enter your name")
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")

    if st.button("Login"):
        if name and email and password:
            st.session_state.logged_in = True
            st.session_state.user_info = {"name": name, "email": email}
            st.rerun()
        else:
            st.error("Please fill in all fields!")

# ---------------- MAIN APP ----------------
else:
    user = st.session_state.user_info

    # SIDEBAR MENU
    st.sidebar.title("Menu")

    if st.sidebar.button("Home"):
        st.session_state.page = "Home"

    if st.sidebar.button("Profile"):
        st.session_state.page = "Profile"

    if st.sidebar.button("Settings"):
        st.session_state.page = "Settings"

    if st.sidebar.button("Gallery"):
        st.session_state.page = "Gallery"

    if st.sidebar.button("About Us"):
        st.session_state.page = "About"

    # ---------------- PAGES ----------------

    if st.session_state.page == "Home":
        st.header("Home Page")
        st.write("Welcome to the app!")

    elif st.session_state.page == "Profile":
        st.header("My Profile")
        st.write(f"👤 **Name:** {user['name']}")
        st.write(f"📧 **Email:** {user['email']}")

    elif st.session_state.page == "Settings":
        st.header("Settings")
        st.checkbox("Enable notifications")
        st.color_picker("Pick a theme color")

    elif st.session_state.page == "Gallery":
        st.header("Gallery")
        st.image("https://via.placeholder.com/400")

    elif st.session_state.page == "About":
        st.header("About Us")

        about_texts = [
            "We are a group of students learning Streamlit.",
            "This app was built to demonstrate UI components.",
            "Our goal is to create simple and interactive apps.",
            "Technology helps us solve real-world problems.",
            "This section shows random text each time."
        ]

        st.markdown(random.choice(about_texts))

    # logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
