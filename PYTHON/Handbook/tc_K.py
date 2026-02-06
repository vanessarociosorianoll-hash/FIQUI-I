def tc(a):
    if a=="1-propanol/n_propanol":
        tc=536.8-273.15
    elif a=="Metanol":
        tc=512.5-273.15
    elif a=="2-propanol":
        tc=508.3-273.15
    else:
        tc=514-273.15
    return tc