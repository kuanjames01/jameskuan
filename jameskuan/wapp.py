import streamlit as st
import random

st.title("you and i - Translator App")

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
    password = st.text_input("password", type="password")

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

    if st.sidebar.button("Recent"):
        st.session_state.page = "Recent"

    if st.sidebar.button("About Us"):
        st.session_state.page = "About"

    if st.sidebar.button("Settings"):
        st.session_state.page = "Settings"

    # ---------------- PAGES ----------------

    if st.session_state.page == "Home":
        st.header("🌐 Translator")
        st.write(f"Welcome, **{user['name']}**! Translate between English, Filipino, and Japanese.")

        # Language selection
        col1, col2 = st.columns(2)
        with col1:
            source_lang = st.selectbox("From", ["English", "Filipino", "Japanese"])
        with col2:
            target_options = [l for l in ["English", "Filipino", "Japanese"] if l != source_lang]
            target_lang = st.selectbox("To", target_options)

        # Input text
        input_text = st.text_area("Enter text to translate", height=150, placeholder="Type here...")

        if st.button("Translate"):
            if input_text.strip():
                with st.spinner("Translating..."):
                    import urllib.request, json

                    prompt = f"Translate the following text from {source_lang} to {target_lang}. Reply with ONLY the translated text, nothing else.\n\n{input_text}"

                    payload = json.dumps({
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 1000,
                        "messages": [{"role": "user", "content": prompt}]
                    }).encode("utf-8")

                    req = urllib.request.Request(
                        "https://api.anthropic.com/v1/messages",
                        data=payload,
                        headers={
                            "Content-Type": "application/json",
                            "anthropic-version": "2023-06-01"
                        },
                        method="POST"
                    )

                    try:
                        with urllib.request.urlopen(req) as resp:
                            result = json.loads(resp.read().decode("utf-8"))
                            translation = result["content"][0]["text"]

                            st.success("Translation:")
                            st.write(translation)

                            # Save to recent
                            if "recent_translations" not in st.session_state:
                                st.session_state.recent_translations = []
                            st.session_state.recent_translations.insert(0, {
                                "from": source_lang,
                                "to": target_lang,
                                "original": input_text,
                                "translated": translation
                            })
                            # Keep only last 10
                            st.session_state.recent_translations = st.session_state.recent_translations[:10]

                    except Exception as e:
                        st.error(f"Translation failed: {e}")
            else:
                st.warning("Please enter some text to translate.")

    elif st.session_state.page == "Recent":
        st.header("🕐 Recent Translations")

        if "recent_translations" not in st.session_state or not st.session_state.recent_translations:
            st.info("No recent translations yet. Go to Home to start translating!")
        else:
            for i, item in enumerate(st.session_state.recent_translations):
                with st.expander(f"{item['from']} → {item['to']}: {item['original'][:40]}..."):
                    st.write(f"**Original ({item['from']}):** {item['original']}")
                    st.write(f"**Translated ({item['to']}):** {item['translated']}")

    elif st.session_state.page == "About":
        st.header("About Us")

        about_texts = [
            "We are a group of students learning Streamlit.",
            "This app was built to demonstrate UI components.",
            "Our goal is to create simple and interactive apps.",
            "Technology helps us solve real-world problems.",
            "This translator supports English, Filipino, and Japanese."
        ]

        st.markdown(random.choice(about_texts))
        st.write("---")
        st.write("**Supported Languages:** 🇺🇸 English | 🇵🇭 Filipino | 🇯🇵 Japanese")

    elif st.session_state.page == "Settings":
        st.header("⚙️ Settings")
        st.write(f"👤 **Name:** {user['name']}")
        st.write(f"📧 **Email:** {user['email']}")
        st.write("---")
        st.checkbox("Enable notifications")
        st.color_picker("Pick a theme color")

    # logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()