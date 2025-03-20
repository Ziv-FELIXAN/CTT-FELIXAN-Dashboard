import streamlit as st
import sqlite3
import json
from datetime import datetime

def setup_general_ui():
    # Initialize session state for interface and users
    if 'interface_type' not in st.session_state:
        st.session_state['interface_type'] = 'Management'
    if 'users' not in st.session_state:
        st.session_state['users'] = {
            "Private": {"type": "Private", "modules": ["Dashboard", "Members", "Loans Regular", "Assets", "Contracts", "Carat", "Triple C"], "color": "#E74C3C"},  # Red for Private
            "Business": {"type": "Business", "modules": ["Dashboard", "Members", "Loans Regular", "Carat Letter of Credit", "Assets", "Contracts", "Carat", "Triple C", "Secure Transport", "Bids", "Exchange", "Meeting Room"], "color": "#1E3A8A"},
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
    c.execute("INSERT OR REPLACE INTO versions (version, data, timestamp) VALUES (?, ?, ?)", (current_version, current_data, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

    # Header with background image and color strip
    header_color = st.session_state['users'][st.session_state['interface_type']]['color']
    st.markdown(
        f"<div style='background-image: url(\"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1500&q=80\"); background-size: cover; background-position: center; padding: 20px; text-align: center; position: relative;'>"
        f"<h1 style='color: white; font-size: 24px;'><i class='fas fa-house'></i> CTT/FELIXAN System Ver3 - {st.session_state['interface_type']}</h1>"
        "<div style='position: absolute; top: 10px; right: 10px;'>"
        "<button style='background: none; border: none; color: white; font-size: 20px; cursor: pointer;' onclick='alert(\"Preferences not implemented yet.\")'><i class='fas fa-cog'></i></button>"
        " "
        "<button style='background: none; border: none; color: white; font-size: 20px; cursor: pointer;' onclick='alert(\"User Management not implemented yet.\")'><i class='fas fa-user-circle'></i></button>"
        "</div>"
        "</div>"
        f"<div style='background-color: {header_color}; height: 15px; width: 100%;'></div>",
        unsafe_allow_html=True
    )

    # Spacer
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    # Navigation buttons
    st.markdown(
        "<style>"
        ".nav-buttons {display: flex; justify-content: flex-start; gap: 5px; margin-top: 15px; flex-wrap: wrap; align-items: flex-start;}"
        ".nav-buttons .stButton {margin-right: 5px; flex: 0 0 auto;}"
        ".nav-buttons .stButton>button {padding: 5px 10px; background-color: #f1f1f1; border: none; border-radius: 5px; cursor: pointer; text-align: left; width: auto; display: inline-block; font-size: 14px;}"
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

    return conn, c, current_version

def setup_version_management(conn, c, current_version):
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

    # Close database connection
    conn.close()
