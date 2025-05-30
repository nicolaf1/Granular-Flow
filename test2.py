import numpy as np
import ctypes
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy.ctypeslib import ndpointer

# Carica la libreria C
lib = ctypes.CDLL('./lib/libgranular.so')

# Definizione della funzione C
lib.step_forward.argtypes = [
    ndpointer(ctypes.c_double, flags='C_CONTIGUOUS'),
    ndpointer(ctypes.c_double, flags='C_CONTIGUOUS'),
    ndpointer(ctypes.c_double, flags='C_CONTIGUOUS'),
    ndpointer(ctypes.c_double, flags='C_CONTIGUOUS'),
    ctypes.c_int, ctypes.c_int,
    ctypes.c_double, ctypes.c_double, ctypes.c_double,
    ctypes.c_double, ctypes.c_double
]

# Parametri dominio
nx, ny = 100, 100
dx = dy = 1.0
dt = 0.05
g = 9.81
k = 0.1
num_steps = 200

# Variabili fisiche
h = np.ones((ny, nx), dtype=np.float64)
u = np.zeros((ny, nx), dtype=np.float64)
v = np.zeros((ny, nx), dtype=np.float64)
z = np.zeros((ny, nx), dtype=np.float64)

# Piccola elevazione al centro
z[ny//2 - 5:ny//2 + 5, nx//2 - 5:nx//2 + 5] = 0.5

# Prepara la figura
fig, ax = plt.subplots()
im = ax.imshow(h, origin='lower', cmap='viridis', animated=True)
plt.colorbar(im, ax=ax, label='h')
ax.set_title("Evoluzione di h (altezza)")

# Funzione per aggiornare ogni frame
def update(frame):
    lib.step_forward(h.ravel(), u.ravel(), v.ravel(), z.ravel(),
                     nx, ny, dx, dy, dt, g, k)
    im.set_array(h)
    ax.set_title(f"h al passo {frame}")
    return [im]

# Crea animazione
ani = animation.FuncAnimation(fig, update, frames=num_steps, blit=True, interval=50)

plt.show()

