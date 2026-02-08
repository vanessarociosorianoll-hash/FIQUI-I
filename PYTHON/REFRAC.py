#REFRAC
import streamlit as st
from Handbook.pesos_moleculares import masa
from Handbook.densidades import densidad_agua,uno_propanol,dos_propanol,mezlca_1_prop_in,mezcla_2_prop_in,mezcla_sacarosa_propin
import pandas as pd
from sympy import symbols, Eq,solve,lambdify
from math import*
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
st.title("LABORATORIO REFRACCIÓN-FSQI")
st.sidebar.header("Condiciones del laboratorio")
temp=st.sidebar.number_input("Temperatura (℃):")
pres=st.sidebar.number_input("Presion (mmhg): ")
hum=st.sidebar.number_input("Humedad (%)")
sol_org=st.sidebar.selectbox("Compuesto organico:",("1-propanol O n-propanol ", "2-propanol"))
V_ml=st.sidebar.number_input("Volumen de las soluciones", min_value=0, max_value=100000, value=3)
col_img, col_file = st.columns([1, 1])

with col_img:
    st.image("REFRACMODEL.png", caption="Estructura sugerida del Excel",width=500)

with col_file:
    st.subheader("Carga de datos")
    excel = st.file_uploader("Sube tu archivo Excel de Refractometria", type=["xlsx", "xls"])
 

def id_col_indices(df):

    keywords = ["índices", "índice", "ɳ", "refraccion", "refracción"]
    
    for col in df.columns:
        
        col_lower = col.lower()
        if any(key in col_lower for key in keywords):
            return col
    return None

if excel is None:
    st.info("Tenga en cuenta la etiqueta y estructura del archivo Excel, si desea puede agregar otra hoja con los datos de la Sacarosa , en caso haya realizado esa parte experimental")
