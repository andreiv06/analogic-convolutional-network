import numpy as np
import subprocess
import matplotlib.pyplot as plt
import os

# --- CONFIGURARE ---
NGSPICE_CMD = "ngspice"
MODEL_FILE = "model_mos.lib"
TEMP_SP = "sim_full_range.sp"
DATA_ID_VGS = "id_vgs_data.txt"
DATA_ID_ITAIL = "id_itail_data.txt"


def run_spice(netlist, output_file):
    if os.path.exists(output_file):
        os.remove(output_file)
    with open(TEMP_SP, "w") as f:
        f.write("\n".join(netlist))
    subprocess.run([NGSPICE_CMD, "-b", TEMP_SP], capture_output=True)
    if os.path.exists(output_file):
        return np.loadtxt(output_file)
    return None


# --- 1. SIMULARE: Id vs Vgs (Tranzistor unic) ---
netlist_id_vgs = [
    f".include {MODEL_FILE}",
    "Vds d 0 DC 1.0",
    "Vgs g 0 DC 0.5",
    "M1 d g 0 0 NMOS W=5u L=0.18u",
    ".control",
    "dc Vgs 0 1.8 0.01",
    f"wrdata {DATA_ID_VGS} -i(Vds)",
    "quit",
    ".endc",
    ".end"
]

# --- 2. SIMULARE: Id vs Itail (Pereche diferențială) ---
# Fixăm Vin la 0.55V și Vref la 0.5V pentru a vedea cum un braț preia o parte din Itail
netlist_id_itail = [
    f".include {MODEL_FILE}",
    "Vdd vdd 0 DC 1.8",
    "Vref vref 0 DC 0.5",
    "Vin in 0 DC 0.55",
    "It tail 0 DC 1u",
    "M1 bus_p in   tail 0 NMOS W=5u L=0.18u",
    "M2 bus_n vref tail 0 NMOS W=5u L=0.18u",
    #"RloadP bus_p bus_p_1 1k",
    "VmeasP bus_p vdd DC 0", # Ampermetru pentru I_bus_plus
    ".control",
    "dc It 0 20u 20n",
    f"wrdata {DATA_ID_ITAIL} -i(VmeasP)",
    "quit",
    ".endc",
    ".end"
]

print("Simulăm caracteristicile...")
data_vgs = run_spice(netlist_id_vgs, DATA_ID_VGS)
data_itail = run_spice(netlist_id_itail, DATA_ID_ITAIL)

# --- PLOTARE ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: Id vs Vgs (Log)
if data_vgs is not None:
    ax1.semilogy(data_vgs[:, 0], data_vgs[:, 1], 'r-', linewidth=2)
    ax1.set_title(r'Caracteristica $I_d$ vs $V_{gs}$ (Scară Log)')
    ax1.set_xlabel(r'$V_{gs}$ (V)')
    ax1.set_ylabel(r'$I_d$ (A)')
    ax1.grid(True, which="both", alpha=0.3)

# Plot 2: Id vs Itail (Liniar)
if data_itail is not None:
    # data_itail are coloanele: [Itail, Id_M1, Itail, Id_M1_repeat...]
    ax2.plot(data_itail[:, 0] * 1e6, data_itail[:, 1] * 1e6, 'b-', linewidth=2)
    ax2.set_title(r'$I_{bus\_plus}$ vs $I_{tail}$ ($V_{in}=0.55V, V_{ref}=0.5V$)')
    ax2.set_xlabel(r'$I_{tail}$ (µA)')
    ax2.set_ylabel(r'$I_{d}$ (µA)')
    ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

for f in [TEMP_SP, DATA_ID_VGS, DATA_ID_ITAIL]:

    if os.path.exists(f): os.remove(f)
