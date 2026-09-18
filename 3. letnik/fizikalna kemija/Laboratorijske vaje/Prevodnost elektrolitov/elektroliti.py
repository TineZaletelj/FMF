import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Linearna funkcija za fitanje (y = k * x + n)
def premica(x, k, n):
    return k * x + n

# ==============================================================================
# KONSTANTE IN VHODNE NAPAKE
# ==============================================================================
kappa_t_us = 1.14       # muS/cm
kappa_t = kappa_t_us * 1e-4  # pretvorba v S/m

rel_err_c = 0.01        # 1% relativna napaka koncentracije
c_standard = 1000.0     # Standardna koncentracija c_0 = 1000 mol/m^3 (kar je 1 mol/L)

# Napake prevodnosti (pretvorjene v S/m)
err_kappa_sibki = 0.1 * 1e-4   # 0.1 muS/cm -> S/m
err_kappa_mocni = 0.01 * 1e-1  # 0.01 mS/cm -> S/m

# ==============================================================================
# 1. PODATKI IN PRETVORBA V SI ENOTE
# ==============================================================================

# --- ŠIBEK ELEKTROLIT ---
c_sibki_L = np.array([0.00025, 0.0005, 0.001, 0.002]) # mol/L
c_sibki = c_sibki_L * 1000                             # mol/m^3
kappa_sibki = np.array([26.1, 38.3, 55.2, 79.0]) * 1e-4 # S/m

err_c_sibki = c_sibki * rel_err_c 

Lambda_sibki = (kappa_sibki - kappa_t) / c_sibki
err_Lambda_sibki = Lambda_sibki * np.sqrt((err_kappa_sibki / (kappa_sibki - kappa_t))**2 + (err_c_sibki / c_sibki)**2)

# Osi za graf šibkega elektrolita
x_sibki = 1.0 / Lambda_sibki
err_x_sibki = err_Lambda_sibki / (Lambda_sibki**2)

# POPRAVEK: y os deljena s c_standard
y_sibki = (Lambda_sibki * c_sibki) / c_standard
err_y_sibki = y_sibki * np.sqrt((err_Lambda_sibki / Lambda_sibki)**2 + (err_c_sibki / c_sibki)**2)


# --- MOČAN ELEKTROLIT ---
c_mocni_L = np.array([0.005, 0.01, 0.02, 0.04, 0.08]) # mol/L
c_mocni = c_mocni_L * 1000                            # mol/m^3
kappa_mocni = np.array([0.610, 1.416, 2.75, 5.34, 10.29]) * 1e-1 # S/m

err_c_mocni = c_mocni * rel_err_c

Lambda_mocni = (kappa_mocni - kappa_t) / c_mocni
err_Lambda_mocni = Lambda_mocni * np.sqrt((err_kappa_mocni / (kappa_mocni - kappa_t))**2 + (err_c_mocni / c_mocni)**2)

# Osi za graf močnega elektrolita
x_mocni = np.sqrt(c_mocni)
err_x_mocni = err_c_mocni / (2 * np.sqrt(c_mocni))

y_mocni = Lambda_mocni
err_y_mocni = err_Lambda_mocni


# ==============================================================================
# 2. FITANJE IN GRAF ZA MOČAN ELEKTROLIT
# ==============================================================================
popt_m, pcov_m = curve_fit(premica, x_mocni[1:], y_mocni[1:], sigma=err_y_mocni[1:], absolute_sigma=True)
k_m, n_m = popt_m
err_k_m, err_n_m = np.sqrt(np.diag(pcov_m))

plt.figure(figsize=(13, 5.5))

plt.subplot(1, 2, 1)
plt.errorbar(x_mocni, y_mocni, xerr=err_x_mocni, yerr=err_y_mocni, 
             fmt='o', color='blue', ecolor='black', capsize=3, label='Meritve')

