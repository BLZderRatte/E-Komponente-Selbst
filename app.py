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

# Giftgrünes Dark-Cyber Design
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

# ====================== WISSENSCHAFTLICHE BESCHREIBUNGEN ======================
component_info = {
    "Diode": "Ermöglicht den Stromfluss nur in eine Richtung. Wird zur Gleichrichtung von Wechselstrom und als Schutzdiode eingesetzt.",
    "Induktor": "Speichert Energie in einem magnetischen Feld. Wird in Schaltnetzteilen, Filtern und zur Entstörung verwendet.",
    "Kondensator": "Speichert elektrische Energie in einem elektrischen Feld. Dient zur Spannungsglättung, Entkopplung und in Filterschaltungen.",
    "LED": "Lichtemittierende Diode. Wandelt Strom direkt in Licht um. Hauptanwendung: Beleuchtung und optische Anzeigen.",
    "Transformator": "Überträgt Energie durch elektromagnetische Induktion. Hauptsächlich zur Spannungswandlung und galvanischen Trennung.",
    "Transistor": "Aktives Bauelement zur Verstärkung und Schaltung von Signalen. Grundlage aller modernen Elektronik.",
    "Widerstand": "Begrenzt den Stromfluss nach dem ohmschen Gesetz. Wird zur Strombegrenzung und Spannungsteilung eingesetzt."
}

# ====================== PRAKTISCHE ANWENDUNGSBEISPIELE ======================
component_examples = {
    "Diode": "• Einweggleichrichter für Netzteile\n• Freilaufdiode bei Relais und Motoren\n• Logikgatter (UND/OR)",
    "Induktor": "• LC-Filter und Tiefpassfilter\n• DC-DC-Wandler (Buck/Boost)\n• Schwingkreise und Oszillatoren",
    "Kondensator": "• 555-Timer Schaltungen\n• Netzteil-Glättung\n• Hochpass- und Tiefpassfilter",
    "LED": "• Einfache Leuchtdioden-Anzeige\n• Ampelschaltung mit Arduino\n• Lauflichter und 7-Segment Displays",
    "Transformator": "• Steckernetzteile (230V → 12V)\n• Audio-Übertrager\n• Isolierte Stromversorgungen",
    "Transistor": "• Einfacher Verstärker\n• Schalttransistor für Motoren/Relais\n• Darlington-Paar oder H-Brücke",
    "Widerstand": "• Spannungsteiler\n• Strombegrenzung für LEDs\n• Pull-up/Pull-down Widerstände"
}

# ====================== UPLOAD & ANALYSE ======================
uploaded_file = st.file_uploader(
    "Foto der Komponente hochladen", 
    type=["jpg", "jpeg", "png", "webp"],
    help="Hochauflösendes, gut beleuchtetes Bild liefert optimale Ergebnisse"
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Hochgeladenes Bild", use_column_width=True)
    
    # Vorverarbeitung
    size = (224, 224)
    image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    
    img_array = np.asarray(image_resized, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    
    # Inference
    with st.spinner("Analysiere mit neuronalem Netz..."):
        predictions = model.predict(img_array, verbose=0)
    
    predicted_idx = int(np.argmax(predictions[0]))
    confidence = float(predictions[0][predicted_idx]) * 100
    predicted_label = class_names[predicted_idx]

    # Ergebnis
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
    
    # Praktische Beispiele (neu)
    st.subheader("Praktische Anwendungsbeispiele")
    st.info(component_examples.get(predicted_label, "Keine Beispiele verfügbar."))

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
