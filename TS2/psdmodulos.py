# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 00:00:00 2023

@author: david
"""
#%%   Importamos librerias y modulos necesarios
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, Image
from scipy import signal

#%% Funciones para generar las siguientes funciones:
def mi_funcion_sen(vmax = 1, dc = 0, ff = 1, ph = 0, nn = 500, fs = 500):
    tt = np.arange(start=0, stop=nn/fs, step=1/fs)
    xx = vmax*np.sin(2*np.pi*ff*tt + ph) + dc
    return tt, xx

def mi_funcion_cuadrada(vmax=1, dc=0, ff=10, duty=0.5, nn=500, fs=500):
    tt = np.arange(start=0, stop=nn/fs, step=1/fs)
    xx = vmax*signal.square( (2*np.pi*ff*tt), duty) + dc
    return tt, xx

def mi_funcion_triangular(vmax=1, dc=0, ff=1, width=0.5, nn=500, fs=500):
    tt = np.arange(start=0, stop=nn/fs, step=1/fs)
    xx = vmax*signal.sawtooth( (2*np.pi*ff*tt), width) + dc
    return tt, xx

#%% Generar ruido aleatorio
def generar_ruido(signal, snr, noise = 'normal'):
    pot_señal = np.var(signal)
    pot_ruido = pot_señal / (10**(snr / 10))  # Convertir SNR a escala lineal
    #ruido = np.random.uniform(-np.sqrt(3*pot_ruido) , np.sqrt(3*pot_ruido) , len(signal))
    if noise == 'normal':
        ruido = np.random.normal(0, np.sqrt(pot_ruido), len(signal))
    elif noise == 'uniform':
        ruido = np.random.uniform(-np.sqrt(3*pot_ruido), np.sqrt(3*pot_ruido), len(signal))
    else:
        raise ValueError("El tipo de ruido debe ser 'normal' o 'uniform'.")  
    print(f"\n\tSNR = {10*np.log10((np.var(signal))/np.var(ruido))}[dB]")
    print(f"\n\tPotencia de la Señal:\t {pot_señal}[W]")
    print(f"\n\tPotencia del Ruido:\t {pot_ruido}[W]")
    return ruido

#%% Generador de señales
def SignalGenerator(AA, ff, ph, dc, N, fs, signal = 'Senoidal', duty = None, width = None, snr = None, noise = 'normal'):
    if signal == 'Senoidal':
        tt, xx = mi_funcion_sen(vmax=AA, ff=ff, ph=ph, nn=N, fs=fs)
        if snr == None:
            return tt, xx
        else:
            ruido = generar_ruido(xx, snr, noise=noise)
            return tt, xx+ruido
    elif signal == 'Cuadrada':
        tt, xx = mi_funcion_cuadrada(AA, dc, ff, duty, N, fs)
        if snr == None:
            return tt, xx
        else:
            ruido = generar_ruido(xx, snr, noise=noise)
            return tt, xx+ruido
    elif signal == 'Triangular':
        tt, xx = mi_funcion_triangular(AA, dc, ff, width, N, fs)
        if snr == None:
            return tt, xx
        else:
            ruido = generar_ruido(xx, snr, noise=noise)
            return tt, xx+ruido
    else:
        raise ValueError("El tipo de señal debe ser 'Senoidal' o 'Cuadrada' o 'Triangular'.")
    
#%% Graficar las señales
def plot_signal(tt, signal, name, color, xlabel='Tiempo [s]', ylabel='AA [V]'):
    plt.rcParams['savefig.transparent'] = True
    plt.rcParams['axes.edgecolor'] = 'gray'
    plt.rcParams['axes.labelcolor'] = 'gray'
    plt.rcParams['xtick.color'] = 'gray'
    plt.rcParams['ytick.color'] = 'gray'
    plt.figure(figsize=(12, 4))
    plt.plot(tt, signal, color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, linestyle='dotted', color='gray')
    plt.savefig(f'{name}.png', bbox_inches='tight', transparent=True)
    plt.close()

    