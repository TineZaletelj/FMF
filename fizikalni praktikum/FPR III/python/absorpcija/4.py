import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

s, N, n = np.loadtxt("4.csv", delimiter=",", unpack=True)
A = N/400 - 0.384
y=1/(20*np.sqrt(A))
a=np.log(A)
d=s/1134
x = np.linspace(0, 11, 5)

func = lambda t, K, R: K*t + R
p, c = curve_fit(func, d, a, sigma=y, absolute_sigma=True)

napake = c[0][0]**0.5 , c[1][1]**0.5
print(p, napake)

fig, ax = plt.subplots()

plt.xlabel("d[mm]")
plt.ylabel(r'$ln(A_\gamma)$')

ax.errorbar(d, a, yerr=y, capsize=3, marker="o", ls="")
ax.plot(x, func(x, *p), linewidth=1)
ax.grid(True)

plt.show()