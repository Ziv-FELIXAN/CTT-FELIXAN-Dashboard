import streamlit as st
import sqlite3
import json
from datetime import datetime
import sys
import os

# Add the 'static/modules' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'modules')))

# Import the module directly
from members_private import display_members_private

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
