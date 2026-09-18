import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

a = np.array([5.75, 8, 11, 16.25, 24.5, 36.25, 52.25, 68.5, 81])
r=np.array([0.524, 0.474, 0.424, 0.374, 0.324, 0.274, 0.224, 0.174, 0.124])

y=np.array([0.03, 0.035, 0.035, 0.03, 0.044, 0.057, 0.039, 0.097, 0.12])
xe=(r**-1)
x = np.linspace(6.95, 525, 5)

func = lambda t, K, R: K*t + R
p, c = curve_fit(func, r**-3, np.tan(np.deg2rad(a)), sigma=y)

napake = c[0][0]**0.5 , c[1][1]**0.5
print(p, napake)

fig, ax = plt.subplots()

plt.ylabel(r'$tan(\alpha)$')
plt.xlabel(r'$r^{-3}[m^{-3}]$')

#ax.plot(r**-3, np.tan(np.deg2rad(a)))
ax.errorbar(r**-3, np.tan(np.deg2rad(a)), yerr=y, xerr=xe, capsize=3, marker="o", ls="")
ax.plot(x, func(x, *p), linewidth=1)
ax.grid(True)
plt.savefig("A.jpg")

plt.show()