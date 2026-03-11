import streamlit as st
import random

st.title("you and i - Translator App")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = {}
    st.session_state.page = "Home"
if "recent_translations" not in st.session_state:
    st.session_state.recent_translations = []
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False


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

    if st.session_state.page == "Home":
        st.header("🌐 Translator")
        st.write(f"Welcome, **{user['name']}**! Translate between English, Filipino, and Japanese.")

        lang_options = ["🇺🇸 English", "🇵🇭 Filipino", "🇯🇵 Japanese"]

        col1, col2 = st.columns(2)
        with col1:
            source_lang_flag = st.selectbox("From", lang_options)
        with col2:
            target_options = [l for l in lang_options if l != source_lang_flag]
            target_lang_flag = st.selectbox("To", target_options)

        source_lang = source_lang_flag.split(" ", 1)[1]
        target_lang = target_lang_flag.split(" ", 1)[1]

        default_text = "" if st.session_state.clear_input else None
        if st.session_state.clear_input:
            st.session_state.clear_input = False

        input_text = st.text_area(
            "Enter text to translate",
            value="" if default_text is not None else st.session_state.get("last_input", ""),
            height=150,
            placeholder="Type here..."
        )

        st.session_state.last_input = input_text

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
            st.markdown("** Available phrases you can type:**")
            for phrase in translations[pair].keys():
                st.markdown(f"- `{phrase}`")

        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("Translate"):
                if input_text.strip():
                    key = input_text.strip().lower()
                    result = translations.get(pair, {}).get(key)
                    if result:
                        st.success(f"✅ Translation ({source_lang_flag} → {target_lang_flag}):")
                        st.markdown(f"### {result}")
                        st.code(result, language=None)
                        st.caption("Click the copy icon on the top right of the box to copy!")

                        st.session_state.recent_translations.insert(0, {
                            "from": source_lang_flag,
                            "to": target_lang_flag,
                            "original": input_text,
                            "translated": result
                        })
                        st.session_state.recent_translations = st.session_state.recent_translations[:10]
                    else:
                        st.warning("⚠️ Phrase not found. Try one of the example phrases listed above.")
                else:
                    st.warning("Please enter some text to translate.")

        with col_b:
            if st.button("Clear"):
                st.session_state.clear_input = True
                st.session_state.last_input = ""
                st.rerun()

    elif st.session_state.page == "Recent":
        st.header(f"Recent Translations ({len(st.session_state.recent_translations)})")

        if not st.session_state.recent_translations:
            st.info("No recent translations yet. Go to Home to start translating!")
        else:
            if st.button("Clear History"):
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

        st.write(
            "The You and I – Translator App is a simple web application that translates phrases "
            "between English, Filipino, and Japanese. Since there are no API yet the creator use "
            "several phrases that can be translated. Also, the language that you can translate is "
            "also limited for now but will be expanding in the future."
        )

        st.write(
            "The target users of this application are the people who want to understand "
            "translations between different languages."
        )

        st.write(
            "The application collects several inputs from the user. First, the user enters their "
            "name, email, and password to log in. After logging in, the user selects a source "
            "language and a target language and types the phrase they want to translate."
        )

        st.write(
            "On the other hand, the output of the app is the translated phrase displayed on the "
            "screen after the user clicks the Translate button."
        )

        st.write("---")
        st.write("**Supported Languages:** 🇺🇸 English | 🇵🇭 Filipino | 🇯🇵 Japanese")

    elif st.session_state.page == "Settings":
        st.header("⚙️ Settings")
        st.write(f"👤 **Name:** {user['name']}")
        st.write(f"📧 **Email:** {user['email']}")
        st.write("---")
        st.checkbox("Enable notifications")
        st.color_picker("Pick a theme color")

    st.sidebar.write("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()