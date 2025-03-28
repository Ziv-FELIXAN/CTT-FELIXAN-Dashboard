import streamlit as st
from datetime import datetime
from templates import render_table, render_summary_card, render_filter, render_checklist, render_document_manager

def display_members_private():
    # Initialize session state for members, activities, checklist, contracts, assets, and log
    if 'members' not in st.session_state:
        st.session_state['members'] = [{
            'id': 1,
            'user_type': 'Private',
            'name': 'John Doe',
            'join_date': '2024-01-15',
            'status': 'Active',
            'verification': 'Complete',
            'security': 'High',
            'premium': 'Yes',
            'email': 'john.doe@example.com',
            'phone': '+1234567890'
        }]

    if 'activities' not in st.session_state:
        st.session_state['activities'] = [
            {'id': 1, 'user_id': 1, 'activity': 'Loan Application Submitted', 'date': '2025-03-01', 'amount': None, 'is_active': True},
            {'id': 2, 'user_id': 1, 'activity': 'Carat Transaction', 'date': '2025-03-02', 'amount': '$50,000', 'is_active': True}
        ]

    if 'checklist' not in st.session_state:
        st.session_state['checklist'] = [
            {'id': 1, 'user_id': 1, 'object_id': 1, 'step': 'Submit Application', 'completed': True, 'documents': []},
            {'id': 2, 'user_id': 1, 'object_id': 1, 'step': 'Verify Identity', 'completed': False, 'documents': []},
            {'id': 3, 'user_id': 1, 'object_id': 1, 'step': 'Review Terms', 'completed': False, 'documents': []},
            {'id': 4, 'user_id': 1, 'object_id': 1, 'step': 'Sign Agreement', 'completed': False, 'documents': []}
        ]

    if 'contracts' not in st.session_state:
        st.session_state['contracts'] = [
            {'id': 1, 'user_id': 1, 'contract_id': 'Contract #123', 'description': 'Loan Agreement', 'date': '2025-03-01', 'amount': '$10,000', 'status': 'Active'}
        ]

    if 'assets' not in st.session_state:
        st.session_state['assets'] = [
            {'id': 1, 'user_id': 1, 'asset_id': 'Asset #456', 'description': 'Car', 'value': '$20,000', 'status': 'Active'}
        ]

    if 'action_log' not in st.session_state:
        st.session_state['action_log'] = []

    if 'action_counter' not in st.session_state:
        st.session_state['action_counter'] = 0

    if 'notify_user' not in st.session_state:
        st.session_state['notify_user'] = False  # Default: no notifications

    # Get user and filter activities
    user = st.session_state['members'][0]
    user_id = user['id']
    activities = [activity for activity in st.session_state['activities'] if activity['user_id'] == user_id and activity['is_active']]
    non_active_activities = [activity for activity in st.session_state['activities'] if activity['user_id'] == user_id and not activity['is_active']]
    checklist_items = [item for item in st.session_state['checklist'] if item['user_id'] == user_id]
    contracts = [contract for contract in st.session_state['contracts'] if contract['user_id'] == user_id]
    assets = [asset for asset in st.session_state['assets'] if asset['user_id'] == user_id]

    # Function to log actions
    def log_action(action_type, object_id, details):
        st.session_state['action_counter'] += 1
        action_id = st.session_state['action_counter']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'action_id': action_id,
            'action_type': action_type,
            'object_id': object_id,
            'details': details,
            'timestamp': timestamp
        }
        st.session_state['action_log'].insert(0, log_entry)  # Add to the top of the log

    # Overview tab
    with st.session_state['tabs'][0]:
        st.markdown(
            "<div style='border: 1px solid #E0E0E0; border-radius: 4px; padding: 8px; margin-bottom: 8px;'>"
            "<h3 style='margin-top: 0;'>Members - Private Individuals</h3>",
            unsafe_allow_html=True
        )

        # Summary cards
        st.markdown("<div style='border: 1px solid #E0E0E0; border-radius: 4px; padding: 8px; margin-bottom: 8px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='font-size: 14px; font-weight: 500; margin-top: 0;'>Activity Summary</h4>", unsafe_allow_html=True)
        render_summary_card("far fa-tasks", "Active Projects", len(activities))
        render_summary_card("far fa-exclamation-circle", "Projects Needing Action", sum(1 for item in checklist_items if not item['completed']))
        render_summary_card("far fa-archive", "Non-Active Projects", len(non_active_activities))
        render_summary_card("far fa-file-alt", "Documents Pending Approval", sum(len(item['documents']) for item in checklist_items))
        st.markdown("</div>", unsafe_allow_html=True)

    # Manage Objects tab
    with st.session_state['tabs'][1]:
        st.markdown(
            "<div style='border: 1px solid #E0E0E0; border-radius: 4px; padding: 8px; margin-bottom: 8px;'>"
            "<h3 style='margin-top: 0;'>Manage Members Activities</h3>",
            unsafe_allow_html=True
        )

        # Display active activities table
        st.markdown("<h4 style='font-size: 14px; font-weight: 500; margin-top: 0;'>Active Activities</h4>", unsafe_allow_html=True)
        columns = [
            {"name": "Object ID", "field": "id"},
            {"name": "Activity", "field": "activity"},
            {"name": "Date", "field": "date"},
            {"name": "Amount", "field": "amount"}
        ]
        # Define actions dynamically for each activity
        for activity in activities:
            activity['actions'] = [
                {"icon": "far fa-edit", "action": f"edit_{activity['id']}", "title": "Edit Activity"},
                {"icon": "far fa-trash-alt", "action": f"delete_{activity['id']}", "title": "Move to Non-Active"}
            ]
        render_table(activities, columns, actions_field="actions", checkbox_key="selected_activities", key="download_active_activities")

        # Handle actions
        for activity in activities:
            edit_key = f"edit_{activity['id']}"
            delete_key = f"delete_{activity['id']}"
            # Edit activity
            if st.session_state.get(edit_key):
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
                        st.session_state[edit_key] = False
                        st.rerun()
            # Delete activity (move to non-active)
            if st.session_state.get(delete_key):
                with st.form(key=f"delete_activity_form_{activity['id']}"):
                    st.subheader(f"Move Activity to Non-Active: {activity['activity']}")
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
                            st.session_state[delete_key] = False
                            st.rerun()
                        else:
                            st.error("Activity name does not match. Action cancelled.")

        # Display non-active activities table
        st.markdown("<h4 style='font-size: 14px; font-weight: 500; margin-top: 8px;'>Non-Active Projects</h4>", unsafe_allow_html=True)
        columns = [
            {"name": "Object ID", "field": "id"},
            {"name": "Activity", "field": "activity", "style": "color: red;"},
            {"name": "Date", "field": "date", "style": "color: red;"},
            {"name": "Amount", "field": "amount", "style": "color: red;"}
        ]
        # Define actions dynamically for each non-active activity
        for activity in non_active_activities:
            activity['actions'] = [
                {"icon": "far fa-undo-alt", "action": f"restore_{activity['id']}", "title": "Restore to Active"},
                {"icon": "far fa-trash-alt", "action": f"permanent_delete_{activity['id']}", "title": "Permanently Delete"}
            ]
        render_table(non_active_activities, columns, actions_field="actions", checkbox_key="selected_non_active_activities", key="download_non_active_activities")

        # Handle actions
        for activity in non_active_activities:
            restore_key = f"restore_{activity['id']}"
            permanent_delete_key = f"permanent_delete_{activity['id']}"
            # Restore activity
            if st.session_state.get(restore_key):
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
                            st.session_state[restore_key] = False
                            st.rerun()
                        else:
                            st.error("Activity name does not match. Action cancelled.")
            # Permanently delete activity
            if st.session_state.get(permanent_delete_key):
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
                            st.session_state[permanent_delete_key] = False
                            st.rerun()
                        else:
                            st.error("Activity name does not match. Deletion cancelled.")

        st.markdown("</div>", unsafe_allow_html=True)

    # Checklist tab
    with st.session_state['tabs'][2]:
        st.markdown(
            "<div style='border: 1px solid #E0E0E0; border-radius: 4px; padding: 8px; margin-bottom: 8px;'>"
            "<h3 style='margin-top: 0;'>Checklist Management</h3>",
            unsafe_allow_html=True
        )

        # Part 1: Filter and select object
        st.markdown("<h4 style='font-size: 14px; font-weight: 500; margin-top: 0;'>Select Object to Manage</h4>", unsafe_allow_html=True)
        object_types = ["Loan", "Auction", "Exchange"]
        selected_type, selected_object_id = render_filter(object_types, activities, "checklist_object_type", "checklist_object_select")

        # Part 2: Checklist for selected object
        if selected_object_id:
            st.markdown(f"<h4 style='font-size: 14px; font-weight: 500; margin-top: 8px;'>Checklist for Object ID: {selected_object_id}</h4>", unsafe_allow_html=True)
            render_checklist(checklist_items, selected_object_id, log_action)

        # Part 3: Completed projects
        st.markdown("<h4 style='font-size: 14px; font-weight: 500; margin-top: 8px;'>Completed Projects</h4>", unsafe_allow_html=True)
        completed_items = [item for item in checklist_items if item['completed']]
        completed_objects = set(item['object_id'] for item in completed_items)
        completed_activities = [activity for activity in st.session_state['activities'] if activity['id'] in completed_objects]
        columns = [
            {"name": "Object ID", "field": "id"},
            {"name": "Activity", "field": "activity"},
            {"name": "Date", "field": "date"},
            {"name": "Amount", "field": "amount"}
        ]
        # Define actions dynamically for each completed activity
        for activity in completed_activities:
            activity['actions'] = [
                {"icon": "far fa-edit", "action": f"edit_completed_{activity['id']}", "title": "Edit Activity"},
                {"icon": "far fa-trash-alt", "action": f"delete_completed_{activity['id']}", "title": "Delete Activity"}
            ]
        render_table(completed_activities, columns, actions_field="actions", key="download_completed_activities")

        # Handle actions
        for activity in completed_activities:
            edit_completed_key = f"edit_completed_{activity['id']}"
            delete_completed_key = f"delete_completed_{activity['id']}"
            # Edit completed activity
            if st.session_state.get(edit_completed_key):
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
                        st.session_state[edit_completed_key] = False
                        st.rerun()
            # Delete completed activity
            if st.session_state.get(delete_completed_key):
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
                            st.session_state[delete_completed_key] = False
                            st.rerun()
                        else:
                            st.error("Activity name does not match. Deletion cancelled.")

        st.markdown("</div>", unsafe_allow_html=True)

    # Related Assets tab
    with st.session_state['tabs'][3]:
        st.markdown(
            "<div style='border: 1px solid #E0E0E0; border-radius: 4px; padding: 8px; margin-bottom: 8px;'>"
            "<h3 style='margin-top: 0;'>Related Assets for Members</h3>",
            unsafe_allow_html=True
        )

        # Filter by module
        st.markdown("<h4 style='font-size: 14px; font-weight: 500; margin-top: 0;'>Filter by Module</h4>", unsafe_allow_html=True)
        module_types = ["Contracts", "Assets"]
        selected_module = st.selectbox("Select Module", module_types, key="related_assets_module")

        # Display table based on selected module
        if selected_module == "Contracts":
            items = contracts
            columns = [
                {"name": "ID", "field": "id"},
                {"name": "Description", "field": "description"},
                {"name": "Details", "field": "date", "format": lambda x: f"{x['date']} | {x['amount']}"},
                {"name": "Status", "field": "status", "style": lambda x: "color: green;" if x['status'] == "Active" else "color: red;"}
            ]
        else:
            items = assets
            columns = [
                {"name": "ID", "field": "id"},
                {"name": "Description", "field": "description"},
                {"name": "Details", "field": "value", "format": lambda x: f"Value: {x['value']}"},
                {"name": "Status", "field": "status", "style": lambda x: "color: green;" if x['status'] == "Active" else "color: red;"}
            ]

        render_table(items, columns, key="download_related_assets")

        st.markdown("</div>", unsafe_allow_html=True)

    # Log tab
    with st.session_state['tabs'][4]:
        st.markdown(
            "<div style='border: 1px solid #E0E0E0; border-radius: 4px; padding: 8px; margin-bottom: 8px;'>"
            "<h3 style='margin-top: 0;'>Activity Log</h3>",
            unsafe_allow_html=True
        )

        # Option to enable/disable notifications
        st.markdown("<h4 style='font-size: 14px; font-weight: 500; margin-top: 0;'>Notification Settings</h4>", unsafe_allow_html=True)
        notify_user = st.checkbox("Send notifications to email/phone for each action", value=st.session_state['notify_user'])
        if notify_user != st.session_state['notify_user']:
            st.session_state['notify_user'] = notify_user
            st.success("Notification settings updated!")

        # Display log table
        st.markdown("<h4 style='font-size: 14px; font-weight: 500; margin-top: 8px;'>Log Entries</h4>", unsafe_allow_html=True)
        columns = [
            {"name": "Action ID", "field": "action_id"},
            {"name": "Action Type", "field": "action_type"},
            {"name": "Object ID", "field": "object_id"},
            {"name": "Details", "field": "details"},
            {"name": "Timestamp", "field": "timestamp"}
        ]
        render_table(st.session_state['action_log'], columns, key="download_log")

        st.markdown("</div>", unsafe_allow_html=True)
