import streamlit as st

def display_members_private(conn, c):
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
    c.execute("SELECT * FROM activities WHERE user_id = ?", (user_id,))
    activities = c.fetchall()
    if not activities:
        c.executemany("INSERT INTO activities (user_id, activity, date, amount) VALUES (?, ?, ?, ?)",
                      [(user_id, "Loan Application Submitted", "2025-03-01", None),
                       (user_id, "Carat Transaction", "2025-03-02", "$50,000")])
        conn.commit()
        c.execute("SELECT * FROM activities WHERE user_id = ?", (user_id,))
        activities = c.fetchall()

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
            "<h3>Manage Members Activities</h3>"
            "<table style='width: 100%; border-collapse: collapse;'>"
            "<tr style='background-color: #f1f1f1;'><th style='border: 1px solid #ddd; padding: 8px;'>Select</th>"
            "<th style='border: 1px solid #ddd; padding: 8px;'>Activity</th>"
            "<th style='border: 1px solid #ddd; padding: 8px;'>Date</th>"
            "<th style='border: 1px solid #ddd; padding: 8px;'>Amount</th>"
            "<th style='border: 1px solid #ddd; padding: 8px;'>Actions</th></tr>",
            unsafe_allow_html=True
        )
        selected_activities = []
        for i, activity in enumerate(activities):
            checked = st.checkbox("", key=f"activity_{i}")
            if checked:
                selected_activities.append(activity[0])  # Store activity ID
            st.markdown(
                f"<tr><td style='border: 1px solid #ddd; padding: 8px;'>{'' if not checked else '✔'}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'>{activity[2]}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'>{activity[3]}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'>{activity[4] if activity[4] else 'N/A'}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'><button>✏️</button> <button>🗑️</button></td></tr>",
                unsafe_allow_html=True
            )
        st.markdown("</table>", unsafe_allow_html=True)
        if st.button("Delete Selected Activities"):
            confirm = st.button("Confirm Delete? This will remove selected activities!")
            if confirm:
                for activity_id in selected_activities:
                    c.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
                conn.commit()
                st.success(f"Deleted {len(selected_activities)} activities!")
                st.rerun()

    # Checklist tab
    with st.session_state['tabs'][2]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Members Checklist</h3>"
            "<p>Steps to complete a loan application:</p>"
            "<ul>"
            "<li><input type='checkbox' checked> Submit Application</li>"
            "<li><input type='checkbox'> Verify Identity</li>"
            "<li><input type='checkbox'> Review Terms</li>"
            "<li><input type='checkbox'> Sign Agreement</li>"
            "</ul>"
            "<div style='background-color: #e0e0e0; height: 20px; width: 50%; border-radius: 10px;'>"
            "<div style='background-color: #4CAF50; height: 20px; width: 25%; border-radius: 10px;'></div>"
            "</div>"
            "<p>Progress: 25%</p>"
            "</div>",
            unsafe_allow_html=True
        )

    # Related Assets tab
    with st.session_state['tabs'][3]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Related Assets for Members</h3>"
            "<p>Contracts: None</p>"
            "<p>Assets: None</p>"
            "</div>",
            unsafe_allow_html=True
        )
