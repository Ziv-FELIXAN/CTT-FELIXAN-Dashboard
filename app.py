import streamlit as st
import sqlite3
import json
from datetime import datetime
import sys
import os

# Add the 'static/modules' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'modules')))

# Import the module
from static.modules.members_private import display_members_private

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
if 'members_private' not in st.session_state:
    st.session_state['members_private'] = [
        {"name": "John Doe", "join_date": "2024-01-15", "status": "Active", "verification": "Complete", "security": "High", "premium": "Yes"},
    ]
if 'activities_private' not in st.session_state:
    st.session_state['activities_private'] = [
        {"activity": "Loan Application Submitted", "date": "2025-03-01"},
        {"activity": "Carat Transaction", "amount": "$50,000", "date": "2025-03-02"}
    ]

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

# Header with background image and color strip
header_color = st.session_state['users'][st.session_state['interface_type']]['color']
st.markdown(
    f"<div style='background-image: url(\"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1500&q=80\"); background-size: cover; background-position: center; padding: 20px; text-align: center; position: relative;'>"
    f"<h1 style='color: white;'><i class='fas fa-house'></i> CTT/FELIXAN System Ver3 - {st.session_state['interface_type']}</h1>"
    "<div style='position: absolute; top: 10px; right: 10px;'>"
    "<button style='background: none; border: none; color: white; font-size: 20px; cursor: pointer;' onclick='alert(\"Preferences not implemented yet.\")'>⚙️</button>"
    " "
    "<button style='background: none; border: none; color: white; font-size: 20px; cursor: pointer;' onclick='alert(\"User Management not implemented yet.\")'>👤</button>"
    "</div>"
    "</div>"
    f"<div style='background-color: {header_color}; height: 20px; width: 100%;'></div>",
    unsafe_allow_html=True
)

# Spacer
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# Navigation buttons
st.markdown(
    "<style>"
    ".nav-buttons {display: flex; justify-content: flex-start; gap: 5px; margin-top: 20px; flex-wrap: wrap; align-items: flex-start;}"
    ".nav-buttons .stButton {margin-right: 5px; flex: 0 0 auto;}"
    ".nav-buttons .stButton>button {padding: 8px 16px; background-color: #f1f1f1; border: none; border-radius: 5px; cursor: pointer; text-align: left; width: auto; display: inline-block;}"
    ".nav-buttons .stButton>button:hover {background-color: #e0e0e0;}"
    "</style>",
    unsafe_allow_html=True
)
nav_container = st.container()
with nav_container:
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("FELIXAN Management", key="management-btn"):
            st.session_state['interface_type'] = "Management"
            st.session_state['selected_module'] = "Dashboard"
            st.rerun()
    with col2:
        if st.button("Private Individuals", key="private-btn"):
            st.session_state['interface_type'] = "Private"
            st.session_state['selected_module'] = "Dashboard"
            st.rerun()
    with col3:
        if st.button("Business", key="business-btn"):
            st.session_state['interface_type'] = "Business"
            st.session_state['selected_module'] = "Dashboard"
            st.rerun()
    with col4:
        about_option = st.selectbox("About", ["Select", "System Info", "Help"], key="about_dropdown")
        if about_option != "Select":
            st.write(f"Selected: {about_option} (Content to be added later)")

# Module navigation
st.markdown(
    "<style>"
    ".module-nav {display: flex; justify-content: flex-start; gap: 5px; margin-top: 10px; flex-wrap: wrap; align-items: flex-start;}"
    ".module-nav .stButton {margin-right: 5px; flex: 0 0 auto;}"
    ".module-nav .stButton>button {padding: 8px 16px; background-color: #f1f1f1; border: none; border-radius: 5px; cursor: pointer; text-align: left; width: auto; display: inline-block;}"
    ".module-nav .stButton>button:hover {background-color: #e0e0e0;}"
    ".module-content {border: 1px solid #e6e6e6; padding: 10px; border-radius: 5px;}"
    "</style>",
    unsafe_allow_html=True
)
module_container = st.container()
with module_container:
    st.write("Modules:")
    modules = st.session_state['users'][st.session_state['interface_type']]["modules"]
    module_cols = st.columns(len(modules))
    for i, module in enumerate(modules):
        with module_cols[i]:
            if st.button(module, key=f"module_{i}"):
                st.session_state['selected_module'] = module
                st.rerun()

# Main content area with tabs
st.session_state['tabs'] = st.tabs(["Overview", "Manage Objects", "Checklist", "Related Assets"])

# Display module content based on selection
if st.session_state['selected_module'] == "Members" and st.session_state['interface_type'] == "Private":
    display_members_private()
elif st.session_state['selected_module'] == "Dashboard":
    with st.session_state['tabs'][0]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Dashboard Overview</h3>"
            "<p>Welcome to your Dashboard! Here you can see a summary of your activities and status.</p>"
            "</div>",
            unsafe_allow_html=True
        )
    with st.session_state['tabs'][1]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Manage Dashboard Objects</h3>"
            "<p>No objects to manage in the Dashboard.</p>"
            "</div>",
            unsafe_allow_html=True
        )
    with st.session_state['tabs'][2]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Dashboard Checklist</h3>"
            "<p>No checklist items for the Dashboard.</p>"
            "</div>",
            unsafe_allow_html=True
        )
    with st.session_state['tabs'][3]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Related Assets for Dashboard</h3>"
            "<p>No related assets for the Dashboard.</p>"
            "</div>",
            unsafe_allow_html=True
        )
else:
    with st.session_state['tabs'][0]:
        st.markdown(
            "<div class='module-content'>"
            f"<h3>{st.session_state['selected_module']} Overview</h3>"
            "Content for Overview tab (to be implemented)."
            "</div>",
            unsafe_allow_html=True
        )
    with st.session_state['tabs'][1]:
        st.markdown(
            "<div class='module-content'>"
            f"<h3>Manage {st.session_state['selected_module']} Objects</h3>"
            "Content for Manage Objects tab (to be implemented)."
            "</div>",
            unsafe_allow_html=True
        )
    with st.session_state['tabs'][2]:
        st.markdown(
            "<div class='module-content'>"
            f"<h3>{st.session_state['selected_module']} Checklist</h3>"
            "Content for Checklist tab (to be implemented)."
            "</div>",
            unsafe_allow_html=True
        )
    with st.session_state['tabs'][3]:
        st.markdown(
            "<div class='module-content'>"
            f"<h3>Related Assets for {st.session_state['selected_module']}</h3>"
            "Content for Related Assets tab (to be implemented)."
            "</div>",
            unsafe_allow_html=True
        )

# Footer
st.markdown(
    f"<div style='background-color: #f1f1f1; padding: 10px; text-align: center; margin-top: 20px;'>"
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
