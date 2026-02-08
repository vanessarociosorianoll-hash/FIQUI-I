import streamlit as st
from Handbook.pesos_moleculares import masa 
import pandas as pd
from sympy import symbols, Eq,solve
from math import*
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from Handbook.densidades import densidad_agua,uno_propanol,dos_propanol,metanol,etanol
from matplotlib import cm
from Handbook.tension_superficial import tension_agua
from Handbook.tc_K import tc
tab1,tab2=st.tabs(["CALCULOS","FUNDAMENTO TEORICO"])
with tab1:
    st.title("LABORATORIO TENSION SUPERFICIAL -FSQI")
    st.sidebar.header("Condiciones del laboratorio")
    temp=st.sidebar.number_input("Temperatura (℃):")
    pres=st.sidebar.number_input("Presion (mmhg): ")
    radiio_capilar=st.sidebar.number_input("Radio del capilar usado (mm): ")
    sol_org=st.sidebar.selectbox("Compuesto organico:",("1-propanol/n_propanol ", "2-propanol","Metanol","Etanol"))
    st.subheader("TABLA DE DATOS")
    st.subheader("I) AGUA")
    col1, col2 = st.columns(2)
    with col1:
        numb_temperaturas = st.number_input("¿Cuántas temperaturas vas a registrar?", min_value=1, value=3)
    with col2:
        numb_mediciones = st.number_input("¿Cuántas alturas por temperatura?", min_value=1, value=2)
    columnas = ["Temperatura"]
    for i in range(1, int(numb_mediciones) + 1):
        columnas.append(f"Altura {i} (mm)")

    df_base = pd.DataFrame(0.0, index=range(int(numb_temperaturas)), columns=columnas)
    df_editado_agua = st.data_editor(
        df_base, 
        use_container_width=True, 
        hide_index=True,
        key="tabla_agua" 
    )
    columnas_alturas = [c for c in df_editado_agua.columns if "Altura" in c]
    promedio_agua = df_editado_agua[columnas_alturas].mean(axis=1)
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
    promedio_organico = df_editado_organico[columnas_alturas].mean(axis=1)
    if st.button("Resultados"):
        cap_o = np.array(promedio_organico)
        if sol_org=="1-propanol/n_propanol ":
            dens_o=uno_propanol(temperaturas)
        elif sol_org=="2-propanol":
            dens_o=dos_propanol(temperaturas)
        elif sol_org=="Etanol":
            dens_o=etanol(temperaturas)
        else:
            dens_o=metanol(temperaturas)
        #tension teorica
        gamma_agua=tension_agua(temperaturas)
        #tension expe
        gamman_exp=gamma_agua*(promedio_organico*dens_o)/(promedio_agua*densidades_agua)
        #ESCRUBURS LATEX COMO HALALR EL RADIO DEL VPAILAR
        g=981 #cm/s2
        #radio del capilar
        r=2*gamma_agua/((promedio_agua/10)*densidades_agua*g)*10
        df_2={
            "Temperatura(℃)":temperaturas,
            "prom-altura_agua(mm)":promedio_agua,
            "prom_altura_orgánico(mmm)":promedio_organico,
            "Densidad agua(g/ml)":densidades_agua,
            "Densidad organico(g/ml)":dens_o,
            "Tension superficial agua(mN/m)":tension_agua(temperaturas),
            "Tension superficial experimental(mN/m)":gamman_exp,
            "Radio del capilar(mm)":r
        }
        promedio_radio=r.mean()
        st.success(f"Promedio del radio del capilar: {promedio_radio:.4f} mm")
        col1,col2,col3=st.columns(3)
        if radiio_capilar <=0.00:
            st.warning("""
            **Si desea hallar el error relativo del radio del capilar:** Ingrese el valor del radio del capilar usado en el laboratorio (solicítelo al docente).
            """)
        else:
            error=abs(radiio_capilar-promedio_radio)*100/radiio_capilar
            st.error(f" Error:{error:.2f} %")
        st.subheader("TENSION SUPERFICIAL EXPERIMENTAL Y RADIO DEL CAPILAR")
        st.dataframe(df_2)        
        st.subheader("GRAFICA")
        if sol_org=="1-propanol/n_propanol ":
            masa_g_mol=masa("C3H8O",4)
        elif sol_org=="2-propanol":
            masa_g_mol=masa("C3H8O",4)
        elif sol_org=="Etanol":
            masa_g_mol=masa("C2H5OH",4)
        else:
            masa_g_mol=masa("CH3OH",4)
        #tc
        tck=tc(sol_org)
        if len(temperaturas) > 0 and np.any(gamman_exp > 0):
            tck = tc(sol_org)
            x = tck - 6 - temperaturas
            k_t = 2.12
            y=gamman_exp*(masa_g_mol/dens_o)**(2/3)
            y_t = y[0] + k_t * (x - x[0])
            x_t=tck-6-temperaturas
            #gráfica
            fig, ax=plt.subplots(figsize=(8, 6))
            ax.xaxis.set_major_locator(ticker.AutoLocator())
            ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(10))
            ax.yaxis.set_major_locator(ticker.AutoLocator())
            ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(10))
            ax.grid(which='major', color="#2761AB", linestyle='-', linewidth=0.8, alpha=0.6)
            ax.grid(which="minor",color="#2761AB",linestyle="-",linewidth=0.2,alpha=0.3)
            ax.plot(x, y, color="skyblue", linestyle="-", marker="o",label="Expermental")
            ax.plot(x_t, y_t, color="red", linestyle="-",marker="o",label="teorico")
            
            nx=max(x)
            mx=max(y)
            ax.set_xlim(min(x),nx)
            todos_los_y = np.concatenate([y, y_t])
            ax.set_ylim(np.min(todos_los_y) - 5, np.max(todos_los_y) + 5)
            ax.set_title("GRAFICA DE EÖTVÖS")
            ax.set_xlabel(r"$T_c - 6 - t$")
            ax.set_ylabel(r"$\gamma (M/\rho)^{2/3}$")
            ax.legend()
            st.pyplot(fig)
            k,intercepto=np.polyfit(x,y,1)
            st.write(f"Pendiente(cte de Eotvos) experimental: {k:.4f} $erg \cdot mol^{{-2/3}} \cdot K^{{-1}}$")
            st.write(f"Pendiente(cte de Eotvos) teorico: {k_t:.4f} $erg \cdot mol^{{-2/3}} \cdot K^{{-1}}$")
            error_relativo = abs(k - k_t) / k_t * 100
            st.info(f"Diferencia porcentual con la teoría: {error_relativo:.2f}%")
    with tab2:
        st.header("Formulas")
        st.subheader("Tension superficial experimental")
        st.text("1->Liquido Organico")
        st.text("2->Agua")
        st.text("Usando un liquido de referencia(Agua), ademas considerando el angulo de contacto (cosɵ=1)")
        st.latex(r"\frac{γ_{1}}{γ_{2}}=\frac{h_{1}*ρ_{1}}{h_{2}*ρ_{2}}")
        st.subheader("Radio del capilar")
        st.latex(r"r=\frac{2*γ_{2}}{h_{2}*g}")
        with st.expander("Significado de los términos"):
            st.markdown("""
            | Símbolo | Significado |
            | :--- | :--- |
            | $γ$ | Tension superficial(mN/m) |
            | $h$ | Altura del liquido en el capilar(mm). |
            | $ρ$ | Densidad (g/mm3). |
            | $g$ | Gravedad(9810 mm/s2). |
            """)
        
        st.subheader("Constante de Eötvos")
        st.latex(r"y(\frac{M}{ρ})^{\frac{2}{3}} vs (T_{c}-6-t)")
        with st.expander("Significado de los términos"):
            st.markdown("""
            | Símbolo | Significado |
            | :--- | :--- |
            | $γ$ | Tension superficial(mN/m) |
            | $M$ | Masa molar del liquido organico(g/mol). |
            | $ρ$ | Densidad (g/ml). |
            | $Tc$ | Temperatura del liquido organico(℃). |
            | $T$ | Temperatura de trabajo(℃). |
            | $k$ | Constante de Eotvos($erg*mol^{-2/3}*K^{-1}$). |
            """)
    else:
        st.warning("PORFAVOR INGRESE DATOS ")
    





