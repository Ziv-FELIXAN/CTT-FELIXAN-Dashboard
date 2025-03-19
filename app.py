import streamlit as st

# Set page layout to wide
st.set_page_config(layout="wide")

# Initialize session state for interface
if 'interface_type' not in st.session_state:
    st.session_state['interface_type'] = 'Management'

# Simulated user data
users = {
    "Private": {"type": "Private", "modules": ["Dashboard", "Members", "Loans Regular", "Assets", "Contracts", "Carat", "Triple C"], "color": "#4CAF50"},
    "Business": {"type": "Business", "modules": ["Dashboard", "Members", "Loans Regular", "Carat Letter of Credit", "Assets", "Contracts", "Carat", "Triple C", "Secure Transport", "Bids", "Exchange", "Meeting Room"], "color": "#F39C12"},
    "Management": {"type": "Management", "modules": ["Dashboard", "Members", "Loans Regular", "Carat Letter of Credit", "Assets", "Contracts", "Carat", "Triple C", "Insurance", "Transactions Audit", "Secure Transport", "Bids", "Exchange", "System Revenue", "Meeting Room"], "color": "#2C3E50"}
}

# Header
header_color = users[st.session_state['interface_type']]['color']
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
        st.rerun()
with col2:
    if st.button("Private Individuals"):
        st.session_state['interface_type'] = "Private"
        st.rerun()
with col3:
    if st.button("Business"):
        st.session_state['interface_type'] = "Business"
        st.rerun()
with col4:
    about_option = st.selectbox("About", ["Select", "System Info", "Help"], key="about_dropdown")
    if about_option != "Select":
        st.write(f"Selected: {about_option} (Content to be added later)")

# Module navigation
st.write("Modules:")
modules = users[st.session_state['interface_type']]["modules"]
module_cols = st.columns(len(modules))
for i, module in enumerate(modules):
    with module_cols[i]:
        st.button(module, key=f"module_{i}")

# Main content area
st.write("Main Content Area:")
st.write("Select a module to view content.")

# Footer
st.markdown(
    "<div style='background-color: #f1f1f1; padding: 10px; text-align: center;'>"
    "<p>System Status: Online | Version: VER3 | Date: 18/03/2025 | © System copyright Ziv Rotem-Bar 2025</p>"
    "</div>",
    unsafe_allow_html=True
)
