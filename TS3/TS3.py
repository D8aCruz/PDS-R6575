# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 21:45:44 2023

@author: david
"""
#%%   Importamos librerias y modulos necesarios
import numpy as np
import matplotlib.pyplot as plt
import pdsmodulos as pds
from scipy import signal as sig
import spectrum as sp
#%%     Parámetros de la Simulación
os  = 4        # Oversampling
fsa = 2000     # Frecuencia de muestreo analogico 
fsd = fsa/os    # Frecuencia de muestreo digital
Na  = fsa       # Cantidad de muestras digitalizadas por el ADC (# muestras)
Nd  = Na/os
B   = 10         # bits
Vcc = 2.5       # Tension de referencia
SNR = 40        # Relacion señal a ruido en dB
    
#%% Parametros de la señal
AA  = np.sqrt(2)# Amplitud de la señal analogica
ff  = 10.0      # Frecuencia de tono
dc  = 0         # Componente de continua
ph  = 0.0       # Fase

#%% Generamos la señal senoidal con ruido de distribucion normal tal que SNR = 60dB        
ta, xx = pds.mi_funcion_sen(vmax=AA, ff=ff, dc=dc, ph=ph, nn=Na, fs=fsa)
na = pds.generar_ruido(signal=xx, snr=SNR, noise='normal')
xa = xx + na

#%% Simulación del filtro analógico de desambiguacion

# Tipo de aproximación.
        
aprox_name = 'butter'
# aprox_name = 'cheby1'
# aprox_name = 'cheby2'
# aprox_name = 'ellip'

# Requerimientos de plantilla
filter_type = 'lowpass'

ftran = 0.1
fstop = np.min([1/os + ftran/2, 1/os* 5/4])  #

fpass = np.max([fstop - ftran/2, fstop * 3/4]) # 
ripple = 0.5 # dB
attenuation = 40 # dB

# como usaremos filtrado bidireccional, alteramos las restricciones para
# ambas pasadas
ripple = ripple / 2 # dB
attenuation = attenuation / 2 # dB


if aprox_name == 'butter':

    # order, wcutof = sig.buttord( 2*np.pi*fpass*fs/2, 2*np.pi*fstop*fs/2, ripple, attenuation, analog=True)
    orderz, wcutofz = sig.buttord( fpass, fstop, ripple, attenuation, analog=False)

elif aprox_name == 'cheby1':

    # order, wcutof = sig.cheb1ord( 2*np.pi*fpass*fs/2, 2*np.pi*fstop*fs/2, ripple, attenuation, analog=True)
    orderz, wcutofz = sig.cheb1ord( fpass, fstop, ripple, attenuation, analog=False)
    
elif aprox_name == 'cheby2':

    # order, wcutof = sig.cheb2ord( 2*np.pi*fpass*fs/2, 2*np.pi*fstop*fs/2, ripple, attenuation, analog=True)
    orderz, wcutofz = sig.cheb2ord( fpass, fstop, ripple, attenuation, analog=False)
    
elif aprox_name == 'ellip':
   
    # order, wcutof = sig.ellipord( 2*np.pi*fpass*fs/2, 2*np.pi*fstop*fs/2, ripple, attenuation, analog=True)
    orderz, wcutofz = sig.ellipord( fpass, fstop, ripple, attenuation, analog=False)


# Diseño del filtro digital

filter_sos = sig.iirfilter(orderz, wcutofz, rp=ripple, rs=attenuation, 
                            btype=filter_type, 
                            analog=False, 
                            ftype=aprox_name,
                            output='sos')

xaf = sig.sosfiltfilt(filter_sos, xa)

#%% Agregamos el ruido de cuantizacion de distribucion uniforme
q   = 2*Vcc/(2**B - 1)
nq  = np.random.uniform(low=-q/2, high=q/2, size=Na)
xaqf = xaf 
xaq = xa

xaq[xaq > +Vcc] = +Vcc
xaq[xaq < -Vcc] = -Vcc

xaqf[xaqf > +Vcc] = +Vcc
xaqf[xaqf < -Vcc] = -Vcc

#%% Cuantizacion ADC
xdq  = (np.floor(xaq/q)*q + q/2)[::os]
xdqf = (np.floor(xaqf/q)*q + q/2)[::os]
td   = ta[::os]     
ndq  = xdq - xaq[::os]
ndqf = xdqf - xaqf[::os]

#%% Grficos en el tiempo
plt.close('all')
plt.figure(1)
plt.style.use('dark_background')
plt.plot(td, xdqf, label='$X_{dq}$ = Q{$X_{aq}$}', color='red')
plt.plot(ta, xaqf, linestyle=':', color='green', marker='.', markersize=3, markerfacecolor='none', markeredgecolor='green', fillstyle='none', label='$X_{aq}$ = $X_af$ + $n_q$')
plt.plot(ta, xaf, color='purple', ls='dotted', label='$X_{af}$ = Filtro[$X$ + $n_a$]')
plt.plot(ta, xx, color='white', ls='dotted', label='X Analog Signal')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud [V]')
plt.legend()
plt.title(f'ADC de {B} bits')
plt.show()
# Configurar etiquetas y títulos


#%% Analisis frecuencial
Xfft_xx  = 1/Na*np.fft.fft(xx, axis=0)

Xfft_xa  = 1/Na*np.fft.fft(xa, axis=0)
Xfft_xaf = 1/Na*np.fft.fft(xaf, axis=0)

Xfft_xaq = 1/Na*np.fft.fft(xaq, axis=0)
Xfft_xaqf = 1/Na*np.fft.fft(xaqf, axis=0)

Xfft_xdq = 1/Nd*np.fft.fft(xdq, axis=0)
Xfft_xdqf = 1/Nd*np.fft.fft(xdqf, axis=0)

# Crear un vector de frecuencia
dfa  = fsa/Na
dfd  = fsd/Nd

frequencies_a = np.arange(start=0, stop=(Na)*dfa, step=dfa)
frequencies_d = np.arange(start=0, stop=(Nd)*dfd, step=dfd)
bfrec_a = frequencies_a <= fsa/2
bfrec_d = frequencies_d <= fsd/2

#%% Grafico con filtro antialiasing
plt.figure(2)
#plt.style.use('dark_background')
plt.plot(frequencies_a[bfrec_a], 10*np.log10(2*np.abs(Xfft_xa[bfrec_a])**2), color='gray', ls='dotted', label='$X_a = X + n_a$ Señal analogica')
plt.plot(frequencies_a[bfrec_a], 10*np.log10(2*np.abs(Xfft_xaf[bfrec_a])**2), color='purple', ls='dotted', label='$X_{af}$ = Filtro[$X_a$]')
plt.plot(frequencies_a[bfrec_a], 10*np.log10(2*np.abs(Xfft_xaqf[bfrec_a])**2), linestyle=':', color='green', marker='.', markersize=3, markerfacecolor='none', markeredgecolor='green', fillstyle='none', label='$X_{aqf}$ = $X_{af}$ + $n_q$')
plt.plot(frequencies_d[bfrec_d], 10*np.log10(2*np.abs(Xfft_xdqf[bfrec_d])**2),  linestyle=':', label='$X_{dqf}$ = Q{$X_{aqf}$}', color='red')
plt.xlabel('Frecuencia [f]')
plt.ylabel('Amplitud [dB]')
plt.legend()
plt.title(f'ADC de {B} bits')
plt.show()

#%% Grafico sin filtro antialiasing
plt.figure(3)
#plt.style.use('dark_background')
plt.plot(frequencies_a[bfrec_a], 10*np.log10(2*np.abs(Xfft_xa[bfrec_a])**2), color='gray', ls='dotted', label='$X_a$ Señal analogica')
plt.plot(frequencies_a[bfrec_a], 10*np.log10(2*np.abs(Xfft_xaq[bfrec_a])**2), linestyle=':', color='green', marker='.', markersize=3, markerfacecolor='none', markeredgecolor='green', fillstyle='none', label='$X_{aq}$ = $X_{a}$ + $n_q$')
plt.plot(frequencies_d[bfrec_d], 10*np.log10(2*np.abs(Xfft_xdq[bfrec_d])**2),  linestyle=':', label='$X_{dq}$ = Q{$X_{aq}$}', color='red')
plt.xlabel('Frecuencia [f]')
plt.ylabel('Amplitud [dB]')
plt.legend()
plt.title(f'ADC de {B} bits')
plt.show()

#%% Analisis frecuencial
Xfft_na  = 1/Na*np.fft.fft(na, axis=0)

Xfft_nq  = 1/Na*np.fft.fft(nq, axis=0)

Xfft_ndq = 1/Nd*np.fft.fft(ndq, axis=0)

Xfft_ndqf = 1/Nd*np.fft.fft(ndqf, axis=0)
# Crear un vector de frecuencia
dfa  = fsa/Na
dfd  = fsd/Nd

frequencies_a = np.arange(start=0, stop=(Na)*dfa, step=dfa)
frequencies_d = np.arange(start=0, stop=(Nd)*dfd, step=dfd)
bfrec_a = frequencies_a <= fsa/2
bfrec_d = frequencies_d <= fsd/2
#%% Grafico con filtro antialiasing
plt.figure(4)
#plt.style.use('dark_background')
plt.plot(frequencies_a[bfrec_a], 10*np.log10(2*np.abs(Xfft_na[bfrec_a])**2), color='gray', ls='dotted', label='$n_a$')
plt.plot(frequencies_a[bfrec_a], 10*np.log10(2*np.abs(Xfft_nq[bfrec_a])**2), color='purple', ls='dotted', label='$n_{q}$')
plt.plot(frequencies_d[bfrec_d], 10*np.log10(2*np.abs(Xfft_ndq[bfrec_d])**2),  linestyle=':', label='$n_{dq}$', color='red')
plt.plot(frequencies_d[bfrec_d], 10*np.log10(2*np.abs(Xfft_ndqf[bfrec_d])**2),  linestyle=':', label='$n_{dqf}$', color='orange')
plt.xlabel('Frecuencia [f]')
plt.ylabel('Amplitud [dB]')
plt.legend()
plt.title(f'ADC de {B} bits')
plt.show()
