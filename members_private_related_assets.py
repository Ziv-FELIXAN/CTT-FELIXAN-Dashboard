from templates import render_table

def display_members_private_related_assets(contracts, assets):
    """Display the Related Assets tab for Members - Private."""
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
        columns = [
            {"name": "ID", "field": "id"},
            {"name": "Description", "field": "description"},
            {"name": "Details", "field": "date", "format": lambda x: f"{x['date']} | {x['amount']}"},
            {"name": "Status", "field": "status", "style": "color: green;" if x['status'] == "Active" else "color: red;"}
        ]
    else:
        items = assets
        columns = [
            {"name": "ID", "field": "id"},
            {"name": "Description", "field": "description"},
            {"name": "Details", "field": "value", "format": lambda x: f"Value: {x['value']}"},
            {"name": "Status", "field": "status", "style": "color: green;" if x['status'] == "Active" else "color: red;"}
        ]

    render_table(items, columns)

    st.markdown("</div>", unsafe_allow_html=True)
