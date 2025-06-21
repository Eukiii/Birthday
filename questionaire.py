import streamlit as st
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="Birthday Verification",
    page_icon="🔐",
    layout="centered"
)

# File to store correct answers (you'll need to set these)
CONFIG_FILE = "birthday_config.json"


# Function to load configuration
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"name": "", "birthday": ""}
    return {"name": "", "birthday": ""}


# Function to save configuration
def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving configuration: {e}")


# Load current config
config = load_config()

# Main header
st.title("🔐 Birthday Verification")
st.markdown("---")

# Setup section (only show if not configured)
if not config.get("name") or not config.get("birthday"):
    st.subheader("⚙️ Initial Setup")
    st.info("First, set up the correct name and birthday for verification.")

    with st.form("setup_form"):
        setup_name = st.text_input("Mom's Full Name", placeholder="Enter the exact name for verification")
        setup_birthday = st.date_input("Mom's Birthday", value=datetime(1950, 1, 1))

        if st.form_submit_button("Save Setup"):
            if setup_name.strip():
                new_config = {
                    "name": setup_name.strip(),
                    "birthday": setup_birthday.strftime("%Y-%m-%d")
                }
                save_config(new_config)
                st.success("Setup complete! The questionnaire is now ready.")
                st.rerun()
            else:
                st.error("Please enter a name")

    st.markdown("---")

# Questionnaire section
if config.get("name") and config.get("birthday"):
    st.subheader("🎂 Birthday Questionnaire")
    st.markdown("Please answer the following questions to continue:")

    with st.form("verification_form"):
        user_name = st.text_input("What is your full name?", placeholder="Enter your full name")
        user_birthday = st.date_input("What is your birthday?", value=datetime(1950, 1, 1))

        if st.form_submit_button("Submit"):
            # Check if answers match
            correct_name = config["name"].lower().strip()
            correct_birthday = config["birthday"]

            entered_name = user_name.lower().strip()
            entered_birthday = user_birthday.strftime("%Y-%m-%d")

            if entered_name == correct_name and entered_birthday == correct_birthday:
                # Store verification in session state
                st.session_state.verified = True
                st.session_state.verified_name = user_name.strip()
                st.success("✅ Verification successful!")

                # Show link to birthday messages
                st.markdown("---")
                st.subheader("🎉 Welcome!")
                st.markdown(f"Happy Birthday, {user_name}! 🎂")
                st.markdown("Click the link below to see your birthday messages:")
                st.markdown("[**🎁 View Your Birthday Messages**](http://localhost:5002)")

            else:
                st.error("❌ The information doesn't match. Please try again.")
                if 'verified' in st.session_state:
                    del st.session_state.verified

# Admin section to reset configuration
if config.get("name"):
    with st.expander("🔧 Admin - Reset Configuration"):
        st.warning("This will clear the stored name and birthday settings.")
        if st.button("Reset Configuration"):
            save_config({"name": "", "birthday": ""})
            if 'verified' in st.session_state:
                del st.session_state.verified
            st.success("Configuration reset!")
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p style="color: #666; font-style: italic;">
        🔐 Secure birthday verification system
    </p>
</div>
""", unsafe_allow_html=True)