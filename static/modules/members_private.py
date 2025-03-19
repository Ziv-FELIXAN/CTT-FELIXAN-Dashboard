import streamlit as st

def display_members_private():
    # Initialize session state for members, activities, checklist, contracts, and assets
    if 'members' not in st.session_state:
        st.session_state['members'] = [{
            'id': 1,
            'user_type': 'Private',
            'name': 'John Doe',
            'join_date': '2024-01-15',
            'status': 'Active',
            'verification': 'Complete',
            'security': 'High',
            'premium': 'Yes'
        }]

    if 'activities' not in st.session_state:
        st.session_state['activities'] = [
            {'id': 1, 'user_id': 1, 'activity': 'Loan Application Submitted', 'date': '2025-03-01', 'amount': None, 'is_active': True},
            {'id': 2, 'user_id': 1, 'activity': 'Carat Transaction', 'date': '2025-03-02', 'amount': '$50,000', 'is_active': True}
        ]

    if 'checklist' not in st.session_state:
        st.session_state['checklist'] = [
            {'id': 1, 'user_id': 1, 'step': 'Submit Application', 'completed': True},
            {'id': 2, 'user_id': 1, 'step': 'Verify Identity', 'completed': False},
            {'id': 3, 'user_id': 1, 'step': 'Review Terms', 'completed': False},
            {'id': 4, 'user_id': 1, 'step': 'Sign Agreement', 'completed': False}
        ]

    if 'contracts' not in st.session_state:
        st.session_state['contracts'] = [
            {'id': 1, 'user_id': 1, 'contract_id': 'Contract #123', 'description': 'Loan Agreement', 'date': '2025-03-01', 'amount': '$10,000'}
        ]

    if 'assets' not in st.session_state:
        st.session_state['assets'] = [
            {'id': 1, 'user_id': 1, 'asset_id': 'Asset #456', 'description': 'Car', 'value': '$20,000'}
        ]

    # Get user and filter activities
    user = st.session_state['members'][0]
    user_id = user['id']
    activities = [activity for activity in st.session_state['activities'] if activity['user_id'] == user_id and activity['is_active']]
    non_active_activities = [activity for activity in st.session_state['activities'] if activity['user_id'] == user_id and not activity['is_active']]
    checklist_items = [item for item in st.session_state['checklist'] if item['user_id'] == user_id]
    contracts = [contract for contract in st.session_state['contracts'] if contract['user_id'] == user_id]
    assets = [asset for asset in st.session_state['assets'] if asset['user_id'] == user_id]

    # Overview tab
    with st.session_state['tabs'][0]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Members - Private Individuals</h3>"
            "<div class='alert alert-info' style='border: 2px solid #1E90FF; border-radius: 8px;'>"
            "<strong>User Profile</strong>"
            "<ul class='list-unstyled mt-3'>"
            f"<li class='mb-3'><i class='bi bi-person-circle'></i> <strong>{user['name']}</strong> "
            f"<span class='badge bg-success'>{user['status']}</span><br>"
            f"<small class='text-muted ms-4'>Individual Account • Member since: {user['join_date']}</small></li>"
            "<li class='mb-3'><strong>Recent Activity</strong><ul class='list-unstyled ms-4'>",
            unsafe_allow_html=True
        )
        for activity in activities:
            st.markdown(
                f"<li class='mb-2'><i class='bi bi-file-text'></i> {activity['activity']} "
                f"<span class='badge bg-info'>{activity['date']}</span>"
                f"{' <span class=\"badge bg-warning\">' + activity['amount'] + '</span>' if activity['amount'] else ''}</li>",
                unsafe_allow_html=True
            )
        st.markdown(
            "</ul></li>"
            "<li class='mb-2'><strong>Account Status</strong><ul class='list-unstyled ms-4'>"
            f"<li><i class='bi bi-check-circle-fill text-success'></i> Verification: {user['verification']}</li>"
            f"<li><i class='bi bi-shield-check'></i> Security Level: {user['security']}</li>"
            f"<li><i class='bi bi-star-fill text-warning'></i> Premium: {user['premium']}</li>"
            "</ul></li></ul></div>"
            "<p class='text-info mt-3'>Status: Active</p>"
            "</div>",
            unsafe_allow_html=True
        )

    # Manage Objects tab
    with st.session_state['tabs'][1]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Manage Members Activities</h3>",
            unsafe_allow_html=True
        )

        # Form to add a new activity
        with st.form(key="add_activity_form"):
            st.subheader("Add New Activity")
            activity_type = st.text_input("Activity Type", placeholder="e.g., Loan Application Submitted")
            activity_date = st.text_input("Date (YYYY-MM-DD)", placeholder="e.g., 2025-03-01")
            activity_amount = st.text_input("Amount (optional)", placeholder="e.g., $50,000")
            submit_button = st.form_submit_button("Add Activity")
            if submit_button:
                if activity_type and activity_date:
                    new_id = max([activity['id'] for activity in st.session_state['activities']], default=0) + 1
                    st.session_state['activities'].append({
                        'id': new_id,
                        'user_id': user_id,
                        'activity': activity_type,
                        'date': activity_date,
                        'amount': activity_amount if activity_amount else None,
                        'is_active': True
                    })
                    st.success("Activity added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (Activity Type and Date).")

        # Display active activities table
        st.subheader("Active Activities")
        st.markdown(
            "<style>"
            ".activity-table {width: 100%; border-collapse: collapse; margin-top: 10px;}"
            ".activity-table th, .activity-table td {border: 1px solid #ddd; padding: 8px; text-align: left;}"
            ".activity-table th {background-color: #f1f1f1;}"
            "</style>",
            unsafe_allow_html=True
        )

        # Store selected activities in session state
        if 'selected_activities' not in st.session_state:
            st.session_state['selected_activities'] = []

        # Create table header using st.columns
        col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 2])
        with col1:
            st.markdown("**Select**")
        with col2:
            st.markdown("**Activity**")
        with col3:
            st.markdown("**Date**")
        with col4:
            st.markdown("**Amount**")
        with col5:
            st.markdown("**Actions**")

        # Display each activity as a row
        for i, activity in enumerate(activities):
            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 2])
            with col1:
                checked = st.checkbox("", value=activity['id'] in st.session_state['selected_activities'], key=f"active_checkbox_{activity['id']}")
                if checked:
                    if activity['id'] not in st.session_state['selected_activities']:
                        st.session_state['selected_activities'].append(activity['id'])
                else:
                    if activity['id'] in st.session_state['selected_activities']:
                        st.session_state['selected_activities'].remove(activity['id'])
            with col2:
                st.write(activity['activity'])
            with col3:
                st.write(activity['date'])
            with col4:
                st.write(activity['amount'] if activity['amount'] else 'N/A')
            with col5:
                if st.button("✏️", key=f"edit_button_{activity['id']}"):
                    st.session_state[f"edit_activity_{activity['id']}"] = True
                if st.button("🗑️", key=f"delete_button_{activity['id']}"):
                    st.session_state[f"delete_activity_{activity['id']}"] = True

            # Edit activity
            if f"edit_activity_{activity['id']}" in st.session_state and st.session_state[f"edit_activity_{activity['id']}"]:
                with st.form(key=f"edit_activity_form_{activity['id']}"):
                    st.subheader(f"Edit Activity: {activity['activity']}")
                    new_activity_type = st.text_input("Activity Type", value=activity['activity'])
                    new_activity_date = st.text_input("Date (YYYY-MM-DD)", value=activity['date'])
                    new_activity_amount = st.text_input("Amount (optional)", value=activity['amount'] if activity['amount'] else "")
                    edit_submit = st.form_submit_button("Save Changes")
                    if edit_submit:
                        for act in st.session_state['activities']:
                            if act['id'] == activity['id']:
                                act['activity'] = new_activity_type
                                act['date'] = new_activity_date
                                act['amount'] = new_activity_amount if new_activity_amount else None
                                break
                        st.success("Activity updated successfully!")
                        st.session_state[f"edit_activity_{activity['id']}"] = False
                        st.rerun()

            # Delete activity (move to non-active)
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
                            st.success("Activity moved to Non-Active Projects!")
                            st.session_state[f"delete_activity_{activity['id']}"] = False
                            st.rerun()
                        else:
                            st.error("Activity name does not match. Action cancelled.")

        # Delete selected activities (move to non-active)
        if st.button("Move Selected to Non-Active"):
            if st.session_state['selected_activities']:
                confirm = st.button("Confirm Move? This will move selected activities to Non-Active Projects!")
                if confirm:
                    for activity_id in st.session_state['selected_activities']:
                        for act in st.session_state['activities']:
                            if act['id'] == activity_id:
                                act['is_active'] = False
                                break
                    st.session_state['selected_activities'] = []  # Clear selection
                    st.success(f"Moved {len(st.session_state['selected_activities'])} activities to Non-Active Projects!")
                    st.rerun()
            else:
                st.error("No activities selected to move.")

        # Display non-active activities table
        st.subheader("Non-Active Projects")
        st.markdown(
            "<style>"
            ".activity-table {width: 100%; border-collapse: collapse; margin-top: 10px;}"
            ".activity-table th, .activity-table td {border: 1px solid #ddd; padding: 8px; text-align: left;}"
            ".activity-table th {background-color: #f1f1f1;}"
            "</style>",
            unsafe_allow_html=True
        )

        # Create table header using st.columns
        col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 2])
        with col1:
            st.markdown("**Select**")
        with col2:
            st.markdown("**Activity**")
        with col3:
            st.markdown("**Date**")
        with col4:
            st.markdown("**Amount**")
        with col5:
            st.markdown("**Actions**")

        # Store selected non-active activities in session state
        if 'selected_non_active_activities' not in st.session_state:
            st.session_state['selected_non_active_activities'] = []

        for i, activity in enumerate(non_active_activities):
            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 2])
            with col1:
                checked = st.checkbox("", value=activity['id'] in st.session_state['selected_non_active_activities'], key=f"non_active_checkbox_{activity['id']}")
                if checked:
                    if activity['id'] not in st.session_state['selected_non_active_activities']:
                        st.session_state['selected_non_active_activities'].append(activity['id'])
                else:
                    if activity['id'] in st.session_state['selected_non_active_activities']:
                        st.session_state['selected_non_active_activities'].remove(activity['id'])
            with col2:
                st.markdown(f"<span style='color: red;'>{activity['activity']}</span>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<span style='color: red;'>{activity['date']}</span>", unsafe_allow_html=True)
            with col4:
                st.markdown(f"<span style='color: red;'>{activity['amount'] if activity['amount'] else 'N/A'}</span>", unsafe_allow_html=True)
            with col5:
                if st.button("🔄", key=f"restore_button_{activity['id']}"):
                    st.session_state[f"restore_activity_{activity['id']}"] = True
                if st.button("🗑️", key=f"permanent_delete_button_{activity['id']}"):
                    st.session_state[f"permanent_delete_activity_{activity['id']}"] = True

            # Restore activity
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
                            st.success("Activity restored to Active Projects!")
                            st.session_state[f"restore_activity_{activity['id']}"] = False
                            st.rerun()
                        else:
                            st.error("Activity name does not match. Action cancelled.")

            # Permanently delete activity
            if f"permanent_delete_activity_{activity['id']}" in st.session_state and st.session_state[f"permanent_delete_activity_{activity['id']}"]:
                with st.form(key=f"permanent_delete_activity_form_{activity['id']}"):
                    st.subheader(f"Permanently Delete Activity: {activity['activity']}")
                    st.write("Are you sure you want to permanently delete this activity? This action cannot be undone.")
                    confirm_permanent_delete = st.text_input("Type the activity name to confirm", placeholder=activity['activity'])
                    permanent_delete_submit = st.form_submit_button("Confirm Permanent Delete")
                    if permanent_delete_submit:
                        if confirm_permanent_delete == activity['activity']:
                            st.session_state['activities'] = [act for act in st.session_state['activities'] if act['id'] != activity['id']]
                            st.success("Activity permanently deleted!")
                            st.session_state[f"permanent_delete_activity_{activity['id']}"] = False
                            st.rerun()
                        else:
                            st.error("Activity name does not match. Deletion cancelled.")

        # Restore selected non-active activities
        if st.button("Restore Selected to Active"):
            if st.session_state['selected_non_active_activities']:
                confirm = st.button("Confirm Restore? This will move selected activities to Active Projects!")
                if confirm:
                    for activity_id in st.session_state['selected_non_active_activities']:
                        for act in st.session_state['activities']:
                            if act['id'] == activity_id:
                                act['is_active'] = True
                                break
                    st.session_state['selected_non_active_activities'] = []  # Clear selection
                    st.success(f"Restored {len(st.session_state['selected_non_active_activities'])} activities to Active Projects!")
                    st.rerun()
            else:
                st.error("No activities selected to restore.")

        # Permanently delete selected non-active activities
        if st.button("Permanently Delete Selected"):
            if st.session_state['selected_non_active_activities']:
                confirm = st.button("Confirm Permanent Delete? This will permanently remove selected activities!")
                if confirm:
                    st.session_state['activities'] = [act for act in st.session_state['activities'] if act['id'] not in st.session_state['selected_non_active_activities']]
                    st.session_state['selected_non_active_activities'] = []  # Clear selection
                    st.success(f"Permanently deleted {len(st.session_state['selected_non_active_activities'])} activities!")
                    st.rerun()
            else:
                st.error("No activities selected for permanent deletion.")

    # Checklist tab
    with st.session_state['tabs'][2]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Members Checklist</h3>"
            "<p>Steps to complete a loan application:</p>",
            unsafe_allow_html=True
        )
        total_steps = len(checklist_items)
        completed_steps = sum(1 for item in checklist_items if item['completed'])
        progress = (completed_steps / total_steps) * 100 if total_steps > 0 else 0

        for i, item in enumerate(checklist_items):
            checked = st.checkbox(item['step'], value=bool(item['completed']), key=f"checklist_{i}")
            if checked != bool(item['completed']):
                for chk in st.session_state['checklist']:
                    if chk['id'] == item['id']:
                        chk['completed'] = checked
                        break
                st.rerun()

        st.markdown(
            "<div style='background-color: #e0e0e0; height: 20px; width: 50%; border-radius: 10px;'>"
            f"<div style='background-color: #4CAF50; height: 20px; width: {progress}%; border-radius: 10px;'></div>"
            "</div>"
            f"<p>Progress: {progress:.0f}%</p>"
            "</div>",
            unsafe_allow_html=True
        )

    # Related Assets tab
    with st.session_state['tabs'][3]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Related Assets for Members</h3>",
            unsafe_allow_html=True
        )

        # Contracts
        st.subheader("Contracts")
        if contracts:
            for contract in contracts:
                st.markdown(
                    f"<p>{contract['contract_id']} - {contract['description']} | {contract['date']} | {contract['amount']}</p>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown("<p>No contracts found.</p>", unsafe_allow_html=True)

        # Assets
        st.subheader("Assets")
        if assets:
            for asset in assets:
                st.markdown(
                    f"<p>{asset['asset_id']} - {asset['description']} | Value: {asset['value']}</p>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown("<p>No assets found.</p>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
