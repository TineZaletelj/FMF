import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Definiramo linearno funkcijo za fitanje (y = k * t + n)
def linearna_funkcija(t, k, n):
    return k * t + n

# ==========================================
# 1. PODATKI IN IZRAČUN Y VREDNOSTI
# ==========================================

# Tabela 1
t1 = np.array([510, 1031, 1345, 1480, 2110, 3042, 3770, 5061, 5785])
phi1 = np.array([11.28, 11.25, 11.13, 10.83, 10.5, 9.95, 9.73, 9.21, 8.65])
az1, ak1 = 11.44, -3.72
y1 = np.log((az1 - ak1) / (phi1 - ak1))
c_s1=0.25/(az1 - ak1) * (phi1 - ak1)

# Tabela 2
t2 = np.array([469, 1457, 2380, 3390, 4286, 5324, 6344])
phi2 = np.array([10.88, 9.8, 8.75, 7.88, 6.97, 6.35, 5.42])
az2, ak2 = 11.38, -3.7
y2 = np.log((az2 - ak2) / (phi2 - ak2))
c_s2=0.25/(az2 - ak2) * (phi2 - ak2)

# Tabela 3
t3 = np.array([417, 526, 1570, 2352, 3422, 4472, 5581])
phi3 = np.array([19.88, 18.92, 15.83, 14.28, 12.4, 10.88, 8.88])
az3, ak3 = 21.74, -7.06
y3 = np.log((az3 - ak3) / (phi3 - ak3))
c_s3=0.5/(az3 - ak3) * (phi3 - ak3)

# Združimo v strukturo za lažjo zanko
podatki = [
    {"t": t1, "y": y1, "label": "Vzorec 1", "color": "blue", "marker": "o"},
    {"t": t2, "y": y2, "label": "Vzorec 2", "color": "green", "marker": "s"},
    {"t": t3, "y": y3, "label": "Vzorec 3", "color": "red", "marker": "^"}
]

# ==========================================
# 2. FITANJE IN IZRIS GRAFA
# ==========================================
plt.figure(figsize=(10, 7))

print("REZULTATI LINEARNEGA FITANJA (y = k * t + n):")
print("-" * 60)

for p in podatki:
    # curve_fit vrne optimalne parametre (popt) in kovariantno matriko (pcov)
    popt, pcov = curve_fit(linearna_funkcija, p["t"], p["y"])
    
    k_opt, n_opt = popt
    # Standardna napaka parametrov je koren diagonalnih elementov kovariantne matrike
    k_err, n_err = np.sqrt(np.diag(pcov))
    
    # Izpis rezultatov v terminal
    print(f"{p['label']}:")
    print(f"  Naklon (k) = {k_opt:.6e} ± {k_err:.6e} s^-1")
    print(f"  Presek (n) = {n_opt:.4f} ± {n_err:.4f}")
    print("-" * 60)
    
    # Izris eksperimentalnih točk
    plt.scatter(p["t"], p["y"], color=p["color"], marker=p["marker"], 
                s=50, label=f"{p['label']}")
    
    # Izris fitane premice (generiramo gladke t-točke od min do max)
    t_fit = np.linspace(min(p["t"])*0.8, max(p["t"])*1.1, 100)
    y_fit = linearna_funkcija(t_fit, k_opt, n_opt)
    
    # Dodamo informacijo o naklonu v legendi grafa
    legenda_text = f"Fit"
    plt.plot(t_fit, y_fit, color=p["color"], linestyle="--", label=legenda_text)

# Urejanje izgleda grafa
plt.xlabel("$t$[s]", fontsize=12)
plt.ylabel(r"$\ln\left(\frac{\alpha_z - \alpha_k}{\alpha - \alpha_k}\right)$", fontsize=14)
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(fontsize=10, loc="upper left")

# Prikaz grafa
plt.tight_layout()
plt.savefig("inverzija saharoze ln.pdf")
plt.show()

k_1=3.69e-05
k_2=7.89e-05
k_3=9.71e-05

time=np.linspace(0,6500,100000)
def funkcija(c_0,k,t):
    return c_0*np.exp(-k*t)

y_1=funkcija(0.25, k_1, time)
y_2=funkcija(0.25, k_2, time)
y_3=funkcija(0.48, k_3, time)

plt.scatter(t1,c_s1, color="tab:blue", label="vzorec 1")
plt.scatter(t2,c_s2, color="tab:green", label="vzorec 2")
plt.scatter(t3,c_s3, color="tab:red", label="vzorec 3")
plt.plot(time, y_1, color="tab:blue")
plt.plot(time, y_2, color="tab:green")
plt.plot(time, y_3, color="tab:red")
plt.legend()
plt.xlabel(f"$t$[s]")
plt.ylabel(f"$c_S$[mol/l]")
plt.savefig("inverzija saharoze c.pdf")
plt.show()