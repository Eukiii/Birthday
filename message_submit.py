import streamlit as st
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="Happy Birthday Mom! 🎉",
    page_icon="🎂",
    layout="wide"
)

# File path for storing messages
MESSAGES_FILE = "birthday_messages.json"


# Function to load messages from file
def load_messages():
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []


# Function to save messages to file
def save_messages(messages):
    try:
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving messages: {e}")


# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = load_messages()

# Header section with birthday celebration
st.title("🎉 Happy Birthday Mom! 🎂")
st.markdown("---")

# Birthday message section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center;">
        <h2>🌟 Celebrating Another Wonderful Year! 🌟</h2>
        <p style="font-size: 18px;">
            Today we celebrate someone truly special - a amazing mom who brings joy, 
            love, and warmth to everyone around her. Please leave a birthday message 
            to make her day even more special!
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Message submission form
st.subheader("📝 Leave a Birthday Message")

with st.form("birthday_message_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        sender_name = st.text_input(
            "Your Name *",
            placeholder="Enter your name",
            help="This will appear as your signature"
        )

    with col2:
        relationship = st.selectbox(
            "Your Relationship (Optional)",
            [
                "",
                # Immediate Family
                "Son", "Daughter", "Husband", "Partner",
                # Children & Grandchildren
                "Grandson", "Granddaughter", "Great-Grandson", "Great-Granddaughter",
                # Parents & Grandparents
                "Mother", "Father", "Grandmother", "Grandfather",
                # Siblings
                "Sister", "Brother", "Twin Sister", "Twin Brother",
                # Extended Family - Aunts/Uncles
                "Aunt", "Uncle", "Great-Aunt", "Great-Uncle",
                # Extended Family - Cousins
                "Cousin", "First Cousin", "Second Cousin",
                # In-Laws
                "Mother-in-Law", "Father-in-Law", "Sister-in-Law", "Brother-in-Law",
                "Daughter-in-Law", "Son-in-Law",
                # Nieces/Nephews
                "Niece", "Nephew", "Great-Niece", "Great-Nephew",
                # Step Family
                "Stepmother", "Stepfather", "Stepdaughter", "Stepson",
                "Stepsister", "Stepbrother",
                # Godparents/Godchildren
                "Godmother", "Godfather", "Goddaughter", "Godson",
                # Friends & Others
                "Best Friend", "Close Friend", "Friend", "Family Friend",
                "Neighbor", "Colleague", "Coworker", "Boss",
                "Former Colleague", "Childhood Friend", "School Friend",
                # Community
                "Church Friend", "Club Member", "Volunteer Friend",
                "Other"
            ],
            help="Optional: Let her know how you know her"
        )

    message = st.text_area(
        "Birthday Message *",
        placeholder="Write your heartfelt birthday message here...",
        height=100,
        help="Share your birthday wishes, memories, or what makes her special"
    )

    submitted = st.form_submit_button("🎁 Send Birthday Message", use_container_width=True)

    # Form validation and submission
    if submitted:
        if not sender_name.strip():
            st.error("Please enter your name")
        elif not message.strip():
            st.error("Please write a birthday message")
        elif len(message.strip()) < 10:
            st.error("Please write a longer message (at least 10 characters)")
        else:
            # Create message entry
            new_message = {
                'name': sender_name.strip(),
                'relationship': relationship if relationship else None,
                'message': message.strip(),
                'timestamp': datetime.now().strftime("%B %d, %Y at %I:%M %p")
            }

            # Add to session state and save to file
            st.session_state.messages.append(new_message)
            save_messages(st.session_state.messages)
            st.success(f"Thank you {sender_name}! Your birthday message has been saved! 🎉")
            st.rerun()

st.markdown("---")

# Display messages section
if st.session_state.messages:
    st.subheader(f"💕 Birthday Messages ({len(st.session_state.messages)} messages)")
    st.markdown("*Here are all the wonderful birthday messages:*")

    # Display messages in reverse order (newest first)
    for i, msg in enumerate(reversed(st.session_state.messages)):
        with st.container():
            # Create message card
            col1, col2 = st.columns([3, 1])

            with col1:
                # Message content
                st.markdown(f"**💌 {msg['message']}**")

                # Signature line
                signature = f"— {msg['name']}"
                if msg['relationship']:
                    signature += f" ({msg['relationship']})"

                st.markdown(f"*{signature}*")
                st.caption(f"Sent on {msg['timestamp']}")

            with col2:
                # Message number/decoration
                st.markdown(f"<div style='text-align: center; font-size: 24px;'>🎈</div>",
                            unsafe_allow_html=True)

            st.markdown("---")
else:
    # Empty state
    st.subheader("💕 Birthday Messages")
    st.info("No messages yet. Be the first to wish her a happy birthday! 🎂")

# Footer section
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center;">
        <p style="color: #666; font-style: italic;">
            🎂 Wishing you joy, happiness, and all the wonderful things life has to offer! 🎂
        </p>
        <p style="font-size: 12px; color: #999;">
            All messages are saved permanently
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar with additional birthday elements
with st.sidebar:
    st.markdown("### 🎉 Birthday Celebration")
    st.markdown("🎂 🎈 🎁 🌟 💕")
    st.markdown("---")

    if st.session_state.messages:
        st.metric("Total Messages", len(st.session_state.messages))

        # Show recent activity
        st.markdown("### Recent Messages")
        for msg in st.session_state.messages[-3:]:
            st.markdown(f"💌 **{msg['name']}**")
            if len(msg['message']) > 50:
                preview = msg['message'][:50] + "..."
            else:
                preview = msg['message']
            st.caption(preview)
            st.markdown("---")

    # Clear messages button (for admin purposes)
    if st.session_state.messages:
        st.markdown("### Admin Actions")
        if st.button("🗑️ Clear All Messages", help="This will remove all messages"):
            st.session_state.messages = []
            save_messages(st.session_state.messages)
            st.success("All messages cleared!")
            st.rerun()
