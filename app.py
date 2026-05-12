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
        animation: glitch 1.5s infinite;
    }
    
    @keyframes glitch {
        0% { text-shadow: 2px 0 #ff00ff, -2px 0 #00ffff; }
        20% { text-shadow: -2px 0 #ff00ff, 2px 0 #00ffff; }
        100% { text-shadow: 0 0 25px #00ff41; }
    }
    
    /* Matrix Rain */
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
        box-shadow: 0 0 20px #00ff41;
        padding: 15px;
        border-radius: 8px;
    }
    
    /* === HACKER STYLE SELECTBOXES & RADIO === */
    div[data-baseweb="select"] {
        background-color: #0a0a0a !important;
        border: 2px solid #00ff41 !important;
        box-shadow: 0 0 15px #00ff41;
    }
    div[data-baseweb="select"] div {
        background-color: #111111 !important;
        color: #00ff41 !important;
    }
    div[data-baseweb="select"] span {
        color: #00ff41 !important;
    }
    
    /* Dropdown Optionen */
    div[role="listbox"] {
        background-color: #0a0a0a !important;
        border: 1px solid #00ff41 !important;
    }
    div[role="option"] {
        color: #00ff41 !important;
        background-color: #111111 !important;
    }
    div[role="option"]:hover {
        background-color: #003300 !important;
        color: #ffff00 !important;
    }
    
    /* Radio Buttons */
    .stRadio label {
        color: #00ff41 !important;
        text-shadow: 0 0 8px #00ff41;
    }
    .stRadio div[role="radiogroup"] label {
        background: #111111;
        border: 1px solid #00ff41;
        padding: 8px;
        margin: 4px;
        border-radius: 4px;
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
        box-shadow: 0 0 30px #ffff00;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: #000000 !important;
        border: 2px dashed #00ff41 !important;
        border-radius: 8px;
        padding: 25px !important;
    }
    .stFileUploader:hover {
        border-color: #ffff00;
        box-shadow: 0 0 25px #00ff41;
    }
    </style>
""", unsafe_allow_html=True)

# Matrix Rain
st.markdown("""
    <canvas id="matrix"></canvas>
    <script>
    const canvas = document.getElementById('matrix');
    const ctx = canvas.getContext('2d');
    function resize() { canvas.height = window.innerHeight; canvas.width = window.innerWidth; }
    resize(); window.addEventListener('resize', resize);
    
    const chars = "01アイウエオ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$@#";
    const fontSize = 14;
    let drops = Array(Math.floor(canvas.width/fontSize)).fill(1);
    
    function draw() {
        ctx.fillStyle = 'rgba(0,0,0,0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00ff41';
        ctx.font = fontSize + 'px VT323';
        for (let i = 0; i < drops.length; i++) {
            const text = chars[Math.floor(Math.random()*chars.length)];
            ctx.fillText(text, i*fontSize, drops[i]*fontSize);
            if (drops[i]*fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(draw, 35);
    </script>
""", unsafe_allow_html=True)

st.title("⚡ NEON VOID DETECTOR v1.337")
st.markdown("**SYSTEM BREACH PROTOCOL ACTIVE**")

# ====================== MODELL & DATEN ======================
@st.cache_resource(show_spinner=False)
def load_model():
    return tf.keras.models.load_model("model/keras_model.h5", compile=False)

model = load_model()

@st.cache_data
def load_labels():
    with open("model/labels.txt", "r", encoding="utf-8") as f:
        return [line.strip().split(" ", 1)[-1] for line in f.readlines()]

class_names = load_labels()

component_info = { ... }      # Ihre Beschreibungen hier einfügen
component_examples = { ... }  # Ihre Beispiele hier einfügen

# ====================== FARBRING DECODER ======================
color_options = ["— Ignorieren —", "Schwarz", "Braun", "Rot", "Orange", "Gelb", "Grün", "Blau", "Violett", "Grau", "Weiß"]
color_values = {"Schwarz":0, "Braun":1, "Rot":2, "Orange":3, "Gelb":4, "Grün":5, "Blau":6, "Violett":7, "Grau":8, "Weiß":9}
multiplier_options = ["— Ignorieren —", "Schwarz", "Braun", "Rot", "Orange", "Gelb", "Grün", "Blau", "Gold", "Silber"]
tolerance_options = ["— Ignorieren —", "Gold (±5%)", "Silber (±10%)", "Braun (±1%)", "Rot (±2%)"]

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
        time.sleep(0.6)
        predictions = model.predict(img_array, verbose=0)
    
    predicted_idx = int(np.argmax(predictions[0]))
    confidence = float(predictions[0][predicted_idx]) * 100
    predicted_label = class_names[predicted_idx]

    # Ergebnis
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
        st.info(component_info.get(predicted_label, "Keine Daten"))
    with col2:
        st.subheader("PRAKTISCHE ANWENDUNGEN")
        st.info(component_examples.get(predicted_label, "Keine Daten"))

    # ====================== WIDERSTAND DECODER ======================
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
            b6 = cols[5].selectbox("Band 6", ["— Ignorieren —", "Braun (100ppm)", "Rot (50ppm)"], index=0, key="b6")
        else:
            b6 = "— Ignorieren —"

        if st.button("🔢 DECODE RESISTANCE", type="primary"):
            try:
                digits = [str(color_values[b]) for b in [b1, b2, b3] if b != "— Ignorieren —"]
                if len(digits) < 2:
                    st.error("Mindestens Band 1 und Band 2 müssen gesetzt sein.")
                else:
                    value = int("".join(digits))
                    if b_mult == "Gold": multiplier = 0.1
                    elif b_mult == "Silber": multiplier = 0.01
                    elif b_mult != "— Ignorieren —": multiplier = 10 ** color_values[b_mult]
                    else: multiplier = 1
                    
                    resistance = value * multiplier
                    if resistance >= 1000000:
                        result = f"{resistance/1000000:.2f} MΩ"
                    elif resistance >= 1000:
                        result = f"{resistance/1000:.2f} kΩ"
                    else:
                        result = f"{int(resistance)} Ω"
                    
                    st.success(f"**DECODED VALUE:** {result}")
                    if b_tol != "— Ignorieren —":
                        st.info(f"**TOLERANZ:** {b_tol}")
            except:
                st.error("Fehler bei der Berechnung.")

    st.caption(f"**SYSTEM LOG:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

else:
    st.markdown("""
        <div class="neon-border" style="text-align:center; padding:40px;">
            <p>> WAITING FOR TARGET IMAGE...</p>
            <p>> SYSTEM READY FOR BREACH</p>
        </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("**NEON VOID v1.337**")
    st.write(f"**ACTIVE CLASSES:** {len(class_names)}")
