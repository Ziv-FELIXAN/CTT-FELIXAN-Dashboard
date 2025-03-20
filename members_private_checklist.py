from templates import render_filter, render_checklist, render_table

def display_members_private_checklist(activities, checklist_items, log_action):
    """Display the Checklist tab for Members - Private."""
    st.markdown(
        "<div class='module-content'>"
        "<h3>Checklist Management</h3>",
        unsafe_allow_html=True
    )

    # Part 1: Filter and select object
    st.subheader("Select Object to Manage")
    object_types = ["Loan", "Auction", "Exchange"]
    selected_type, selected_object_id = render_filter(object_types, activities, "checklist_object_type", "checklist_object_select")

    # Part 2: Checklist for selected object
    if selected_object_id:
        st.subheader(f"Checklist for Object ID: {selected_object_id}")
        render_checklist(checklist_items, selected_object_id, log_action)

    # Part 3: Completed projects
    st.subheader("Completed Projects")
    completed_items = [item for item in checklist_items if item['completed']]
    completed_objects = set(item['object_id'] for item in completed_items)
    completed_activities = [activity for activity in st.session_state['activities'] if activity['id'] in completed_objects]
    columns = [
        {"name": "ID", "field": "id"},
        {"name": "Activity", "field": "activity"},
        {"name": "Date", "field": "date"},
        {"name": "Amount", "field": "amount"}
    ]
    actions = [
        {"icon": "fas fa-edit", "action": "edit_completed", "title": "Edit Activity"},
        {"icon": "fas fa-trash-alt", "action": "delete_completed", "title": "Delete Activity"}
    ]
    render_table(completed_activities, columns, actions)

    # Handle actions
    for activity in completed_activities:
        # Edit completed activity
        if f"edit_completed_{activity['id']}" in st.session_state:
            st.session_state[f"edit_completed_{activity['id']}"] = True
        if f"edit_completed_{activity['id']}" in st.session_state and st.session_state[f"edit_completed_{activity['id']}"]:
            with st.form(key=f"edit_completed_form_{activity['id']}"):
                st.subheader(f"Edit Completed Activity: {activity['activity']}")
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
                    log_action("Edit Completed Activity", activity['id'], f"Edited completed activity: {old_activity_type} to {new_activity_type}")
                    st.success("Activity updated successfully!")
                    st.session_state[f"edit_completed_{activity['id']}"] = False
                    st.rerun()
        # Delete completed activity
        if f"delete_completed_{activity['id']}" in st.session_state:
            st.session_state[f"delete_completed_{activity['id']}"] = True
        if f"delete_completed_{activity['id']}" in st.session_state and st.session_state[f"delete_completed_{activity['id']}"]:
            with st.form(key=f"delete_completed_form_{activity['id']}"):
                st.subheader(f"Delete Completed Activity: {activity['activity']}")
                st.write("Are you sure you want to permanently delete this activity? This action cannot be undone.")
                confirm_delete = st.text_input("Type the activity name to confirm", placeholder=activity['activity'])
                delete_submit = st.form_submit_button("Confirm Delete")
                if delete_submit:
                    if confirm_delete == activity['activity']:
                        st.session_state['activities'] = [act for act in st.session_state['activities'] if act['id'] != activity['id']]
                        log_action("Delete Completed Activity", activity['id'], f"Permanently deleted completed activity: {activity['activity']}")
                        st.success("Activity permanently deleted!")
                        st.session_state[f"delete_completed_{activity['id']}"] = False
                        st.rerun()
                    else:
                        st.error("Activity name does not match. Deletion cancelled.")

    st.markdown("</div>", unsafe_allow_html=True)
