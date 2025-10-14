import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000/users"  # Update this if hosted elsewhere

st.title("🛡️ User Registration and Login")

# Sidebar selection
choice = st.sidebar.selectbox("Choose Action", ["Register", "Login"])

# Common fields
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if choice == "Register":
    st.subheader("📋 Register")
    email = st.text_input("Email")
    password2 = st.text_input("Confirm Password", type="password")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")

    if st.button("Register"):
        payload = {
            "username": username,
            "password": password,
            "password2": password2,
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }
        response = requests.post(f"{API_BASE}/register/", json=payload)
        st.write("Status Code:", response.status_code)
        st.write("Content-Type:", response.headers.get("Content-Type"))
        # st.json(response.json())
        try:
            st.json(response.json())
        except requests.exceptions.JSONDecodeError:
            st.error("Response is not JSON!")
            st.write("Raw response:")
            st.text(response.text)


elif choice == "Login":
    st.subheader("🔐 Login")

    if st.button("Login"):
        payload = {
            "username": username,
            "password": password
        }
        response = requests.post(f"{API_BASE}/login/", json=payload)
        if response.status_code == 200:
            tokens = response.json()
            st.success("Login successful!")
            st.write("Access Token:", tokens["access"])
            st.write("Refresh Token:", tokens["refresh"])
        else:
            st.error("Login failed!")
            st.json(response.json())
