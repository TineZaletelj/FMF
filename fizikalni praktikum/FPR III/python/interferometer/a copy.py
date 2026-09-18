import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


P = np.array([0.5, 1, 1.15, 1.3, 1.4, 1.5])
N=np.array([24, 50, 52, 57, 70, 72])
y=(0.04*N)
xe=0.05*P
x = np.linspace(0.25, 1.75, 5)

func = lambda t, K, R: K*t + R
p, c = curve_fit(func, P, N, sigma=y, absolute_sigma=True)

napake = c[0][0]**0.5 , c[1][1]**0.5
print(p, napake)

fig, ax = plt.subplots()

plt.ylabel("N")
plt.xlabel("p[bar]")

ax.errorbar(P, N, yerr=y, xerr=xe, capsize=3, marker="o", ls="")
ax.plot(x, func(x, *p), linewidth=1)
ax.grid(True)
plt.savefig("A.jpg")

plt.show()