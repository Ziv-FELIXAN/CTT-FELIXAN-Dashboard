import streamlit as st
from datetime import datetime

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
    assets = [asset for asset in st.session_state['assets'] if contract['user_id'] == user_id]

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
            "<div class='module-content'>"
            "<h3>Members - Private Individuals</h3>",
            unsafe_allow_html=True
        )

        # Summary cards
        st.markdown(
            "<div class='overview-card'>"
            "<i class='fas fa-tasks'></i>"
            f"<p>Active Projects: {len(activities)}</p>"
            "</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div class='overview-card'>"
            "<i class='fas fa-exclamation-circle'></i>"
            f"<p>Projects Needing Action: {sum(1 for item in checklist_items if not item['completed'])}</p>"
            "</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div class='overview-card'>"
            "<i class='fas fa-archive'></i>"
            f"<p>Non-Active Projects: {len(non_active_activities)}</p>"
            "</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div class='overview-card'>"
            "<i class='fas fa-file-alt'></i>"
            f"<p>Documents Pending Approval: {sum(len(item['documents']) for item in checklist_items)}</p>"
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # Manage Objects tab
    with st.session_state['tabs'][1]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Manage Members Activities</h3>",
            unsafe_allow_html=True
        )

        # Display active activities table
        st.subheader("Active Activities")
        st.markdown("<table class='custom-table'>", unsafe_allow_html=True)
        st.markdown("<tr><th>ID</th><th>Select</th><th>Activity</th><th>Date</th><th>Amount</th><th>Actions</th></tr>", unsafe_allow_html=True)
        for i, activity in enumerate(activities):
            st.markdown(
                f"<tr>"
                f"<td>{activity['id']}</td>"
                f"<td><input type='checkbox' {'checked' if activity['id'] in st.session_state.get('selected_activities', []) else ''} id='active_checkbox_{activity['id']}'></td>"
                f"<td>{activity['activity']}</td>"
                f"<td>{activity['date']}</td>"
                f"<td>{activity['amount'] if activity['amount'] else 'N/A'}</td>"
                f"<td>"
                f"<button class='icon-button' onclick=\"alert('Edit not implemented yet')\" title='Edit Activity'><i class='fas fa-edit'></i></button>"
                f"<button class='icon-button' onclick=\"alert('Delete not implemented yet')\" title='Move to Non-Active'><i class='fas fa-trash-alt'></i></button>"
                f"</td>"
                f"</tr>",
                unsafe_allow_html=True
            )
            # Handle checkbox state
            checked = st.checkbox("", value=activity['id'] in st.session_state.get('selected_activities', []), key=f"active_checkbox_{activity['id']}", label_visibility="hidden")
            if checked:
                if 'selected_activities' not in st.session_state:
                    st.session_state['selected_activities'] = []
                if activity['id'] not in st.session_state['selected_activities']:
                    st.session_state['selected_activities'].append(activity['id'])
            else:
                if 'selected_activities' in st.session_state and activity['id'] in st.session_state['selected_activities']:
                    st.session_state['selected_activities'].remove(activity['id'])
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
        st.markdown("</table>", unsafe_allow_html=True)

        # Display non-active activities table
        st.subheader("Non-Active Projects")
        st.markdown("<table class='custom-table'>", unsafe_allow_html=True)
        st.markdown("<tr><th>ID</th><th>Select</th><th>Activity</th><th>Date</th><th>Amount</th><th>Actions</th></tr>", unsafe_allow_html=True)
        if 'selected_non_active_activities' not in st.session_state:
            st.session_state['selected_non_active_activities'] = []
        for i, activity in enumerate(non_active_activities):
            st.markdown(
                f"<tr>"
                f"<td>{activity['id']}</td>"
                f"<td><input type='checkbox' {'checked' if activity['id'] in st.session_state['selected_non_active_activities'] else ''} id='non_active_checkbox_{activity['id']}'></td>"
                f"<td style='color: red;'>{activity['activity']}</td>"
                f"<td style='color: red;'>{activity['date']}</td>"
                f"<td style='color: red;'>{activity['amount'] if activity['amount'] else 'N/A'}</td>"
                f"<td>"
                f"<button class='icon-button' onclick=\"alert('Restore not implemented yet')\" title='Restore to Active'><i class='fas fa-undo-alt'></i></button>"
                f"<button class='icon-button' onclick=\"alert('Delete not implemented yet')\" title='Permanently Delete'><i class='fas fa-trash-alt'></i></button>"
                f"</td>"
                f"</tr>",
                unsafe_allow_html=True
            )
            # Handle checkbox state
            checked = st.checkbox("", value=activity['id'] in st.session_state['selected_non_active_activities'], key=f"non_active_checkbox_{activity['id']}", label_visibility="hidden")
            if checked:
                if activity['id'] not in st.session_state['selected_non_active_activities']:
                    st.session_state['selected_non_active_activities'].append(activity['id'])
            else:
                if activity['id'] in st.session_state['selected_non_active_activities']:
                    st.session_state['selected_non_active_activities'].remove(activity['id'])
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
        st.markdown("</table>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Checklist tab
    with st.session_state['tabs'][2]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Checklist Management</h3>",
            unsafe_allow_html=True
        )

        # Part 1: Filter and select object
        st.subheader("Select Object to Manage")
        object_types = ["Loan", "Auction", "Exchange"]
        selected_type = st.selectbox("Select Object Type", object_types, key="checklist_object_type")
        objects = [activity for activity in st.session_state['activities'] if selected_type.lower() in activity['activity'].lower()]
        object_ids = [obj['id'] for obj in objects]
        selected_object_id = st.selectbox("Select Object", object_ids, format_func=lambda x: next(obj['activity'] for obj in objects if obj['id'] == x), key="checklist_object_select")

        # Part 2: Checklist for selected object
        if selected_object_id:
            st.subheader(f"Checklist for Object ID: {selected_object_id}")
            object_checklist = [item for item in checklist_items if item['object_id'] == selected_object_id]
            total_steps = len(object_checklist)
            completed_steps = sum(1 for item in object_checklist if item['completed'])
            progress = (completed_steps / total_steps) * 100 if total_steps > 0 else 0

            for i, item in enumerate(object_checklist):
                col1, col2, col3 = st.columns([0.5, 3, 1])
                with col1:
                    st.write(f"{i+1}.")
                with col2:
                    checked = st.checkbox(item['step'], value=bool(item['completed']), key=f"checklist_{item['id']}")
                    if checked != bool(item['completed']):
                        for chk in st.session_state['checklist']:
                            if chk['id'] == item['id']:
                                chk['completed'] = checked
                                break
                        log_action("Update Checklist", item['id'], f"Updated checklist item: {item['step']} to {'Completed' if checked else 'Not Completed'}")
                        st.rerun()
                with col3:
                    if st.button("", key=f"docs_{item['id']}", help="Manage Documents"):
                        st.session_state[f"manage_docs_{item['id']}"] = True
                    st.markdown("<i class='fas fa-paperclip'></i>", unsafe_allow_html=True)

                # Manage documents
                if f"manage_docs_{item['id']}" in st.session_state and st.session_state[f"manage_docs_{item['id']}"]:
                    with st.form(key=f"docs_form_{item['id']}"):
                        st.subheader(f"Manage Documents for: {item['step']}")
                        uploaded_file = st.file_uploader("Upload Document", key=f"upload_{item['id']}")
                        notes = st.text_area("Notes", key=f"notes_{item['id']}")
                        submit_doc = st.form_submit_button("Add Document")
                        if submit_doc and uploaded_file:
                            for chk in st.session_state['checklist']:
                                if chk['id'] == item['id']:
                                    chk['documents'].append({'name': uploaded_file.name, 'notes': notes})
                                    break
                            st.success("Document added successfully!")
                            st.session_state[f"manage_docs_{item['id']}"] = False
                            st.rerun()

                    # Display uploaded documents
                    if object_checklist[i]['documents']:
                        st.write("Uploaded Documents:")
                        for doc in object_checklist[i]['documents']:
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                st.write(doc['name'])
                            with col2:
                                st.write(f"Notes: {doc['notes']}")
                            with col3:
                                if st.button("Delete", key=f"delete_doc_{item['id']}_{doc['name']}"):
                                    for chk in st.session_state['checklist']:
                                        if chk['id'] == item['id']:
                                            chk['documents'] = [d for d in chk['documents'] if d['name'] != doc['name']]
                                            break
                                    st.rerun()

            st.markdown(
                "<div style='background-color: #e0e0e0; height: 20px; width: 50%; border-radius: 10px;'>"
                f"<div style='background-color: #4CAF50; height: 20px; width: {progress}%; border-radius: 10px;'></div>"
                "</div>"
                f"<p>Progress: {progress:.0f}%</p>",
                unsafe_allow_html=True
            )

        # Part 3: Completed projects
        st.subheader("Completed Projects")
        completed_items = [item for item in checklist_items if item['completed']]
        completed_objects = set(item['object_id'] for item in completed_items)
        completed_activities = [activity for activity in st.session_state['activities'] if activity['id'] in completed_objects]
        st.markdown("<table class='custom-table'>", unsafe_allow_html=True)
        st.markdown("<tr><th>ID</th><th>Activity</th><th>Date</th><th>Amount</th><th>Actions</th></tr>", unsafe_allow_html=True)
        for activity in completed_activities:
            st.markdown(
                f"<tr>"
                f"<td>{activity['id']}</td>"
                f"<td>{activity['activity']}</td>"
                f"<td>{activity['date']}</td>"
                f"<td>{activity['amount'] if activity['amount'] else 'N/A'}</td>"
                f"<td>"
                f"<button class='icon-button' onclick=\"alert('Edit not implemented yet')\" title='Edit Activity'><i class='fas fa-edit'></i></button>"
                f"<button class='icon-button' onclick=\"alert('Delete not implemented yet')\" title='Delete Activity'><i class='fas fa-trash-alt'></i></button>"
                f"</td>"
                f"</tr>",
                unsafe_allow_html=True
            )
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
        st.markdown("</table>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Related Assets tab
    with st.session_state['tabs'][3]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Related Assets for Members</h3>",
            unsafe_allow_html=True
        )

        # Filter by module
        st.subheader("Filter by Module")
        module_types = ["Contracts", "Assets"]
        selected_module = st.selectbox("Select Module", module_types, key="related_assets_module")

        # Display table based on selected module
        if selected_module == "Contracts":
            items = contracts
        else:
            items = assets

        st.markdown("<table class='custom-table'>", unsafe_allow_html=True)
        st.markdown("<tr><th>ID</th><th>Description</th><th>Details</th><th>Status</th></tr>", unsafe_allow_html=True)
        for item in items:
            st.markdown(
                f"<tr>"
                f"<td>{item['id']}</td>"
                f"<td>{item['description']}</td>"
                f"<td>{item['date'] + ' | ' + item['amount'] if selected_module == 'Contracts' else 'Value: ' + item['value']}</td>"
                f"<td><span style='color: {'green' if item['status'] == 'Active' else 'red'}'>{item['status']}</span></td>"
                f"</tr>",
                unsafe_allow_html=True
            )
        st.markdown("</table>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Log tab
    with st.session_state['tabs'][4]:
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
        st.markdown("<table class='custom-table'>", unsafe_allow_html=True)
        st.markdown("<tr><th>Action ID</th><th>Action Type</th><th>Object ID</th><th>Details</th><th>Timestamp</th></tr>", unsafe_allow_html=True)
        if st.session_state['action_log']:
            for entry in st.session_state['action_log']:
                st.markdown(
                    f"<tr>"
                    f"<td>{entry['action_id']}</td>"
                    f"<td>{entry['action_type']}</td>"
                    f"<td>{entry['object_id']}</td>"
                    f"<td>{entry['details']}</td>"
                    f"<td>{entry['timestamp']}</td>"
                    f"</tr>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown("<tr><td colspan='5'>No activities logged yet.</td></tr>", unsafe_allow_html=True)
        st.markdown("</table>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
