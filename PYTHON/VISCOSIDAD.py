import streamlit as st
from Handbook.pesos_moleculares import masa 
import pandas as pd
from sympy import symbols, Eq,solve
from math import*
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from Handbook.densidades import densidad_agua,uno_propanol,dos_propanol,metanol,etanol
from Handbook.viscosidades import v_1_propanol,v_2_prop,v_w
st.title("LABORATORIO VISCOSIDAD Y DENSIDAD -FSQI")
st.warning("⚠️TENER EN CUENTA LOS DATOS DE LA BARRA LATERAL PARA LOS CÁLCULOS")
st.sidebar.header("Condiciones del laboratorio")
temp=st.sidebar.number_input("Temperatura (℃):")
pres=st.sidebar.number_input("Presion (mmhg): ")
sol_org=st.sidebar.selectbox("Compuesto organico:",("1-propanol/n_propanol ", "2-propanol","Metanol","Etanol"))
st.header("VISCOSIMETRO DE OSTWALD")
col1, col2 = st.columns(2)
with col1:
    numb_temperaturas = st.number_input("¿Cuántas temperaturas vas a registrar?", min_value=1, value=1)
with col2:
    numb_mediciones = st.number_input("¿Cuántas tiempos por temperatura?", min_value=1, value=1)
    columnas = ["Temperatura"]
for i in range(1, int(numb_mediciones) + 1):
    columnas.append(f"Tiempo {i} (s)")
st.header("I)AGUA")
df_base = pd.DataFrame(0.0, index=range(int(numb_temperaturas)), columns=columnas)
df_editado_agua = st.data_editor(
    df_base, 
    use_container_width=True, 
    hide_index=True,
    key="Tabla"
)
columnas_tiempos = [c for c in df_editado_agua.columns if "Tiempo" in c]
promedio_agua = df_editado_agua[columnas_tiempos].mean(axis=1)
temperaturas = df_editado_agua["Temperatura"].values 
densidades_agua = densidad_agua(temperaturas)
st.subheader("II) LIQUIDO ORGANICO")
df_1 = pd.DataFrame(0.0, index=range(int(numb_temperaturas)), columns=columnas)
df_1["Temperatura"] = df_editado_agua["Temperatura"]

df_editado_organico = st.data_editor(
    df_1, 
    use_container_width=True, 
    hide_index=True,
    key="tabla_organico" 
    )
