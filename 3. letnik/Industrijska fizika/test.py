import numpy as np
import matplotlib.pyplot as plt
import time

def load_sinogram(filename):
    """
    Naloži sinogram p(phi, s) iz .dat datoteke.
    Vrnemo sinogram p matriko z dimenzijami (n_phi, n_s), n_s in n_phi.
    """
    p = np.loadtxt(filename)
    n_phi, n_s = p.shape
    return p, n_phi, n_s

def filter_R_space(s, k0):
    """
    Analitični filter R_k0(s) v realnem prostoru (Enačba 4).
    Za s = 0 se uporabi limito k0^2 / pi.
    """
    R = np.zeros_like(s, dtype=float)
    nonzero = np.abs(s) > 1e-12
    
    # Enačba 4: R_k0(s) = (1 / 2pi) * [ (2 k0 / s) sin(k0 s) - (4 / s^2) sin^2(k0 s / 2) ]
    s_nz = s[nonzero]
    R[nonzero] = (1.0 / (2 * np.pi)) * (
        (2 * k0 / s_nz) * np.sin(k0 * s_nz) - 
        (4 / (s_nz**2)) * (np.sin(k0 * s_nz / 2.0)**2)
    )
    
    # Limita ko s -> 0
    R[~nonzero] = (k0**2) / (2 * np.pi)
    return R

def reconstruct_fbp_spatial(p, n_phi, n_s, k0=None, grid_size=256):
    """
    Rekonstrukcija v prostorski domeni z uporabo matričnega produkta/sledi (Enačbi 6 in 7).
    """
    delta_s = 2.0 / n_s
    delta_phi = np.pi / n_phi
    k_max = (n_s * np.pi) / 2.0
    
    if k0 is None:
        k0 = k_max / 2.0  # Privzeta izbira filtra

    # Ustvarimo mrežo točk (x, y) na intervalu [-1, 1]^2
    x = np.linspace(-1, 1, grid_size)
    y = np.linspace(-1, 1, grid_size)
    X, Y = np.meshgrid(x, y)

    # Koti phi_i
    angles = np.arange(n_phi) * delta_phi
    cos_phi = np.cos(angles)
    sin_phi = np.sin(angles)

    # Indeksi j za s_j = -1 + j * delta_s
    j_indices = np.arange(n_s)
    shift_s = 1.0 - j_indices * delta_s  # s + 1 - j*delta_s

    f_reconstructed = np.zeros((grid_size, grid_size))

    # Izračun f(x, y) z vektorizacijo po kotih in s-smerem
    for idx_x in range(grid_size):
        for idx_y in range(grid_size):
            xi = X[idx_x, idx_y]
            yi = Y[idx_x, idx_y]

            # Enotska krožnica: zunaj nje postavimo na 0
            if xi**2 + yi**2 >= 1.0:
                continue

            # s_i = x * cos(phi_i) + y * sin(phi_i)
            s_i = xi * cos_phi + yi * sin_phi  # oblike (n_phi,)

            # Argument filtra: s_i + 1 - j * delta_s
            # Tvorimo matriko R_ji z dimenzijo (n_s, n_phi)
            arg_R = s_i[np.newaxis, :] + shift_s[:, np.newaxis]
            R_mat = filter_R_space(arg_R, k0)

            # Enačba 7: f(x,y) = (1 / (n_s * n_phi)) * Tr(p @ R) = sum_ij (p_ij * R_ji)
            f_reconstructed[idx_x, idx_y] = np.sum(p.T * R_mat) / (n_s * n_phi)

    # Post-processing navodila:
    # 1. Negativne vrednosti postavimo na 0
    f_reconstructed[f_reconstructed < 0] = 0.0

    # 2. Normalizacija z f_max
    f_max = np.max(f_reconstructed)
    if f_max > 0:
        f_reconstructed /= f_max

    return f_reconstructed

def reconstruct_fft(p, n_phi, n_s, filter_type="ramp", grid_size=256):
    """
    Hitrejša alternativa z uporabo FFT (filtriranje sinograma v k-prostoru z ramp filtrom)[cite: 1].
    """
    delta_s = 2.0 / n_s
    delta_phi = np.pi / n_phi

    # Ramp filter v Fourierjevem prostoru
    k = np.fft.fftfreq(n_s, d=delta_s) * 2 * np.pi
    k_max = np.pi / delta_s
    abs_k = np.abs(k)
    
    if filter_type == 'ramp':
        H = abs_k
    elif filter_type == 'shepp-logan':
        H = abs_k * np.sinc(abs_k / (2 * k_max))
    elif filter_type == 'hann':
        H = abs_k * (0.5 + 0.5 * np.cos(np.pi * abs_k / k_max))
    else:
        H = abs_k

    H[abs_k > k_max] = 0.0

    # Filtriranje vsake vrstice sinograma
    p_filtered = np.zeros_like(p)
    for i in range(n_phi):
        p_fft = np.fft.fft(p[i, :])
        p_filtered[i, :] = np.real(np.fft.ifft(p_fft * H))

    # Povratna projekcija (Back-projection)
    x = np.linspace(-1, 1, grid_size)
    y = np.linspace(-1, 1, grid_size)
    X, Y = np.meshgrid(x, y)
    
    f_reconstructed = np.zeros((grid_size, grid_size))
    angles = np.arange(n_phi) * delta_phi
    s_coords = np.linspace(-1, 1, n_s)

    for i, angle in enumerate(angles):
        s_proj = X * np.cos(angle) + Y * np.sin(angle)
        # Linearna interpolacija projekcije na mrežo
        f_reconstructed += np.interp(s_proj, s_coords, p_filtered[i, :], left=0, right=0)

    f_reconstructed *= (delta_phi / np.pi)

    # Post-processing[cite: 1]
    f_reconstructed[X**2 + Y**2 >= 1.0] = 0.0
    f_reconstructed[f_reconstructed < 0] = 0.0
    f_max = np.max(f_reconstructed)
    if f_max > 0:
        f_reconstructed /= f_max

    return f_reconstructed

