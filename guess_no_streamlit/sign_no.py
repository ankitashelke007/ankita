import streamlit as st
import random
import sqlite3
import hashlib

# Database Connection
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Create users table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")
conn.commit()

# Hash Password Function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "number" not in st.session_state:
    st.session_state["number"] = random.randint(1, 100)
if "game_active" not in st.session_state:
    st.session_state["game_active"] = False

# Signup Function
def signup():
    st.header("Create an Account")

    username = st.text_input("Enter Username:")
    email = st.text_input("Enter Email:")
    password = st.text_input("Enter Password:", type="password")

    if st.button("Sign Up"):
        if username and email and password:
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))
            if cursor.fetchone():
                st.warning("Email already registered! Try logging in.")
            else:
                hashed_pw = hash_password(password)
                cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                               (username, email, hashed_pw))
                conn.commit()
                st.success(f"Account created for {username}! You can now log in.")
        else:
            st.error("All fields are required!")

# Login Function
def login():
    st.header("Login to Your Account")

    email = st.text_input("Enter Email:")
    password = st.text_input("Enter Password:", type="password")

    if st.button("Login"):
        if email and password:
            cursor.execute("SELECT username, password FROM users WHERE email=?", (email,))
            user = cursor.fetchone()
            if user and user[1] == hash_password(password):
                st.success(f"Welcome back, {user[0]}!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = user[0]
                st.session_state["game_active"] = True  # Activate game after login
            else:
                st.error("Invalid email or password. Please try again.")
        else:
            st.error("All fields are required!")

# Game Function
def guessing_game():
    st.header(f"🎮 Welcome, {st.session_state['username']}! Guess the Number 🎯")

    if not st.session_state["game_active"]:
        st.write("Click 'Start New Game' to begin!")

    if st.button("Start New Game"):
        st.session_state["number"] = random.randint(1, 100)
        st.session_state["game_active"] = True
        st.success("A new number has been generated! Start guessing.")

    if st.session_state["game_active"]:
        guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1)

        if st.button("Submit Guess"):
            if guess < st.session_state["number"]:
                st.warning("Guess higher! 🔼")
            elif guess > st.session_state["number"]:
                st.warning("Guess lower! 🔽")
            else:
                st.success("🎉 You Won! 🎊 The number was " + str(st.session_state["number"]))
                st.session_state["game_active"] = False  # End game

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["game_active"] = False
        st.success("You have logged out successfully.")

# Main App Function
def main():
    st.title("🎮 Number Guessing Game with Login 🏆")

    st.sidebar.header("Navigation")

    if st.session_state["logged_in"]:
        guessing_game()
    else:
        page = st.sidebar.radio("Go to", ["Home", "About", "Signup", "Login"])

        if page == "Home":
            st.header("Welcome to the Number Guessing Game!")
            st.write("Sign up or log in to start playing!")

        elif page == "About":
            st.header("About This App")
            st.write("This is a simple number guessing game built with Streamlit and SQLite.")

        elif page == "Signup":
            signup()

        elif page == "Login":
            login()

if __name__ == "__main__":
    main()
