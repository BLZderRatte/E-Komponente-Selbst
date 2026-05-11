import streamlit as st
from PIL import Image, ImageOps
import tensorflow as tf
import numpy as np
from datetime import datetime

# ====================== SEITENKONFIGURATION & CUSTOM CSS ======================
st.set_page_config(
    page_title="Elektro-Komponenten Detektor",
    page_icon="🔌",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0a0a0a;
        color: #39ff14;
    }
    h1, h2, h3, .stMarkdown, label {
        color: #39ff14 !important;
        font-family: 'Courier New', monospace;
    }
    .stButton>button {
        background-color: #0a0a0a;
        color: #39ff14;
        border: 2px solid #39ff14;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #39ff14;
        color: #0a0a0a;
        box-shadow: 0 0 15px #39ff14;
    }
    .stFileUploader {
        background-color: #111111;
        border: 2px dashed #39ff14;
        border-radius: 12px;
        padding: 20px;
    }
    .stMetricValue {
        color: #39ff14 !important;
        font-size: 1.8rem !important;
    }
    .stAlert, .stInfo {
        background-color: #111111 !important;
        color: #39ff14 !important;
        border-left: 5px solid #39ff14;
    }
    section[data-testid="stSidebar"] {
        background-color: #0f0f0f;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔌 ELEKTRO-KOMPONENTEN DETEKTOR")
st.markdown("**KI-gestützte Erkennung & technische Charakterisierung**")

# ====================== MODELL LADEN ======================
@st.cache_resource(show_spinner="Modell wird geladen...")
def load_model():
    model = tf.keras.models.load_model("model/keras_model.h5", compile=False)
    return model

model = load_model()

@st.cache_data
def load_labels():
    with open("model/labels.txt", "r", encoding="utf-8") as f:
        return [line.strip().split(" ", 1)[-1] for line in f.readlines()]

class_names = load_labels()

# ====================== KOMPONENTEN-INFORMATIONEN ======================
component_info = {
    "Diode": "Ermöglicht den Stromfluss nur in eine Richtung. Wird zur Gleichrichtung von Wechselstrom und als Schutzdiode eingesetzt.",
    "Induktor": "Speichert Energie in einem magnetischen Feld. Wird in Schaltnetzteilen, Filtern und zur Entstörung verwendet.",
    "Kondensator": "Speichert elektrische Energie in einem elektrischen Feld. Dient zur Spannungsglättung, Entkopplung und in Filterschaltungen.",
    "LED": "Lichtemittierende Diode. Wandelt Strom direkt in Licht um. Hauptanwendung: Beleuchtung und optische Anzeigen.",
    "Transformator": "Überträgt Energie durch elektromagnetische Induktion. Hauptsächlich zur Spannungswandlung und galvanischen Trennung.",
    "Transistor": "Aktives Bauelement zur Verstärkung und Schaltung von Signalen. Grundlage aller modernen Elektronik.",
    "Wiederstand": "Begrenzt den elektrischen Stromfluss nach dem ohmschen Gesetz."
}

component_examples = {
    "Diode": "• Einweggleichrichter\n• Freilaufdiode bei Motoren\n• Logikschaltungen",
    "Induktor": "• DC-DC-Wandler\n• LC-Filter\n• Schwingkreise",
    "Kondensator": "• Netzteil-Glättung\n• 555-Timer\n• Hoch-/Tiefpassfilter",
    "LED": "• Leuchtanzeigen\n• Arduino-Projekte\n• Lauflichter",
    "Transformator": "• Steckernetzteile\n• Audio-Übertrager\n• Isolierte Versorgungen",
    "Transistor": "• Signalverstärker\n• Motorsteuerung\n• Schaltstufen",
    "Wiederstand": "• Spannungsteiler\n• LED-Strombegrenzung\n• Pull-up/Pull-down"
}

# Farbring-Rechner für Widerstand
color_options = ["Schwarz", "Braun", "Rot", "Orange", "Gelb", "Grün", "Blau", "Violett", "Grau", "Weiß"]
color_values = {"Schwarz":0, "Braun":1, "Rot":2, "Orange":3, "Gelb":4, "Grün":5, "Blau":6, "Violett":7, "Grau":8, "Weiß":9}
multiplier_values = {"Schwarz":1, "Braun":10, "Rot":100, "Orange":1000, "Gelb":10000, "Grün":100000, "Blau":1000000, "Gold":0.1, "Silber":0.01}

# ====================== UPLOAD & ANALYSE ======================
uploaded_file = st.file_uploader(
    "Foto der Komponente hochladen", 
    type=["jpg", "jpeg", "png", "webp"],
    help="Hochauflösendes, gut beleuchtetes Bild liefert optimale Ergebnisse"
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Hochgeladenes Bild", use_column_width=True)
    
    size = (224, 224)
    image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    
    img_array = np.asarray(image_resized, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    
    with st.spinner("Analysiere mit neuronalem Netz..."):
        predictions = model.predict(img_array, verbose=0)
    
    predicted_idx = int(np.argmax(predictions[0]))
    confidence = float(predictions[0][predicted_idx]) * 100
    predicted_label = class_names[predicted_idx]

    # === ERGEBNISSE ===
    if confidence >= 75:
        st.success(f"**ERKANNTE KOMPONENTE:** {predicted_label.upper()}")
    elif confidence >= 50:
        st.warning(f"**WAHRSCHEINLICHE KOMPONENTE:** {predicted_label.upper()}")
    else:
        st.error(f"**UNSICHERE ERKENNUNG:** {predicted_label.upper()}")
    
    st.metric(label="**KONFIDENZ**", value=f"{confidence:.1f}%")
    
    # Technische Funktion
    st.subheader("Technische Funktion")
    st.info(component_info.get(predicted_label, "Keine Beschreibung verfügbar."))
    
    # Praktische Beispiele
    st.subheader("Praktische Anwendungsbeispiele")
    st.info(component_examples.get(predicted_label, "Keine Beispiele verfügbar."))

    # ====================== WIDERSTANDS-RECHNER ======================
    if predicted_label == "Wiederstand":
        st.subheader("🎨 Widerstands-Farbring-Code Rechner (4-Band)")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            band1 = st.selectbox("Band 1 (1. Ziffer)", color_options, index=1, key="band1")
        with col2:
            band2 = st.selectbox("Band 2 (2. Ziffer)", color_options, index=0, key="band2")
        with col3:
            band3 = st.selectbox("Band 3 (Multiplikator)", ["Schwarz", "Braun", "Rot", "Orange", "Gelb", "Grün", "Blau", "Gold", "Silber"], key="band3")
        with col4:
            band4 = st.selectbox("Band 4 (Toleranz)", ["Gold (±5%)", "Silber (±10%)", "Braun (±1%)", "Rot (±2%)"], key="band4")

        if st.button("🔢 Widerstand berechnen", type="primary"):
            try:
                digit1 = color_values[band1]
                digit2 = color_values[band2]
                
                if band3 in ["Gold", "Silber"]:
                    multiplier = multiplier_values[band3]
                else:
                    multiplier = 10 ** color_values[band3]
                
                resistance = (digit1 * 10 + digit2) * multiplier
                
                if resistance >= 1000000:
                    value_str = f"{resistance/1000000:.2f} MΩ"
                elif resistance >= 1000:
                    value_str = f"{resistance/1000:.2f} kΩ"
                else:
                    value_str = f"{int(resistance)} Ω"
                
                st.success(f"**Widerstandswert:** {value_str}")
                st.info(f"Toleranz: {band4}")
            except:
                st.error("Fehler bei der Berechnung.")

    st.caption(f"Analyse durchgeführt um {datetime.now().strftime('%H:%M:%S')} Uhr")

else:
    st.info("👆 Bitte laden Sie ein Foto einer elektrotechnischen Komponente hoch.")

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("Systeminformationen")
    st.write(f"**Trainierte Klassen:** {len(class_names)}")
    st.write(f"**Eingabegröße:** 224 × 224 px")
    st.write("**Modell:** Teachable Machine (Keras)")
    
    st.divider()
    st.markdown("**Verfügbare Komponenten:**")
    for label in class_names:
        st.markdown(f"• **{label}**")
    
    st.divider()
    st.caption("Dark Neon Edition • Giftgrün / Schwarz")
