# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 21:45:44 2023

@author: david
"""
#%%   Importamos librerias y modulos necesarios
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, Image
from scipy import signal
import psdmodulos as psd

#%%     Parámetros de la Simulación
fs = 1000                #   Frecuencia de muestreo en Hz
N  = fs                 #   Cantidad de muestras digitalizadas por el ADC (# muestras)
Ts = 1/fs               #   Periodo de muestreo
    
#%% Parametros de la señal
frecuencia  = 50            # frecuencia de la señal en Hz
Amplitud    = np.sqrt(2)    # Amplitud máxiva en Volt
Phase       = np.pi/2.0     # Fase en radianes
ValorMedio  = 0             # Componente de continua
snr         = 30            # Relación señal-ruido en dB        
 
tt, xx = psd.SignalGenerator(Amplitud, frecuencia, Phase, ValorMedio, N, fs, signal='Senoidal', noise='normal', snr=snr)
psd.plot_signal(tt, xx, 'SenoidalRuido', color='red', snr=snr)

#%% Algoritmo de la DFT
def mi_funcion_DFT(xx):
    N = len(xx)  # Número de muestras de la señal de entrada
    XX = np.zeros(N, dtype=np.complex128)  # Inicializamos un arreglo para almacenar la DFT

    for k in range(N):
        XX[k] = 0
        for n in range(N):
            XX[k] += xx[n] * np.exp(-2j * np.pi * k * n / N)
    return XX/N

#%% Calculamos la DSP a partir del Algoritmo de la DFT
XX = mi_funcion_DFT( xx )

# Calcular la magnitud del espectro en frecuencia
X_mag = np.abs(XX)

# Crear un vector de frecuencia
df  = fs/N
frequencies = np.arange(start=0, stop=(N)*df, step=df)
bfrec = frequencies <= fs/2
# Visualizar el espectro en frecuencia
psd.plot_signal(frequencies[bfrec], 10*np.log10(2*np.abs(XX[bfrec])**2),'PSD', color='#CD5C5C', xlabel='Frecuencia [f]', ylabel='Amplitud [dB]')