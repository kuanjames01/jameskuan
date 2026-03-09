import streamlit as st
st.title("pabobohan")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = {}

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

else:
    user = st.session_state.user_info
    st.subheader("My Profile")
    st.write(f"👤 **Name:** {user['name']}")
    st.write(f"📧 **Email:** {user['email']}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
