from templates import render_table

def display_members_private_manage(activities, non_active_activities, log_action):
    """Display the Manage Objects tab for Members - Private."""
    st.markdown(
        "<div class='module-content'>"
        "<h3>Manage Members Activities</h3>",
        unsafe_allow_html=True
    )

    # Display active activities table
    st.subheader("Active Activities")
    columns = [
        {"name": "ID", "field": "id"},
        {"name": "Activity", "field": "activity"},
        {"name": "Date", "field": "date"},
        {"name": "Amount", "field": "amount"}
    ]
    actions = [
        {"icon": "fas fa-edit", "action": "edit", "title": "Edit Activity"},
        {"icon": "fas fa-trash-alt", "action": "delete", "title": "Move to Non-Active"}
    ]
    render_table(activities, columns, actions, "selected_activities")

    # Handle actions
    for activity in activities:
        # Edit activity
        if f"edit_button_{activity['id']}" in st.session_state:
            st.session_state[f"edit_activity_{activity['id']}"] = True
        if f"edit_activity_{activity['id']}" in st.session_state and st.session_state[f"edit_activity_{activity['id']}"]:
            with st.form(key=f"edit_activity_form_{activity['id']}"):
                st.subheader(f"Edit Activity: {activity['activity']}")
                new_activity_type = st.text_input("Activity Type", value=activity['activity'])
                new_activity_date = st.text_input("Date (YYYY-MM-DD)", value=activity['date'])
                new_activity_amount = st.text_input("Amount (optional)", value=activity['amount'] if activity['amount'] else "")
                edit_submit = st.form_submit_button("Save Changes")
                if edit_submit:
                    old_activity_type = activity['activity']
                    for act in st.session_state['activities']:
                        if act['id'] == activity['id']:
                            act['activity'] = new_activity_type
                            act['date'] = new_activity_date
                            act['amount'] = new_activity_amount if new_activity_amount else None
                            break
                    log_action("Edit Activity", activity['id'], f"Edited activity: {old_activity_type} to {new_activity_type}")
                    st.success("Activity updated successfully!")
                    st.session_state[f"edit_activity_{activity['id']}"] = False
                    st.rerun()
        # Delete activity (move to non-active)
        if f"delete_button_{activity['id']}" in st.session_state:
            st.session_state[f"delete_activity_{activity['id']}"] = True
        if f"delete_activity_{activity['id']}" in st.session_state and st.session_state[f"delete_activity_{activity['id']}"]:
            with st.form(key=f"delete_activity_form_{activity['id']}"):
                st.subheader(f"Delete Activity: {activity['activity']}")
                st.write("Are you sure you want to move this activity to Non-Active Projects?")
                confirm_delete = st.text_input("Type the activity name to confirm", placeholder=activity['activity'])
                delete_submit = st.form_submit_button("Confirm Move to Non-Active")
                if delete_submit:
                    if confirm_delete == activity['activity']:
                        for act in st.session_state['activities']:
                            if act['id'] == activity['id']:
                                act['is_active'] = False
                                break
                        log_action("Move to Non-Active", activity['id'], f"Moved activity to Non-Active: {activity['activity']}")
                        st.success("Activity moved to Non-Active Projects!")
                        st.session_state[f"delete_activity_{activity['id']}"] = False
                        st.rerun()
                    else:
                        st.error("Activity name does not match. Action cancelled.")

    # Display non-active activities table
    st.subheader("Non-Active Projects")
    columns = [
        {"name": "ID", "field": "id"},
        {"name": "Activity", "field": "activity", "style": "color: red;"},
        {"name": "Date", "field": "date", "style": "color: red;"},
        {"name": "Amount", "field": "amount", "style": "color: red;"}
    ]
    actions = [
        {"icon": "fas fa-undo-alt", "action": "restore", "title": "Restore to Active"},
        {"icon": "fas fa-trash-alt", "action": "permanent_delete", "title": "Permanently Delete"}
    ]
    render_table(non_active_activities, columns, actions, "selected_non_active_activities")

    # Handle actions
    for activity in non_active_activities:
        # Restore activity
        if f"restore_button_{activity['id']}" in st.session_state:
            st.session_state[f"restore_activity_{activity['id']}"] = True
        if f"restore_activity_{activity['id']}" in st.session_state and st.session_state[f"restore_activity_{activity['id']}"]:
            with st.form(key=f"restore_activity_form_{activity['id']}"):
                st.subheader(f"Restore Activity: {activity['activity']}")
                st.write("Are you sure you want to restore this activity to Active Projects?")
                confirm_restore = st.text_input("Type the activity name to confirm", placeholder=activity['activity'])
                restore_submit = st.form_submit_button("Confirm Restore")
                if restore_submit:
                    if confirm_restore == activity['activity']:
                        for act in st.session_state['activities']:
                            if act['id'] == activity['id']:
                                act['is_active'] = True
                                break
                        log_action("Restore Activity", activity['id'], f"Restored activity to Active: {activity['activity']}")
                        st.success("Activity restored to Active Projects!")
                        st.session_state[f"restore_activity_{activity['id']}"] = False
                        st.rerun()
                    else:
                        st.error("Activity name does not match. Action cancelled.")
        # Permanently delete activity
        if f"permanent_delete_button_{activity['id']}" in st.session_state:
            st.session_state[f"permanent_delete_activity_{activity['id']}"] = True
        if f"permanent_delete_activity_{activity['id']}" in st.session_state and st.session_state[f"permanent_delete_activity_{activity['id']}"]:
            with st.form(key=f"permanent_delete_activity_form_{activity['id']}"):
                st.subheader(f"Permanently Delete Activity: {activity['activity']}")
                st.write("Are you sure you want to permanently delete this activity? This action cannot be undone.")
                confirm_permanent_delete = st.text_input("Type the activity name to confirm", placeholder=activity['activity'])
                permanent_delete_submit = st.form_submit_button("Confirm Permanent Delete")
                if permanent_delete_submit:
                    if confirm_permanent_delete == activity['activity']:
                        st.session_state['activities'] = [act for act in st.session_state['activities'] if act['id'] != activity['id']]
                        log_action("Delete Activity", activity['id'], f"Permanently deleted activity: {activity['activity']}")
                        st.success("Activity permanently deleted!")
                        st.session_state[f"permanent_delete_activity_{activity['id']}"] = False
                        st.rerun()
                    else:
                        st.error("Activity name does not match. Deletion cancelled.")

    st.markdown("</div>", unsafe_allow_html=True)
