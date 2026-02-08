#TERMOQUIMICA
#PRESION DE VAPOR
import streamlit as st
from Handbook.pesos_moleculares import masa 
import pandas as pd
from sympy import symbols, Eq,solve
from math import*
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from Handbook.densidades import densidad_agua
from matplotlib import cm
st.title("LABORATORIO TERMOQUIMICA -FSQI")
st.warning("⚠️TENGA EN CUENTA LOS DATOS SOLICITADOS EN LA BARRA LATERAL")
st.sidebar.header("Condiciones del laboratorio")
temp=st.sidebar.number_input("Temperatura (℃):")
pres=st.sidebar.number_input("Presion (mmhg): ")
st.header("I) CAPACIDAD CALORIFICA DEL CALORÍMETRO")
med=st.number_input("¿Cuantas mediciones realizará?")
lista_med=list(range(1,int(med)+1))
st.subheader("TABLA DE DATOS")
df1=pd.DataFrame({
     "# MEDICION":lista_med,
    "AGUA FRIA(℃)":[0.0]*int(med),
    "AGUA CALIENTE(℃)":[0.0]*int(med),
    "TEMPERATURA DE EQUILIBRIO(℃)":[0.0]*int(med),

})
df1_editar=st.data_editor(df1,num_rows="fixed",disabled=["#MEDICION"],hide_index=True)
lista_frio=df1_editar["AGUA FRIA(℃)"].tolist()
lista_caliente=df1_editar["AGUA CALIENTE(℃)"].tolist()
lista_tempequilibri=df1_editar["TEMPERATURA DE EQUILIBRIO(℃)"].tolist()
st.sidebar.header("VOLUMENES")
st.sidebar.info("Por defecto ambos volumenes se encuentran en 150 ml , sin embargo; si usó diferentes cantidades modifiquelos acá :")
vol_agua_fria=st.sidebar.number_input(label="Agua fria(ml)):",value=150)
vol_agua_cal=st.sidebar.number_input(label="Agua caliente (ml):",value=150)
lista_capacidad_cal=[]
st.text("Si desea considerar calculos mas exacto(considerar densidades a temperaturas respectivas) o simples (ρ agua=1g/ml), indiquelo porfavor: ")
opcion=st.radio(
    "Seleccione una opcion de calculo:D",
    ["Exacto","Simple"],
    index=1,
    horizontal=True
)
cap_prom = 0.0
cap_prom2 = 0.0
lista_Ccal = []
if opcion=="Exacto":
        lista_Ccal=[]
        for i,j,k in zip(lista_frio,lista_caliente,lista_tempequilibri):
            if k>i and i>0:
                m_caliente=vol_agua_cal*densidad_agua(j)
                m_frio=vol_agua_fria*densidad_agua(i)
                Ccal=-1*(m_caliente*(k-j)+m_frio*(k-i))/((k-i))
                lista_Ccal.append(Ccal)

            else:
                lista_Ccal.append(0.0)
        if 0.0 in lista_Ccal:
            st.warning("Tiene valores incoherentes, revise la tabla")
        else:
            CCALL=np.array(lista_Ccal)*4.184
        st.subheader("Resultados de capacidades calorificas")
        CCALL=np.array(lista_Ccal)*4.184
        df1=pd.DataFrame({
             "# MEDICION":lista_med,
            "CAPACIDAD CALORIFICA (cal/℃)":lista_Ccal,
            "CAPACIDAD CALORIFICA (J/℃)":CCALL
        })
        cap_prom=0.0
        if len(lista_Ccal)>0:
            st.dataframe(df1,hide_index=True)
            cap_prom=sum(lista_Ccal)/len(lista_Ccal)
            cap_prom2=np.mean(CCALL)
            st.success(f"CAPACIDAD CALORIFICA PROMEDIO: {cap_prom:.4f} cal/℃={cap_prom2:.4f} J/℃")
else:
        for i,j,k in zip(lista_frio,lista_caliente,lista_tempequilibri):
            if k>i and i>0:
                m_caliente=vol_agua_cal*1
                m_frio=vol_agua_fria*1
                ce=1 #cal/g℃
                Ccal=(m_caliente*ce*(j-k)-m_frio*ce*(k-i))/(k-i)
                lista_Ccal.append(Ccal)
            else:
                lista_Ccal.append(0.0)
        if 0.0 in lista_Ccal:
            st.warning("Tiene valores incoherentes, revise la tabla")
        else:
            CCALL=np.array(lista_Ccal)*4.184
            df1=pd.DataFrame({
                "# MEDICION":lista_med,
                "CAPACIDAD CALORIFICA (cal/℃)":lista_Ccal,
                "CAPACIDAD CALORIFICA (J/℃)":CCALL
            })
        cap_prom2 = 0.0
        if len(lista_Ccal)>0:
            st.dataframe(df1,hide_index=True)
            cap_prom=sum(lista_Ccal)/len(lista_Ccal)
            cap_prom2=np.mean(CCALL)
            st.success(f"CAPACIDAD CALORIFICA PROMEDIO: {cap_prom:.4f} cal/℃={cap_prom2:.4f} J/℃")

