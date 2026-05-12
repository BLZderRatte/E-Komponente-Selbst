import streamlit as st
from PIL import Image, ImageOps
import tensorflow as tf
import numpy as np
from datetime import datetime
import time

# ====================== ULTIMATIVE HACKER UI ======================
st.set_page_config(page_title="NEON VOID DETECTOR", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    
    .stApp {
        background: #000000;
        color: #00ff41;
        font-family: 'VT323', monospace;
    }
    
    h1, h2, h3 {
        text-shadow: 0 0 20px #00ff41, 0 0 40px #00ff41;
        animation: glitch 1.8s infinite;
    }
    
    @keyframes glitch {
        0% { text-shadow: 2px 0 #ff00ff, -2px 0 #00ffff; }
        20% { text-shadow: -2px 0 #ff00ff, 2px 0 #00ffff; }
        40% { text-shadow: 2px 0 #00ff41, -2px 0 #ffff00; }
        100% { text-shadow: 0 0 25px #00ff41; }
    }
    
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(transparent 0px, transparent 2px, rgba(0, 255, 65, 0.04) 2px, rgba(0, 255, 65, 0.04) 4px);
        pointer-events: none;
        z-index: 9999;
        animation: scan 4s linear infinite;
    }
    @keyframes scan { 0% { transform: translateY(-100%); } 100% { transform: translateY(100%); } }
    
    /* Epische Hacker Boxes */
    .hacker-box, .result-box {
        background: rgba(0, 25, 0, 0.92);
        border: 2px solid #00ff41;
        box-shadow: 0 0 20px #00ff41, 0 0 45px #00ff41;
        padding: 20px;
        border-radius: 8px;
        margin: 12px 0;
        animation: pulse 2.5s infinite alternate;
    }
    
    @keyframes pulse { 
        from { box-shadow: 0 0 15px #00ff41; } 
        to { box-shadow: 0 0 45px #00ff41; } 
    }
    
    /* === KRASSER HACKER SELECT STYLE === */
    div[data-baseweb="select"] {
        background-color: #0a0a0a !important;
        border: 2px solid #00ff41 !important;
        box-shadow: 0 0 15px #00ff41 !important;
        border-radius: 6px;
    }
    div[data-baseweb="select"] div {
        background-color: #111111 !important;
        color: #00ff41 !important;
    }
    div[data-baseweb="select"] span {
        color: #00ff41 !important;
        text-shadow: 0 0 8px #00ff41;
    }
    
    /* Dropdown Liste */
    div[role="listbox"] {
        background-color: #0a0a0a !important;
        border: 2px solid #00ff41 !important;
    }
    div[role="option"] {
        color: #00ff41 !important;
        background-color: #111111 !important;
        padding: 10px;
    }
    div[role="option"]:hover {
        background-color: #003300 !important;
        color: #ffff00 !important;
        text-shadow: 0 0 10px #ffff00;
    }
    
    /* Radio Buttons */
    .stRadio label {
        color: #00ff41 !important;
        text-shadow: 0 0 8px #00ff41;
    }
    
    /* Button */
    .stButton>button {
        background-color: #000000;
        color: #00ff41;
        border: 2px solid #00ff41;
        font-size: 1.25em;
        padding: 12px 30px;
        box-shadow: 0 0 20px #00ff41;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #00ff41;
        color: #000000;
        box-shadow: 0 0 35px #ffff00;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: #000000 !important;
        border: 2px dashed #00ff41 !important;
        border-radius: 8px;
        padding: 25px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ NEON VOID DETECTOR v1.337")
st.markdown("**SYSTEM BREACH PROTOCOL ACTIVE**")

# ====================== MODELL LADEN ======================
@st.cache_resource(show_spinner=False)
def load_model():
    return tf.keras.models.load_model("model/keras_model.h5", compile=False)

model = load_model()

@st.cache_data
def load_labels():
    with open("model/labels.txt", "r", encoding="utf-8") as f:
        return [line.strip().split(" ", 1)[-1] for line in f.readlines()]

class_names = load_labels()

# ====================== DATEN ======================
component_info = { ... }   # Ihre vollständigen Beschreibungen hier
component_examples = { ... }  # Ihre vollständigen Beispiele hier

# ====================== FARBRING RECHNER ======================
color_options = ["— Ignorieren —", "Schwarz", "Braun", "Rot", "Orange", "Gelb", "Grün", "Blau", "Violett", "Grau", "Weiß"]
color_values = {"Schwarz":0, "Braun":1, "Rot":2, "Orange":3, "Gelb":4, "Grün":5, "Blau":6, "Violett":7, "Grau":8, "Weiß":9}
multiplier_options = ["— Ignorieren —", "Schwarz", "Braun", "Rot", "Orange", "Gelb", "Grün", "Blau", "Gold", "Silber"]
tolerance_options = ["— Ignorieren —", "Gold (±5%)", "Silber (±10%)", "Braun (±1%)", "Rot (±2%)"]

# ====================== UPLOAD & ANALYSE ======================
uploaded_file = st.file_uploader("**UPLOAD IMAGE TO ANALYZE**", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    # ... (Rest des Codes bleibt gleich wie in der letzten Version) ...
    
    # Ergebnis-Box
    st.markdown(f"""
    <div class="result-box">
        <h2>BREACH SUCCESSFUL</h2>
        <h3>{predicted_label.upper()}</h3>
        <p>CONFIDENCE: {confidence:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

    # Technische + Praktische in Hacker-Boxes
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("TECHNISCHE SPEZIFIKATION")
        st.markdown(f'<div class="hacker-box">{component_info.get(predicted_label, "Daten nicht verfügbar.")}</div>', unsafe_allow_html=True)
    with col2:
        st.subheader("PRAKTISCHE ANWENDUNGEN")
        st.markdown(f'<div class="hacker-box">{component_examples.get(predicted_label, "Keine Daten.")}</div>', unsafe_allow_html=True)

    # Widerstands-Decoder (mit verbesserten Feldern)
    if predicted_label == "Widerstand":
        st.subheader("🎨 WIDERSTANDS-FARBRING DECODER")
        band_count = st.radio("Anzahl der Farbringe", [4, 5, 6], horizontal=True, key="band_count")
        cols = st.columns(6)
        b1 = cols[0].selectbox("Band 1", color_options, index=1, key="b1")
        b2 = cols[1].selectbox("Band 2", color_options, index=1, key="b2")
        b3 = cols[2].selectbox("Band 3", color_options, index=0, key="b3") if band_count >= 5 else "— Ignorieren —"
        b_mult = cols[3].selectbox("Multiplikator", multiplier_options, index=1, key="b_mult")
        b_tol = cols[4].selectbox("Toleranz", tolerance_options, index=1, key="b_tol")
        
        if band_count == 6:
            b6 = cols[5].selectbox("Band 6", ["— Ignorieren —", "Braun (100 ppm)", "Rot (50 ppm)"], index=0, key="b6")
        else:
            b6 = "— Ignorieren —"

        if st.button("🔢 DECODE RESISTANCE", type="primary"):
            # ... (Berechnungs-Code bleibt gleich) ...
            pass

else:
    st.markdown("""
        <div class="hacker-box" style="text-align:center; padding:50px;">
            <h2>> NEURAL INTERFACE ONLINE</h2>
            <p>> WAITING FOR TARGET IMAGE UPLOAD...</p>
            <p>> SYSTEM READY FOR BREACH</p>
        </div>
    """, unsafe_allow_html=True)

# Sidebar (wie zuvor)
with st.sidebar:
    st.markdown("**NEON VOID v1.337**")
    st.write(f"**ACTIVE TARGET CLASSES:** {len(class_names)}")
    st.divider()
    st.markdown("**KNOWN TARGETS:**")
    for label in class_names:
        st.markdown(f"⚡ **{label}**")
