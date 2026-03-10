import numpy as np
import subprocess
import matplotlib.pyplot as plt
from PIL import Image
import os

# --- CONFIGURARE ---
NGSPICE_CMD = "ngspice"
MODEL_FILE = "model_mos.lib"
IMAGE_FILE = "checkerboard.png"
TEMP_SP = "temp.sp"
RESULT_FILE = "rezultat.txt"


def run_spice_sim(pixels, weights):
    # 1. Asigură-te că fișierul rezultat vechi este șters
    if os.path.exists(RESULT_FILE):
        os.remove(RESULT_FILE)

    netlist = [
        f".include {MODEL_FILE}",
        "Vdd vdd 0 DC 1.8",
        "Vref vref 0 DC 0.5",
        "RsumP vdd bus_p 10k",
        "RsumN vdd bus_n 10k"
    ]

    for i in range(9):
        # Normalizare intrare
        vin = 0.4 + (pixels[i] - 0.5) * 0.4
        itail = abs(weights[i]) * 100e-6
        p, n = ("bus_p", "bus_n") if weights[i] >= 0 else ("bus_n", "bus_p")

        netlist.append(f"V{i} in{i} 0 DC {vin}")
        netlist.append(f"It{i} tail{i} 0 DC {itail}")
        netlist.append(f"M1_{i} {p} in{i} tail{i} 0 NMOS W=5u L=0.18u")
        netlist.append(f"M2_{i} {n} vref   tail{i} 0 NMOS W=5u L=0.18u")

    # Forțăm scrierea în rezultat.txt
    netlist.extend([
        ".op",
        ".control",
        "run",
        "let rez = (v(vdd)-v(bus_p))-(v(vdd)-v(bus_n))",
        "print rez > rezultat.txt",
        "quit",
        ".endc",
        ".end"
    ])

    with open(TEMP_SP, "w") as f:
        f.write("\n".join(netlist))

    # Rulăm fără captură, deoarece scriem direct în fișier
    subprocess.run([NGSPICE_CMD, "-b", TEMP_SP], capture_output=True)

    # Citim rezultatul proaspăt din fișier
    if os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, "r") as f:
            for line in f:
                if "rez" in line:
                    try:
                        return float(line.split("=")[-1].strip())
                    except:
                        continue
    return 0.0


# --- PROCESARE ---
if not os.path.exists(IMAGE_FILE):
    print(f"EROARE: Nu gasesc imaginea {IMAGE_FILE}!")
    exit()

img = Image.open(IMAGE_FILE).convert('L').resize((30, 30))
data = np.array(img) / 255.0
h, w = data.shape
res_img = np.zeros((h - 2, w - 2))
kernel = np.array([0, -1, 0, -1, 4, -1, 0, -1, 0])

print("Testam prima simulare...")
test_val = run_spice_sim(data[0:3, 0:3].flatten(), kernel)
print(f"Valoare detectata la prima iteratie: {test_val}")

for y in range(1, h - 1):
    for x in range(1, w - 1):
        window = data[y - 1:y + 2, x - 1:x + 2].flatten()
        res_img[y - 1, x - 1] = abs(run_spice_sim(window, kernel))
    print(f"Progres: {int(y / (h - 2) * 100)}%")

# Normalizare pentru vizualizare
if np.max(res_img) > 0:
    res_img = res_img / np.max(res_img)

plt.imshow(res_img, cmap='magma')
plt.colorbar(label="Intensitate contur (normalizata)")
plt.title("Procesare imagine prin circuit analogic")
plt.show()