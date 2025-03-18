import streamlit as st
import pandas as pd

# Initialize session state for members
if 'members' not in st.session_state:
    st.session_state.members = {
        "Private": ["Ziv"],
        "Business": ["ZivCorp"],
        "Management": ["Admin"]
    }

# Simulated user data
users = {
    "Private": {"type": "Private", "modules": ["Dashboard", "Members", "Loans Regular", "Assets", "Contracts", "Carat", "Triple C"], "color": "#4CAF50"},
    "Business": {"type": "Business", "modules": ["Dashboard", "Members", "Loans Regular", "Carat Letter of Credit", "Assets", "Contracts", "Carat", "Triple C", "Secure Transport", "Bids", "Exchange", "Meeting Room"], "color": "#F39C12"},
    "Management": {"type": "Management", "modules": ["Dashboard", "Members", "Loans Regular", "Carat Letter of Credit", "Assets", "Contracts", "Carat", "Triple C", "Insurance", "Transactions Audit", "Secure Transport", "Bids", "Exchange", "System Revenue", "Meeting Room"], "color": "#2C3E50"}
}

# Dashboard UI
st.title("CTT/FELIXAN Dashboard")
user_type = st.selectbox("Select User Type", ["Private", "Business", "Management"])
user = users[user_type]

# Header with dynamic color
st.markdown(f"<h2 style='color: {user['color']};'>Welcome, {user_type} User</h2>", unsafe_allow_html=True)

# Display modules in a table
st.write("Available Modules:")
df = pd.DataFrame({"Module": user["modules"], "Status": ["Active"] * len(user["modules"])})
st.table(df)

# Members section with management table and edit
st.write("Members List:")
members_df = pd.DataFrame({"Name": st.session_state.members[user_type], "Actions": ["Edit | Delete"] * len(st.session_state.members[user_type])})
st.table(members_df)

# Add/Edit member
new_member = st.text_input("Add/Edit Member Name")
if st.button("Add Member"):
    if new_member and new_member not in st.session_state.members[user_type]:
        st.session_state.members[user_type].append(new_member)
        st.success(f"Added {new_member} to {user_type} members!")
        st.rerun()

# Delete member
if st.button("Delete Selected Member"):
    selected_member = st.session_state.members[user_type][0] if st.session_state.members[user_type] else None
    if selected_member:
        st.session_state.members[user_type].remove(selected_member)
        st.success(f"Deleted {selected_member} from {user_type} members!")
        st.rerun()

# Footer with system info
st.write(f"System Status: Online | Version: VER3 | Date: 18/03/2025 | © System copyright Ziv Rotem-Bar 2025")

# Refresh functionality
if st.button("Refresh Dashboard"):
    st.rerun()
