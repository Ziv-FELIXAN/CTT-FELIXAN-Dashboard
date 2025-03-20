from templates import render_summary_card
import streamlit as st

def display_members_private_overview(activities, non_active_activities, checklist_items):
    """Display the Overview tab for Members - Private."""
    # Simplified st.markdown call to test if the issue is with HTML parsing
    st.markdown("### Members - Private Individuals")

    # Summary cards
    render_summary_card("fas fa-tasks", "Active Projects", len(activities))
    render_summary_card("fas fa-exclamation-circle", "Projects Needing Action", sum(1 for item in checklist_items if not item['completed']))
    render_summary_card("fas fa-archive", "Non-Active Projects", len(non_active_activities))
    render_summary_card("fas fa-file-alt", "Documents Pending Approval", sum(len(item['documents']) for item in checklist_items))
