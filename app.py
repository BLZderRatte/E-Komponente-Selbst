import streamlit as st
from PIL import Image, ImageOps
import tensorflow as tf
import numpy as np
from datetime import datetime
import time

# ====================== ULTIMATIVE CYBERPUNK UI ======================
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
        font-family: 'VT323', monospace;
        text-shadow: 0 0 20px #00ff41, 0 0 40px #00ff41;
        animation: glitch 1.5s infinite;
    }
    
    @keyframes glitch {
        0% { text-shadow: 2px 0 #ff00ff, -2px 0 #00ffff; }
        20% { text-shadow: -2px 0 #ff00ff, 2px 0 #00ffff; }
        40% { text-shadow: 2px 0 #00ff41, -2px 0 #ffff00; }
        100% { text-shadow: 0 0 25px #00ff41; }
    }
    
    /* Matrix Rain - Hintergrund */
    #matrix {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: -1;
        opacity: 0.18;
        pointer-events: none;
    }
    
    .neon-border {
        border: 2px solid #00ff41;
        box-shadow: 0 0 15px #00ff41, 0 0 35px #00ff41;
        padding: 15px;
        border-radius: 8px;
        animation: pulse 2s infinite alternate;
    }
    
    @keyframes pulse { 
        from { box-shadow: 0 0 10px #00ff41; } 
        to { box-shadow: 0 0 40px #00ff41; } 
    }
    
    /* Bessere Sichtbarkeit der Inhalte */
    .stFileUploader, .stSelectbox, .stRadio, .stButton, .stAlert, .stInfo {
        z-index: 10;
        position: relative;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== MATRIX RAIN ====================
st.markdown("""
    <canvas id="matrix"></canvas>
    <script>
    const canvas = document.getElementById('matrix');
    const ctx = canvas.getContext('2d');
    
    function resizeCanvas() {
        canvas.height = window.innerHeight;
        canvas.width = window.innerWidth;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    const chars = "01アイウエオカキクケコ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$@#%&";
    const fontSize = 14;
    let columns = canvas.width / fontSize;
    let drops = Array(Math.floor(columns)).fill(1);
    
    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00ff41';
        ctx.font = fontSize + 'px VT323';
        
        for (let i = 0; i < drops.length; i++) {
            const text = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    setInterval(draw, 35);
    </script>
""", unsafe_allow_html=True)

st.title("⚡ NEON VOID DETECTOR v1.337")
st.markdown("**SYSTEM BREACH PROTOCOL ACTIVE — MATRIX LINK ESTABLISHED**")

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

# ====================== UPLOAD & ANALYSE ======================
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

    # Widerstands-Rechner (dynamisch)
    if predicted_label == "Widerstand":
        st.subheader("🎨 WIDERSTANDS-FARBRING DECODER")
        # ... (Ihr bisheriger Rechner-Code kann hier eingefügt werden) ...

    st.caption(f"**SYSTEM LOG:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

else:
    st.markdown("""
        <div class="neon-border" style="text-align:center; padding:30px;">
            <p>> INITIALIZING NEURAL SCAN INTERFACE...</p>
            <p>> WAITING FOR TARGET IMAGE...</p>
            <p>> SYSTEM ARMED AND READY</p>
        </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("**NEON VOID v1.337**")
    st.write(f"**ACTIVE CLASSES:** {len(class_names)}")
    st.divider()
    st.markdown("**KNOWN TARGETS:**")
    for label in class_names:
        st.markdown(f"⚡ **{label}**")
