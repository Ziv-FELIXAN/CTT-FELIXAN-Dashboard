import streamlit as st

def apply_styling():
    # Add Font Awesome for icons
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        """,
        unsafe_allow_html=True
    )

    # Custom CSS for tabs, tables, and cards
    st.markdown(
        """
        <style>
        /* General styling */
        body {
            font-family: 'Arial', sans-serif;
            font-size: 13px;
            color: #333;
        }
        h3 {
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 8px;
        }
        h4 {
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 5px;
        }
        .stButton>button {
            font-size: 13px;
            padding: 4px 8px;
            border-radius: 4px;
        }
        .stSelectbox, .stTextInput {
            font-size: 13px;
        }
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #f5f5f5;
            padding: 2px;
            border-radius: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 4px 12px;
            margin: 0 2px;
            border-radius: 4px;
            font-size: 13px;
            font-weight: 500;
        }
        /* Active tab color based on user type */
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #2C3E50; /* Default for Management */
            color: white;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #2C3E5080; /* 50% opacity for non-active tabs */
            color: #333;
        }
        /* Override for Private (red) */
        [data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
            background-color: #E74C3C !important; /* Red for Private */
        }
        [data-testid="stTabs"] [data-baseweb="tab"] {
            background-color: #E74C3C80 !important; /* 50% opacity for non-active tabs */
        }
        /* Table styling */
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 5px;
            border: 1px solid #E0E0E0;
        }
        .custom-table th, .custom-table td {
            border: 1px solid #E0E0E0;
            padding: 4px;
            text-align: left;
            font-size: 13px;
        }
        .custom-table th {
            background-color: #f1f1f1;
            font-weight: 500;
        }
        .custom-table tr:nth-child(even) {
            background-color: #F5F5F5;
        }
        /* Card styling for Overview */
        .overview-card {
            background-color: #F5F5F5;
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 8px;
            margin: 4px 0;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .overview-card i {
            font-size: 14px;
            color: #666;
        }
        .overview-card p {
            margin: 0;
            font-size: 13px;
        }
        /* Button styling for icons */
        .icon-button {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 13px;
            padding: 2px;
            margin: 0 2px;
        }
        /* Checkbox styling */
        input[type="checkbox"] {
            width: 13px;
            height: 13px;
        }
        /* Container styling */
        .module-content {
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 10px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
