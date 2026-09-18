import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


T = np.array([6.36, 8.15, 9.43, 11.27])
P=np.array([30.1, 40.8, 49.8, 63.5])
y=(0.005*P)
xe=0.02*T
x = np.linspace(6, 11.5, 5)

func = lambda t, K, R: K*t + R
p, c = curve_fit(func, T, P, sigma=y, absolute_sigma=True)

napake = c[0][0]**0.5 , c[1][1]**0.5
print(p, napake)

fig, ax = plt.subplots()

plt.ylabel(r'P[W]')
plt.xlabel(r'$\Delta T[K]$')

ax.errorbar(T, P, yerr=y, xerr=xe, capsize=3, marker="o", ls="")
ax.plot(x, func(x, *p), linewidth=1)
ax.grid(True)
plt.savefig("B.jpg")

plt.show()

print(str.join('',[f'{U_0:.2f} & {P_m:.2f} \\\\\n'
                   for U_0, P_m in zip(T[:], P[:])]))