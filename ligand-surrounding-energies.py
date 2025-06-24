"""
Script Usage Instructions:

- Place this script in the main project directory that contains the 'complex_#' folders.
  Each 'complex_#' folder should be inside a parent folder 'complex/', with subfolders '1' and '2' containing:
    complex/complex_#/1/production1_#.log
    complex/complex_#/2/production2_#.log

- Adjust the ligand range in the script (default is 1 to 38) if you have more or fewer ligands.

- Run the script using Python 3:
    python ligand-surrounding-energies.py

- The script will process all matching log files, extract energies, compute errors,
  and generate a combined energy plot saved as 'combined_energy_plot.png'.

Author: Marcia C
"""

import os
import matplotlib.pyplot as plt
import numpy as np

def extract_qsurr_energies(filename):
    vdws = []
    elecs = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith("Q-surr."):
                parts = line.split()
                if len(parts) >= 5:
                    elecs.append(float(parts[3]))
                    vdws.append(float(parts[4]))
    return np.array(elecs), np.array(vdws)

def compute_error_bind_separate(elecs, vdws):
    half = len(elecs) // 2
    el_b = np.mean(elecs[:half])
    el_f = np.mean(elecs[half:])
    vdW_b = np.mean(vdws[:half])
    vdW_f = np.mean(vdws[half:])
    error_vdw = abs(vdW_f - vdW_b) / 2
    error_el = abs(el_f - el_b) / 2
    return error_vdw, error_el, (el_b, el_f, vdW_b, vdW_f)

def plot_single_energy(log_file, elecs, vdws, error_vdw, error_el, el_b, el_f, vdW_b, vdW_f, total_steps, total_ps):
    plt.figure(figsize=(8, 5))
    step_interval = 50
    n_points = len(vdws)
    steps = np.arange(n_points) * step_interval
    ps = steps * (total_ps / total_steps)

    plt.plot(ps, vdws, label=f"vdW (b={vdW_b:.2f}, f={vdW_f:.2f}, err={error_vdw:.2f})", linestyle='-')
    plt.plot(ps, elecs, label=f"Electrostatic (b={el_b:.2f}, f={el_f:.2f}, err={error_el:.2f})", linestyle='--')

    plt.xlabel("Time (ps)")
    plt.ylabel("Energy (kcal/mol)")
    plt.title(f"Energies for {os.path.basename(log_file)}")
    plt.legend(fontsize=8)
    plt.tight_layout()

    os.makedirs("individual_plots", exist_ok=True)
    outname = os.path.join("individual_plots", os.path.basename(log_file).replace(".log", "_plot.png"))
    plt.savefig(outname, dpi=300)
    plt.close()

def main():
    ligand_numbers = range(1, 39)  # Adjust as needed
    total_steps = 20000
    total_ps = 20

    log_files = []
    for ligand in ligand_numbers:
        path1 = os.path.join("complex", f"complex_{ligand}", "1", f"production1_{ligand}.log")
        path2 = os.path.join("complex", f"complex_{ligand}", "2", f"production2_{ligand}.log")
        if os.path.isfile(path1):
            log_files.append(path1)
        if os.path.isfile(path2):
            log_files.append(path2)

    if not log_files:
        print("No .log files found in the specified directories.")
        return

    elec_data = {}
    vdw_data = {}

    errors_vdw = []
    errors_el = []
    vdws_bounds = []
    els_bounds = []

    print("\n--- Energy Extraction and Binding Error Calculation ---\n")

    for log_file in log_files:
        elecs, vdws = extract_qsurr_energies(log_file)
        if len(elecs) == 0 or len(vdws) == 0:
            print(f"{log_file}: No Q-surr energies found.")
            continue

        error_vdw, error_el, (el_b, el_f, vdW_b, vdW_f) = compute_error_bind_separate(elecs, vdws)

        print(f"{log_file}")
        print(f"  vdW_b = {vdW_b:.2f}, vdW_f = {vdW_f:.2f}")
        print(f"  el_b  = {el_b:.2f}, el_f  = {el_f:.2f}")
        print(f"  Error vdW = {error_vdw:.2f}")
        print(f"  Error Electrostatic = {error_el:.2f}\n")

        elec_data[log_file] = elecs
        vdw_data[log_file] = vdws
        errors_vdw.append(error_vdw)
        errors_el.append(error_el)
        vdws_bounds.append((vdW_b, vdW_f))
        els_bounds.append((el_b, el_f))

        # Individual plot
        plot_single_energy(log_file, elecs, vdws, error_vdw, error_el, el_b, el_f, vdW_b, vdW_f, total_steps, total_ps)

    # Optionally: combined plot
    # plot_energies_together(vdw_data, elec_data, errors_vdw, errors_el, vdws_bounds, els_bounds, total_steps, total_ps, "combined_energy_plot.png")

if __name__ == "__main__":
    main()
