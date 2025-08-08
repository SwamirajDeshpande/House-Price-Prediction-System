import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# -------------------------------
# 1. Initialize session state
# -------------------------------
st.set_page_config(page_title="House Price Predictor", layout="centered")

st.session_state.setdefault("credentials", {})  # For storing username-passwords
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", "")

# -------------------------------
# 2. Sign-In Page (create user)
# -------------------------------
def signin_page():
    st.title("📝 Sign-Up")
    with st.form("signup_form"):
        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create 4-digit Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Create Account")
        
        if submit:
            if not new_user or not new_pass or not confirm:
                st.warning("Please fill in all fields.")
            elif new_pass != confirm:
                st.warning("Passwords do not match.")
            elif new_user in st.session_state["credentials"]:
                st.warning("Username already exists.")
            else:
                st.session_state["credentials"][new_user] = new_pass
                st.success("Account created successfully! You can now log in.")

# -------------------------------
# 3. Login Page
# -------------------------------
def login_page():
    st.title("🔐 Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")

        if login:
            stored_pass = st.session_state["credentials"].get(username)
            if stored_pass and stored_pass == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")

# -------------------------------
# 4. House Price Predictor App
# -------------------------------
def house_price_app():
    st.title("🏠 House Price Prediction App")
    st.markdown(f"Welcome, **{st.session_state.username}**!")

    # Sample Dataset
    data = {
        'Area': [1000, 1500, 1200, 1000, 2000],
        'Bedroom': [2, 3, 2, 4, 4],
        'Age': [5, 7, 3, 10, 2],
        'Price': [50, 65, 55, 70, 85]
    }
    df = pd.DataFrame(data)

    # Train Model
    x = df[['Area', 'Bedroom', 'Age']]
    y = df[['Price']]
    model = LinearRegression()
    model.fit(x, y)

    # Prediction Inputs
    st.subheader("🔍 Enter House Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        area = st.number_input("Area (sqft)", min_value=500, max_value=5000, value=1600, step=100)
    with col2:
        bedroom = st.number_input("Bedrooms", min_value=1, max_value=10, value=3)
    with col3:
        age = st.number_input("Age of House (years)", min_value=0, max_value=100, value=4)

    if st.button("Predict Price"):
        prediction = model.predict([[area, bedroom, age]])
        st.success(f"Predicted House Price: ₹ {round(float(prediction[0]), 2)} lakhs")

    #------- Optional work-------
    # # Training Data & Model Info
    # with st.expander(" View Training Data and Model Details"):
    #     st.dataframe(df)
    #     st.write("### Model Coefficients")
    #     st.write(f"Area: {model.coef_[0][0]:.2f}")
    #     st.write(f"Bedroom: {model.coef_[0][1]:.2f}")
    #     st.write(f"Age: {model.coef_[0][2]:.2f}")
    #     st.write(f"Intercept: {model.intercept_[0]:.2f}")

    #     y_pred = model.predict(x)
    #     st.write("### Model Evaluation")
    #     st.write(f"MSE: {mean_squared_error(y, y_pred):.2f}")
    #     st.write(f"R² Score: {r2_score(y, y_pred):.2f}")

    # Visualization
    # with st.expander(" Area vs Price Plot"):
    #     plt.figure(figsize=(8, 5))
    #     plt.scatter(df['Area'], df['Price'], color='blue', label='Actual Prices')
    #     plt.plot(df['Area'], model.predict(x), color='red', label='Model Prediction')
    #     plt.xlabel("Area (sqft)")
    #     plt.ylabel("Price (in lakhs)")
    #     plt.title("Area vs Price")
    #     plt.legend()
    #     st.pyplot(plt)

    # Logout
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""

# -------------------------------
# 5. Navigation: Sign-in | Login | App
# -------------------------------
menu = st.sidebar.radio("Navigation", ["Sign-in", "Login", "App"])

if menu == "Sign-in":
    signin_page()
elif menu == "Login":
    login_page()
elif menu == "App":
    if st.session_state.logged_in:
        house_price_app()
    else:
        st.warning("You must log in first.")

