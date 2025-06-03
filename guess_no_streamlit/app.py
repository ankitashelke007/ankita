import streamlit as st
import sqlite3
import bcrypt

# Database setup
conn = sqlite3.connect('new.db')
c = conn.cursor()

# Create users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password BLOB
)
''')
conn.commit()

# Function to hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Function to check password
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# Sign up function
def signup_user(username, password):
    hashed_pw = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Login function
def login_user(username, password):
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    if result and check_password(password, result[0]):
        return True
    return False

# Streamlit UI
st.title("Login / Sign Up Page")

menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

if menu == "Sign Up":
    st.subheader("Create a New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')
    
    if st.button("Sign Up"):
        if signup_user(new_user, new_password):
            st.success("Account created successfully! Go to Login.")
        else:
            st.error("Username already exists!")

elif menu == "Login":
    st.subheader("Login to Your Account")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type='password')
    
    if st.button("Login"):
        if login_user(user, pwd):
            st.success(f"Welcome {user}!")
        else:
            st.error("Invalid username or password")