promedio_organico = df_editado_organico[columnas_tiempos].mean(axis=1)
if st.button("Resultados"):
    st.subheader("A) VISCOSIDAD ABSOLUTA")
    #declarar vairbales
    #AGUA:
    temperaturas_trabo=temperaturas
    tiempos=promedio_agua
    #LIQUIDO PROBLEMA
    temp_orga=df_editado_organico["Temperatura"].tolist()
    temperatura_organico=np.array(temp_orga)
    tiempos_orga=promedio_organico
    if sol_org=="1-propanol/n_propanol ":
        dens_o=uno_propanol(temperatura_organico)
    elif sol_org=="2-propanol":
        dens_o=dos_propanol(temperatura_organico)
    elif sol_org=="Etanol":
        dens_o=etanol(temperatura_organico)
    else:
        dens_o=metanol(temperatura_organico)
    #VISCOSIDAD ABSOLUTA 
    n_visco=v_w(temperaturas_trabo)*(dens_o/densidades_agua)*(tiempos_orga/tiempos)
    df3={
        "Temperatura(℃)":temperaturas,
        "Tiempo agua(s)":promedio_agua,
        "Tiempo organico (s)":tiempos_orga,
        "Viscosidad agua(cP)":v_w(temperaturas),
        "Densidad organico (g/ml)":dens_o,
        "Densidad agua(g/ml)":densidad_agua(temperaturas),
        "Viscosidad organico(cP)":n_visco
    }
    df3_f=pd.DataFrame(df3)
    st.dataframe(df3_f.style.background_gradient(cmap='RdYlBu', subset=["Viscosidad organico(cP)"]))
    st.subheader("GRÁFICO AGUA")
    x=1/(temperaturas_trabo+273.15)
    y=np.log(v_w(temperaturas_trabo))
    m, b = np.polyfit(x, y, 1)
    p = np.poly1d([m, b])
    y_fit = p(x)
    y_avg = np.mean(y)
    ss_res = np.sum((y - y_fit)**2)
    ss_tot = np.sum((y - y_avg)**2)
    r_squared = 1 - (ss_res / ss_tot)
    texto_ecuacion = f'y = {m:.4f}x + {b:.4f}\n$R^2$ = {r_squared:.4f}'
    fig, ax=plt.subplots()
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(10))
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(10))
    ax.grid(which='major', color="#2761AB", linestyle='-', linewidth=0.8, alpha=0.6)
    ax.grid(which="minor",color="#2761AB",linestyle="-",linewidth=0.2,alpha=0.3)
    ax.plot(x,y,color="skyblue",linestyle="-", marker="o")
    nx=max(x)
    mx=max(y)
    ax.set_xlim(min(x),nx)
    ax.set_ylim(min(y),mx)
    ax.set_title("Ln n vs 1/T")
    ax.set_xlabel("1/T(K^-1)")
    ax.set_ylabel("Ln n")
    ax.text(0.05, 0.95, texto_ecuacion, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
    ax.legend("best")
    st.pyplot(fig)
    st.subheader("GRÁFICO LIQUIDO ORGANICO")
    x=1/(temperatura_organico+273.15)
    y=np.log(n_visco)
    m, b =np.polyfit(x, y, 1)
    p =np.poly1d([m, b])
    y_fit = p(x)
    y_avg =np.mean(y)
    ss_res =np.sum((y - y_fit)**2)
    ss_tot =np.sum((y - y_avg)**2)
    r_squared = 1-(ss_res / ss_tot)
    texto_ecuacion = f'y = {m:.4f}x + {b:.4f}\n$R^2$ = {r_squared:.4f}'
    fig, ax=plt.subplots()
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(10))
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(10))
    ax.grid(which='major', color="#2761AB", linestyle='-', linewidth=0.8, alpha=0.6)
    ax.grid(which="minor",color="#2761AB",linestyle="-",linewidth=0.2,alpha=0.3)
    ax.plot(x,y,color="skyblue",linestyle="-", marker="o")
    nx=max(x)
    mx=max(y)
    ax.set_xlim(min(x),nx)
    ax.set_ylim(min(y),mx)
    ax.set_title("Ln n vs 1/T")
    ax.set_xlabel("1/T(K^-1)")
    ax.set_ylabel("Ln n")
    ax.text(0.05, 0.95, texto_ecuacion, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
    ax.legend("best")
    st.pyplot(fig)

st.header("DENSIDADES")

st.subheader("DATOS DEL PICNOMETRO")
st.subheader("AGUA")
df1=pd.DataFrame({
    "TEMPERATURA(℃)":[21,26],
    "MASA(g)":[0.0]*2,
    "Volumen experimental(ml)":[0.0]*2,

})
df1_editar=st.data_editor(df1,num_rows="fixed",hide_index=True)
lista_temp=df1_editar["TEMPERATURA(℃)"].tolist()
lista_masa=np.array(df1_editar["MASA(g)"].tolist())
lista_vol=df1_editar["Volumen experimental(ml)"].tolist()
st.subheader("LIQUIDO ORGANICO")
df2=pd.DataFrame({
    "TEMPERATURA(℃)":[21,26],
    "MASA(g)":[0.0]*2,
    "Volumen experimental(ml)":[0.0]*2,

})
df1_editar=st.data_editor(df2,num_rows="fixed",hide_index=True,key="segudo")
if st.button("Resultados",key="densidades"):
    lista_temp_O=df1_editar["TEMPERATURA(℃)"].tolist()
    lista_masa_O=np.array(df1_editar["MASA(g)"].tolist())
    lista_vol_O=df1_editar["Volumen experimental(ml)"].tolist()
    temp_pic=np.array(lista_temp)
    #Gravedad especifica o densidad relativa
    G=lista_masa_O/lista_masa
    #Densidad relativa corregida
    densidad_vec = np.vectorize(densidad_agua)
    p_corr = G * (densidad_vec(temp_pic) / densidad_agua(4))
    #LLEVAR la temperatura a 26(teorico)
    p_26=p_corr[0]/(1-0.00107*(26-21))
    st.subheader("RESULTADOS")
    df4=pd.DataFrame({
        "TEMPERATURA(℃)":[21,26],
        "GRAVEDAD ESPECIFICA":G,
        "DENSIDAD CORREGIDA(g/ml)":p_corr,
    })
    st.dataframe(df4)
    st.text("Haciendo uso de la ecuacion que inlcuye el factor de compreisbilidad para halalr la densidad teorica a 26 grados cecius")
    st.success(f"Densidad a 26℃ teorico: {p_26:.4f} g/ml")
    st.success(f"Densidad a 26℃ experiemntal:{p_corr[1]:.4f} g/ml")
    if sol_org=="1-propanol/n_propanol ":
        dens_o=uno_propanol(26)
    elif sol_org=="2-propanol":
        dens_o=dos_propanol(26)
    st.success(f"Densidad segun el CRC:{dens_o} g/ml")
    error=abs(p_26-p_corr[0])*100/p_26

    st.error(f"%Error relativo(densidad de 26℃):{error:.2f} %")
