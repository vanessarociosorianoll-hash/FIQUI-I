#GASES-FSQI
import streamlit as st
from Handbook import pesos_moleculares as pm
from Handbook.densidades import densidad_agua
import pandas as pd
from sympy import symbols, Eq, solve
from math import *

st.title("LABORATORIO DE GASES-FSQI")
st.warning("⚠️TENGA EN CUENTA LOS DATOS SOLICITADOS EN LA BARRA LATERAL")
st.sidebar.header("Condiciones del laboratorio")
temp = st.sidebar.number_input("Temperatura (℃):")
pres = st.sidebar.number_input("Presion (mmhg): ")
hum_relativa=st.sidebar.number_input("Humedad relativa (%)")

st.header("              DENSIDAD DE GASES                ")

datos_gases_init = pd.DataFrame({
    "Descripción": [
        "Presión Barométrica (mmhg)",
        "Presión de Vapor a T. amb (mmhg)",
        "Temperatura en la pera (K)",
        "Masa de componente orgánico (g)",
        "Volumen desalojado (ml)",
        "% Humedad relativa"
    ],
    "Valor": [pres, 0, 0, 0, 0, hum_relativa] 
})

df_gases = st.data_editor(datos_gases_init, hide_index=True, use_container_width=True, key="editor_gases")

st.header("    DETERMINACION DE CAPACIDADES CALORIFICAS    ")
datos_h_init = pd.DataFrame({
    "Desnivel": ["10 cm", "15 cm", "20 cm", "25 cm"],
    "H1(cm)": [0.0, 0.0,0.0,0.0],
    "H2(cm)": [0.0,0.0,0.0,0.0,]
})
df_h_edit = st.data_editor(datos_h_init, hide_index=True, use_container_width=True, key="editor_h")

compuesto = st.text_input("Ingrese el compuesto orgánico:", placeholder="Ej: C6H14")
decimales = st.number_input("Ingrese el número de decimales:", min_value=0, max_value=10, value=2)

if st.button("Calcular con estos datos"):
    # Asignación de variables desde la tabla interactiva
    Pb = df_gases.iloc[0, 1]
    Pvap = df_gases.iloc[1, 1]
    Temp_pera = df_gases.iloc[2, 1]
    masa_g = df_gases.iloc[3, 1]
    vol_des_ml = df_gases.iloc[4, 1]
    Hum_rel = df_gases.iloc[5, 1]

    if compuesto:
        try:
            # a)
            Pb_nuevo = Pb - (100 - Hum_rel) * Pvap / 100
            
            # b)
            V_CN = symbols("V_CN")
            P_CN = 760 #mmhg
            T_CN = 273.15 #K
            ecua1 = Eq(V_CN * P_CN / T_CN, vol_des_ml * Pb_nuevo / Temp_pera)
            solu1 = solve(ecua1, V_CN)
            v_corr = solu1[0]

            # c)
            den = symbols("den")
            Pc = 40880.4 #mmgh
            Tc = 536.55 #K
            R_gases = 62.36 #mmgh*L/molK
            
            M = pm.masa(compuesto, int(decimales))
            st.success(f"El peso molecular calculado es: **{M}**")
            
            ecua2 = Eq(P_CN * M, den * R_gases * T_CN * (1 + (9 * P_CN * Tc / (128 * Pc * T_CN)) * (1 - 6 * (Tc**2 / T_CN**2))))
            solu2 = solve(ecua2, den)
            den_teorica = solu2[0]

            # d)
            den_ex = masa_g / (float(v_corr) * 10**-3)
            
            # e) %Error exp
            Error_exp = abs(den_ex - den_teorica) / den_teorica * 100

            st.write(f"a) Presión barométrica corregida: {Pb_nuevo:.4f} mmhg")
            st.write(f"b) Volumen de aire desplazado corregido (CN): {v_corr:.4f} ml")
            st.write(f"c) Densidad teorica (CN): {den_teorica:.4f} g/L")
            st.write(f"d) Densidad experimental: {den_ex:.4f} g/L")
            st.write(f"e) Error experimental: {Error_exp:.2f} %")

            # --- CAPACIDADES CALORÍFICAS ---
            densidad_del_agua = densidad_agua(temp)
            H1 = df_h_edit["H1(cm)"].tolist()
            H2 = df_h_edit["H2(cm)"].tolist()

            def p_total(altura):
                P_agua = float(densidad_del_agua) * 1000 * (9.81 / 100) * (760 / (101.3 * 10**3)) * float(altura)
                Ptotal = Pb + P_agua
                return Ptotal
            
            lista_presionesP1 = []
            for i in H1:
                P = p_total(i)
                lista_presionesP1.append(P)
                
            lista_presionesP2 = []
            for i in H2:
                P = p_total(i)
                lista_presionesP2.append(P)

            datos = {
                "P1(mmhg)/corresponde a H1":lista_presionesP1,
                "P2(mmhg)/corresponde a H2":lista_presionesP2
            }
            df3 = pd.DataFrame(datos, index=["Desnivel: 10 cm", "Desnivel: 15 cm", "Desnivel: 20 cm", "Desnivel: 25 cm"])
            st.dataframe(df3)

            # PARA HALLAR EL Y
            lista_y = []
            for i, j in zip(lista_presionesP1, lista_presionesP2):
                y = (log(i) - log(Pb)) / (log(i) - log(j))
                lista_y.append(y)
            
            df4 = pd.DataFrame(lista_y, index=["Y1", "Y2", "Y3", "Y4"]).T
            st.dataframe(df4, hide_index=True)
            
            # yprom
            Y_promedio = sum(lista_y) / len(lista_y)
            R_const = 8.314 # J/mol*K
            CV = symbols("CV")
            ecua3 = Eq(Y_promedio, (CV + R_const) / CV)
            solu3 = solve(ecua3, CV)
            
            CV_val = solu3[0]
            CP_val = CV_val + R_const
            
            # TEORICOS
            Y_teorico = 1.4
            CV_T = symbols("CV_T")
            ecua4 = Eq(Y_teorico, (CV_T + R_const) / CV_T)
            solu4 = solve(ecua4, CV_T)
            CV_teorico = solu4[0]
            CP_teorico = CV_teorico + R_const

            # ERRORES
            E_Y = abs(Y_teorico - Y_promedio) * 100 / Y_teorico
            E_CV = abs(CV_teorico - CV_val) * 100 / CV_teorico
            E_CP = abs(CP_teorico - CP_val) * 100 / CP_teorico
            
            st.header("RESULTADOS FINALES")
            df5 = pd.DataFrame({
                "Teórico": [Y_teorico, float(CV_teorico), float(CP_teorico)],
                "Experimental": [float(Y_promedio), float(CV_val), float(CP_val)],
                "Error (%)": [float(E_Y), float(E_CV), float(E_CP)]
            }, index=["Y", "CV", "CP"])
            
            st.dataframe(df5)
        except Exception as e:
            st.error(f"Error en los cálculos o fórmula química: {e}")


    else:
        st.info("Por favor, ingrese la fórmula química para comenzar.")
    
    
    
    
    
    
    





















