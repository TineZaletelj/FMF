import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


r = np.array([0,10.3,20.7,31,41.3,51.7,62,72.3,82.7,93])
N=np.array([1209,1090,1066,1062,831,756,670,644,583,528,456,386,277,267,178,134,102,80,78,71,65])
A = np.array([67.1,39.75,24.8,16.4,13.5,10.3,7.25,5.85,4.5,3.65])
a=1/(np.sqrt(A))
y=1/(np.sqrt(20)*A)
x = np.linspace(-10, 110, 5)

func = lambda t, K, R: K*t + R
p, c = curve_fit(func, r, a, sigma=y, absolute_sigma=True)

napake = c[0][0]**0.5 , c[1][1]**0.5
print(p, napake)

fig, ax = plt.subplots()

plt.xlabel("r[mm]")
plt.ylabel(r'$A^{-1/2}[s^{1/2}]$')
plt.xlim(-5,100)

ax.errorbar(r, a, yerr=y, capsize=3, marker="o", ls="")
ax.plot(x, func(x, *p), linewidth=1)
ax.grid(True)

plt.show()