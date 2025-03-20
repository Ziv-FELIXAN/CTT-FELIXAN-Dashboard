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
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #f5f5f5;
            padding: 5px;
            border-radius: 5px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            margin: 0 2px;
            border-radius: 5px;
            font-weight: bold;
        }
        /* Active tab color based on user type */
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #4CAF50; /* Green for Private */
            color: white;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #4CAF5080; /* 50% opacity for non-active tabs */
            color: #333;
        }
        /* Table styling */
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            border: 1px solid #E0E0E0;
        }
        .custom-table th, .custom-table td {
            border: 1px solid #E0E0E0;
            padding: 8px;
            text-align: left;
        }
        .custom-table th {
            background-color: #f1f1f1;
            font-weight: bold;
        }
        .custom-table tr:nth-child(even) {
            background-color: #F5F5F5;
        }
        /* Card styling for Overview */
        .overview-card {
            background-color: #F5F5F5;
            border: 1px solid #E0E0E0;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .overview-card i {
            font-size: 24px;
            color: #4CAF50;
        }
        .overview-card p {
            margin: 0;
            font-size: 16px;
        }
        /* Button styling for icons */
        .icon-button {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 16px;
            padding: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
