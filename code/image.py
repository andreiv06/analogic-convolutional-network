import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from PIL import Image


def adauga_eroare_mismatch(kernel_ideal, sigma=0.1):
    """
    sigma: reprezinta gradul de eroare (ex: 0.1 inseamna 10% variatie).
    Aceasta reprezinta abaterea standard a valorilor greutatilor (Weight)
    din cauza mismatch-ului tranzistoarelor.
    """
    # Generam o matrice de zgomot cu aceeasi forma ca si kernel-ul
    # Media 0, Abaterea standard 'sigma'
    eroare = np.random.normal(loc=0.0, scale=sigma, size=kernel_ideal.shape)

    # Adaugam eroarea peste kernel-ul ideal
    kernel_real = kernel_ideal + eroare

    return kernel_real


# Exemplu de utilizare:

def procesare_si_afisare_matrice(cale_imagine):
    # 1. Încărcăm imaginea
    try:
        img = Image.open(cale_imagine).convert('L')
        # Redimensionăm la 50x50 pentru a fi lizibilă în consolă
        img = img.resize((30,30))
    except FileNotFoundError:
        print(f"Eroare: Nu am găsit fișierul.")
        return

    img_array = np.array(img) / 255.0

    # 2. Kernel-ul Laplace
    kernel = np.array([[0, -1, 0],
                       [-1, 4, -1],
                       [0, -1, 0]])
    kernel_cu_eroare = adauga_eroare_mismatch(kernel, sigma=0.3)
    # 3. Procesarea (Convoluția)
    imagine_contur = signal.convolve2d(img_array, kernel_cu_eroare, mode='same')
    imagine_contur_clean = signal.convolve2d(img_array, kernel, mode='same')
    # --- NOU: AFIȘAREA VALORILOR NUMERICE ---
    # Alegem un sub-bloc de 10x10 din centrul imaginii
    start = 20
    end = 30
    print("--- Matricea de intrare (10x10 sub-bloc) ---")
    print(np.round(img_array[start:end, start:end], 2))

    print("\n--- Matricea rezultată (10x10 sub-bloc) ---")
    print(np.round(np.abs(imagine_contur[start:end, start:end]), 2))
    # ----------------------------------------

    # 4. Vizualizare
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.imshow(img_array, cmap='gray')
    ax1.set_title("Imagine Input")
    ax2.imshow(np.abs(imagine_contur), cmap='magma')
    ax2.set_title("Rezultat Convoluție (Iout)")
    plt.show()
   # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    #ax1.imshow(img_array, cmap='gray')
    #ax1.set_title("Imagine Input")
    #ax2.imshow(np.abs(imagine_contur_clean), cmap='magma')
    #ax2.set_title("Rezultat Convoluție (Iout)")
   # plt.show()


calea_mea1 = r"checkerboard.png"
#calea_mea2 = r"circle_filled.png"
#calea_mea3 = r"cross.png"
procesare_si_afisare_matrice(calea_mea1)
#procesare_si_afisare_matrice(calea_mea2)
#procesare_si_afisare_matrice(calea_mea3)