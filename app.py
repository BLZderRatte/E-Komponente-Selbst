import streamlit as st
from PIL import Image, ImageOps
import tensorflow as tf
import numpy as np
from datetime import datetime

# ====================== SEITENKONFIGURATION ======================
st.set_page_config(page_title="Elektro-Komponenten Detektor", page_icon="🔌", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; color: #39ff14; }
    h1, h2, h3, label { color: #39ff14 !important; font-family: 'Courier New', monospace; }
    .stButton>button {
        background-color: #0a0a0a; color: #39ff14; border: 2px solid #39ff14; border-radius: 8px;
    }
    .stButton>button:hover { background-color: #39ff14; color: #0a0a0a; box-shadow: 0 0 15px #39ff14; }
    .stFileUploader { background-color: #111111; border: 2px dashed #39ff14; border-radius: 12px; padding: 20px; }
    .stMetricValue { color: #39ff14 !important; font-size: 1.8rem !important; }
    .stAlert, .stInfo { background-color: #111111 !important; color: #39ff14 !important; border-left: 5px solid #39ff14; }
    </style>
""", unsafe_allow_html=True)

st.title("🔌 ELEKTRO-KOMPONENTEN DETEKTOR")
st.markdown("**KI-gestützte Erkennung & technische Charakterisierung**")

# ====================== MODELL LADEN ======================
@st.cache_resource(show_spinner="Modell wird geladen...")
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

# Farbring Rechner
color_options = ["— Ignorieren —", "Schwarz", "Braun", "Rot", "Orange", "Gelb", "Grün", "Blau", "Violett", "Grau", "Weiß"]
color_values = {"Schwarz":0, "Braun":1, "Rot":2, "Orange":3, "Gelb":4, "Grün":5, "Blau":6, "Violett":7, "Grau":8, "Weiß":9}
multiplier_options = ["— Ignorieren —", "Schwarz", "Braun", "Rot", "Orange", "Gelb", "Grün", "Blau", "Gold", "Silber"]
tolerance_options = ["— Ignorieren —", "Gold (±5%)", "Silber (±10%)", "Braun (±1%)", "Rot (±2%)"]

# ====================== HAUPTBEREICH ======================
uploaded_file = st.file_uploader("Foto der Komponente hochladen", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Hochgeladenes Bild", use_column_width=True)
    
    # Vorverarbeitung & Vorhersage
    size = (224, 224)
    image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    img_array = np.asarray(image_resized, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
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
    
    st.metric("**KONFIDENZ**", f"{confidence:.1f}%")

    # Immer angezeigte Texte
    st.subheader("Technische Funktion")
    st.info(component_info.get(predicted_label, "Keine Beschreibung verfügbar."))
    
    st.subheader("Praktische Anwendungsbeispiele")
    st.info(component_examples.get(predicted_label, "Keine Beispiele verfügbar."))

    # ====================== WIDERSTANDS-RECHNER ======================
    if predicted_label == "Widerstand":
        st.subheader("🎨 Widerstands-Farbring-Code Rechner (4–6 Bänder)")
        
        band_count = st.radio("Anzahl der Farbringe", [4, 5, 6], horizontal=True, key="band_count")
        
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        
        b1 = c1.selectbox("Band 1", color_options, index=1, key="b1")
        b2 = c2.selectbox("Band 2", color_options, index=1, key="b2")
        b3 = c3.selectbox("Band 3", color_options, index=0, key="b3")
        b4 = c4.selectbox("Band 4 (Multiplikator)", multiplier_options, index=1, key="b4")
        b5 = c5.selectbox("Band 5 (Toleranz)", tolerance_options, index=1, key="b5")
        b6 = c6.selectbox("Band 6 (optional)", ["— Ignorieren —", "Braun", "Rot", "Orange"], index=0, key="b6")

        if st.button("🔢 Widerstand berechnen", type="primary"):
            try:
                digits = []
                for b in [b1, b2, b3]:
                    if b != "— Ignorieren —":
                        digits.append(str(color_values[b]))
                
                if len(digits) < 2:
                    st.error("Mindestens Band 1 und Band 2 müssen gesetzt sein.")
                else:
                    significant = int("".join(digits))
                    mult_str = b4
                    
                    if mult_str == "Gold":
                        multiplier = 0.1
                    elif mult_str == "Silber":
                        multiplier = 0.01
                    elif mult_str != "— Ignorieren —":
                        multiplier = 10 ** color_values[mult_str]
                    else:
                        multiplier = 1
                    
                    resistance = significant * multiplier
                    
                    if resistance >= 1_000_000:
                        val = f"{resistance/1_000_000:.2f} MΩ"
                    elif resistance >= 1_000:
                        val = f"{resistance/1_000:.2f} kΩ"
                    else:
                        val = f"{int(resistance)} Ω"
                    
                    st.success(f"**Widerstandswert:** {val}")
                    if b5 != "— Ignorieren —":
                        st.info(f"**Toleranz:** {b5}")
            except:
                st.error("Fehler bei der Berechnung. Bitte Farben überprüfen.")

    st.caption(f"Analyse um {datetime.now().strftime('%H:%M:%S')}")

else:
    st.info("👆 Bitte laden Sie ein Foto hoch.")

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("Systeminformationen")
    st.write(f"**Klassen:** {len(class_names)}")
    st.write("**Modell:** Teachable Machine")
    st.divider()
    st.markdown("**Verfügbare Komponenten:**")
    for label in class_names:
        st.markdown(f"• **{label}**")
