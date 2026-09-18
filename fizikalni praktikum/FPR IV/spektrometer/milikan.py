import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

g=9.81
vis=0.0000183
ro=973-1.3
E=5
d=5

# prvi del (A, naziv, v[mm/s], U[V], I[uA])
v = np.array([37.04, 24.26, 27.04, 28.54, 24.34, 29.99, 24.89, 31.572, 51.17, 22.95, 28.97, 22.42, 20.36, 35.67, 36.48])
U = np.array([197.6, 72.1, 157.8, 98.7, 91.3, 117.8, 93.6, 140.2, 118.8, 88.3, 110.2, 76.8, 44.3, 87.6, 87.6])

r0=np.round(np.sqrt(9*vis*v)/(2*ro*g)*10**6,2)
ne0=np.round((4*3.14*(r0**3)*ro*g)/(3*U/d)*10**(-24),21)


# Drugi del (v₁, v₂)
v1 = np.array([109.265, 105.338, 190.925, 96.23, 100.06, 156.323, 100.207, 151.864, 141.987, 107.007, 93.127, 95.172, 101.132, 129.235, 120.908, 112.129, 105.245])
v2 = np.array([58.461, 59.984, 66.915, 40.595, 48.245, 66.906, 5.512, 45.509, 10.687, 56.089, 30.087, 10.902, 20.803, 60.753, 54.326, 42.052, 28.283])

r1=np.round(np.sqrt((4*vis/(4*g*ro))*(v1-v2))*10**(4),2)
ne1=(3*3.14*r1*vis)*(v1+v2)/E*10**(-17)
ne1=np.round(ne1, decimals=21)

plt.hist(ne0, bins=13, cumulative=1)
plt.show()

#print(r" \\ ".join([str(v1[i]) + " & " + str(v2[i]) + " & " + str(r1[i]) + " & " + str(ne1[i]) for i in range(len(v1))]))
a=np.array([v, U, r0, ne0*10**19])
a=np.rot90(a, k=1, axes=(0, 1))
df = pd.DataFrame(a)

# Save the DataFrame to an Excel file
#df.to_excel('output1.xlsx', index=False)
ne0=np.sort(ne0)
print(ne0)
print(np.average(ne0[3::]), np.average(ne1))
