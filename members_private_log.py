from templates import render_table

def display_members_private_log():
    """Display the Log tab for Members - Private."""
    st.markdown(
        "<div class='module-content'>"
        "<h3>Activity Log</h3>",
        unsafe_allow_html=True
    )

    # Option to enable/disable notifications
    st.subheader("Notification Settings")
    notify_user = st.checkbox("Send notifications to email/phone for each action", value=st.session_state['notify_user'])
    if notify_user != st.session_state['notify_user']:
        st.session_state['notify_user'] = notify_user
        st.success("Notification settings updated!")

    # Display log table
    st.subheader("Log Entries")
    columns = [
        {"name": "Action ID", "field": "action_id"},
        {"name": "Action Type", "field": "action_type"},
        {"name": "Object ID", "field": "object_id"},
        {"name": "Details", "field": "details"},
        {"name": "Timestamp", "field": "timestamp"}
    ]
    render_table(st.session_state['action_log'], columns)

    st.markdown("</div>", unsafe_allow_html=True)
