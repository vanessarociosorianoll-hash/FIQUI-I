#CRIOSCOPIA
import streamlit as st
from Handbook.pesos_moleculares import masa 
import pandas as pd
from sympy import symbols, Eq,solve
from math import*
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from scipy import stats
from Handbook.densidades import densidad_agua as den

st.title("LABORATORIO CRIOSCOPIA -FSQI")
st.sidebar.header("Condiciones del laboratorio")
temp=st.sidebar.number_input("Temperatura (℃):")
pres=st.sidebar.number_input("Presion (mmhg): ")
hum=st.sidebar.number_input("Humedad (%)")
st.sidebar.text("Volumen de solvente y peso del soluto, para calculos mas exactos se convertira el volumen a masa , con la densidad a la temepratura del laboratorio ingresada")
V_ml=st.sidebar.number_input("Volumen agua(ml)", min_value=0, max_value=100000, value=25)
W2=st.sidebar.number_input("Peso del solvente(g)",min_value=0.00000, max_value=200000.00000,value=0.2000,step=0.00001,format="%.4f")

st.divider()

col1, col2 = st.columns([2, 1]) 

with col1:
    st.subheader("Estructura del archivo:")
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.image("criosagua.png", caption="Analisis del agua",width=300)
    with sub_col2:
        st.image("criosolve.png", caption="Analisis del soluto",width=300)

with col2:
    excel = st.file_uploader("SUBA EL ARCHIVO CORRECTO :D", type=["xlsx"])
if excel is not None: 
    #AGUA
    df1=pd.read_excel(excel, sheet_name=0)
    st.subheader("Configuración de Columnas")
    col_t =st.selectbox("¿Cuál es tu columna de tiempo/intervalo", df1.columns)
    col_temp = [c for c in df1.columns if c != col_t][0]
    es_intervalo =st.checkbox("¿Son intervalos (1, 2, 3...)?")

    if es_intervalo:
        df1["Tiempo_Final (s)"] = df1[col_t] * 30
    else:
        df1["Tiempo_Final (s)"] = df1[col_t]
    lista_tiempo=df1["Tiempo_Final (s)"].tolist()
    lista_temper=df1[col_temp].tolist()
    tiempo=np.array(lista_tiempo)
    temperatura=np.array(lista_temper)
    x=tiempo
    y=temperatura
    fig, ax=plt.subplots()
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(10))
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(10))
    ax.grid(which='major', color="#2761AB", linestyle='-', linewidth=0.8, alpha=0.6)
    ax.grid(which="minor",color="#2761AB",linestyle="-",linewidth=0.2,alpha=0.3)
    ax.plot(x,y,color="skyblue",linestyle="", marker="o")
    nx=max(tiempo)
    mx=max(temperatura)
    ax.set_xlim(min(tiempo),nx)
    ax.set_ylim(min(temperatura),mx)
    ax.set_title("tiempo vs Temperatura-AGUA")
    ax.set_xlabel("Tiempo(s)")
    ax.set_ylabel("temepratura(℃)")
    #temp de congelamiento:
    temp_n1=np.round(temperatura,2)
    minimo=np.argmin(temp_n1)
    cont=temp_n1[minimo+2:]
    t_conge_c=stats.mode(cont,keepdims=True)
    T1_SL=float(t_conge_c[0])
    ax.plot(x,y,color="#144B97C3",linestyle="-",label=f"T_congelacion={T1_SL}℃")
    ax.legend(loc="best")
    st.pyplot(fig)
    st.info("Los puntos de congelacion se hallaron, en la meseta formada despues del pico mas bajo de la grafica;sinendo este ultimo un punto inestable")
    #SOLVENTE

    df2=pd.read_excel(excel, sheet_name=1)
    
    st.subheader("Configuración de Columnas")
    col_time =st.selectbox("¿Cuál es tu columna de tiempo/intervalo", df2.columns,key="Solvente")
    col_temp_c = [c for c in df2.columns if c != col_time][0]
    conf_intervalo =st.checkbox("¿Son intervalos (1, 2, 3...)?",key="Solvent")

    if conf_intervalo:
        df2["Tiempo_Final (s)"] = df2[col_time] * 30
    else:
        df2["Tiempo_Final (s)"] = df2[col_time]
    lista_tiempo_s=df2["Tiempo_Final (s)"].tolist()
    lista_temper_s=df2[col_temp_c].tolist()
    tiempo_s=np.array(lista_tiempo_s)
    temperatura_s=np.array(lista_temper_s)
    x=tiempo_s
    y=temperatura_s
    fig, ax=plt.subplots()
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(10))
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(10))
    ax.grid(which='major', color="#2761AB", linestyle='-', linewidth=0.8, alpha=0.6)
    ax.grid(which="minor",color="#2761AB",linestyle="-",linewidth=0.2,alpha=0.3)
    ax.plot(x,y,color="skyblue",linestyle="", marker="o")
    nx=max(tiempo_s)
    mx=max(temperatura_s)
    ax.set_xlim(min(tiempo_s),nx)
    ax.set_ylim(min(temperatura_s),mx)
    ax.set_title("tiempo vs Temperatura-AGUA")
    ax.set_xlabel("Tiempo(s)")
    ax.set_ylabel("temepratura(℃)")
    #temp de congelamiento:
    temp_n1_s=np.round(temperatura_s,2)
    min=np.argmin(temp_n1_s)
    paracontarr=temp_n1_s[min+2: ]
    t_conge_c_s=stats.mode(paracontarr,keepdims=True)
    T_2S=float(t_conge_c_s[0])
    ax.plot(x,y,color="#144B97C3",linestyle="-",label=f"T_congelacion={T_2S}℃")
    ax.legend(loc="best")
    st.pyplot(fig)
    st.header("HALLAR EL PESO MOLECULAR DEL SOLUTO")
    st.latex(r"\Delta_T=K_{f}m")
    st.text("Siendo m , concentracionn molal")
    st.latex(r"M=\frac{1000*K_{f}*W_{2}}{W_{1}*\Delta_T}")
    st.text("Considerando Kf=1.86 ℃.kg/mol ")
    kf=1.86
    W1=V_ml*den(temp) #g
    compuesto =st.text_input("Ingrese la formula del soluto:", placeholder="Ej: C6H12O6")
    decimales =4
    DELTAT=abs(T1_SL-T_2S)
    if compuesto:
        try:
            if DELTAT==0:
                st.warning("REVISA LOS DATOS")
            else:
                M=(1000*kf*W2)/(W1*DELTAT)

                with st.expander("Ver detalles del cálculo "):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Masa solvente (W1)", f"{W1:.4f} g")
                    col2.metric("△T crioscópico", f"{DELTAT:.4f} °C")
                    col3.metric("Masa soluto (W2)", f"{W2:4f} g")
                    

   
                st.success(f"Masa molar experimental:{M:.4f} g/mol")
                st.success(f"Masa molar teorico= {masa(compuesto,4)} g/mol")
                error1=abs(masa(compuesto,4)-M)*100/masa(compuesto,4)
                st.error(f"%Error={error1:.2f} %")
        except:
            st.error(f"Error en la fórmula química. Revise el compuesto ingresado")
else:
    st.info("PORFAVOR,SUBA UN ARCHIVO ACORDE A LA ESTRUCTURA PRESENTADA(TENGA EN CUENTA LAS UNIDADES, SIN EMBARGO, EL NOMBRE DE LOS ROTULOS ES RELATIVO, RESPETE EL ORDEN")
    
        



