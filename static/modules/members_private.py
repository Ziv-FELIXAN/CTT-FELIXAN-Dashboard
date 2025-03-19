import streamlit as st
import sqlite3

def display_members_private():
    # Connect to a module-specific database
    conn = sqlite3.connect('static/modules/members_private.db', check_same_thread=False)
    c = conn.cursor()

    # Ensure tables exist
    c.execute('''CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_type TEXT,
        name TEXT,
        join_date TEXT,
        status TEXT,
        verification TEXT,
        security TEXT,
        premium TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        activity TEXT,
        date TEXT,
        amount TEXT,
        is_active BOOLEAN DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES members(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS checklist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        step TEXT,
        completed BOOLEAN,
        FOREIGN KEY (user_id) REFERENCES members(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS contracts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        contract_id TEXT,
        description TEXT,
        date TEXT,
        amount TEXT,
        FOREIGN KEY (user_id) REFERENCES members(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        asset_id TEXT,
        description TEXT,
        value TEXT,
        FOREIGN KEY (user_id) REFERENCES members(id)
    )''')
    conn.commit()

    # Check if a user exists, if not, insert a default user
    c.execute("SELECT * FROM members WHERE user_type = 'Private'")
    user = c.fetchone()
    if not user:
        c.execute("INSERT INTO members (user_type, name, join_date, status, verification, security, premium) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  ('Private', 'John Doe', '2024-01-15', 'Active', 'Complete', 'High', 'Yes'))
        conn.commit()
        c.execute("SELECT * FROM members WHERE user_type = 'Private'")
        user = c.fetchone()

    # Check if activities exist for the user, if not, insert default activities
    user_id = user[0]
    c.execute("SELECT * FROM activities WHERE user_id = ? AND is_active = 1", (user_id,))
    activities = c.fetchall()
    if not activities:
        c.executemany("INSERT INTO activities (user_id, activity, date, amount, is_active) VALUES (?, ?, ?, ?, ?)",
                      [(user_id, "Loan Application Submitted", "2025-03-01", None, 1),
                       (user_id, "Carat Transaction", "2025-03-02", "$50,000", 1)])
        conn.commit()
        c.execute("SELECT * FROM activities WHERE user_id = ? AND is_active = 1", (user_id,))
        activities = c.fetchall()

    # Check for non-active activities
    c.execute("SELECT * FROM activities WHERE user_id = ? AND is_active = 0", (user_id,))
    non_active_activities = c.fetchall()

    # Check if checklist exists for the user, if not, insert default checklist
    c.execute("SELECT * FROM checklist WHERE user_id = ?", (user_id,))
    checklist_items = c.fetchall()
    if not checklist_items:
        default_steps = [
            (user_id, "Submit Application", 1),
            (user_id, "Verify Identity", 0),
            (user_id, "Review Terms", 0),
            (user_id, "Sign Agreement", 0)
        ]
        c.executemany("INSERT INTO checklist (user_id, step, completed) VALUES (?, ?, ?)", default_steps)
        conn.commit()
        c.execute("SELECT * FROM checklist WHERE user_id = ?", (user_id,))
        checklist_items = c.fetchall()

    # Check if contracts exist for the user, if not, insert default contracts
    c.execute("SELECT * FROM contracts WHERE user_id = ?", (user_id,))
    contracts = c.fetchall()
    if not contracts:
        c.execute("INSERT INTO contracts (user_id, contract_id, description, date, amount) VALUES (?, ?, ?, ?, ?)",
                  (user_id, "Contract #123", "Loan Agreement", "2025-03-01", "$10,000"))
        conn.commit()
        c.execute("SELECT * FROM contracts WHERE user_id = ?", (user_id,))
        contracts = c.fetchall()

    # Check if assets exist for the user, if not, insert default assets
    c.execute("SELECT * FROM assets WHERE user_id = ?", (user_id,))
    assets = c.fetchall()
    if not assets:
        c.execute("INSERT INTO assets (user_id, asset_id, description, value) VALUES (?, ?, ?, ?)",
                  (user_id, "Asset #456", "Car", "$20,000"))
        conn.commit()
        c.execute("SELECT * FROM assets WHERE user_id = ?", (user_id,))
        assets = c.fetchall()

    # Overview tab
    with st.session_state['tabs'][0]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Members - Private Individuals</h3>"
            "<div class='alert alert-info' style='border: 2px solid #1E90FF; border-radius: 8px;'>"
            "<strong>User Profile</strong>"
            "<ul class='list-unstyled mt-3'>"
            f"<li class='mb-3'><i class='bi bi-person-circle'></i> <strong>{user[2]}</strong> "
            f"<span class='badge bg-success'>{user[4]}</span><br>"
            f"<small class='text-muted ms-4'>Individual Account • Member since: {user[3]}</small></li>"
            "<li class='mb-3'><strong>Recent Activity</strong><ul class='list-unstyled ms-4'>",
            unsafe_allow_html=True
        )
        for activity in activities:
            st.markdown(
                f"<li class='mb-2'><i class='bi bi-file-text'></i> {activity[2]} "
                f"<span class='badge bg-info'>{activity[3]}</span>"
                f"{' <span class=\"badge bg-warning\">' + activity[4] + '</span>' if activity[4] else ''}</li>",
                unsafe_allow_html=True
            )
        st.markdown(
            "</ul></li>"
            "<li class='mb-2'><strong>Account Status</strong><ul class='list-unstyled ms-4'>"
            f"<li><i class='bi bi-check-circle-fill text-success'></i> Verification: {user[5]}</li>"
            f"<li><i class='bi bi-shield-check'></i> Security Level: {user[6]}</li>"
            f"<li><i class='bi bi-star-fill text-warning'></i> Premium: {user[7]}</li>"
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
                    c.execute("INSERT INTO activities (user_id, activity, date, amount, is_active) VALUES (?, ?, ?, ?, ?)",
                              (user_id, activity_type, activity_date, activity_amount if activity_amount else None, 1))
                    conn.commit()
                    st.success("Activity added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (Activity Type and Date).")

        # Display active activities table
        st.subheader("Active Activities")
        st.markdown(
            "<table style='width: 100%; border-collapse: collapse;'>"
            "<tr style='background-color: #f1f1f1;'>"
            "<th style='border: 1px solid #ddd; padding: 8px;'>Select</th>"
            "<th style='border: 1px solid #ddd; padding: 8px;'>Activity</th>"
            "<th style='border: 1px solid #ddd; padding: 8px;'>Date</th>"
            "<th style='border: 1px solid #ddd; padding: 8px;'>Amount</th>"
            "<th style='border: 1px solid #ddd; padding: 8px;'>Actions</th></tr>",
            unsafe_allow_html=True
        )

        # Store selected activities in session state
        if 'selected_activities' not in st.session_state:
            st.session_state['selected_activities'] = []

        for i, activity in enumerate(activities):
            # Use a unique key for each checkbox
            checked = activity[0] in st.session_state['selected_activities']
            st.markdown(
                f"<tr>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'><input type='checkbox' {'checked' if checked else ''} onclick=\"st.session_state['checkbox_{activity[0]}'] = !st.session_state.get('checkbox_{activity[0]}', false); st.rerun()\"></td>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'>{activity[2]}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'>{activity[3]}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'>{activity[4] if activity[4] else 'N/A'}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'>"
                f"<button onclick=\"st.session_state.edit_activity_{activity[0]} = true; st.rerun()\">✏️</button> "
                f"<button onclick=\"st.session_state.delete_activity_{activity[0]} = true; st.rerun()\">🗑️</button>"
                f"</td></tr>",
                unsafe_allow_html=True
            )

            # Update selected activities based on checkbox state
            if f"checkbox_{activity[0]}" in st.session_state:
                if st.session_state[f"checkbox_{activity[0]}"]:
                    if activity[0] not in st.session_state['selected_activities']:
                        st.session_state['selected_activities'].append(activity[0])
                else:
                    if activity[0] in st.session_state['selected_activities']:
                        st.session_state['selected_activities'].remove(activity[0])

            # Edit activity
            if f"edit_activity_{activity[0]}" in st.session_state and st.session_state[f"edit_activity_{activity[0]}"]:
                with st.form(key=f"edit_activity_form_{activity[0]}"):
                    st.subheader(f"Edit Activity: {activity[2]}")
                    new_activity_type = st.text_input("Activity Type", value=activity[2])
                    new_activity_date = st.text_input("Date (YYYY-MM-DD)", value=activity[3])
                    new_activity_amount = st.text_input("Amount (optional)", value=activity[4] if activity[4] else "")
                    edit_submit = st.form_submit_button("Save Changes")
                    if edit_submit:
                        c.execute("UPDATE activities SET activity = ?, date = ?, amount = ? WHERE id = ?",
                                  (new_activity_type, new_activity_date, new_activity_amount if new_activity_amount else None, activity[0]))
                        conn.commit()
                        st.success("Activity updated successfully!")
                        st.session_state[f"edit_activity_{activity[0]}"] = False
                        st.rerun()

            # Delete activity (move to non-active)
            if f"delete_activity_{activity[0]}" in st.session_state and st.session_state[f"delete_activity_{activity[0]}"]:
                with st.form(key=f"delete_activity_form_{activity[0]}"):
                    st.subheader(f"Delete Activity: {activity[2]}")
                    st.write("Are you sure you want to move this activity to Non-Active Projects?")
                    confirm_delete = st.text_input("Type the activity name to confirm", placeholder=activity[2])
                    delete_submit = st.form_submit_button("Confirm Move to Non-Active")
                    if delete_submit:
                        if confirm_delete == activity[2]:
                            c.execute("UPDATE activities SET is_active = 0 WHERE id = ?", (activity[0],))
                            conn.commit()
                            st.success("Activity moved to Non-Active Projects!")
                            st.session_state[f"delete_activity_{activity[0]}"] = False
                            st.rerun()
                        else:
                            st.error("Activity name does not match. Action cancelled.")

        st.markdown("</table>", unsafe_allow_html=True)

        # Delete selected activities (move to non-active)
        if st.button("Move Selected to Non-Active"):
            if st.session_state['selected_activities']:
                confirm = st.button("Confirm Move? This will move selected activities to Non-Active Projects!")
                if confirm:
                    for activity_id in st.session_state['selected_activities']:
                        c.execute("UPDATE activities SET is_active = 0 WHERE id = ?", (activity_id,))
                    conn.commit()
                    st.session_state['selected_activities'] = []  # Clear selection
                    st.success(f"Moved {len(st.session_state['selected_activities'])} activities to Non-Active Projects!")
                    st.rerun()
            else:
                st.error("No activities selected to move.")

        # Display non-active activities table
        st.subheader("Non-Active Projects")
        st.markdown(
            "<table style='width: 100%; border-collapse: collapse;'>"
            "<tr style='background-color: #f1f1f1;'>"
            "<th style='border: 1px solid #ddd; padding: 8px;'>Select</th>"
            "<th style='border: 1px solid #ddd; padding: 8px; color: red;'>Activity</th>"
            "<th style='border: 1px solid #ddd; padding: 8px; color: red;'>Date</th>"
            "<th style='border: 1px solid #ddd; padding: 8px; color: red;'>Amount</th>"
            "<th style='border: 1px solid #ddd; padding: 8px;'>Actions</th></tr>",
            unsafe_allow_html=True
        )

        # Store selected non-active activities in session state
        if 'selected_non_active_activities' not in st.session_state:
            st.session_state['selected_non_active_activities'] = []

        for i, activity in enumerate(non_active_activities):
            # Use a unique key for each checkbox
            checked = activity[0] in st.session_state['selected_non_active_activities']
            st.markdown(
                f"<tr>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'><input type='checkbox' {'checked' if checked else ''} onclick=\"st.session_state['checkbox_non_active_{activity[0]}'] = !st.session_state.get('checkbox_non_active_{activity[0]}', false); st.rerun()\"></td>"
                f"<td style='border: 1px solid #ddd; padding: 8px; color: red;'>{activity[2]}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px; color: red;'>{activity[3]}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px; color: red;'>{activity[4] if activity[4] else 'N/A'}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'>"
                f"<button onclick=\"st.session_state.restore_activity_{activity[0]} = true; st.rerun()\">🔄</button> "
                f"<button onclick=\"st.session_state.permanent_delete_activity_{activity[0]} = true; st.rerun()\">🗑️</button>"
                f"</td></tr>",
                unsafe_allow_html=True
            )

            # Update selected non-active activities based on checkbox state
            if f"checkbox_non_active_{activity[0]}" in st.session_state:
                if st.session_state[f"checkbox_non_active_{activity[0]}"]:
                    if activity[0] not in st.session_state['selected_non_active_activities']:
                        st.session_state['selected_non_active_activities'].append(activity[0])
                else:
                    if activity[0] in st.session_state['selected_non_active_activities']:
                        st.session_state['selected_non_active_activities'].remove(activity[0])

            # Restore activity
            if f"restore_activity_{activity[0]}" in st.session_state and st.session_state[f"restore_activity_{activity[0]}"]:
                with st.form(key=f"restore_activity_form_{activity[0]}"):
                    st.subheader(f"Restore Activity: {activity[2]}")
                    st.write("Are you sure you want to restore this activity to Active Projects?")
                    confirm_restore = st.text_input("Type the activity name to confirm", placeholder=activity[2])
                    restore_submit = st.form_submit_button("Confirm Restore")
                    if restore_submit:
                        if confirm_restore == activity[2]:
                            c.execute("UPDATE activities SET is_active = 1 WHERE id = ?", (activity[0],))
                            conn.commit()
                            st.success("Activity restored to Active Projects!")
                            st.session_state[f"restore_activity_{activity[0]}"] = False
                            st.rerun()
                        else:
                            st.error("Activity name does not match. Action cancelled.")

            # Permanently delete activity
            if f"permanent_delete_activity_{activity[0]}" in st.session_state and st.session_state[f"permanent_delete_activity_{activity[0]}"]:
                with st.form(key=f"permanent_delete_activity_form_{activity[0]}"):
                    st.subheader(f"Permanently Delete Activity: {activity[2]}")
                    st.write("Are you sure you want to permanently delete this activity? This action cannot be undone.")
                    confirm_permanent_delete = st.text_input("Type the activity name to confirm", placeholder=activity[2])
                    permanent_delete_submit = st.form_submit_button("Confirm Permanent Delete")
                    if permanent_delete_submit:
                        if confirm_permanent_delete == activity[2]:
                            c.execute("DELETE FROM activities WHERE id = ?", (activity[0],))
                            conn.commit()
                            st.success("Activity permanently deleted!")
                            st.session_state[f"permanent_delete_activity_{activity[0]}"] = False
                            st.rerun()
                        else:
                            st.error("Activity name does not match. Deletion cancelled.")

        st.markdown("</table>", unsafe_allow_html=True)

        # Restore selected non-active activities
        if st.button("Restore Selected to Active"):
            if st.session_state['selected_non_active_activities']:
                confirm = st.button("Confirm Restore? This will move selected activities to Active Projects!")
                if confirm:
                    for activity_id in st.session_state['selected_non_active_activities']:
                        c.execute("UPDATE activities SET is_active = 1 WHERE id = ?", (activity_id,))
                    conn.commit()
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
                    for activity_id in st.session_state['selected_non_active_activities']:
                        c.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
                    conn.commit()
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
        completed_steps = sum(1 for item in checklist_items if item[3])
        progress = (completed_steps / total_steps) * 100 if total_steps > 0 else 0

        for i, item in enumerate(checklist_items):
            checked = st.checkbox(item[2], value=bool(item[3]), key=f"checklist_{i}")
            if checked != bool(item[3]):
                c.execute("UPDATE checklist SET completed = ? WHERE id = ?", (1 if checked else 0, item[0]))
                conn.commit()
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
                    f"<p>{contract[2]} - {contract[3]} | {contract[4]} | {contract[5]}</p>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown("<p>No contracts found.</p>", unsafe_allow_html=True)

        # Assets
        st.subheader("Assets")
        if assets:
            for asset in assets:
                st.markdown(
                    f"<p>{asset[2]} - {asset[3]} | Value: {asset[4]}</p>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown("<p>No assets found.</p>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Close the database connection
    conn.close()