x_fit_m = np.linspace(0, max(x_mocni)*1.1, 100)
legenda_m = (f'Fit:\n'
             f'$k = ({k_m:.2e} \\pm {err_k_m:.2e})$ S m$^{{7/2}}$ mol$^{{-3/2}}$\n'
             f'$n = ({n_m:.4f} \\pm {err_n_m:.4f})$ S m$^2$ mol$^{{-1}}$')
plt.plot(x_fit_m, premica(x_fit_m, k_m, n_m), 'b--', label=legenda_m)

plt.title('Močan elektrolit (Kohlrauschov zakon)')
plt.xlabel(r'$\sqrt{c}$ [$\sqrt{\mathrm{mol/m^3}}$]')
plt.ylabel(r'$\Lambda$ [$\mathrm{S\,m^2/mol}$]')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=9)

# ==============================================================================
# 3. FITANJE IN GRAF ZA ŠIBEK ELEKTROLIT (Z ENOTAMI Sm^2/mol NA Y OSI)
# ==============================================================================
# c_sibki_L je koncentracija v mol/L, zato je (c_sibki_L / 1.0) brezdimenzijska vrednost c/c_standard
y_sibki = Lambda_sibki * c_sibki_L  
err_y_sibki = y_sibki * np.sqrt((err_Lambda_sibki / Lambda_sibki)**2 + (err_c_sibki / c_sibki)**2)

popt_s, pcov_s = curve_fit(premica, x_sibki, y_sibki, sigma=err_y_sibki, absolute_sigma=True)
k_s, n_s = popt_s
err_s_s, err_n_s = np.sqrt(np.diag(pcov_s))

plt.subplot(1, 2, 2)
plt.errorbar(x_sibki, y_sibki, xerr=err_x_sibki, yerr=err_y_sibki, 
             fmt='s', color='red', ecolor='black', capsize=3, label='Meritve')

x_fit_s = np.linspace(min(x_sibki)*0.9, max(x_sibki)*1.1, 100)

# POPRAVLJENE ENOTE V LEGENDI S SKLADNOSTJO POKRAJŠANIH KONCENTRACIJ
legenda_s = (f'Fit:\n'
             f'$k = ({k_s:.2e} \\pm {err_s_s:.2e})$ S$^2$ m$^4$ mol$^{{-2}}$\n'
             f'$n = ({n_s:.2e} \\pm {err_n_s:.2e})$ S m$^2$ mol$^{{-1}}$')
plt.plot(x_fit_s, premica(x_fit_s, k_s, n_s), 'r--', label=legenda_s)

plt.title('Šibek elektrolit (Ostwaldova modifikacija)')
plt.xlabel(r'$1/\Lambda$ [$\mathrm{mol/(S\,m^2)}$]')
plt.ylabel(r'$\Lambda \cdot (c / c^\circ)$ [$\mathrm{S\,m^2/mol}$]')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=9)

plt.tight_layout()

# ==============================================================================
# 4. REZULTATI V TERMINAL Z NOVIMI ENOTAMI
# ==============================================================================
print("="*60)
print("REZULTATI LINEARNE REGRESIJE Z ENOTAMI Sm^2/mol (SI sistem):")
print("="*60)
print("MOČAN ELEKTROLIT (Lambda vs sqrt(c)):")
print(f"  Naklon (k):       {k_m:.6e} ± {err_k_m:.6e} S m^(7/2) mol^(-3/2)")
print(f"  Začetna vr. (n):  {n_m:.6e} ± {err_n_m:.6e} S m^2 mol^(-1)")
print("-"*60)
print("ŠIBEK ELEKTROLIT (Lambda * (c/c_standard) vs 1/Lambda):")
print(f"  Naklon (k):       {k_s:.6e} ± {err_s_s:.6e} S^2 m^4 mol^(-2)")
print(f"  Začetna vr. (n):  {n_s:.6e} ± {err_n_s:.6e} S m^2 mol^(-1)")
print("="*60)

plt.savefig("elektroliti.pdf")
plt.show()