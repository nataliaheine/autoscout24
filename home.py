from matplotlib import widgets
import streamlit as st

import model_try
import info
import analysis

pages = {
    "1. Info": info,
    "2. Datenanalyse": analysis,
    "3. Modell": model_try
}

st.sidebar.title("Seitenmenü")
select = st.sidebar.radio("", list(pages.keys()))
pages[select].start()