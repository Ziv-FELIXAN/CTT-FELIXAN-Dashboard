import streamlit as st

def display_members_private():
    # Overview tab
    with st.session_state['tabs'][0]:
        st.markdown(
            "<div class='module-content'>"
            "<h3>Members - Private Individuals</h3>"
            "<div class='alert alert-info' style='border: 2px solid #1E90FF; border-radius: 8px;'>"
            "<strong>User Profile</strong>"
            "<ul class='list-unstyled mt-3'>"
            f"<li class='mb-3'><i class='bi bi-person-circle'></i> <strong>{st.session_state['members_private'][0]['name']}</strong> "
            f"<span class='badge bg-success'>{st.session_state['members_private'][0]['status']}</span><br>"
            f"<small class='text-muted ms-4'>Individual Account • Member since: {st.session_state['members_private'][0]['join_date']}</small></li>"
            "<li class='mb-3'><strong>Recent Activity</strong><ul class='list-unstyled ms-4'>",
            unsafe_allow_html=True
        )
        for activity in st.session_state['activities_private']:
            st.markdown(
                f"<li class='mb-2'><i class='bi bi-file-text'></i> {activity['activity']} "
                f"<span class='badge bg-info'>{activity['date']}</span>"
                f"{' <span class=\"badge bg-warning\">' + activity['amount'] + '</span>' if 'amount' in activity else ''}</li>",
                unsafe_allow_html=True
            )
        st.markdown(
            "</ul></li>"
            "<li class='mb-2'><strong>Account Status</strong><ul class='list-unstyled ms-4'>"
            f"<li><i class='bi bi-check-circle-fill text-success'></i> Verification: {st.session_state['members_private'][0]['verification']}</li>"
            f"<li><i class='bi bi-shield-check'></i> Security Level: {st.session_state['members_private'][0]['security']}</li>"
            f"<li><i class='bi bi-star-fill text-warning'></i> Premium: {st.session_state['members_private'][0]['premium']}</li>"
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
        for i, activity in enumerate(st.session_state['activities_private']):
            checked = st.checkbox("", key=f"activity_{i}")
            if checked:
                selected_activities.append(i)
            st.markdown(
                f"<tr><td style='border: 1px solid #ddd; padding: 8px;'>{'' if not checked else '✔'}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'>{activity['activity']}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'>{activity['date']}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'>{activity.get('amount', 'N/A')}</td>"
                f"<td style='border: 1px solid #ddd; padding: 8px;'><button>✏️</button> <button>🗑️</button></td></tr>",
                unsafe_allow_html=True
            )
        st.markdown("</table>", unsafe_allow_html=True)
        if st.button("Delete Selected Activities"):
            confirm = st.button("Confirm Delete? This will remove selected activities!")
            if confirm:
                for i in sorted(selected_activities, reverse=True):
                    st.session_state['activities_private'].pop(i)
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
