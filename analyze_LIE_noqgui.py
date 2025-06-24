import os
import argparse
import numpy as np
import mdlog_energies as mdle  # Asegúrate que mdlog_energies.py esté en el mismo directorio
import csv

def get_logfiles(path):
    logfiles = []
    subdirs = sorted([os.path.join(path, d) for d in os.listdir(path)
                      if os.path.isdir(os.path.join(path, d))])
    for subdir in subdirs:
        for file in os.listdir(subdir):
            if file.endswith('.log'):
                logfiles.append(os.path.join(subdir, file))
    return logfiles

def main(ligand_dir, complex_dir, alpha, beta, gamma, output_file, ligand_name, dg_exp):

    ligand_logs = get_logfiles(ligand_dir)
    complex_logs = get_logfiles(complex_dir)

    if not ligand_logs or not complex_logs:
        print("❌ No se encontraron archivos .log en ligand o complex.")
        return

    lig_qene, lig_ave, lig_stderr = mdle.get_q_energies(ligand_logs)
    comp_qene, comp_ave, comp_stderr = mdle.get_q_energies(complex_logs)

    # Imprimir valores para depuración
    print("Ligand EL_w:", lig_ave[2][0], "VDW_w:", lig_ave[2][1])
    print("Complex EL_w:", comp_ave[2][0], "VDW_w:", comp_ave[2][1])
    print("Complex EL_p:", comp_ave[1][0], "VDW_p:", comp_ave[1][1])

    dg = (beta * ((comp_ave[2][0] + comp_ave[1][0]) - lig_ave[2][0]) +
          (alpha * ((comp_ave[2][1] + comp_ave[1][1]) - lig_ave[2][1])) + gamma)

    dg_stderr = np.sqrt(beta**2 * (lig_stderr[2][0]**2 + comp_stderr[2][0]**2 + comp_stderr[1][0]**2) +
                        alpha**2 * (lig_stderr[2][1]**2 + comp_stderr[2][1]**2 + comp_stderr[1][1]**2))

    print(f"✅ LIGAND: {ligand_name}")
    print(f"ΔG = {dg:.2f} ± {dg_stderr:.2f} kcal/mol")

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ligand_name', 'alpha', 'beta', 'gamma', 'dG_calc', 'stderr', 'dG_exp'])
        writer.writerow([ligand_name, alpha, beta, gamma, round(dg, 2), round(dg_stderr, 2), dg_exp])

    print(f"✅ Resultados guardados en: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Análisis LIE sin GUI")
    parser.add_argument("--ligand_dir", default="ligand", help="Ruta al directorio de ligando")
    parser.add_argument("--complex_dir", default="complex", help="Ruta al directorio de complejo")
    parser.add_argument("--alpha", type=float, default=0.18, help="Valor de α")
    parser.add_argument("--beta", type=float, default=0.50, help="Valor de β")
    parser.add_argument("--gamma", type=float, default=0.00, help="Valor de γ")
    parser.add_argument("--output", default="LIE_results.csv", help="Nombre del archivo de salida CSV")
    parser.add_argument("--ligand_name", default="LIG", help="Nombre del ligando")
    parser.add_argument("--dg_exp", type=float, default=0.0, help="Valor experimental de ΔG")

    args = parser.parse_args()
    main(args.ligand_dir, args.complex_dir, args.alpha, args.beta, args.gamma,
         args.output, args.ligand_name, args.dg_exp)