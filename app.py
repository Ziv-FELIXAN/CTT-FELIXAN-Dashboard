import streamlit as st
import pandas as pd

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

# Footer with system info
st.write(f"System Status: Online | Version: VER3 | Date: 18/03/2025 | © System copyright Ziv Rotem-Bar 2025")

# Refresh functionality
if st.button("Refresh Dashboard"):
    st.experimental_rerun()
