import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from skimage import color
import joblib
import os

# Must be the first Streamlit command
st.set_page_config(
    page_title="Ammonia Gas Detector", 
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Custom CSS for mobile-like interface
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .css-1d391kg {visibility: hidden;}
    
    /* Set modern gradient background */
    html, body {
        background: linear-gradient(135deg, #2c3e50, #3498db, #1abc9c) !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* Hide the vertical sidebar completely */
    .css-1lcbmhc {display: none;}
    .css-1outpf7 {display: none;}
    section[data-testid="stSidebar"] {display: none;}
    .css-1cypcdb {display: none;}
    .css-17eq0hr {display: none;}
    
    /* Remove any vertical lines or separators */
    .css-1544g2n {display: none;}
    .css-18e3th9 {display: none;}
    .vertical-divider {display: none;}
    
    /* Force full width layout with modern gradient background */
    .main .block-container {
        padding: clamp(15px, 3vw, 25px) !important;
        max-width: 800px !important;
        margin: clamp(20px, 4vw, 40px) clamp(30px, 6vw, 60px) !important;
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: clamp(20px, 4vw, 30px) !important;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #2c3e50, #3498db, #1abc9c) !important;
    }
    
    /* Remove the rectangle background - navbar text directly on green */
    .navbar-background {
        display: none;
    }
    
    /* Modern Header with glassmorphism effect */
    .custom-navbar {
        background: linear-gradient(135deg, rgba(52, 152, 219, 0.9), rgba(26, 188, 156, 0.9)) !important;
        padding: clamp(20px, 4vw, 30px) !important;
        color: white;
        text-align: center;
        border-radius: clamp(20px, 4vw, 30px) clamp(20px, 4vw, 30px) 0 0 !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        margin: clamp(-15px, -3vw, -25px) clamp(-15px, -3vw, -25px) clamp(20px, 4vw, 30px) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
    }
    
    .navbar-title {
        font-size: clamp(24px, 6vw, 36px) !important;
        font-weight: 700 !important;
        margin: 0 !important;
        color: white !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3) !important;
        letter-spacing: 0.5px !important;
    }
    
    .navbar-subtitle {
        font-size: clamp(14px, 3.5vw, 18px) !important;
        opacity: 0.95 !important;
        margin: clamp(8px, 2vw, 12px) 0 0 0 !important;
        color: rgba(255, 255, 255, 0.9) !important;
        text-shadow: 0 1px 5px rgba(0,0,0,0.2) !important;
        font-weight: 300 !important;
    }
    
    /* Modern content area styling */
    .main > div {
        padding: clamp(20px, 4vw, 30px) !important;
        max-width: 100% !important;
        margin: 0 !important;
        background: transparent !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        min-height: auto !important;
    }
    
    /* Modern card-like content wrapper */
    .content-card {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: clamp(15px, 3vw, 25px) !important;
        padding: clamp(25px, 5vw, 40px) !important;
        margin: clamp(20px, 4vw, 30px) 0 !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Custom Footer - Compact bottom area */
    .custom-footer {
        background: transparent;
        padding: clamp(8px, 2vw, 12px) clamp(15px, 4vw, 20px) clamp(15px, 4vw, 20px);
        color: white;
        text-align: center;
        margin-top: auto;
    }
    
    .footer-text {
        font-size: clamp(8px, 2vw, 10px);
        opacity: 0.8;
        margin: 1px 0;
        color: white;
    }
    
    .footer-icon {
        font-size: clamp(12px, 2.5vw, 14px);
        margin: 3px 0;
        color: white;
    }
    
    /* Modern title styling */
    .app-title {
        color: #2c3e50 !important;
        font-size: clamp(24px, 6vw, 36px) !important;
        font-weight: 600 !important;
        margin-bottom: clamp(20px, 4vw, 25px) !important;
        text-align: center !important;
        background: linear-gradient(135deg, #3498db, #2c3e50) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Modern image display with elegant frame - smaller size and centered */
    .image-container {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: clamp(15px, 3vw, 20px) auto !important;
        width: 100% !important;
        text-align: center !important;
    }
    
    .uploaded-image {
        max-width: clamp(120px, 25vw, 180px) !important;
        max-height: clamp(120px, 25vw, 180px) !important;
        width: auto !important;
        height: auto !important;
        object-fit: contain !important;
        border-radius: clamp(12px, 2.5vw, 15px) !important;
        margin: 0 auto !important;
        display: block !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
        border: 2px solid rgba(52, 152, 219, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .uploaded-image:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.2) !important;
    }
    
    /* Innovative modern button styling with futuristic design */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: clamp(25px, 5vw, 35px) 0 !important;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: clamp(30px, 6vw, 50px) !important;
        padding: clamp(18px, 4vw, 25px) clamp(35px, 7vw, 50px) !important;
        font-size: clamp(16px, 4vw, 20px) !important;
        font-weight: 700 !important;
        margin: 0 !important;
        cursor: pointer !important;
        box-shadow: 
            0 8px 25px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: clamp(200px, 45vw, 280px) !important;
        height: clamp(55px, 13vw, 70px) !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        font-family: 'Segoe UI', sans-serif !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
        transition: left 0.5s !important;
        z-index: 1 !important;
    }
    
    .stButton > button:hover::before {
        left: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 
            0 15px 45px rgba(102, 126, 234, 0.6),
            0 5px 15px rgba(118, 75, 162, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        background: linear-gradient(45deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 
            0 8px 25px rgba(102, 126, 234, 0.5),
            inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stButton > button:focus {
        outline: none !important;
        box-shadow: 
            0 15px 45px rgba(102, 126, 234, 0.6),
            0 0 0 3px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Modern result display with enhanced styling */
    .result-circle {
        width: clamp(120px, 25vw, 160px) !important;
        height: clamp(120px, 25vw, 160px) !important;
        background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: clamp(25px, 5vw, 35px) auto !important;
        color: white !important;
        font-size: clamp(14px, 3.5vw, 18px) !important;
        font-weight: 700 !important;
        text-align: center !important;
        box-shadow: 0 15px 50px rgba(231, 76, 60, 0.4) !important;
        border: 4px solid rgba(255, 255, 255, 0.3) !important;
        animation: pulse 2s infinite !important;
        position: relative !important;
    }
    
    .result-circle::before {
        content: '' !important;
        position: absolute !important;
        width: 100% !important;
        height: 100% !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, rgba(231, 76, 60, 0.3), rgba(192, 57, 43, 0.3)) !important;
        animation: ripple 2s infinite !important;
        z-index: -1 !important;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes ripple {
        0% { transform: scale(1); opacity: 1; }
        100% { transform: scale(1.3); opacity: 0; }
    }
    
    /* Modern upload area styling */
    .stFileUploader > div > div {
        border: 2px dashed rgba(52, 152, 219, 0.6) !important;
        border-radius: clamp(12px, 2.5vw, 15px) !important;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(244, 247, 251, 0.9)) !important;
        padding: clamp(20px, 4vw, 25px) !important;
        transition: all 0.3s ease !important;
        margin: clamp(15px, 3vw, 20px) 0 !important;
    }
    
    .stFileUploader > div > div > div {
        color: #3498db !important;
        font-weight: 600 !important;
        font-size: clamp(14px, 3.5vw, 18px) !important;
        text-align: center !important;
    }
    
    .stFileUploader > div > div:hover {
        background: linear-gradient(135deg, rgba(52, 152, 219, 0.1), rgba(26, 188, 156, 0.1)) !important;
        border-color: #2980b9 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(52, 152, 219, 0.2) !important;
    }
    
    /* Hide default streamlit file uploader styling */
    .uploadedFile {
        display: none;
    }
    
    /* Modern background coverage */
    .stApp > div:first-child {
        background: linear-gradient(135deg, #2c3e50, #3498db, #1abc9c) !important;
    }
    
    /* Ensure modern gradient background coverage */
    .main {
        background: linear-gradient(135deg, #2c3e50, #3498db, #1abc9c) !important;
    }
    
    /* Override any remaining background colors with modern palette */
    .css-1d391kg, .css-18e3th9, .css-1rs6os, .css-17eq0hr {
        background: linear-gradient(135deg, #2c3e50, #3498db, #1abc9c) !important;
    }
    
    /* Ensure full width usage with modern background */
    .block-container {
        padding: clamp(15px, 3vw, 25px) !important;
        max-width: 800px !important;
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: clamp(20px, 4vw, 30px) !important;
        margin: clamp(20px, 4vw, 40px) clamp(30px, 6vw, 60px) !important;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Additional background coverage */
    .element-container {
        background: transparent !important;
    }
    
    /* Remove any white spaces or gaps */
    .stMarkdown, .stButton {
        background: transparent !important;
    }
    
    /* Hide streamlit branding */
    .css-1d391kg {
        display: none;
    }
    
    /* Mobile-specific optimizations */
    @media (max-width: 480px) {
        .custom-navbar {
            padding: 15px 20px 8px;
        }
        
        .uploaded-image {
            max-width: 100px !important;
            max-height: 100px !important;
        }
        
        .custom-footer {
            padding: 5px 15px 15px;
        }
    }
    
    /* Tablet optimizations */
    @media (min-width: 481px) and (max-width: 768px) {
        .uploaded-image {
            max-width: 130px !important;
            max-height: 130px !important;
        }
    }
    
    /* Desktop optimizations */
    @media (min-width: 769px) {
        .uploaded-image {
            max-width: 150px !important;
            max-height: 150px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load the trained model
@st.cache_resource
def load_model():
    # best model path ['models\\best_model_random_forest_regressor.pkl']
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'best_model_random_forest_regressor.pkl')
    if not os.path.exists(model_path):
        st.error("Model file not found. Please ensure the model is in the correct directory.")
        return None
    model = joblib.load(model_path)
    return model

# Load the model    
model = load_model()

# Modern header section with glassmorphism effect
st.markdown("""
<div class="custom-navbar">
    <div class="navbar-title">🔬 Ammonia Gas Detector</div>
    <div class="navbar-subtitle">AI-Powered Chemical Sensing Technology</div>
</div>
""", unsafe_allow_html=True)
# File upload section
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file:
    # Show modern styled image with perfect centering
    img = Image.open(uploaded_file).convert('RGB')
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(img, width=180, caption="", use_column_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('''
    <div style="
        color: #7f8c8d; 
        font-size: clamp(14px, 3.5vw, 18px); 
        padding: clamp(25px, 5vw, 35px); 
        text-align: center;
        background: linear-gradient(135deg, rgba(52, 152, 219, 0.1), rgba(26, 188, 156, 0.1));
        border-radius: clamp(12px, 2.5vw, 15px);
        border: 2px dashed rgba(52, 152, 219, 0.3);
        margin: clamp(15px, 3vw, 20px) auto;
        font-weight: 500;
        max-width: 400px;
    ">
        📸 Upload an image to begin analysis
        <br><small style="opacity: 0.7; font-size: 0.8em;">Supported formats: JPG, JPEG, PNG</small>
    </div>
    ''', unsafe_allow_html=True)

# Innovative centered predict button
predict_clicked = st.button("Predict", key="predict_btn", help="Click to analyze the uploaded image using AI")

# Process image and show results
if uploaded_file and predict_clicked:
    # Extract features
    img = Image.open(uploaded_file).convert('RGB')
    img_array = np.array(img)
    avg_r = np.mean(img_array[:,:,0])
    avg_g = np.mean(img_array[:,:,1])
    avg_b = np.mean(img_array[:,:,2])

    img_lab = color.rgb2lab(img_array / 255.0)
    avg_l = np.mean(img_lab[:,:,0])
    avg_a = np.mean(img_lab[:,:,1])
    avg_b_lab = np.mean(img_lab[:,:,2])

    features = np.array([[avg_r, avg_g, avg_b, avg_l, avg_a, avg_b_lab, 0]])  # dE = 0

    # Predict
    concentration = model.predict(features)[0]
    
    # Display modern result with enhanced styling
    st.markdown(f'''
    <div class="result-circle">
        <div>
            <div style="font-size: clamp(20px, 5vw, 28px); font-weight: 700; margin-bottom: 5px;">{concentration:.0f}</div>
            <div style="font-size: clamp(12px, 3vw, 16px); opacity: 0.9; font-weight: 400;">PPM</div>
        </div>
    </div>
    <div style="text-align: center; margin-top: 15px; color: #2c3e50; font-size: clamp(14px, 3.5vw, 18px); font-weight: 600;">
        Ammonia Concentration Detected
    </div>
    ''', unsafe_allow_html=True)
