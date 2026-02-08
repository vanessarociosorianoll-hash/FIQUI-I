import streamlit as st
import sys
import os

st.sidebar.title("LABO FIQUI I - FQIQ")
st.sidebar.markdown("---")
ruta_python = os.path.join(os.path.dirname(__file__), "PYTHON")
if ruta_python not in sys.path:
    sys.path.insert(0, ruta_python)

pagina_0 = st.Page("PYTHON/GASES-FSQI.py", title="GASES", icon="🎈")
pagina_1 = st.Page("PYTHON/PRESION DE VAPOR.py", title="PRESIÓN DE VAPOR", icon="🌡️")
pagina_2 = st.Page("PYTHON/TERMOQUIMICA.py", title="TERMOQUÍMICA", icon="🔥")
pagina_3 = st.Page("PYTHON/CRIOSCOPIA.py", title="CRIOSCOPÍA", icon="❄️")
pagina_5 = st.Page("PYTHON/REFRAC.py", title="REFRACTOMETRÍA", icon="🔍")
pagina_6 = st.Page("PYTHON/TENSION SUPERFICIAL.py", title="TENSIÓN SUPERFICIAL", icon="💧")
pagina_7=st.Page("PYTHON/VISCOSIDAD.py", title="VISCOSIDAD", icon="🫗")


pg = st.navigation([pagina_0, pagina_1, pagina_2, pagina_3, pagina_5, pagina_6,pagina_7])

st.set_page_config(page_title="Laboratorio de Fisicoquímica - UNMSM", layout="wide")

pg.run()







