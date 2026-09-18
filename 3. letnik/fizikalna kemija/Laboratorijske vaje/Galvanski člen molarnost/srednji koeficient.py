import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# ==========================================
# 1. PODATKI IZ TVOJE TABELE
# ==========================================
# Koncentracija c v M
c_podatki = np.array([0.05, 0.025, 0.0125, 0.00625, 0.003125]) 
# Napetost U v mV
U_podatki = np.array([275.9, 242.5, 208.8, 174.7, 140.1]) 

# ==========================================
# 2. KONSTANTE IN PRERAČUNI OSEH
# ==========================================
R = 8.31446        # Plinska konstanta [J / (mol K)]
F = 96485.3        # Faradayeva konstanta [C / mol]
T = 25 + 273.15    # 25 °C v Kelvine [K]
c_st = 1.0         # Standardna koncentracija [M]

# Pretvorba U iz mV v V, da se enote ujemajo s konstantami R, T, F
E_V = U_podatki / 1000.0

# Izračun koordinat za graf
x = np.sqrt(c_podatki)
# Izračun y po formuli: E - (2RT/F) * ln(c/c_st)
y = E_V - (2 * R * T) * np.log(c_podatki)/F
#y=np.array([0.4261, 0.4264, 0.4261, 0.4253, 0.4242])
print(y)

# Linearna regresija (fittanje premice)
res = linregress(x, y)
k, n, k_napaka = res.slope, res.intercept, res.stderr

# Izpis izračunanih vrednosti v terminal (za vnos v tekst poročila)
print("--- REZULTATI FITANJA ---")
print(f"Naklon premice (k): {k:.4f} ± {k_napaka:.4f} V/M^0.5")
print(f"Odsek na osi y (n): {n:.4f} V")

# ==========================================
# 3. STILSKA PRILAGODITEV ZA LATEX
# ==========================================
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

# Ustvarjanje slike (dimenzije primerne za standardno širino strani)
fig, ax = plt.subplots(figsize=(5.5, 4))

# Izris eksperimentalnih točk
ax.scatter(x, y, color='#d32f2f', edgecolor='k', linewidth=0.5, s=35, label='Meritve', zorder=5)

# Generiranje točk za izris fitane premice (malo čez meje podatkov za lepši izgled)
x_fit = np.linspace(0, max(x) * 1.2, 100)
y_fit = k * x_fit + n
ax.plot(x_fit, y_fit, color='#1976d2', linestyle='-', linewidth=1.5,
        label=f'Fit')

# Oznake osi (spremenljivke poševno, enote pokončno v oglatih oklepajih)
ax.set_xlabel('$\\sqrt{c} \\quad [\\mathrm{mol}^{1/2}\\mathrm{dm}^{3/2}]$')
ax.set_ylabel('$E - \\frac{2RT}{F}\\ln(c/c^{\\circ}) \\quad [\\mathrm{V}]$')

# Mreža in legenda
ax.grid(True, linestyle='--', alpha=0.5, linewidth=0.5)
ax.legend(loc='lower right', frameon=True, fancybox=False, edgecolor='k', framealpha=0.9)

# Nastavitev tesnejših meja oseh glede na tvoje podatke
ax.set_xlim(0, max(x) * 1.2)

# Avtomatska postavitev, da dolga enačba na y-osi ne bo odrezana
plt.tight_layout()

# Shranjevanje v PDF formatu (brez izgube kakovosti pri povečavi v LaTeX-u)
plt.savefig('srednji koeficient.pdf', format='pdf', bbox_inches='tight')
plt.show()