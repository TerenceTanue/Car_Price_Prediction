import streamlit as st
import pandas as pd
#import pickle
from joblib import load

loaded_model = load('car_price_prediction_model.joblib')

# Load the saved model
#loaded_model = pickle.load(open('car_price_prediction_model_streamlit.pkl', 'rb'))

# Load the dataset
data = pd.read_csv("cleaned_car_data.csv")


# Set page config
st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="centered")

# Main Title
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🚗 Car Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Get an instant estimate for your car's resale value</p>", unsafe_allow_html=True)

st.divider()

# Input Section
st.subheader("🔧 Car Details")

col1, col2 = st.columns(2)

with col1:
    selected_company = st.selectbox("🏢 Car Company", sorted(data['company'].unique()))
    fuel_type = st.selectbox("⛽ Fuel Type", sorted(data['fuel_type'].unique()))
    year = st.slider("📅 Year of Manufacture", min_value=2005, max_value=2024, value=2019)

with col2:
    filtered_names = data[data['company'] == selected_company]['name'].unique()
    selected_name = st.selectbox("🚘 Car Model", sorted(filtered_names))
    kms_driven = st.number_input("🛣️ Kilometers Driven", min_value=0, max_value=500000, value=60000, step=500)

# Prediction Button
predict_button = st.button("🔍 Predict Price", type="primary")

if predict_button:
    new_data = pd.DataFrame({
        'name': [selected_name],
        'company': [selected_company],
        'year': [year],
        'kms_driven': [kms_driven],
        'fuel_type': [fuel_type]
    })

    predicted_price = loaded_model.predict(new_data)

    # Result Animation and Display
    st.session_state.show_result = True
    st.balloons()

    st.markdown("### 🎯 Estimated Price")
    st.metric(label="💰 Resale Value", value=f"₹{predicted_price[0]:,.2f}")

    # Scroll down using Streamlit's st.session_state to manage the flow
    st.session_state.auto_scroll = True


# Auto-scroll to results section when the prediction button is clicked
if st.session_state.get('auto_scroll', False):
    st.markdown("<a id='result'></a>", unsafe_allow_html=True)  # Anchor for auto-scrolling

st.divider()
st.caption("Made with ❤️ by Terence W Tanue")