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

# Members section with management table and checkboxes
st.write("Members List:")
members_list = st.session_state.members[user_type]
selected_indices = []
for i, member in enumerate(members_list):
    col1, col2 = st.columns([1, 4])
    with col1:
        checked = st.checkbox("", key=f"checkbox_{i}")
    with col2:
        st.write(member)
    if checked:
        selected_indices.append(i)
if selected_indices and st.button("Delete Selected Members"):
    if st.button(f"Confirm delete {len(selected_indices)} member(s)?"):
        for i in sorted(selected_indices, reverse=True):
            del st.session_state.members[user_type][i]
        st.success(f"Deleted {len(selected_indices)} member(s) from {user_type}!")
        st.rerun()

# Add/Edit member
new_member = st.text_input("Add/Edit Member Name")
if st.button("Add Member"):
    if new_member and new_member not in st.session_state.members[user_type]:
        st.session_state.members[user_type].append(new_member)
        st.success(f"Added {new_member} to {user_type} members!")
        st.rerun()

# Footer with system info
st.write(f"System Status: Online | Version: VER3 | Date: 18/03/2025 | © System copyright Ziv Rotem-Bar 2025")

# Refresh functionality
if st.button("Refresh Dashboard"):
    st.rerun()
