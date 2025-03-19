import streamlit as st

# Initialize session state for interface
if 'interface_type' not in st.session_state:
    st.session_state.interface_type = 'management'

# Simulated user data
users = {
    "Private": {"type": "Private", "modules": ["Dashboard", "Members", "Loans Regular", "Assets", "Contracts", "Carat", "Triple C"], "color": "#4CAF50"},
    "Business": {"type": "Business", "modules": ["Dashboard", "Members", "Loans Regular", "Carat Letter of Credit", "Assets", "Contracts", "Carat", "Triple C", "Secure Transport", "Bids", "Exchange", "Meeting Room"], "color": "#F39C12"},
    "Management": {"type": "Management", "modules": ["Dashboard", "Members", "Loans Regular", "Carat Letter of Credit", "Assets", "Contracts", "Carat", "Triple C", "Insurance", "Transactions Audit", "Secure Transport", "Bids", "Exchange", "System Revenue", "Meeting Room"], "color": "#2C3E50"}
}

# Header
st.markdown(f"""
<div style='background-color: {users[st.session_state.interface_type]['color']}; padding: 10px; text-align: center;'>
    <h1 style='color: white;'>CTT/FELIXAN System Ver3</h1>
</div>
""", unsafe_allow_html=True)

# Navigation buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("FELIXAN Management"):
        st.session_state.interface_type = "Management"
        st.rerun()
with col2:
    if st.button("Private Individuals"):
        st.session_state.interface_type = "Private"
        st.rerun()
with col3:
    if st.button("Business"):
        st.session_state.interface_type = "Business"
        st.rerun()

# Module navigation
st.write("Modules:")
modules = users[st.session_state.interface_type]["modules"]
module_cols = st.columns(len(modules))
for i, module in enumerate(modules):
    with module_cols[i]:
        st.button(module, key=f"module_{i}")

# Main content area
st.write("Main Content Area:")
st.write("Select a module to view content.")

# Footer
st.markdown("""
<div style='background-color: #f1f1f1; padding: 10px; text-align: center;'>
    <p>System Status: Online | Version: VER
