import streamlit as st
from datetime import datetime
import json
import os
import base64

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
    # Try main file first
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # Try backup file if main file fails
    backup_file = f"./{MESSAGES_FILE}.backup"
    if os.path.exists(backup_file):
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Restore main file from backup
                save_messages(data)
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    return []

# Function to save messages to file
def save_messages(messages):
    try:
        # Ensure the file is created with proper permissions
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        # Verify the file was written correctly
        with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
            verification = json.load(f)
            if len(verification) != len(messages):
                st.error("Warning: File save verification failed")
    except Exception as e:
        st.error(f"Error saving messages: {e}")
        # Try alternative storage location
        try:
            backup_file = f"./{MESSAGES_FILE}.backup"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(messages, f, indent=2, ensure_ascii=False)
            st.warning(f"Messages saved to backup location: {backup_file}")
        except:
            st.error("Failed to save to backup location as well")

# Function to encode uploaded image to base64
def encode_image(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        base64_string = base64.b64encode(bytes_data).decode()
        return base64_string
    return None

# Function to display image from base64
def display_image(base64_string, width=200):
    if base64_string:
        st.image(f"data:image/jpeg;base64,{base64_string}", width=width)

# Initialize session state for messages and likes
if 'messages' not in st.session_state:
    st.session_state.messages = load_messages()

# Initialize likes for existing messages
for i, msg in enumerate(st.session_state.messages):
    if 'likes' not in msg:
        msg['likes'] = 0
    if 'comments' not in msg:
        msg['comments'] = []

# Header section with birthday celebration
st.title("🎉 Happy Birthday Mom! 🎂")

# Instructions for visitors
st.info("🎉 **Welcome to the birthday celebration!** Click the buttons below for fun animations, then scroll down to leave your birthday message. You can also like and comment on messages from others!")

# Fun celebration buttons
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🎈 Balloons"):
        st.balloons()
with col2:
    if st.button("🎊 Confetti"):
        st.snow()
with col3:
    if st.button("🎉 Party"):
        st.balloons()
        st.snow()
with col4:
    st.markdown("🎂")
with col5:
    st.markdown("💕")

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
                "Son", "Daughter", "Husband", "Wife",
                # Children & Grandchildren
                "Grandson", "Granddaughter",
                # Parents & Grandparents
                "Mother", "Father",
                # Siblings
                "Sister", "Brother",
                # Extended Family - Aunts/Uncles
                "Aunt", "Uncle",
                # Extended Family - Cousins
                "Cousin",
                # In-Laws
                "Mother-in-Law", "Father-in-Law", "Sister-in-Law", "Brother-in-Law",
                "Daughter-in-Law", "Son-in-Law",
                # Nieces/Nephews
                "Niece", "Nephew",
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
    
    # Photo upload option
    uploaded_photo = st.file_uploader(
        "📸 Add a Photo (Optional)",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a photo to include with your message"
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
            # Encode photo if uploaded
            photo_data = None
            if uploaded_photo is not None:
                photo_data = encode_image(uploaded_photo)
            
            # Create message entry
            new_message = {
                'name': sender_name.strip(),
                'relationship': relationship if relationship else None,
                'message': message.strip(),
                'timestamp': datetime.now().strftime("%B %d, %Y at %I:%M %p"),
                'photo': photo_data,
                'likes': 0,
                'comments': []
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
    
    # Show persistence status
    if os.path.exists(MESSAGES_FILE):
        st.success("✅ Messages are being saved permanently")
    else:
        st.warning("⚠️ Message file not found - creating new storage")
    
    # Display messages in reverse order (newest first)
    for i, msg in enumerate(reversed(st.session_state.messages)):
        actual_index = len(st.session_state.messages) - 1 - i
        with st.container():
            # Message card with enhanced features
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Message content
                st.markdown(f"**💌 {msg['message']}**")
                
                # Display photo if included
                if msg.get('photo'):
                    display_image(msg['photo'], width=300)
                
                # Signature line
                signature = f"— {msg['name']}"
                if msg.get('relationship'):
                    signature += f" ({msg['relationship']})"
                
                st.markdown(f"*{signature}*")
                st.caption(f"Sent on {msg['timestamp']}")
                
                # Like and comment system
                col_like, col_comment, col_count = st.columns([1, 1, 2])
                
                with col_like:
                    if st.button("❤️ Like", key=f"like_{actual_index}"):
                        st.session_state.messages[actual_index]['likes'] += 1
                        save_messages(st.session_state.messages)
                        st.rerun()
                
                with col_comment:
                    if st.button("💬 Comment", key=f"comment_btn_{actual_index}"):
                        st.session_state[f"show_comment_{actual_index}"] = not st.session_state.get(f"show_comment_{actual_index}", False)
                        st.rerun()
                
                with col_count:
                    st.caption(f"❤️ {msg.get('likes', 0)} likes • 💬 {len(msg.get('comments', []))} comments")
                
                # Comment section
                if st.session_state.get(f"show_comment_{actual_index}", False):
                    with st.expander("💬 Comments", expanded=True):
                        # Show existing comments
                        for comment in msg.get('comments', []):
                            st.markdown(f"**{comment['name']}:** {comment['text']}")
                            st.caption(f"Posted on {comment['timestamp']}")
                            st.markdown("---")
                        
                        # Add new comment
                        with st.form(f"comment_form_{actual_index}"):
                            comment_name = st.text_input("Your name", key=f"comment_name_{actual_index}")
                            comment_text = st.text_area("Add a comment", key=f"comment_text_{actual_index}")
                            
                            if st.form_submit_button("Post Comment"):
                                if comment_name.strip() and comment_text.strip():
                                    new_comment = {
                                        'name': comment_name.strip(),
                                        'text': comment_text.strip(),
                                        'timestamp': datetime.now().strftime("%B %d, %Y at %I:%M %p")
                                    }
                                    if 'comments' not in st.session_state.messages[actual_index]:
                                        st.session_state.messages[actual_index]['comments'] = []
                                    st.session_state.messages[actual_index]['comments'].append(new_comment)
                                    save_messages(st.session_state.messages)
                                    st.success("Comment added!")
                                    st.rerun()
                                else:
                                    st.error("Please enter your name and comment")
            
            with col2:
                # Message decoration
                st.markdown(f"<div style='text-align: center; font-size: 24px;'>🎈</div>", 
                           unsafe_allow_html=True)
            
            st.markdown("---")
else:
    # Empty state
    st.subheader("💕 Birthday Messages")
    st.info("No messages yet. Be the first to wish her a happy birthday! 🎂")

# Admin section with password protection
st.markdown("---")
st.markdown("### 🔧 Admin Controls")

# Initialize admin state
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    # Password input
    admin_password = st.text_input("Enter admin password:", type="password", key="admin_pass")
    if st.button("Login as Admin"):
        if admin_password == "admin123":
            st.session_state.admin_authenticated = True
            st.success("Admin access granted!")
            st.rerun()
        else:
            st.error("Incorrect password")
else:
    st.success("Admin mode active")
    
    # Admin controls
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚪 Logout Admin"):
            st.session_state.admin_authenticated = False
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear All Messages"):
            if st.button("⚠️ Confirm Clear All", key="confirm_clear"):
                st.session_state.messages = []
                save_messages([])
                st.success("All messages cleared!")
                st.rerun()
    
    # Individual message deletion
    if st.session_state.messages:
        st.markdown("#### Delete Individual Messages")
        for i, msg in enumerate(st.session_state.messages):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                signature = f"{msg['name']}"
                if msg.get('relationship'):
                    signature += f" ({msg['relationship']})"
                st.markdown(f"**{signature}:** {msg['message'][:50]}...")
                st.caption(f"Sent on {msg['timestamp']}")
            
            with col2:
                if st.button("🗑️", key=f"delete_{i}", help="Delete this message"):
                    st.session_state.messages.pop(i)
                    save_messages(st.session_state.messages)
                    st.success("Message deleted!")
                    st.rerun()

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
    
    # Admin controls for message management
    if st.session_state.messages:
        st.markdown("### Admin Actions")
        with st.expander("🔒 Admin Controls"):
            admin_password = st.text_input("Admin Password", type="password", help="Enter password to access admin controls")
            if admin_password == "admin123":
                st.markdown("**Message Management:**")
                
                # Clear all messages button
                if st.button("🗑️ Clear All Messages", help="This will remove all messages"):
                    st.session_state.messages = []
                    save_messages(st.session_state.messages)
                    st.success("All messages cleared!")
                    st.rerun()
                
                st.markdown("---")
                st.markdown("**Delete Individual Messages:**")
                
                # Display each message with delete button
                for i, msg in enumerate(st.session_state.messages):
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            # Show message preview
                            preview = msg['message'][:60] + "..." if len(msg['message']) > 60 else msg['message']
                            relationship_text = f"({msg['relationship']})" if msg.get('relationship') else "(No relationship)"
                            st.markdown(f"**{msg['name']}** {relationship_text}")
                            st.caption(f"{preview}")
                            st.caption(f"Sent: {msg['timestamp']}")
                        
                        with col2:
                            # Delete button for this specific message
                            if st.button("❌", key=f"delete_{i}", help=f"Delete message from {msg['name']}"):
                                # Remove the message at index i
                                st.session_state.messages.pop(i)
                                save_messages(st.session_state.messages)
                                st.success(f"Message from {msg['name']} deleted!")
                                st.rerun()
                        
                        st.markdown("---")
                        
            elif admin_password:
                st.error("Incorrect password")
