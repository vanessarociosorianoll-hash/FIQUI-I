def tension_agua(T):
    gamma_teorica = 75.64014 + (-0.1371863 * T) + (-0.0003982 * T**2) + (1.525e-06 * T**3) + (-5.536e-09 * T**4)
    return gamma_teorica
