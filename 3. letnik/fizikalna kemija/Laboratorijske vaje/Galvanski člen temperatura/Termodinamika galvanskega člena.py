import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# 1. Podatki iz LaTeX tabele
T = np.array([20.0, 25.0, 30.0, 35.0, 40.0, 35.0, 30.0, 25.0, 20.0])
U = np.array([434.1, 426.9, 419.5, 411.6, 404.2, 412.0, 419.1, 425.9, 432.6])

# Definiranje natančnosti merilnih instrumentov (napake)
T_napaka_instr = 0.5  # +- 0.5 °C
U_napaka_instr = 0.3  # +- 0.3 mV

# Linearna regresija
res = linregress(T, U)
k, n, k_napaka = res.slope, res.intercept, res.stderr
print(k, n, k_napaka)

# 2. Tipografske nastavitve za LaTeX
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"] + plt.rcParams["font.serif"],
    "font.size": 11,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "mathtext.fontset": "cm"
})

# 3. Ustvarjanje slike
fig, ax = plt.subplots(figsize=(5, 3.5))

# Izris meritev z errorbar-i
# fmt='o' določi obliko točke, capsize doda prečne črtice na koncu intervala napake
# POPRAVLJENO: 'edgecolor' zamenjan z 'markeredgecolor' (ali mec)
ax.errorbar(T, U, xerr=T_napaka_instr, yerr=U_napaka_instr, fmt='o', 
            color='#d32f2f', markeredgecolor='k', linewidth=1, elinewidth=1, 
            capsize=3, markersize=4, label='Meritve', zorder=5)

# Generiranje točk in izris premice prilagoditve
T_fit = np.linspace(18, 42, 100)
U_fit = k * T_fit + n
ax.plot(T_fit, U_fit, color='#1976d2', linestyle='-', linewidth=1.5,
        label=f'Fit')

# Oznake osi in grafične nastavitve
ax.set_xlabel('$\mathit{T}$ [$^\circ\mathrm{C}$]')
ax.set_ylabel('$\mathit{\\bar{E}}$ [$\mathrm{mV}$]')

ax.grid(True, linestyle='--', alpha=0.5, linewidth=0.5)
ax.legend(loc='upper right', frameon=True, fancybox=False, edgecolor='k', framealpha=0.8)

# Prilagoditev meja oseh
ax.set_xlim(18, 42)
ax.set_ylim(400, 440)

# 4. Izvoz v PDF za LaTeX
plt.tight_layout()
plt.savefig('temodinamika_galvanskega_člena.pdf', format='pdf', bbox_inches='tight')
plt.show()