import streamlit as st
import numpy as np
from PIL import Image
from skimage import color
import joblib

# Load model
model = joblib.load('ammonia_prediction_model.pkl')

st.set_page_config(page_title="Ammonia Gas Detector", layout="centered")

st.title("🎨 Ammonia Color Sensor - Concentration Prediction")
st.write("Upload an image of your coated sensor, and predict ammonia concentration (%)")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert('RGB')
    st.image(img, caption="Uploaded Image", width=300)

    # Extract features
    img_array = np.array(img)
    avg_r = np.mean(img_array[:,:,0])
    avg_g = np.mean(img_array[:,:,1])
    avg_b = np.mean(img_array[:,:,2])
    img_lab = color.rgb2lab(img_array / 255.0)
    avg_l = np.mean(img_lab[:,:,0])
    avg_a = np.mean(img_lab[:,:,1])
    avg_b_lab = np.mean(img_lab[:,:,2])

    features = np.array([[avg_r, avg_g, avg_b, avg_l, avg_a, avg_b_lab, 0]])

    # Predict
    concentration = model.predict(features)[0]
    st.success(f"✅ Predicted Ammonia Concentration: **{concentration:.2f}%**")
