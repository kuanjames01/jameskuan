import streamlit as st
import random

st.title("you and i - Translator App")

# session states
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = {}
    st.session_state.page = "Home"
if "recent_translations" not in st.session_state:
    st.session_state.recent_translations = []

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

    # SIDEBAR MENU using radio (no typing allowed)
    st.sidebar.title("Menu")

    recent_count = len(st.session_state.recent_translations)
    recent_label = f"🕐 Recent ({recent_count})" if recent_count > 0 else "🕐 Recent"

    page_choice = st.sidebar.radio(
        "Navigate",
        ["🏠 Home", recent_label, "ℹ️ About Us", "⚙️ Settings"],
        label_visibility="collapsed"
    )

    if "Home" in page_choice:
        st.session_state.page = "Home"
    elif "Recent" in page_choice:
        st.session_state.page = "Recent"
    elif "About" in page_choice:
        st.session_state.page = "About"
    elif "Settings" in page_choice:
        st.session_state.page = "Settings"

    # ---------------- PAGES ----------------

    if st.session_state.page == "Home":
        st.header("🌐 Translator")
        st.write(f"Welcome, **{user['name']}**! Translate between English, Filipino, and Japanese.")

        # Language flags
        lang_options = ["🇺🇸 English", "🇵🇭 Filipino", "🇯🇵 Japanese"]

        col1, col2 = st.columns(2)
        with col1:
            source_lang_flag = st.selectbox("From", lang_options)
        with col2:
            target_options = [l for l in lang_options if l != source_lang_flag]
            target_lang_flag = st.selectbox("To", target_options)

        # Strip flag for dictionary lookup
        source_lang = source_lang_flag.split(" ", 1)[1]
        target_lang = target_lang_flag.split(" ", 1)[1]

        input_text = st.text_area("Enter text to translate", height=150, placeholder="Type here...", key="translate_input")

        # Clear button
        if st.button("🗑️ Clear"):
            st.session_state["translate_input"] = ""
            st.rerun()

        translations = {
            ("English", "Filipino"): {
                "hello": "kamusta",
                "thank you": "salamat",
                "good morning": "magandang umaga",
                "i love you": "mahal kita",
                "goodbye": "paalam",
            },
            ("English", "Japanese"): {
                "hello": "konnichiwa (こんにちは)",
                "thank you": "arigatou (ありがとう)",
                "good morning": "ohayou (おはよう)",
                "i love you": "aishiteru (愛してる)",
                "goodbye": "sayonara (さようなら)",
            },
            ("Filipino", "English"): {
                "kamusta": "hello",
                "salamat": "thank you",
                "magandang umaga": "good morning",
                "mahal kita": "i love you",
                "paalam": "goodbye",
            },
            ("Filipino", "Japanese"): {
                "kamusta": "konnichiwa (こんにちは)",
                "salamat": "arigatou (ありがとう)",
                "magandang umaga": "ohayou (おはよう)",
                "mahal kita": "aishiteru (愛してる)",
                "paalam": "sayonara (さようなら)",
            },
            ("Japanese", "English"): {
                "konnichiwa": "hello",
                "arigatou": "thank you",
                "ohayou": "good morning",
                "aishiteru": "i love you",
                "sayonara": "goodbye",
            },
            ("Japanese", "Filipino"): {
                "konnichiwa": "kamusta",
                "arigatou": "salamat",
                "ohayou": "magandang umaga",
                "aishiteru": "mahal kita",
                "sayonara": "paalam",
            },
        }

        pair = (source_lang, target_lang)
        if pair in translations:
            st.markdown("**💡 Available phrases you can type:**")
            for phrase in translations[pair].keys():
                st.markdown(f"- `{phrase}`")

        if st.button("Translate"):
            if input_text.strip():
                key = input_text.strip().lower()
                result = translations.get(pair, {}).get(key)
                if result:
                    st.success(f"✅ Translation ({source_lang_flag} → {target_lang_flag}):")
                    st.markdown(f"### {result}")

                    # Copy to clipboard button
                    st.code(result, language=None)
                    st.caption("👆 Click the copy icon on the top right of the box to copy!")

                    st.session_state.recent_translations.insert(0, {
                        "from": source_lang_flag,
                        "to": target_lang_flag,
                        "original": input_text,
                        "translated": result
                    })
                    st.session_state.recent_translations = st.session_state.recent_translations[:10]
                    st.rerun()
                else:
                    st.warning("⚠️ Phrase not found. Try one of the example phrases listed above.")
            else:
                st.warning("Please enter some text to translate.")

    elif st.session_state.page == "Recent":
        st.header(f"🕐 Recent Translations ({len(st.session_state.recent_translations)})")

        if not st.session_state.recent_translations:
            st.info("No recent translations yet. Go to Home to start translating!")
        else:
            if st.button("🗑️ Clear History"):
                st.session_state.recent_translations = []
                st.rerun()

            for i, item in enumerate(st.session_state.recent_translations):
                with st.expander(f"{item['from']} → {item['to']}: {item['original'][:40]}"):
                    st.write(f"**Original ({item['from']}):** {item['original']}")
                    st.write(f"**Translated ({item['to']}):** {item['translated']}")
                    st.code(item['translated'], language=None)
                    st.caption("👆 Click the copy icon to copy the translation!")

    elif st.session_state.page == "About":
        st.header("ℹ️ About Us")

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
    st.sidebar.write("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()