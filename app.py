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
    
    .result-box, .hacker-box {
        background: rgba(0, 25, 0, 0.95);
        border: 2px solid #00ff41;
        box-shadow: 0 0 25px #00ff41, 0 0 50px #00ff41;
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0;
        animation: pulse 2.5s infinite alternate;
    }
    
    @keyframes pulse { 
        from { box-shadow: 0 0 15px #00ff41; } 
        to { box-shadow: 0 0 50px #00ff41; } 
    }
    
    /* Starke Hacker Select-Style */
    div[data-baseweb="select"] {
        background-color: #0a0a0a !important;
        border: 2px solid #00ff41 !important;
        box-shadow: 0 0 20px #00ff41 !important;
    }
    div[data-baseweb="select"] span {
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41;
    }
    div[role="option"]:hover {
        background-color: #003300 !important;
        color: #ffff00 !important;
    }
    
    /* Decode Button */
    .stButton>button {
        background-color: #000000;
        color: #00ff41;
        border: 3px solid #00ff41;
        font-size: 1.35em;
        padding: 15px 40px;
        box-shadow: 0 0 25px #00ff41;
    }
    .stButton>button:hover {
        background-color: #00ff41;
        color: #000000;
        box-shadow: 0 0 40px #ffff00;
        transform: scale(1.05);
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

# ====================== HAUPTBEREICH ======================
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

    # Epische Ergebnis-Box
    st.markdown(f"""
    <div class="result-box">
        <h2>BREACH SUCCESSFUL</h2>
        <h3>{predicted_label.upper()}</h3>
        <p>CONFIDENCE: {confidence:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

    # Hacker-Boxes
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("TECHNISCHE SPEZIFIKATION")
        st.markdown(f'<div class="hacker-box">{component_info.get(predicted_label, "Daten nicht verfügbar.")}</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("PRAKTISCHE ANWENDUNGEN")
        st.markdown(f'<div class="hacker-box">{component_examples.get(predicted_label, "Keine Daten.")}</div>', unsafe_allow_html=True)

    # ====================== WIDERSTANDS DECODER ======================
    if predicted_label == "Widerstand":
        st.subheader("🎨 WIDERSTANDS-FARBRING DECODER")
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
        <div class="hacker-box" style="text-align:center; padding:60px; margin-top:30px;">
            <h2>> NEURAL INTERFACE ONLINE</h2>
            <p>> WAITING FOR TARGET IMAGE UPLOAD...</p>
            <p>> SYSTEM READY FOR BREACH</p>
        </div>
    """, unsafe_allow_html=True)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("**NEON VOID v1.337**")
    st.write(f"**ACTIVE TARGET CLASSES:** {len(class_names)}")
    st.divider()
    st.markdown("**KNOWN TARGETS:**")
    for label in class_names:
        st.markdown(f"⚡ **{label}**")
