#PRESION DE VAPOR
import streamlit as st
from Handbook import pesos_moleculares as pm
import pandas as pd
from sympy import symbols, Eq,solve
from math import*
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
st.title("LABORATORIO PRESION DE VAPOR -FSQI")
st.header("⚠️TENER EN CUENTA LOS DATOS DE LA BARRA LATERAL PARA LOS CÁLCULOS")
st.sidebar.header("Condiciones del laboratorio")
temp=st.sidebar.number_input("Temperatura (℃):")
pres=st.sidebar.number_input("Presion (mmhg): ")
col1, col2 = st.columns([1, 1])

with col1:
    st.info("Asegúrate de que el archivo Excel tenga la siguiente estructura:D")
    st.image("datos vap.png", caption="Modelo de Excel requerido",width=200)
with col2:
    st.write("**Sube tu archivo :D**")
    excel=st.file_uploader("EXCEL:",type=["xlsx", "xls", "csv"])
if excel is not None:
    if pres==0:
        st.warning("CÁLCULOS NO DISPONIBLES. INGRESE LAS CONDICIONES DEL LABORATORIO")
        st.stop()
    else:
        df1=pd.read_excel(excel, sheet_name=0)
        cols = df1.columns.tolist()
        col_t = [c for c in cols if 'T' in c.upper()][0] 
        col_p = [c for c in cols if 'P' in c.upper()][0] 
        lista_temperatura = df1[col_t].tolist()
        lista_presiones = df1[col_p].tolist()
        temperatura_array=np.array(lista_temperatura)
        presionhg_array=np.array(lista_presiones)
        # COLUMNA: T(K)
        temperatura_K=temperatura_array+273.15
        #COLUMNA(Pgas mmhg)
        Pgas_mmhg=pres-presionhg_array
    
        #COLUMNA(ln(pgas))
        Ln_pgas=np.log(Pgas_mmhg)
        #COLUMNA (1/T)
        inversa_T=1/temperatura_K
        datos2={
            "T(℃)":lista_temperatura,
            "Presión manométrica Hg(mmhg)":lista_presiones,
            "T(K)":temperatura_K,
            "Presión del gas (mmHg)":Pgas_mmhg,
            "Ln(P_gas)":Ln_pgas,
            "1/T":inversa_T
        }
        df2=pd.DataFrame(datos2)
        st.subheader("TABLA DE DATOS PRINCIPAL")
        st.dataframe(df2)
        st.header("A)GRÁFICA Ln(P) vs 1/T")
    
        x=inversa_T
        y=Ln_pgas
        if x.size > 0 and y.size > 0:
            fig, ax=plt.subplots()
            ax.xaxis.set_major_locator(ticker.AutoLocator())
            ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(10))
            ax.yaxis.set_major_locator(ticker.AutoLocator())
            ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(10))
            ax.grid(which='major', color="#2761AB", linestyle='-', linewidth=0.8, alpha=0.6)
            ax.grid(which="minor",color="#2761AB",linestyle="-",linewidth=0.2,alpha=0.3)
            ax.plot(x,y,color="skyblue",linestyle="", marker="o")
            n, nx = np.nanmin(x), np.nanmax(x)
            m, mx = np.nanmin(y), np.nanmax(y)
            
            if np.isfinite([n, nx, m, mx]).all():
                margin_x = (nx - n) * 0.05 if nx != n else 0.1
                margin_y = (mx - m) * 0.05 if mx != m else 0.1
                ax.set_xlim(n - margin_x, nx + margin_x)
                ax.set_ylim(m - margin_y, mx + margin_y)
                
            ax.set_title("1/T vs Ln(Presion del gas)")
            ax.set_xlabel("1/T")
            ax.set_ylabel("Ln(Pgas)")
            #ECUACION : AX+B=Y
            a,b=np.polyfit(inversa_T,Ln_pgas,1)
            y_pred = a * inversa_T + b

            residuals = Ln_pgas - y_pred
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((Ln_pgas - np.mean(Ln_pgas))**2)
            r_squared = 1 - (ss_res / ss_tot)
            st.success(f"Ecuación de la recta: y={a:.4f}x+{b:.4f}. Coeficiente de determinación  $R^2$ = {r_squared:.4f}")
            
            #PARA GRAFICAR LA REGRESIÓN LINEAL:
            ynuevo=a*inversa_T+b
            ax.plot(inversa_T,ynuevo,color="#000000C3",linestyle="-",label=f"Regresion lineal: y={a:.4f}x+{b:.4f}")
            ax.legend(loc="best")
            st.pyplot(fig,width=600)
            st.header("B)CALOR MOLAR DE VAPORIZACIÓN USANDO EC. DE CLAUSIUS-CLAPEYRON")
            st.text("Usando la formula:")
            st.latex(r"\frac{dp}{dT} = \frac{\Delta HV}{(Vg - Vl)T} = \frac{\Delta HV}{T \Delta V}")
            st.text("Desarrollando: ")
            st.latex(r"Ln(P)=\frac{-\Delta HV}{RT}+C")
            R=8.314 #J/molK
            deltaHV=-R*a
            st.subheader("Método gráfico: ")
            st.success(f"△HV= {deltaHV:.4f}J/mol*K")
            st.subheader("Metodo analitico:")
            st.latex(r"2.3*log(\frac{P2}{P1})=\frac{\Delta HV}{R}*\frac{T2-T1}{T2*T1}")
            puntos=st.slider(
                label="Seleccione la cantidad de puntos a considerar",
                min_value=2,
                max_value=len(Pgas_mmhg)
            )
            lista_valordedeltaHV=[]
            
            for m in range (puntos-1):
                P1,P2=list(Pgas_mmhg)[m],list(Pgas_mmhg)[m+1]
                T1,T2=list(temperatura_K)[m],list(temperatura_K)[m+1]
                delta_HV=symbols("HV")
                ecua1=Eq(2.3*log10(P1/(P2)),-delta_HV*(T2-T1)/((R*(T2)*(T1))))
                solu=solve(ecua1,delta_HV)
                HV=solu[0]
                lista_valordedeltaHV.append(HV)
            HV_prom=sum(lista_valordedeltaHV)/len(lista_valordedeltaHV)
        
            st.success(f"HV={HV_prom:.4f}J/mol*K")
            st.subheader("PORCENTAJE DE ERROR RELATIVO")
        
            error=abs(HV_prom-deltaHV)*100/HV_prom
            st.warning(f"{error:.2f}%")

            st.header("C)EXPRESIÓN MATEMÁTICA: ")
            st.text("Usando los datos obtenidos por el gráfico, se procede a integrar:")
            st.latex(r"\int \frac{dP}{P}=\frac{\Delta HV}{R}*\int\frac{dT}{T^2}")
            st.latex(r"ln(P)=\frac{-\Delta HV}{R*T}+C")
            st.text("Expresión: ")
            A=e**b
    
            st.latex(fr"P = e^{{ \frac{{ -{deltaHV:.4f} }}{{ {R} \cdot T }} }} \cdot {A:.4f}")
    
    
    































