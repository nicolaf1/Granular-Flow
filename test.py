import numpy as np
import ctypes
from numpy.ctypeslib import ndpointer

# Carica la libreria
lib = ctypes.CDLL('./lib/libgranular.so')

# Imposta l'interfaccia della funzione C
lib.step_forward.argtypes = [
    ndpointer(ctypes.c_double, flags='C_CONTIGUOUS'),
    ndpointer(ctypes.c_double, flags='C_CONTIGUOUS'),
    ndpointer(ctypes.c_double, flags='C_CONTIGUOUS'),
    ndpointer(ctypes.c_double, flags='C_CONTIGUOUS'),
    ctypes.c_int, ctypes.c_int,
    ctypes.c_double, ctypes.c_double, ctypes.c_double,
    ctypes.c_double, ctypes.c_double
]

# Esempio di chiamata
nx, ny = 100, 100
h = np.ones((ny, nx), dtype=np.float64)
u = np.zeros((ny, nx), dtype=np.float64)
v = np.zeros((ny, nx), dtype=np.float64)
z = np.zeros((ny, nx), dtype=np.float64)

# Aggiungi topografia iniziale
z[ny//2 - 5:ny//2 + 5, nx//2 - 5:nx//2 + 5] = 0.1

# Parametri
dx = dy = 1.0
dt = 0.01
g = 9.81
k = 0.1

# Chiama la funzione C
lib.step_forward(h.ravel(), u.ravel(), v.ravel(), z.ravel(),
                 nx, ny, dx, dy, dt, g, k)
