import streamlit as st
from PIL import Image, ImageOps
import tensorflow as tf
import numpy as np
from datetime import datetime

# Seitenkonfiguration
st.set_page_config(
    page_title="Elektro-Komponenten Detektor",
    page_icon="🔌",
    layout="centered"
)

st.title("🔌 Elektrotechnische Komponenten-Erkennung")
st.markdown("**Teachable Machine Modell** — Hochladen eines Fotos für KI-gestützte Analyse")

# ====================== MODELL LADEN ======================
@st.cache_resource(show_spinner="Modell wird geladen...")
def load_model():
    model = tf.keras.models.load_model("model/keras_model.h5", compile=False)
    return model

model = load_model()

# Labels laden
@st.cache_data
def load_labels():
    with open("model/labels.txt", "r", encoding="utf-8") as f:
        return [line.strip().split(" ", 1)[-1] for line in f.readlines()]

class_names = load_labels()

# ====================== UPLOAD & ANALYSE ======================
uploaded_file = st.file_uploader(
    "Foto der Komponente hochladen", 
    type=["jpg", "jpeg", "png", "webp"],
    help="Hochauflösendes, gut ausgeleuchtetes Bild empfohlen"
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Hochgeladenes Bild", use_column_width=True)
    
    # Vorverarbeitung (exakt 224x224)
    size = (224, 224)
    image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    
    img_array = np.asarray(image_resized, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    
    # Inference
    with st.spinner("Analysiere Bild mit dem neuronalen Netz..."):
        predictions = model.predict(img_array, verbose=0)
    
    predicted_idx = int(np.argmax(predictions[0]))
    confidence = float(predictions[0][predicted_idx]) * 100
    predicted_label = class_names[predicted_idx]

    # Ergebnisanzeige
    col1, col2 = st.columns(2)
    with col1:
        if confidence >= 75:
            st.success(f"**Erkannte Komponente:** {predicted_label}")
        elif confidence >= 50:
            st.warning(f"**Wahrscheinliche Komponente:** {predicted_label}")
        else:
            st.error(f"**Unsichere Erkennung:** {predicted_label}")
    
    with col2:
        st.metric(label="Konfidenz", value=f"{confidence:.1f}%")
    
    # Wahrscheinlichkeitsverteilung
    st.subheader("Wahrscheinlichkeitsverteilung aller Klassen")
    prob_dict = {name: float(p * 100) for name, p in zip(class_names, predictions[0])}
    st.bar_chart(prob_dict, use_container_width=True)

    st.caption(f"Analyse durchgeführt um {datetime.now().strftime('%H:%M:%S')}")

else:
    st.info("👆 Bitte laden Sie ein Foto hoch, um die Erkennung zu starten.")

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("Modell-Informationen")
    st.write(f"**Trainierte Klassen:** {len(class_names)}")
    st.write("**Eingabegröße:** 224 × 224 Pixel")
    st.write("**Modelltyp:** Keras (.h5) – Teachable Machine")
    
    st.divider()
    st.caption("**Tipp:** Für die Erkennung mehrerer Komponenten gleichzeitig (mit Bounding Boxes) kann später ein YOLO-Modell integriert werden.")