# ==========================================
# Primer uporabe
# ==========================================
if __name__ == "__main__":
    # Nastavite pot do vaše .dat datoteke ('phantom.dat', 'sg2.dat' ali 'sg3.dat')[cite: 1]
    filename = 'sg3.dat' 
    
    try:
        p, n_phi, n_s = load_sinogram(filename)
        print(f"Datoteka '{filename}' uspešno naložena.")
        print(f"Število kotov (n_phi): {n_phi}, Število vzorcev (n_s): {n_s}\n")

        # Izbira frekvenčne meje k0
        k_max = (n_s * np.pi) / 2.0
        # Preizkusite k_max / 3, k_max / 2, k_max[cite: 1]

        print("filter")
        start=time.perf_counter()
        img_reconstructed_filter=reconstruct_fft(p, n_phi, n_s, "hann", 256)
        end=time.perf_counter()
        print(str(end-start) + "s\n")

        # Rekonstrukcija (uporaba hitrejšega FFT pristopa ali direktne diskretizacije)
        print("fft")
        start=time.perf_counter()
        img_reconstructed_fft=reconstruct_fft(p, n_phi, n_s, "ramp", 256)
        end=time.perf_counter()
        print(str(end-start) + "s\n")

        print("k_max")
        start=time.perf_counter()
        img_reconstructed_k_max = reconstruct_fbp_spatial(p, n_phi, n_s, k_max, grid_size=256)
        end=time.perf_counter()
        print(str(end-start) + "s\n")

        print("k_max/2")
        start=time.perf_counter()
        img_reconstructed_k_max2 = reconstruct_fbp_spatial(p, n_phi, n_s, k_max/2, grid_size=256)
        end=time.perf_counter()
        print(str(end-start) + "s\n")

        print("k_max/3")
        start=time.perf_counter()
        img_reconstructed_k_max3 = reconstruct_fbp_spatial(p, n_phi, n_s, k_max/3, grid_size=256)
        end=time.perf_counter()
        print(str(end-start) + "s\n")
        
        # Prikaz sinograma in rekonstruirane slike
        fig, ax = plt.subplots(3, 2, figsize=(8,10))
        
        ax[0,0].imshow(p, aspect=2/np.pi, cmap='gray', extent=[-1, 1, np.pi, 0])
        ax[0,0].set_title("$p(\\phi, s)$")
        ax[0,0].set_xlabel("$s$")
        ax[0,0].set_ylabel("$\\phi$ [rad]")

        ax[0,1].imshow(img_reconstructed_filter, cmap='gray', extent=[-1, 1, -1, 1])
        ax[0,1].set_title("$f(x,y),$ fft Hanning")
        ax[0,1].set_xlabel("$x$")
        ax[0,1].set_ylabel("$y$")
        ax[0,1].set_xlim([-1,1])
        ax[0,1].set_ylim([-1,1])

        ax[1,0].imshow(img_reconstructed_fft, cmap='gray', extent=[-1, 1, -1, 1])
        ax[1,0].set_title("$f(x,y),$ fft ramp")
        ax[1,0].set_xlabel("$x$")
        ax[1,0].set_ylabel("$y$")

        ax[1,1].imshow(img_reconstructed_k_max, cmap='gray', extent=[-1, 1, -1, 1])
        ax[1,1].set_title("$f(x,y),$ k$_{max}$")
        ax[1,1].set_xlabel("$x$")
        ax[1,1].set_ylabel("$y$")

        ax[2,0].imshow(img_reconstructed_k_max2, cmap='gray', extent=[-1, 1, -1, 1])
        ax[2,0].set_title("$f(x,y),$ k$_{max}$/2")
        ax[2,0].set_xlabel("$x$")
        ax[2,0].set_ylabel("$y$")

        ax[2,1].imshow(img_reconstructed_k_max3, cmap='gray', extent=[-1, 1, -1, 1])
        ax[2,1].set_title("$f(x,y),$ k$_{max}$/3")
        ax[2,1].set_xlabel("$x$")
        ax[2,1].set_ylabel("$y$")

        plt.tight_layout()
        ime=filename.strip(".dat") + ".pdf"
        plt.savefig(ime)
        plt.show()

    except FileNotFoundError:
        print(f"Napaka: Datoteke '{filename}' ni bilo mogoče najti. Preverite pot do datoteke.")