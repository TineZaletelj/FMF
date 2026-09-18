import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


T = np.array([94.0, 92.1, 90.1, 88.1, 86.1, 83.7, 82.2, 80.3, 78.2, 74.6, 71.9, 69.4, 68.2, 65.2, 61.8, 59.9, 57.7, 55.0, 53.5, 51.7, 49.9, 46.4, 44.9, 42.2, 39.7, 36.9, 34.5, 32.8, 30.7, 28.7, 26.4, 23.5, 20.8, 18.3])
U=np.array([3880, 3772, 3705, 3603, 3503, 3402, 3333, 3267, 3179, 3032, 2926, 2827, 2766, 2652, 2510, 2428, 2335, 2225, 2127, 2060, 1984, 1826, 1776, 1665, 1550, 1448, 1351, 1275, 1201, 1125, 1029, 912, 807, 705])
y=(0.005*U)
xe=0.02*T
x = np.linspace(18, 94, 5)

func = lambda t, K, R: K*t + R
p, c = curve_fit(func, T, U, sigma=y, absolute_sigma=True)

napake = c[0][0]**0.5 , c[1][1]**0.5
print(p, napake)

fig, ax = plt.subplots()

plt.ylabel(r'U[$\mu V$]')
plt.xlabel(r'$\Delta T[K]$')

ax.errorbar(T, U, yerr=y, xerr=xe, capsize=3, marker="o", ls="")
ax.plot(x, func(x, *p), linewidth=1)
ax.grid(True)
plt.savefig("A.jpg")

plt.show()

print(str.join('',[f'{U_0:.2f} & {P_m:.2f} \\\\\n'
                   for U_0, P_m in zip(T[:], U[:])]))