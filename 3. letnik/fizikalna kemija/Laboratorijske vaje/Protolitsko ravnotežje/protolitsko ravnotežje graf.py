import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# ==========================================
# 1. PODATKI IZ TVOJE TABELE
# ==========================================
pH = np.array([9.0, 9.5, 10.0, 10.5, 11.0, 11.5])
alpha = np.array([0.0634, 0.157, 0.360, 0.619, 0.803, 0.945])

# ==========================================
# 2. PRERAČUN IN LINEARNA REGRESIJA
# ==========================================
# Izračun y vrednosti: ln(alpha / (1 - alpha))
y = np.log(alpha / (1 - alpha))

# Linearna regresija (fittanje premice y = k * pH + n)
res = linregress(pH, y)
k, n = res.slope, res.intercept
k_napaka = res.stderr
n_napaka = res.intercept_stderr

# Izračun eksperimentalnega pKa iz fita
pKa_eksperimentalni = -n / k

# Prenos napak za izračun napake pKa
pKa_napaka = abs(pKa_eksperimentalni) * np.sqrt((n_napaka / n)**2 + (k_napaka / k)**2)

# Izpis rezultatov v terminal
print("--- REZULTATI FITANJA ---")
print(f"Naklon premice (k): {k:.4f} ± {k_napaka:.4f}")
print(f"Odsek na osi y (n): {n:.4f} ± {n_napaka:.4f}")
print(f"Izračunan pKa iz grafa: {pKa_eksperimentalni:.3f} ± {pKa_napaka:.3f}")

# ==========================================
# 3. NASTAVITVE ZA LATEX GRAFIKO
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

fig, ax = plt.subplots(figsize=(5.5, 4))

# Izris eksperimentalnih točk
ax.scatter(pH, y, color='#d32f2f', edgecolor='k', linewidth=0.5, s=40, label='Meritve', zorder=5)

# Izris fitane premice (malo čez meje podatkov)
pH_fit = np.linspace(8.5, 12.0, 100)
y_fit = k * pH_fit + n
ax.plot(pH_fit, y_fit, color='#1976d2', linestyle='-', linewidth=1.5,
        label=f'Fit')

# Oznake osi
ax.set_xlabel('$\\mathrm{pH}$')
ax.set_ylabel('$\\ln\\left(\\frac{\\alpha}{1-\\alpha}\\right)$')

# Dodatne grafične izboljšave
ax.grid(True, linestyle='--', alpha=0.5, linewidth=0.5)
ax.legend(loc='upper left', frameon=True, fancybox=False, edgecolor='k', framealpha=0.9)

# Nastavitev meja oseh za lepši pregled
ax.set_xlim(8.5, 12.0)
ax.set_ylim(min(y) - 0.5, max(y) + 0.5)

plt.tight_layout()

# Shranjevanje v PDF formatu za LaTeX
plt.savefig('graf_alpha_ph.pdf', format='pdf', bbox_inches='tight')
plt.show()