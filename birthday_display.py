import streamlit as st
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="Birthday Celebration Portal",
    page_icon="🎂",
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
st.title("🎂 Birthday Celebration Portal")
st.markdown("---")

# Welcome section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center;">
        <h3>🌟 Welcome to the Birthday Celebration! 🌟</h3>
        <p style="font-size: 16px;">
            We're celebrating someone very special today! To access your personalized 
            birthday experience, please share a few details about yourself.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Setup section (only show if not configured)
if not config.get("name") or not config.get("birthday"):
    st.subheader("🎈 Celebration Setup")
    st.info("First time setup: Enter the birthday person's details to configure the celebration.")
    
    with st.form("setup_form"):
        setup_name = st.text_input("Birthday Person's Full Name", placeholder="Enter the name")
        setup_birthday = st.date_input("Birthday Date", value=datetime(1950, 1, 1))
        
        if st.form_submit_button("Start Celebration"):
            if setup_name.strip():
                new_config = {
                    "name": setup_name.strip(),
                    "birthday": setup_birthday.strftime("%Y-%m-%d")
                }
                save_config(new_config)
                st.success("Celebration setup complete!")
                st.rerun()
            else:
                st.error("Please enter a name")
    
    st.markdown("---")

# Main portal section
if config.get("name") and config.get("birthday"):
    st.subheader("🎉 Join the Celebration")
    st.markdown("Tell us about yourself to access your personalized birthday experience:")
    
    with st.form("celebration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            user_name = st.text_input("Your Full Name", placeholder="What should we call you?")
        
        with col2:
            user_birthday = st.date_input("Your Special Day", value=datetime(1950, 1, 1), help="When do you celebrate your birthday?")
        
        st.markdown("*We use this information to personalize your birthday experience and ensure you're in the right place.*")
        
        if st.form_submit_button("Enter Celebration", use_container_width=True):
            # Check if answers match
            correct_name = config["name"].lower().strip()
            correct_birthday = config["birthday"]
            
            entered_name = user_name.lower().strip()
            entered_birthday = user_birthday.strftime("%Y-%m-%d")
            
            if entered_name == correct_name and entered_birthday == correct_birthday:
                # Store verification in session state
                st.session_state.verified = True
                st.session_state.verified_name = user_name.strip()
                st.success("Welcome to your special celebration!")
                
                # Show celebration access
                st.markdown("---")
                st.subheader("🎊 Your Birthday Celebration Awaits!")
                st.markdown(f"Happy Birthday, {user_name}!")
                st.markdown("Your personalized birthday messages are ready for you:")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown("""
                    <div style="text-align: center; padding: 20px; background-color: #f0f8ff; border-radius: 10px; border: 2px solid #ff69b4;">
                        <h4>🎁 Your Birthday Messages</h4>
                        <p>Click below to see all the wonderful messages people have left for you!</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("[**🎁 View Your Birthday Messages**](http://localhost:5002)")
                
            else:
                st.warning("Hmm, we can't find your celebration. Please double-check your information or contact the celebration organizer.")
                if 'verified' in st.session_state:
                    del st.session_state.verified

# Admin section to reset configuration (hidden)
if config.get("name"):
    with st.expander("🎂 Celebration Settings"):
        st.info("Reset celebration settings if needed.")
        if st.button("Reset Celebration"):
            save_config({"name": "", "birthday": ""})
            if 'verified' in st.session_state:
                del st.session_state.verified
            st.success("Celebration reset!")
            st.rerun()

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center;">
        <p style="color: #666; font-style: italic;">
            🎂 Making birthdays more special, one celebration at a time
        </p>
        <p style="font-size: 12px; color: #999;">
            Secure celebration portal
        </p>
    </div>
    """, unsafe_allow_html=True)
