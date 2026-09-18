import numpy as np
import matplotlib.pyplot as plt

# 1. Definiranje podatkov iz tabele v numpy sezname
t = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 35, 40, 45, 50, 55, 60])
kappa = np.array([56.9, 114.95, 166, 214, 256, 295.1, 331.7, 365.7, 397.9, 427.7, 488, 538.4, 584.1, 
                  625.9, 665, 698.6, 731.4, 760.6, 787.5, 812.3, 866.1, 910.7, 947.7, 978.3, 1004, 1025.6])/100000

# Konstanta c_0
c_0 = 0.0151
L=1.4803
A=9.962
B=37.74
k_k=0.001139

c_1=kappa*c_0/k_k


# 2. Iterativni izračun preostalih koncentracij
def enačba(c):
    return L - A * np.sqrt(c) + B * c


lam_1 = enačba(c_1)
c_2 = kappa / lam_1

lam_2=enačba(c_2)
c_3 = kappa / lam_2

lam_3=enačba(c_3)
c_4 = kappa / lam_3

lam_4=enačba(c_4)
c_5 = kappa / lam_4

lam_5=enačba(c_5)
c_6 = kappa / lam_5

c=c_6
for i in range(20):
    lam=enačba(c)
    c=kappa / lam


# Funkcija za transformacijo ln(c_0 / (c_0 - c_n))
# Uporabimo np.where, da preprečimo deljenje z nič ali logaritmiranje negativnih vrednosti
def transform(c, c_0):
    imenovalec = c_0 - c
    # Če je imenovalec manjši ali enak 0, vrne NaN, da ne sesuje izrisa
    varen_imenovalec = np.where(imenovalec > 0, i_menovalec := imenovalec, np.nan)
    return np.log(c_0 / varen_imenovalec)

# Transformacija vseh koncentracij za y-os
y_1 = transform(c_1, c_0)
y_2 = transform(c_2, c_0)
y_3 = transform(c_3, c_0)
y_4 = transform(c_4, c_0)
y_5 = transform(c_5, c_0)
y_6 = transform(c_6, c_0)
y = transform(c, c_0)

#fit
k, n = np.polyfit(t, y_6, 1)


# 3. Nastavitve grafike za LaTeX dokument
plt.rcParams.update({
    "text.usetex": True,            # Uporabi LaTeX za izris besedila
    "font.family": "serif",         # Serifna pisava (Computer Modern)
    "font.size": 11,                # Velikost pisave primerna za besedilo naloge
    "axes.labelsize": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.figsize": (6, 4.5)      # Dimenzije slike v inčih
})

# Izris vseh krivulj na enem grafu v enakem merilu
#plt.plot(t, y_1, 'x', color='tab:blue', label=r'$c_1$', linewidth=1.5, markersize=2)
plt.plot(t, y_2, 'x', color='tab:red', label=r'$c_1$', linewidth=1.5, markersize=4)
plt.plot(t, y_3, 'x', color='tab:cyan', label=r'$c_2$', linewidth=1.5, markersize=4)
plt.plot(t, y_4, 'x', color='tab:orange', label=r'$c_3$', linewidth=1.5, markersize=4)
plt.plot(t, y_5, 'x', color='tab:green', label=r'$c_4$', linewidth=1.5, markersize=4)
plt.plot(t, y_6, 'x', color='tab:blue', label=r'$c_5$', linewidth=1.5, markersize=4)
plt.plot(t, y, 'x', color='black', label=r'$c_{25}$', linewidth=1.5, markersize=4)
plt.plot(t, k*t+n)

# Označbe osi in mreža
plt.xlabel(r'$t$[min]')
plt.ylabel(r'$\ln\left(\frac{c_0}{c_0 - c_n}\right)$')
plt.grid(True, linestyle=':', alpha=0.6)

# Dodajanje legende
plt.legend(loc='best')

# Izboljšanje razporeda in shranjevanje v PDF (vektorski format)
plt.tight_layout()
plt.savefig('graf_sadra.pdf', bbox_inches='tight')
plt.show()


print(c,y)