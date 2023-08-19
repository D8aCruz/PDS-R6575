import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, Image
from scipy import signal

# Parámetros de la Simulación
fs = 500                #   Hz
N  = fs                 #   Cantidad de muestras digitalizadas por el ADC (# muestras)
Ts = 1/fs               #   Periodo de muestreo
T_simulacion = N*Ts     #   1 Segundo

def plot_signal(tt, signal, title):
    plt.figure(figsize=(12, 4))
    plt.plot(tt, signal)
    plt.title(title, color='gray')
    plt.xlabel('tt (s)')
    plt.ylabel('Amplitud')
    plt.grid(True, linestyle='dotted', color='gray')
    plt.savefig(f'{title}.png', bbox_inches='tight', transparent=True)
    plt.close()
    
def mi_funcion_sen(vmax = 1, dc = 0, ff = 1, ph = 0, nn = N, fs = fs):
    # Grilla Temporal
    tt = np.arange(start=0, stop=T_simulacion, step=Ts)
    xx = vmax * np.sin(2 * np.pi * ff * tt + ph) + dc
    return tt, xx
def mi_funcion_cuadrada(vmax = 1, dc = 0, ff = 1, duty = 0.5, nn = N, fs = fs):
    tt = np.arange(start=0, stop=T_simulacion, step=Ts)
    xx = vmax*signal.square((2 * np.pi * ff * tt),duty) + dc
    return tt, xx

def mi_funcion_triangular(vmax = 1, dc = 0, ff = 1, width = 0.5, nn = N, fs = fs):
    tt = np.arange(start=0, stop=T_simulacion, step=Ts)
    xx = vmax*signal.sawtooth((2 * np.pi * ff * tt),width) + dc
    return tt, xx



# Parametros de la señal
frecuencia    = 10        # Hz
Amplitud      = 2         # V
Phase         = 0*np.pi/2.0 # Radianes
ValorMedio    = 0         # V
Duty          = 0.5       # 50% de ciclo de actividad
Width         = 0.5           

# Señales periódicas
tiempo, SignalSen = mi_funcion_sen(vmax=Amplitud, ff=frecuencia, dc=ValorMedio, ph=Phase)
tiempo, SignalCua = mi_funcion_cuadrada(vmax=Amplitud, ff=frecuencia, dc=ValorMedio, duty=Duty)
tiempo, SignalTri = mi_funcion_triangular(vmax=Amplitud, ff=frecuencia, dc=ValorMedio, width=Width)

# Configurar estilo global
plt.rcParams['savefig.transparent'] = True
plt.rcParams['axes.edgecolor'] = 'gray'
plt.rcParams['axes.labelcolor'] = 'gray'
plt.rcParams['xtick.color'] = 'gray'
plt.rcParams['ytick.color'] = 'gray'

# Generar y guardar figuras
plot_signal(tiempo, SignalSen, 'Señal Senoidal')
plot_signal(tiempo, SignalCua, 'Señal Cuadrada')
plot_signal(tiempo, SignalTri, 'Señal Triangular')

# Mostrar las imágenes en el notebook
for title in ['Señal Senoidal', 'Señal Cuadrada', 'Señal Triangular']:
    display(Image(filename=f'{title}.png'))