else: 
    if st.button("CALCULAR"):
        st.header("TABLA 1")
        st.text("Los datos de esta tabla pueden ser modificados por usted")
        df1=pd.read_excel(excel, sheet_name=0)
        col_refra=id_col_indices(df1)
        col_comp = [c for c in df1.columns if c != col_refra][0]
        df3={
            "%Composicion":df1[col_comp].tolist(),
            "Indice de refracción":df1[col_refra].tolist()
        }
        df1_nuevo=st.data_editor(df3,use_container_width=True)
        lista_comps = df1_nuevo["%Composicion"]
        lista_refra = df1_nuevo["Indice de refracción"]
        composicion=np.array(lista_comps)
        refrac=np.array(lista_refra)
        volumen_solucion=float(V_ml)
        vol_agua=volumen_solucion*(1-composicion/100)
        vol_orga=volumen_solucion-vol_agua
        den_agua=densidad_agua(temp)
        M1_g_mol=masa("CH3CH2CH2OH",4)
        M2_g_mol=masa("C3H8O",4)
        if sol_org=="1-propanol":
            M_orga=M1_g_mol
        else:
            M_orga=M2_g_mol
    
        n_agua=lista_refra[0]
        n_orga=lista_refra[-1]
        if sol_org=="1-propanol":
            den_so=round(uno_propanol(temp),4)
        else:
            den_so=round(dos_propanol(temp),4)
    
        porcent_peso_teorico=(den_so*vol_orga)*100/(den_so*vol_orga+ den_agua*vol_agua)
        peso_orga=den_so*vol_orga
        peso_agua=den_agua*vol_agua
    
        fracc_molar=(peso_orga/M_orga)/((peso_orga/M_orga)+(peso_agua/masa("H2O",4)))
    
        if sol_org=="1-propanol O n-propanol ":
            dens=mezlca_1_prop_in(refrac) 
        else:
            dens=mezcla_2_prop_in(refrac)
        #%WEXP
        P1=symbols("P1")
        r_sym = symbols("r_sym")
        d_sym = symbols("d_sym")
        ecua1 = Eq(100 * (r_sym-1) / d_sym, (P1 * (n_orga - 1) / den_so) + ((100 - P1) * (n_agua - 1) / den_agua))
        solu=solve(ecua1,P1)[0]
        calc_comp_exp = lambdify((r_sym, d_sym), solu, "numpy")
        comp_exp = calc_comp_exp(refrac,dens)
        comp_exp = np.clip(comp_exp, 0, 100)
    
        error=abs(porcent_peso_teorico-comp_exp)*100/porcent_peso_teorico
        st.subheader("A)% PESO TEORICO")
        st.latex(r"%W=\frac{ρ_{organico}*V_{organico}}{ρ_{organico}*V_{organico}+ρ_{agua}*V_{agua}}")
        df2={
            "% Composicion":lista_comps,
            "Volumen agua (ml)":vol_agua,
            "Volumen comp. organico(ml)":vol_orga,
            "Masa agua (g)":peso_agua,
            "Masa organico(g)":peso_orga,
            "%W teorico":porcent_peso_teorico
        }
        st.dataframe(df2)
        with st.expander("Detalles de calculo"):
            col1,col2=st.columns(2)
            col1.metric("Densidad del agua", f"{den_agua:.4f} g/ml")
            col2.metric("Densidad del componente organico",f"{den_so:.4f} g/ml")
        st.subheader("B)FRACCION MOLAR")
        st.latex(r"X_{orga} = \frac{\frac{W_{organico}}{M_{organico}}}{\frac{W_{organico}}{M_{organico}} + \frac{W_{agua}}{M_{H_2O}}}")
        df4={
            "% Composicion":lista_comps,
            "Volumen agua (ml)":vol_agua,
            "Volumen comp. organico(ml)":vol_orga,
            "Fraccion molar del componente mas volatil":fracc_molar
        }
        st.dataframe(df4)
        with st.expander("Detalles de calculo"):
            col1,col2=st.columns(2)
            col1.metric("Peso molecular del agua", f"{masa('H2O', 4)} g/mol")
            col2.metric("Peso molecular del componente organico",f"{M_orga:.4f} g/mol")
        st.subheader("C)% PESO EXPERIMENTAL")
        st.latex(r'''
        \frac{100 (n_o - 1)}{d_o} = \frac{P_1 (n_1 - 1)}{d_1} + \frac{(100 - P_1)(n_2 - 1)}{d_2}
        ''')
        with st.expander("Significado de los términos"):
            st.markdown("""
            | Símbolo | Significado |
            | :--- | :--- |
            | $n_o$ | Índice de refracción experimental de la mezcla. |
            | $d_o$ | Densidad de la mezcla (g/mL). |
            | $P_1$ | Porcentaje en peso (% p/p) del componente 1 (Orgánico). |
            | $n_1, n_2$ | Índices de refracción de los componentes puros 1 y 2. |
            | $d_1, d_2$ | Densidades de los componentes puros 1 y 2. |
            | $100 - P_1$ | Porcentaje en peso del componente 2 (Agua). |
            """)
        df5={
            "% Composicion":lista_comps,
            "Densidad de la mezcla":dens,
            "%W teorico":porcent_peso_teorico,
            "%W experimental":comp_exp,
            "%_Error":error
    
        }
        st.dataframe(df5)
        with st.expander("Detalles de calculo"):
            fila1_col1, fila1_col2 = st.columns(2)
            fila1_col1.metric("Índice de refracción del agua", f"{n_agua}")
            fila1_col2.metric("Índice de refracción del componente más volátil", f"{n_orga}")
            
            st.divider()
    
            fila2_col1, fila2_col2 = st.columns(2)
            fila2_col1.metric("Densidad del agua", f"{den_agua:.4f} g/ml")
            fila2_col2.metric("Densidad del componente más volátil", f"{den_so:.4f} g/ml")
    
        st.subheader("D)INDICE DE REFRACCION EN FUNCION DE LA FRACCION MOLAR")
        x=fracc_molar
        y=lista_refra
        fig, ax=plt.subplots()
        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(10))
        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(10))
        ax.grid(which='major', color="#2761AB", linestyle='-', linewidth=0.8, alpha=0.6)
        ax.grid(which="minor",color="#2761AB",linestyle="-",linewidth=0.2,alpha=0.3)
        ax.plot(x,y,color="skyblue",linestyle="-", marker="o")
        n=min(fracc_molar)
        m=min(lista_refra)
        nx=max(fracc_molar)
        mx=max(lista_refra)
        ax.set_xlim(n,nx)
        ax.set_ylim(m,mx)
        ax.set_title("ɳ vs Fraccion molar")
        ax.set_xlabel("ɳ")
        ax.set_ylabel("Fraccion molar")
        st.pyplot(fig)
        st.subheader("E) Refraccion molar experimental ")
        st.latex(r"R_{exp}=\frac{n^2 -1}{n^2+2}*\frac{M}{d}")
        with st.expander("Ver leyenda de la Refractividad Molar"):
            st.markdown("""
            | Símbolo | Significado |
            | :--- | :--- |
            | $R_{exp}$ | Refractividad molar experimental. |
            | $n$ | Índice de refracción de la mezcla. |
            | $M$ | Masa molar promedio de la mezcla (g/mol). |
            | $d$ | Densidad de la mezcla (g/mL). |
            """)
        st.text("Para hallar la masa molar promedio de usa:")
        st.latex(r"M=x_{1}*M_{1}+x_{2}*M_{2}")
        refrac=np.array(lista_refra)
        M_H20=masa("H2O",4)
        M_prom=M_orga*fracc_molar+M_H20*(1-fracc_molar)
        Rexp=((refrac**2 -1)/(refrac**2 +2))*M_prom/dens
        df6={
            "% Composicion":lista_comps,
            "Densidad de la mezcla":dens,
            "Masa molar promedio":M_prom,
            "Refraccion molar experimental ": Rexp,   
            "Indice de refraccion":refrac
        }
        st.dataframe(df6)
        st.subheader("E) REFRACCIONES MOLARES TEORICAS")
        st.latex(r"R_{aditiva}=x_{1}*R_{1}+x_{2}*R_{2}")
        with st.expander("Ver leyenda de Refractividad Aditiva"):
            st.markdown("""
            | Símbolo | Significado |
            | :--- | :--- |
            | $R_{add}$ | Refractividad molar aditiva de la mezcla. |
            | $x_1, x_2$ | Fracciones molares del 2-propanol y agua, respectivamente. |
            | $R_1, R_2$ | Refracciones molares de los componentes puros. |
            """)
        R_agua=3.712 #cm3/mol
        if sol_org=="1-propanol":
            R_org=17.58
        else:
            R_org=17.59
        Radd=R_org*fracc_molar +(R_agua*(1-fracc_molar))
        error_r=abs(Radd-Rexp)*100/Radd
        df7={
            "% Composicion":lista_comps,
            "Refraccion molar experimental ": Rexp,  
            "Refraccion molar teorica" : Radd,
            "%_Error":error_r,
            "Indice de refraccion":refrac   
        }
        st.dataframe(df7)
    
        st.header("SACAROSA")
    
    st.subheader("TABLA DE DATOS")
    dfS = pd.DataFrame({
        "%Peso": [0.0] * int(med),
        "Sacarosa (g)": [0.0] * int(med),
        "Indice de refracción": [0.0] * int(med),
    })
    
    dfS_editar = st.data_editor(dfS, num_rows="fixed", hide_index=True)
    
    
    refracSAC = np.array(dfS_editar["Indice de refracción"])
    sacg = np.array(dfS_editar["Sacarosa (g)"])
    lista_compSAC = np.array(dfS_editar["%Peso"])
    
    vol_solucion = st.sidebar.number_input(label="Volumen de solución de sacarosa (ml):", value=10.0) # Cambié a float
    M_sacarosa = masa("C12H22O11", 4)
    M_H2O = 18.01528 
    den_agua=densidad_agua(temp)
    mol_sac = sacg / M_sacarosa
    masa_agua = den_agua * vol_solucion 
    mol_agua = masa_agua / M_H2O
    frac_molar_saca = mol_sac / (mol_agua + mol_sac) 
    
    
    Msaca_prom = frac_molar_saca * M_sacarosa + (1 - frac_molar_saca) * M_H2O
    
    
    densSac = mezcla_sacarosa_propin(refracSAC) 
    
    
    RexpSac = ((refracSAC**2 - 1) / (refracSAC**2 + 2)) * (Msaca_prom / densSac)
    Rsac = 70.2 
    R_agua = 3.71 
    Raditivo = frac_molar_saca * Rsac + (1 - frac_molar_saca) * R_agua
    
    Errorsac = np.abs(Raditivo - RexpSac) * 100 / Raditivo
    
    
    dfsac = pd.DataFrame({
        "%Peso": lista_compSAC,
        "Masa sacarosa (g)": sacg,
        "Masa de agua(g)":masa_agua,
        "Fracc. Molar": np.round(frac_molar_saca, 5),
        "Densidad (g/mL)": np.round(densSac, 5), 
        "R_exp": np.round(RexpSac, 3),
        "R_teor": np.round(Raditivo, 3),
        "% Error": np.round(Errorsac, 2)
    })
    
    st.subheader("RESULTADOS FINALES")
    
    st.dataframe(dfsac)








