import streamlit as st
from PIL import Image, ImageOps
import tensorflow as tf
import numpy as np
from datetime import datetime
import time

# ====================== ULTIMATIVE HACKER UI ======================
st.set_page_config(page_title="E-KOMPONENTEN DETEKTOR", page_icon="⚡", layout="centered")

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
        animation: glitch 1.8s infinite;
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
        background: repeating-linear-gradient(transparent 0px, transparent 2px, rgba(0, 255, 65, 0.04) 2px, rgba(0, 255, 65, 0.04) 4px);
        pointer-events: none;
        z-index: 9999;
        animation: scan 4s linear infinite;
    }
    @keyframes scan { 0% { transform: translateY(-100%); } 100% { transform: translateY(100%); } }
    
    /* Neon Border */
    .neon-border {
        border: 2px solid #00ff41;
        box-shadow: 0 0 15px #00ff41, 0 0 35px #00ff41;
        padding: 15px;
        border-radius: 8px;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { box-shadow: 0 0 10px #00ff41; } to { box-shadow: 0 0 40px #00ff41; } }
    
    /* File Uploader - Hacker Style */
    .stFileUploader {
        background: #000000 !important;
        border: 2px dashed #00ff41 !important;
        border-radius: 8px;
        padding: 25px !important;
        text-align: center;
        box-shadow: 0 0 20px #00ff41;
        transition: all 0.3s;
    }
    .stFileUploader:hover {
        box-shadow: 0 0 35px #00ff41;
        border-color: #ffff00;
    }
    .stFileUploader label {
        color: #00ff41 !important;
        font-size: 1.3em;
        text-shadow: 0 0 10px #00ff41;
    }
    
    /* Select Boxes & Radio - Terminal Style */
    .stSelectbox, .stRadio {
        background: #0a0a0a !important;
    }
    div[data-baseweb="select"] div {
        background-color: #111111 !important;
        border: 1px solid #00ff41 !important;
        color: #00ff41 !important;
    }
    div[data-baseweb="select"] span {
        color: #00ff41 !important;
    }
    
    /* Radio Buttons */
    .stRadio label {
        color: #00ff41 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #000000;
        color: #00ff41;
        border: 2px solid #00ff41;
        font-family: 'VT323', monospace;
        font-size: 1.2em;
        padding: 10px 25px;
        box-shadow: 0 0 15px #00ff41;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #00ff41;
        color: #000000;
        box-shadow: 0 0 30px #ffff00;
    }
    
    .terminal {
        background: rgba(0, 30, 0, 0.9);
        border: 1px solid #00ff41;
        padding: 15px;
        font-family: 'VT323', monospace;
        color: #00ff41;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ E-KOMPONENTEN DETEKTOR ⚡")
st.markdown("**SYSTEM AKTIV**")

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

# ====================== KOMPONENTEN DATEN ======================
component_info = {
    "Diode": "Ermöglicht den Stromfluss nur in eine Richtung. Wird zur Gleichrichtung von Wechselstrom und als Schutzdiode eingesetzt.",
    "Induktor": "Speichert Energie in einem magnetischen Feld. Wird in Schaltnetzteilen, Filtern und zur Entstörung verwendet.",
    "Kondensator": "Speichert elektrische Energie in einem elektrischen Feld. Dient zur Spannungsglättung, Entkopplung und in Filterschaltungen.",
    "LED": "Lichtemittierende Diode. Wandelt Strom direkt in Licht um. Hauptanwendung: Beleuchtung und optische Anzeigen.",
    "Transformator": "Überträgt Energie durch elektromagnetische Induktion. Hauptsächlich zur Spannungswandlung.",
    "Transistor": "Aktives Bauelement zur Verstärkung und Schaltung von Signalen. Grundlage aller modernen Elektronik.",
    "Widerstand": "Begrenzt den elektrischen Stromfluss nach dem ohmschen Gesetz."
}

component_examples = {
    "Diode": "• Einweggleichrichter\n• Freilaufdiode bei Motoren",
    "Induktor": "• DC-DC-Wandler\n• LC-Filter",
    "Kondensator": "• Netzteil-Glättung\n• Timer-Schaltungen",
    "LED": "• Leuchtanzeigen\n• Arduino-Projekte",
    "Transformator": "• Steckernetzteile\n• Spannungswandlung",
    "Transistor": "• Signalverstärker\n• Motorsteuerung",
    "Widerstand": "• Spannungsteiler\n• LED-Strombegrenzung"
}

# ====================== FARBRING RECHNER ======================
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
        time.sleep(0.7)
        predictions = model.predict(img_array, verbose=0)
    
    predicted_idx = int(np.argmax(predictions[0]))
    confidence = float(predictions[0][predicted_idx]) * 100
    predicted_label = class_names[predicted_idx]

    if confidence >= 75:
        st.success(f"**KOMPONENTE ERKANNT → {predicted_label.upper()}**")
    elif confidence >= 50:
        st.warning(f"**WAHRSCHEINLICH → {predicted_label.upper()}**")
    else:
        st.error(f"**VIELLEICHT → {predicted_label.upper()}**")
    
    st.metric("**CONFIDENCE LEVEL**", f"{confidence:.1f}%")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("TECHNISCHE SPEZIFIKATION")
        st.info(component_info.get(predicted_label, "Daten nicht verfügbar."))
    with col2:
        st.subheader("PRAKTISCHE ANWENDUNGEN")
        st.info(component_examples.get(predicted_label, "Keine Daten."))

    # ====================== WIDERSTANDS-RECHNER ======================
    if predicted_label == "Widerstand":
        st.subheader("WIDERSTANDS-FARBRING DECODER")
        band_count = st.radio("Anzahl der Farbringe", [4, 5, 6], horizontal=True, key="band_count")

        cols = st.columns(6)
        b1 = cols[0].selectbox("Band 1", color_options, index=1, key="b1")
        b2 = cols[1].selectbox("Band 2", color_options, index=1, key="b2")
        
        b3 = cols[2].selectbox("Band 3", color_options, index=0, key="b3") if band_count >= 5 else "— Ignorieren —"
        b_mult = cols[3].selectbox("Multiplikator", multiplier_options, index=1, key="b_mult")
        b_tol = cols[4].selectbox("Toleranz", tolerance_options, index=1, key="b_tol")
        
        b6 = cols[5].selectbox("Band 6", ["— Ignorieren —", "Braun (100 ppm)", "Rot (50 ppm)"], index=0, key="b6") if band_count == 6 else "— Ignorieren —"

        if st.button("🔢 DECODE RESISTANCE", type="primary"):
            try:
                digits = [str(color_values[b]) for b in [b1, b2, b3] if b != "— Ignorieren —"]
                if len(digits) < 2:
                    st.error("Mindestens zwei Ziffernbänder erforderlich.")
                else:
                    significant = int("".join(digits))
                    if b_mult == "Gold": multiplier = 0.1
                    elif b_mult == "Silber": multiplier = 0.01
                    elif b_mult != "— Ignorieren —": multiplier = 10 ** color_values[b_mult]
                    else: multiplier = 1
                    
                    resistance = significant * multiplier
                    if resistance >= 1000000:
                        val = f"{resistance/1000000:.2f} MΩ"
                    elif resistance >= 1000:
                        val = f"{resistance/1000:.2f} kΩ"
                    else:
                        val = f"{int(resistance)} Ω"
                    
                    st.success(f"**DECODED VALUE:** {val}")
                    if b_tol != "— Ignorieren —":
                        st.info(f"**TOLERANZ:** {b_tol}")
            except:
                st.error("Decodierungsfehler.")

    st.caption(f"**SYSTEM LOG:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} — NEON VOID ONLINE")

else:
    st.markdown("""
        <div class="terminal neon-border">
            <p>> INITIALIZING NEURAL SCAN INTERFACE...</p>
            <p>> WAITING FOR TARGET IMAGE UPLOAD...</p>
            <p>> SYSTEM ARMED AND READY FOR BREACH</p>
        </div>
    """, unsafe_allow_html=True)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("**E-DETEKTOR**")
    st.write(f"**ACTIVE TARGET CLASSES:** {len(class_names)}")
    st.write("**NEURAL STATUS:** ONLINE")
    st.divider()
    st.markdown("**KNOWN TARGETS:**")
    for label in class_names:
        st.markdown(f"⚡ **{label}**")
