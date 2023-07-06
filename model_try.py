import streamlit as st
import numpy as np
from joblib import load

# Laden des Modells
model = load("auto_price.joblib")

# Eingabefunktion
def get_user_input():
    mileage = st.slider("Kilometerstand", 0, 300000, 10000)
    hp = st.slider("PS", 100, 500, 150)
    year = st.slider("Registrierungsjahr", 2000, 2023, 2015)
    brand = st.selectbox("Brand", ['Volkswagen', 'Opel', 'Ford', 'Skoda', 'Renault'])
    
    # Umwandeln der Marke in Binärvariablen
    make = [0,0,0,0]
    if brand == 'Opel':
        make[0] = 1.0
    elif brand == 'Renault':
        make[1] = 1.0
    elif brand == 'Skoda':
        make[2] = 1.0
    elif brand == 'Volkswagen':
        make[3] = 1.0
    
    # Rückgabe der Eingaben als Liste
    return [mileage, hp, year] + make

# Streamlit-App
def start():
    st.title("Berechne den empfohlenen Preis deines Autos")
    st.write("Gebe dir Parameter deines Autos ein")

    # Eingaben des Benutzers erfassen
    user_input = get_user_input()
    
    # Vorhersage des Preises
    if st.button("Preis berechnen"):
        # Umwandeln der Eingaben in ein Array
        input_array = np.array(user_input).reshape(1, -1)
        
        # Verwendung des Modells zur Preisvorhersage
        predicted_price = model.predict(input_array)
        
        # Anzeigen der Vorhersage
        st.success(f"Der empfohlene Preis für dein Auto liegt bei: {predicted_price[0]}€")

