# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 18:49:54 2023

@author: david
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parámetros de la Simulación
fs = 250    #   Hz
N  = fs     #   Cantidad de muestras digitalizada por el ADC (# muestras)
Ts = 1/fs
T_simulacion = N*Ts     # 1 Segundo

# Parametros de la señal
frecuencia  = 10    # Hz
Amplitud    = 2     # V

# Grilla Temporal
tiempo = np.arange(start = 0, stop = T_simulacion,step = Ts)

# Señales periódicas
SignalSen = Amplitud*np.sin(2*np.pi*frecuencia*tiempo)
SignalCuad = Amplitud*signal.square((2*np.pi*frecuencia*tiempo), 0.5)
SignalTria = Amplitud*signal.sawtooth((2*np.pi*frecuencia*tiempo), 0.5)
# Graficamos la señal
plt.style.use('dark_background')
plt.plot(tiempo, SignalSen)
plt.plot(tiempo, SignalCuad)
plt.plot(tiempo, SignalTria)


