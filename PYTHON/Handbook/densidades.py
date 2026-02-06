#DENSIDADES
#Agua
from math import*
from sympy import*

def densidad_agua(x):
        Den_agua= (1e-12 * x**5) - (4e-10 * x**4) + (6e-08 * x**3) - (8e-06 * x**2) + (6e-05 * x) + 0.9998
        return Den_agua
def densidad_hielo(x):
        Den_hielo=(-1e-09 * x**3) - (7e-07 * x**2) - (0.0002 * x) + 0.9168
        return Den_hielo

def uno_propanol(x):
#se esocgio el ajuste lineal luego de realziar una prueba fischer
#R2=0.9976
        Den_uno_propanol=-0.0008104 * x + 0.8202371
        return Den_uno_propanol
def dos_propanol(x):
        Den_dos_propanol=-0.0009*x +0.8029
        #R2=0.9997
        return Den_dos_propanol
#Densidad de soluciones
#1-propanol de acuerdo a los %peso
#R² = 0.9998

def mezcla_uno_propanol(x):
        Den_uno_propanol_mezlca=(-1.0997e-09*x**4) +(2.79951e-07*x**3)+(-2.63811e-05*x**2)-(0.000984274*x)+0.99578778
        return Den_uno_propanol_mezlca

#2-propanol de acuerod a los %peso
#R² = 0.9989
def mezcla_dos_propanol(x):
        mezcla_Den_dos_propanol=-7.49758e-06*x**2+-0.001399255*x+0.996985365
        return mezcla_Den_dos_propanol
#Sacarosa de acuerdo a los %peso
#R2 ajustado=0.999999874
def mezcla_sacarosa(x):
        Sacarosa=-2.22589e-10*x**4+6.29418e-08*x**3+1.27619e-05*x**2+0.00385902*x+0.998220053
        return Sacarosa
def mezlca_1_prop_in(x):
        #R² = 0.9979
        D_n_1_prop=-883.8057473*x**3+3539.419014*x**2-4726.282154*x+2105.352463
        return D_n_1_prop
def mezcla_2_prop_in(x):
#R² = 0.9965
        D_n_2_prop=-5773.628822*x**3+23328.4464*x**2-31420.35265+14107.64846
        return D_n_2_prop
def mezcla_sacarosa_propin(x):
        #Rajustado=0.999999518
        Dn_sacc=-0.45028838*x**2+3.895268996*x-3.394037736
        return Dn_sacc
def metanol(x):
        Dn_metanol=-1.62202E-06*x**2-0.000766071+0.807447917
        return Dn_metanol
def etanol(x):
        #r2 ajustado=0.999999868
        Dn_etanol=-2.76735E-07*x**2-0.000834286*x+0.806246183
        return Dn_etanol