st.subheader("GRAFICA TEMPERATURA VS TIEMPO")
t=st.number_input("Ingrese la cantidad de minutos monitoreados(min:seg): ")
minutos=int(t)
sec=(t-minutos)*100
if sec>=60:
    st.error(f"{sec:.2f} invalidos. Coloca maxmio 59 ")
else:
    time=t*60+sec
    tiempo=[0,time]
    #papel milimetrado:
    fig, ax=plt.subplots()
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(10))
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(10))
    ax.grid(which='major', color="#2761AB", linestyle='-', linewidth=0.8, alpha=0.6)
    ax.grid(which="minor",color="#2761AB",linestyle="-",linewidth=0.2,alpha=0.3)
    for i,(val1,val2,val3) in enumerate(zip(lista_frio,lista_caliente,lista_tempequilibri)):
        if  val1>0 and val2>0 and val3>0:
            frios=[val1,val3]
            calientes=[val2,val3]
            valor = max(0.3, 1 - (i * 0.2))
            ax.plot(tiempo,frios,alpha=valor,linestyle="-",label=f"Agua fria-Medicion{i+1}")
            ax.plot(tiempo,calientes,linestyle="-",label=f"Agua caliente-Medicion{i+1}")
    ax.set_xlim(0,time)
    ax.set_ylim(0,100)
    ax.set_title("Temperatura(℃)vsTiempo")
    ax.set_xlabel("Tiempos(s)")
    ax.set_ylabel("Temperatura)")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    st.pyplot(fig,width=600)

#NaOH=0.2
#HCl=0.8
#KHP
st.divider()
st.header("TITULACIONES")
st.subheader("I)NaOH")
t1=st.number_input("¿Cuantas valorizaciones realizará?",key="titulacionNaOH")
v=int(t1)
nv=(t1-v)*100
if nv>0:
    st.warning("INGRESE UN NUMERO ENTERO")
if v>0:
    lista_t1=list(range(1,int(t1)+1))
    st.subheader("Valoracion de NaOH")
    ct=st.number_input("¿Cual es la concentracion de NaOH esperada: ")
    if "df2" not in st.session_state or len(st.session_state.df2) != int(t1):
        st.session_state.df2=pd.DataFrame({
            "Masa de KHP(g)":[0.0]*int(t1),
            "Volumen gastado de NaOH(ml)":[0.0]*int(t1),
            "CONCENTRACION CORREGIDA(N)":[0.0]*int(t1),
            "%_ERROR":[0.0]*int(t1)

        })
    df2=st.data_editor(st.session_state.df2,num_rows="fixed",disabled=["CONCENTRACION CORREGIDA(N)","%_ERROR"],hide_index=True,key="titulacion NaOH")
    if st.button("Calcular NaOH"):
        for i  in range(len (df2)):
            a=df2.loc[i,"Masa de KHP(g)"]
            b=df2.loc[i,"Volumen gastado de NaOH(ml)"]
            if a>0 and b>0:
                KHP=masa("C8H5KO4",4)
                n_mol=(a/(KHP*b))*1000
                df2.at[i,"CONCENTRACION CORREGIDA(N)"]=round(n_mol,6)
                if ct>0:
                    error1=abs(ct-n_mol)*100/ct
                    df2.at[i,"%_ERROR"]=round(error1,2)
                else:
                    df2.at[i, "%_ERROR"] = 0.0

        st.session_state.df2 = df2
        st.rerun()

    lista_con1=df2["CONCENTRACION CORREGIDA(N)"]
    prom_cNAOH=sum(lista_con1)/len(lista_con1)#UNICO VALOR NECESARIO
    st.success(f"Promedio de valorizaciones={prom_cNAOH:.4f} N") 
    if ct>0:
        erro2=abs(ct-prom_cNAOH)*100/ct
        st.warning(f"%ERROR={erro2:.2f}%")
    
    #hcl
st.divider()
st.subheader("II)HCl")
t2=st.number_input("¿Cuantas valorizaciones realizará?",key="titulacionHCl")
va=int(t2)
nva=(t2-va)*100
if nva>0:
    st.warning("INGRESE UN NUMERO ENTERO")
