#1-propanol
def v_1_propanol(x):
    #R2 AJUSTADO:0.96823669
    v_1_P=0.001125486*x**2-0.130786286*x+4.398771429
    return v_1_P
#AGUA
#RESULTADO EN kg/(m.s)
def v_w(x):
    v_w_p=4.50121E-15*x**6-1.72863E-12*x**5+2.78904E-10*x**4-2.5213E-08*x**3+1.466E-06*x**2-6.05927E-05*x+0.001789896
    return v_w_p*1000

def v_2_prop(x):
    v_2_p=0.000929101*x**2-0.12081094*x+4.499516644
    return v_2_p






