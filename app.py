import streamlit as st
import pickle
import pandas as pd

# Apply background image
def set_bg(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialize session state for login and user storage
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "users" not in st.session_state:
    try:
        with open("users.pkl", "rb") as f:
            st.session_state["users"] = pickle.load(f)
    except FileNotFoundError:
        st.session_state["users"] = {"admin": "admin123"}  # Default user

# Function to save user data
def save_users():
    with open("users.pkl", "wb") as f:
        pickle.dump(st.session_state["users"], f)

# Function for login page
def login_page():
    set_bg("https://source.unsplash.com/1600x900/?technology,login")  # Background image for login page
    st.markdown("""
    <h1 style="display: inline; font-size: 36px; color: white;">📱 Smartphone Addiction Predictor</h1>
""", unsafe_allow_html=True)
    st.subheader("🔐 Login to Continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state["users"] and st.session_state["users"][username] == password:
            st.session_state["logged_in"] = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")
    
    if st.button("⬅️ Back"):
        st.session_state["show_register"] = False
        st.rerun()

    st.markdown("---")
    if st.button("Don't have an account? Register here"):
        st.session_state["show_register"] = True
        st.rerun()

# Function for registration page
def register_page():
    set_bg("https://source.unsplash.com/1600x900/?register,signup")  # Background image for registration page
    st.title("📝 Register")
    st.subheader("Create a new account")

    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_username in st.session_state["users"]:
            st.error("❌ Username already exists! Try a different one.")
        elif new_password != confirm_password:
            st.error("❌ Passwords do not match!")
        else:
            st.session_state["users"][new_username] = new_password
            save_users()
            st.success("✅ Registration successful! Please log in.")
            st.session_state["show_register"] = False
            st.rerun()
    
    if st.button("⬅️ Back"):
        st.session_state["show_register"] = False
        st.rerun()

# Show Register or Login Page
if "show_register" in st.session_state and st.session_state["show_register"]:
    register_page()
    st.stop()

if not st.session_state["logged_in"]:
    login_page()
    st.stop()

# ========== Main App (Smartphone Addiction Predictor) ==========
set_bg("https://source.unsplash.com/1600x900/?smartphone,technology")  # Background image for main page
# Streamlit app title using HTML for inline styling with smaller font size
st.markdown("""
    <h1 style="display: inline; font-size: 36px; color: white;">📱 Smartphone Addiction Predictor</h1>
""", unsafe_allow_html=True)

# Instructions with smaller font size for subheader
st.markdown("""
    <h3 style="font-size: 18px; color: white;">Choose either 1 (Yes) or 0 (No):</h3>
""", unsafe_allow_html=True)


# Load the trained model
with open('phone_addiction_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Collecting user input
q1 = st.selectbox("Do you use your phone to click pictures of class notes?", [1, 0])
q2 = st.selectbox("Do you buy books/access books from your mobile?", [1, 0])
q3 = st.selectbox("Does your phone's battery last a day?", [1, 0])
q4 = st.selectbox("When your phone's battery dies out, do you run for the charger?", [1, 0])
q5 = st.selectbox("Do you worry about losing your cell phone?", [1, 0])
q6 = st.selectbox("Do you take your phone to the bathroom?", [1, 0])

# Prediction button
if st.button("Predict"):
    input_features = [q1, q2, q3, q4, q5, q6]
    prediction = model.predict([input_features])[0]
    
    if prediction == 1:
        st.error("🔴 You are likely addicted to your smartphone.")
    else:
        st.success("🟢 You are not addicted to your smartphone.")

# Sidebar for additional info
with st.sidebar:
    st.markdown("## Navigation")
    if st.button("About"):
        st.sidebar.write("This app predicts smartphone addiction using a machine learning model.")
    if st.button("Algorithm Used"):
        st.sidebar.write("Algorithm: Ensembled Techniques.")
    if st.button("Dataset"):
        df = pd.read_csv('Smart_phone_addiction.csv')
        st.sidebar.dataframe(df)
    
    if st.button("⬅️ Logout"):
        st.session_state["logged_in"] = False
        st.rerun()
