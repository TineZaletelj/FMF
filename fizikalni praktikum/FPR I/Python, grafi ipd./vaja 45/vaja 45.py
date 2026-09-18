import matplotlib.pyplot as plt
import numpy as np

r = 115
x = np.linspace(1, 9, 3)

#1 I = 3A
I1 = [1.5, 3, 4.5, 6, 7.5, 9]
F1 = [0.3, 0.6, 1, 1.2, 1.6, 1.9]
M1 = []
for i in F1:
    M1.append(i * r)

k1, n1 = np.polyfit(I1, M1, 1)

#2 Ih = 1.5A
I2 = [4.5, 3.75, 3, 2.25, 1.5, 0.75]
F2 = [1, 0.8, 0.7, 0.5, 0.35, 0.2]
M2 = []
for i in F2:
    M2.append(i * r)

k2, n2 = np.polyfit(I2, M2, 1)

#3 I = 2.5A
I3 = [7.5, 6.25, 5, 3.75, 2.5, 1.25]
F3 = [1.65, 1.35, 1.05, 0.8, 0.55, 0.3]
M3 = []
for i in F3:
    M3.append(i * r)

k3, n3 = np.polyfit(M3, I3, 1)

#4 Ih = 2A
I4 = [6, 5, 4, 3, 2, 1]
F4 = [1.3, 1.1, 0.85, 0.65, 0.45, 0.25]
M4 = []
for i in F4:
    M4.append(i * r)

k4, n4 = np.polyfit(M4, I4, 1)


plt.scatter(I1, M1, c="green", s=10)
plt.plot(x, k1*x+n1, c="green", linewidth=1, linestyle="dashed")

plt.scatter(I2, M2, c="red", s=10)
plt.plot(x, k2*x+n2, c="red", linewidth=1, linestyle="dotted")

plt.scatter(I3, M3, c="cyan", s=10)
plt.plot(x, k3*x+n3, c="cyan", linewidth=1.5, linestyle="dashed")

plt.scatter(I4, M4, c="violet", s=10)
plt.plot(x, k4*x+n4, c="violet", linewidth=1, linestyle="dashed")

plt.show()

print(k1, k2, k3, k4)