if va>0:
    st.subheader("Valoracion de HCl")
    ct1=st.number_input("¿Cual es la concentracion esperada de HCl?")
    if "df3" not in st.session_state or len(st.session_state.df3) != int(t2):
        st.session_state.df3=pd.DataFrame({
            "Volumen de HCl(ml)":[0.0]*int(t2),
            "Volumen de NaOH(ml)":[0.0]*int(t2),
            "CONCENTRACION CORREGIDA(N)":[0.0]*int(t2),
            "%_ERROR":[0.0]*int(t2)

        })
    df3=st.data_editor(st.session_state.df3,num_rows="fixed",disabled=["CONCENTRACION CORREGIDA(N)","%_ERROR"],hide_index=True,key="titulacion HCl")
    if st.button("Calcular HCl"):
        for i  in range(len (df2)):
            m=df3.loc[i,"Volumen de HCl(ml)"]
            n=df3.loc[i,"Volumen de NaOH(ml)"]
            if m>0 and n>0:
                    #NVacid=NVbase
                Acido=n*prom_cNAOH/(m)
                df3.at[i,"CONCENTRACION CORREGIDA(N)"]=round(Acido,4)
            if ct1>0:
                error2=abs(ct1-Acido)*100/ct1
                df3.at[i,"%_ERROR"]=round(error2,2)
            else:
                df3.at[i,"%_ERROR"]=0.0

    
        st.session_state.df3 = df3
        st.rerun()

    lista_con2=df3["CONCENTRACION CORREGIDA(N)"]
    prom_cHCl=sum(lista_con2)/len(lista_con2)#UNICO VALOR NECESARIO
    if prom_cHCl:
        CHCl=prom_cHCl
        CNaOH=prom_cNAOH
        V_NaOH=300/(1+(CNaOH/CHCl))
        V_HCl=300-V_NaOH
        st.success(f"Promedio de valorizaciones={prom_cHCl:.4f} N") 
        if ct1>0:
          erro3=abs(ct1-prom_cHCl)*100/ct1
          st.warning(f"%ERROR={erro3:.2f}%")

          st.divider()
          st.header("II)CALOR DE NEUTRALIZACION")
          colteori,colexp=st.columns(2)
          with colteori:
              st.text("Volumenes teoricos")
              st.metric(label="V.NaOH ",value=f"{V_NaOH:.2f} ml")
              st.metric(label="V.HCl ",value=f"{V_HCl:.2f} ml")
          with colexp:
              st.text("Volumenes experimentales")
              V_NaOHexp=st.number_input("V. NaOH usado (ml): ",min_value=0.0, max_value=10000.0)
              V_HClexp=st.number_input("V. HCl usado (ml): ",min_value=0.0,max_value=10000.0)
               #para halalr el calor de neutralización
          st.info("Para el cálculo del calor de neutralización se usará::")
          st.latex(r"Q_{rxn}=(C_{termo}+m_{sol}*Ce_{sol}).(T_{eq}-T_{inicial})")
          st.latex(r"\Delta H_{neutralizacion}=\frac{-Q_{rxn}}{n_{react.limitant}}")
          st.info("Si usted desea un calculo mas exacto, será necesario ingresar los valores de las masas de las soluciones pesadas en el laboratorio,caso contrario; se asumirá 300 g como masa de solucion")
          ti = st.number_input(label="Temperatura inicial de las soluciones(℃): ", min_value=0.0, max_value=100.0, value=0.0)
          te = st.number_input(label="Temperatura de equilibrio (℃): ", min_value=0.0, max_value=100.0, value=0.0)
          temp_inicial=float(ti)
          temp_eq=float(te)
          if opcion=="Simple":
              Q1=(cap_prom+(300))*(temp_eq-temp_inicial)
              Q1_kJ=(Q1* 4.184) / 1000
              if (CHCl * (V_HClexp / 1000))>0:
                   E = -Q1_kJ / (CHCl * (V_HClexp / 1000))
                   st.success(f"△Hrnx= {float(E):.4f} KJ/mol")
                   eroror=abs(-55.8-E)*100/55.8
                   st.error(f"%Error={eroror:.2f} %")
              else:
                   st.info("Ingrese datos porfavor")
          if opcion=="Exacto":
              h=st.number_input(label="Peso en gramos de la solucion de HCl")
              na=st.number_input(label="Peso en gramos de la solucion de NaOH")
              Cp_molar=-90 #J/molK, segun CRC
              CP_molaragua=75.3  #J/Kmol
              cp_molarNaOH=-95.4 #J/Kmol
          
              mtotla=h+na
              n_Nacl=(V_HClexp/1000)*CHCl
              n_NaOHexceso=(V_NaOHexp/1000)*CNaOH-n_Nacl
              magua=mtotla-(n_Nacl*masa("H2O",2)+n_NaOHexceso*masa("NaOH",2))
              n_agua=magua/masa("H2O",2)
              Cptotal_J = (n_agua * CP_molaragua) + (n_Nacl * Cp_molar) + (n_NaOHexceso * cp_molarNaOH)
              Q1_J = (cap_prom2 + Cptotal_J) * (temp_eq - temp_inicial)
              E = -(Q1_J / 1000) / n_Nacl
              st.success(f"△Hrnx= {float(E):.4f} KJ/mol")
              erorrorr=abs(-55.8-E)*100/55.8
              st.error(f"%Error={erorrorr:.2f} %")
          
              st.info("En el cálculo exacto, no se asumió una  solución ideal. Se utilizó un modelo de Capacidad Calorífica Molar Aparente basado en el CRC Handbook. El programa calculó la masa efectiva del solvente restando la masa de los solutos y aplicó las contribuciones térmicas individuales de cada especie ($NaCl, NaOH$ y $H_2O$). Esto permite capturar el efecto de la interacción ion-solvente que reduce la capacidad calorífica del sistema, entregando una entalpía de neutralización basada en la física real de la mezcla.Siendo este calculo , mucho mas sensible en comparacion al simple :D")















