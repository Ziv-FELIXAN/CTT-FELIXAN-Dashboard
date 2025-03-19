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
    # Add is_active column if it doesn't exist
    try:
        c.execute("ALTER TABLE activities ADD COLUMN is_active BOOLEAN DEFAULT 1")
        conn.commit()
    except sqlite3.OperationalError:
        # Column already exists, no need to add it
        pass

    # Set is_active to 1 for all existing activities
    c.execute("UPDATE activities SET is_active = 1 WHERE is_active IS NULL")
    conn.commit()

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
            f"<li class='mb-3'><i class='bi bi-person-circle'></i> <strong>{use
