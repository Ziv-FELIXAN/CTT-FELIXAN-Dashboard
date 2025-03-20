import streamlit as st
from members_private import display_members_private

def manage_modules():
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
    st.session_state['tabs'] = st.tabs(["Overview", "Manage Objects", "Checklist", "Related Assets", "Log"])

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
        with st.session_state['tabs'][4]:
            st.markdown(
                "<div class='module-content'>"
                "<h3>Activity Log</h3>"
                "<p>No activities logged yet for the Dashboard.</p>"
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
        with st.session_state['tabs'][4]:
            st.markdown(
                "<div class='module-content'>"
                "<h3>Activity Log</h3>"
                "<p>No activities logged yet for this module.</p>"
                "</div>",
                unsafe_allow_html=True
            )
