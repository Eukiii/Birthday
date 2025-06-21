import streamlit as st
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="Leave a Birthday Message 🎂",
    page_icon="💌",
    layout="centered"
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


# Initialize messages
if 'messages' not in st.session_state:
    st.session_state.messages = load_messages()

# Header section
st.title("💌 Leave a Birthday Message")
st.markdown("---")

# Introduction section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center;">
        <h3>🎂 Help us celebrate a special birthday! 🎂</h3>
        <p style="font-size: 16px;">
            Leave a heartfelt message that will make this birthday extra special.
            Your message will be saved and displayed as part of the birthday celebration.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Message submission form
st.subheader("📝 Your Birthday Message")

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
            help="Optional: Let them know how you know them"
        )

    message = st.text_area(
        "Birthday Message *",
        placeholder="Write your heartfelt birthday message here...",
        height=120,
        help="Share your birthday wishes, memories, or what makes them special"
    )

    # Message guidelines
    st.markdown("""
    **Message Tips:**
    - Share a favorite memory
    - Express what they mean to you
    - Include birthday wishes for the year ahead
    - Keep it heartfelt and personal
    """)

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

            # Success message
            st.success(f"Thank you {sender_name}! Your birthday message has been saved! 🎉")
            st.balloons()

            # Show confirmation
            st.markdown("---")
            st.subheader("✅ Message Sent Successfully!")
            st.markdown(f"**Your message:** {message}")
            st.markdown(f"**From:** {sender_name}" + (f" ({relationship})" if relationship else ""))
            st.markdown(f"**Sent:** {new_message['timestamp']}")

st.markdown("---")

# Recent messages preview (last 3)
recent_messages = st.session_state.messages[-3:] if st.session_state.messages else []
if recent_messages:
    st.subheader("💕 Recent Messages")
    st.markdown("*Here are some of the recent birthday messages:*")

    for msg in reversed(recent_messages):
        with st.container():
            st.markdown(f"""
            <div style="
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 8px;
                border-left: 3px solid #ff69b4;
                margin: 10px 0;
            ">
                <div style="font-weight: bold; color: #333;">
                    💌 {msg['message'][:100]}{'...' if len(msg['message']) > 100 else ''}
                </div>
                <div style="font-style: italic; color: #666; margin-top: 5px;">
                    — {msg['name']}{f" ({msg['relationship']})" if msg.get('relationship') else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Message count
if st.session_state.messages:
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col2:
        st.metric("Total Messages Sent", len(st.session_state.messages))

# Footer section
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center;">
        <p style="color: #666; font-style: italic;">
            🎂 Help make this birthday celebration extra special! 🎂
        </p>
        <p style="font-size: 12px; color: #999;">
            All messages are saved permanently and will be displayed
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar with message tips
with st.sidebar:
    st.markdown("### 💡 Message Ideas")
    st.markdown("""
    **What to include:**
    - 🎂 Birthday wishes
    - 💕 What they mean to you
    - 📸 Favorite memories
    - 🌟 Hopes for their new year
    - 😊 Something that makes you smile about them
    """)

    st.markdown("---")
    st.markdown("### 📊 Message Stats")
    if st.session_state.messages:
        st.metric("Messages Today", len(st.session_state.messages))

        # Show relationship breakdown
        relationships = [msg.get('relationship') for msg in st.session_state.messages if msg.get('relationship')]
        if relationships:
            st.markdown("**Relationships:**")
            rel_counts = {}
            for rel in relationships:
                rel_counts[rel] = rel_counts.get(rel, 0) + 1

            for rel, count in sorted(rel_counts.items()):
                st.markdown(f"- {rel}: {count}")
    else:
        st.info("No messages yet - be the first!")