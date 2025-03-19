import streamlit as st
import sqlite3
import json
from datetime import datetime

# Set page layout to wide
st.set_page_config(layout="wide")

# Initialize session state for interface and users
if 'interface_type' not in st.session_state:
    st.session_state['interface_type'] = 'Management'
if 'users' not in st.session_state:
    st.session_state['users'] = {
        "Private": {"type": "Private", "modules": ["Dashboard", "Members", "Loans Regular", "Assets", "Contracts", "Carat", "Triple C"], "color": "#4CAF50"},
        "Business": {"type": "Business", "modules": ["Dashboard", "Members", "Loans Regular", "Carat Letter of Credit", "Assets", "Contracts", "Carat", "Triple C", "Secure Transport", "Bids", "Exchange", "Meeting Room"], "color": "#F39C12"},
        "Management": {"type": "Management", "modules": ["Dashboard", "Members", "Loans Regular", "Carat Letter of Credit", "Assets", "Contracts", "Carat", "Triple C", "Insurance", "Transactions Audit", "Secure Transport", "Bids", "Exchange", "System Revenue", "Meeting Room"], "color": "#2C3E50"}
    }
if 'selected_module' not in st.session_state:
    st.session_state['selected_module'] = 'Dashboard'

# Version management with SQLite
conn = sqlite3.connect('versions.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS versions (version TEXT PRIMARY KEY, data TEXT, timestamp TEXT)''')
conn.commit()

# Save current version
current_version = "VER3"
current_data = json.dumps(st.session_state['users'])
c.execute("INSERT OR REPLACE INTO versions (version, data, timestamp) VALUES (?, ?, ?)",
          (current_version, current_data, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
conn.commit()

# Data management with SQLite
data_conn = sqlite3.connect('data.db', check_same_thread=False)
data_c = data_conn.cursor()
data_c.execute('''CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY AUTOINCREMENT, user_type TEXT, name TEXT, status TEXT)''')
data_conn.commit()

# Header
header_color = st.session_state['users'][st.session_state['interface_type']]['color']
st.markdown(
    f"<div style='background-color: {header_color}; padding: 10px; text-align: center;'>"
    "<h1 style='color: white;'>CTT/FELIXAN System Ver3</h1>"
    "</div>",
    unsafe_allow_html=True
)

# Navigation buttons
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("FELIXAN Management"):
        st.session_state['interface_type'] = "Management"
        st.session_state['selected_module'] = "Dashboard"
        st.rerun()
with col2:
    if st.button("Private Individuals"):
        st.session_state['interface_type'] = "Private"
        st.session_state['selected_module'] = "Dashboard"
        st.rerun()
with col3:
    if st.button("Business"):
        st.session_state['interface_type'] = "Business"
        st.session_state['selected_module'] = "Dashboard"
        st.rerun()
with col4:
    about_option = st.selectbox("About", ["Select", "System Info", "Help"], key="about_dropdown")
    if about_option != "Select":
        st.write(f"Selected: {about_option} (Content to be added later)")

# Module navigation
st.write("Modules:")
modules = st.session_state['users'][st.session_state['interface_type']]["modules"]
module_cols = st.columns(len(modules))
for i, module in enumerate(modules):
    with module_cols[i]:
        if st.button(module, key=f"module_{i}"):
            st.session_state['selected_module'] = module
            st.rerun()

# Main content area with tabs
st.write("Main Content Area:")
tabs = ["Overview", "Manage Objects", "Checklist", "Related Assets"]
selected_tab = st.tabs(tabs)
with selected_tab[0]:
    st.write(f"{st.session_state['selected_module']} Overview")
    st.write("Content for Overview tab (to be implemented).")
with selected_tab[1]:
    st.write(f"Manage {st.session_state['selected_module']} Objects")
    st.write("Content for Manage Objects tab (to be implemented).")
with selected_tab[2]:
    st.write(f"{st.session_state['selected_module']} Checklist")
    st.write("Content for Checklist tab (to be implemented).")
with selected_tab[3]:
    st.write(f"Related Assets for {st.session_state['selected_module']}")
    st.write("Content for Related Assets tab (to be implemented).")

# Footer
st.markdown(
    f"<div style='background-color: #f1f1f1; padding: 10px; text-align: center;'>"
    f"<p>System Status: Online | Version: {current_version} | Date: 18/03/2025 | © System copyright Ziv Rotem-Bar 2025</p>"
    "</div>",
    unsafe_allow_html=True
)

# Version management section (below footer)
st.write("Version Management (Admin Only):")
c.execute("SELECT version, timestamp FROM versions ORDER BY timestamp DESC")
versions = c.fetchall()
if versions:
    selected_version = st.selectbox("Select Version to Restore", [f"{v[0]} (Saved at: {v[1]})" for v in versions])
    if st.button("Restore Selected Version"):
        confirm = st.button("Confirm Restore? This will overwrite current data!")
        if confirm:
            version_to_restore = selected_version.split(" ")[0]
            c.execute("SELECT data FROM versions WHERE version = ?", (version_to_restore,))
            data = c.fetchone()
            if data:
                st.session_state['users'] = json.loads(data[0])
                st.success(f"Restored version {version_to_restore}!")
                st.rerun()
else:
    st.write("No versions available to restore.")

conn.close()
data_conn.close()
