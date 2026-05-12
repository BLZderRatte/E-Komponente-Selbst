import streamlit as st
from PIL import Image, ImageOps
import tensorflow as tf
import numpy as np
from datetime import datetime
import time

# ====================== REVOLUTIONÄRES HACKER UI ======================
st.set_page_config(page_title="NEON VOID DETECTOR", page_icon="⚡", layout="centered")

# Matrix + Cyberpunk CSS + Animationen
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    
    .stApp {
        background: #000000;
        color: #00ff41;
        font-family: 'VT323', monospace;
    }
    
    h1, h2, h3 {
        font-family: 'VT323', monospace;
        text-shadow: 0 0 20px #00ff41, 0 0 40px #00ff41;
        animation: glitch 1.5s infinite;
    }
    
    @keyframes glitch {
        0% { text-shadow: 2px 0 #ff00ff, -2px 0 #00ffff; }
        20% { text-shadow: -2px 0 #ff00ff, 2px 0 #00ffff; }
        40% { text-shadow: 2px 0 #00ff41, -2px 0 #ffff00; }
        100% { text-shadow: 0 0 20px #00ff41; }
    }
    
    /* Scanlines */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            transparent 0px,
            transparent 2px,
            rgba(0, 255, 65, 0.03) 2px,
            rgba(0, 255, 65, 0.03) 4px
        );
        pointer-events: none;
        z-index: 9999;
        animation: scan 4s linear infinite;
    }
    
    @keyframes scan {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100%); }
    }
    
    .neon-border {
        border: 2px solid #00ff41;
        box-shadow: 0 0 15px #00ff41, 0 0 30px #00ff41;
        padding: 15px;
        border-radius: 8px;
        animation: pulse 2s infinite alternate;
    }
    
    @keyframes pulse {
        from { box-shadow: 0 0 10px #00ff41; }
        to { box-shadow: 0 0 30px #00ff41, 0 0 50px #00ff41; }
    }
    
    .terminal {
        background: rgba(0, 20, 0, 0.8);
        border: 1px solid #00ff41;
        padding: 12px;
        font-family: 'VT323', monospace;
        color: #00ff41;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ NEON VOID DETECTOR v1.337")
st.markdown("**SYSTEM BREACH PROTOCOL ACTIVE** — Elektrotechnische Komponenten-Erkennung")

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
# ... (component_info und component_examples wie zuvor) ...
component_info = { ... }      # Bitte Ihre bisherigen Beschreibungen hier einfügen
component_examples = { ... }  # Bitte Ihre bisherigen Beispiele hier einfügen

# Farbring Rechner (wie in letzter Version)
color_options = ["— Ignorieren —", "Schwarz", "Braun", "Rot", "Orange", "Gelb", "Grün", "Blau", "Violett", "Grau", "Weiß"]
color_values = {"Schwarz":0, "Braun":1, "Rot":2, "Orange":3, "Gelb":4, "Grün":5, "Blau":6, "Violett":7, "Grau":8, "Weiß":9}
multiplier_options = ["— Ignorieren —", "Schwarz", "Braun", "Rot", "Orange", "Gelb", "Grün", "Blau", "Gold", "Silber"]
tolerance_options = ["— Ignorieren —", "Gold (±5%)", "Silber (±10%)", "Braun (±1%)", "Rot (±2%)"]

# ====================== UPLOAD ======================
uploaded_file = st.file_uploader("**UPLOAD IMAGE TO ANALYZE**", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="**TARGET ACQUIRED**", use_column_width=True)
    
    size = (224, 224)
    image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    img_array = np.asarray(image_resized, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    with st.spinner("**BREACHING NEURAL FIREWALL...**"):
        time.sleep(0.8)  # dramatische Pause
        predictions = model.predict(img_array, verbose=0)
    
    predicted_idx = int(np.argmax(predictions[0]))
    confidence = float(predictions[0][predicted_idx]) * 100
    predicted_label = class_names[predicted_idx]

    # Ergebnis mit Hacker-Style
    if confidence >= 75:
        st.success(f"**BREACH SUCCESSFUL → {predicted_label.upper()}**")
    elif confidence >= 50:
        st.warning(f"**PARTIAL BREACH → {predicted_label.upper()}**")
    else:
        st.error(f"**BREACH COMPROMISED → {predicted_label.upper()}**")
    
    st.metric("**CONFIDENCE LEVEL**", f"{confidence:.1f}%")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("TECHNISCHE SPEZIFIKATION")
        st.info(component_info.get(predicted_label, "Daten nicht verfügbar."))
    with col2:
        st.subheader("PRAKTISCHE ANWENDUNGEN")
        st.info(component_examples.get(predicted_label, "Keine Daten."))

    # Widerstands-Rechner (wie zuvor, bleibt unverändert)
    if predicted_label == "Widerstand":
        # ... (Ihr letzter dynamischer Rechner Code hier einfügen) ...
        pass

    st.caption(f"**SYSTEM LOG:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} — NEON VOID ONLINE")

else:
    st.markdown("""
        <div class="terminal neon-border">
            <p>> INITIALIZING NEURAL SCAN...</p>
            <p>> WAITING FOR TARGET IMAGE...</p>
            <p>> SYSTEM READY FOR BREACH</p>
        </div>
    """, unsafe_allow_html=True)

# Sidebar mit Hacker-Style
with st.sidebar:
    st.markdown("**NEON VOID v1.337**")
    st.write(f"**ACTIVE CLASSES:** {len(class_names)}")
    st.write("**STATUS:** ONLINE")
    st.divider()
    st.markdown("**KNOWN TARGETS:**")
    for label in class_names:
        st.markdown(f"⚡ **{label}**")
