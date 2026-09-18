import matplotlib.pyplot as plt
import pandas as pd

# 1. Nastavitve grafa za LaTeX dokument
plt.rcParams.update(
    {
        "font.family": "serif",
        "axes.labelsize": 11,
        "font.size": 10,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "figure.figsize": (6, 4.5),
    }
)

# 2. Prebiranje številk meritev iz prve vrstice
with open("fizkem.csv", "r", encoding="utf-8", errors="ignore") as f:
    prva_vrstica = f.readline().strip()

# Pretvorimo oznake v števila (int), da jih bomo lahko pravilno sortirali
oznake_meritev = [int(X.strip()) for X in prva_vrstica.split(";") if X.strip() != ""]

# 3. Prebiranje preostalih podatkov
df = pd.read_csv("fizkem.csv", sep=";", decimal=",", skiprows=1)
df = df.dropna(how="all", axis=1)

# Seznam, kamor bomo shranili prečiščene podatke za vsako meritev posebej
vse_meritve = []
stevilo_meritev = df.shape[1] // 2

for i in range(stevilo_meritev):
    idx_x = i * 2
    idx_y = i * 2 + 1

    # Prisilna pretvorba v številke (tekst z dna datoteke postane NaN)
    x_data = pd.to_numeric(df.iloc[:, idx_x], errors="coerce")
    y_data = pd.to_numeric(df.iloc[:, idx_y], errors="coerce")

    # Odstranimo vrstice z NaN (metapodatki)
    veljavni_podatki = pd.concat([x_data, y_data], axis=1).dropna()

    if not veljavni_podatki.empty:
        x_clean = veljavni_podatki.iloc[:, 0]
        y_clean = veljavni_podatki.iloc[:, 1]
        st_meritve = oznake_meritev[i]

        # Shranimo trojico: (številka_meritve, x_podatki, y_podatki)
        vse_meritve.append((st_meritve, x_clean, y_clean))

# 4. KLJUČNI KORAK: Sortiranje meritev po številki iz prve vrstice (od 0 do 8)
vse_meritve.sort(key=lambda x: x[0])

# 5. Risanje grafov v sortiranem vrstnem redu
plt.figure()

ph_vrednosti = [1, 9, 9.5, 10, 10.5, 11, 11.5, 13, 1]

for st_meritve, x_clean, y_clean in vse_meritve:
    plt.plot(x_clean, y_clean, label=f"pH {ph_vrednosti[st_meritve]}", linewidth=1.2)

# 6. Oblikovanje osi in čiste X-osi za LaTeX
plt.xlabel(r"$\lambda$ [nm]")
plt.ylabel(r"$a$")

# Omejitev osi, da se znebimo nepreglednosti
plt.xlim(260, 350)

plt.legend(loc="best", frameon=True, fancybox=False, edgecolor="black")
plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()

# 7. Shranjevanje v vektorski PDF format
plt.savefig("graf_absorbance.pdf", dpi=300)
print("Uspelo! Podatki so sortirani po številki meritve, X-os pa je očiščena.")
plt.show()