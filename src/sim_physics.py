import numpy as np

G = 6.67408e-11
R_e = 6.371e6
M_e = 5.972e24
g = 9.80665
M_d = 0.028964
M_v = 0.018016
R_g = 8.314
L = 0.0065


def pressure_falloff(pressure, height, temperature, moll_mass):
    return pressure * (1 - (L * height) / temperature) ** ((g * moll_mass) / (R_g * L))


def saturation_water_pressure(temperature):
    T_C = temperature - 273.15
    return 0.61078 * np.power(10, (7.5 * T_C) / (T_C + 237.3)) * 100.0


def get_air_density(humidity, temperature, height, air_pressure):
    T = temperature - L * height
    p_air = pressure_falloff(air_pressure, height, temperature, M_d)
    T_C = temperature - 273.15
    p_water0 = saturation_water_pressure(temperature) * humidity
    p_water = pressure_falloff(p_water0, height, temperature, M_v)
    ro = (p_air * M_d + p_water * M_v) / (T * R_g)
    return ro
