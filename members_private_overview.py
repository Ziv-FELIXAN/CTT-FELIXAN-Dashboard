from templates import render_summary_card

def display_members_private_overview(activities, non_active_activities, checklist_items):
    """Display the Overview tab for Members - Private."""
    st.markdown(
        "<div class='module-content'>"
        "<h3>Members - Private Individuals</h3>",
        unsafe_allow_html=True
    )

    # Summary cards
    render_summary_card("fas fa-tasks", "Active Projects", len(activities))
    render_summary_card("fas fa-exclamation-circle", "Projects Needing Action", sum(1 for item in checklist_items if not item['completed']))
    render_summary_card("fas fa-archive", "Non-Active Projects", len(non_active_activities))
    render_summary_card("fas fa-file-alt", "Documents Pending Approval", sum(len(item['documents']) for item in checklist_items))

    st.markdown("</div>", unsafe_allow_html=True)
