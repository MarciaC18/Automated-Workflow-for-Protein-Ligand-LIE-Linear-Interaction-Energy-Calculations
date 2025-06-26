import os
import argparse
import numpy as np
import mdlog_energies as mdle
import csv

def get_logfiles(path, n_replicas):
    """Obtiene archivos .log de las primeras n_replicas subcarpetas."""
    logfiles = []
    subdirs = sorted([os.path.join(path, d) for d in os.listdir(path)
                      if os.path.isdir(os.path.join(path, d))])[:n_replicas]
    for subdir in subdirs:
        for file in os.listdir(subdir):
            if file.endswith('.log'):
                logfiles.append(os.path.join(subdir, file))
    return logfiles

def get_pose_dirs(path):
    """Devuelve todas las subcarpetas (poses) en el directorio dado."""
    return sorted([os.path.join(path, d) for d in os.listdir(path)
                   if os.path.isdir(os.path.join(path, d))])

def main(ligand_dir, complex_dir, alpha, beta, gamma, output_file, ligand_name, dg_exp, n_replicas):
    ligand_poses = get_pose_dirs(ligand_dir)
    complex_poses = get_pose_dirs(complex_dir)

    if not ligand_poses or not complex_poses:
        print("❌ No se encontraron carpetas de poses en ligand o complex.")
        return

    if len(ligand_poses) != len(complex_poses):
        print("❌ El número de poses no coincide entre ligand y complex.")
        return

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ligand_name', 'pose', 'alpha', 'beta', 'gamma', 'dG_calc', 'stderr', 'dG_exp'])

        for i, (lig_pose, comp_pose) in enumerate(zip(ligand_poses, complex_poses), start=1):
            ligand_logs = get_logfiles(lig_pose, n_replicas)
            complex_logs = get_logfiles(comp_pose, n_replicas)

            if not ligand_logs or not complex_logs:
                print(f"❌ Pose {i}: No se encontraron archivos .log suficientes.")
                continue

            lig_qene, lig_ave, lig_stderr = mdle.get_q_energies(ligand_logs)
            comp_qene, comp_ave, comp_stderr = mdle.get_q_energies(complex_logs)

            print(f"\n📌 Pose {i}")
            print("Ligand EL_w:", lig_ave[2][0], "VDW_w:", lig_ave[2][1])
            print("Complex EL_w:", comp_ave[2][0], "VDW_w:", comp_ave[2][1])
            print("Complex EL_p:", comp_ave[1][0], "VDW_p:", comp_ave[1][1])

            dg = (beta * ((comp_ave[2][0] + comp_ave[1][0]) - lig_ave[2][0]) +
                  (alpha * ((comp_ave[2][1] + comp_ave[1][1]) - lig_ave[2][1])) + gamma)

            dg_stderr = np.sqrt(beta**2 * (lig_stderr[2][0]**2 + comp_stderr[2][0]**2 + comp_stderr[1][0]**2) +
                                alpha**2 * (lig_stderr[2][1]**2 + comp_stderr[2][1]**2 + comp_stderr[1][1]**2))

            print(f"✅ ΔG = {dg:.2f} ± {dg_stderr:.2f} kcal/mol")

            writer.writerow([ligand_name, i, alpha, beta, gamma, round(dg, 2), round(dg_stderr, 2), dg_exp])

    print(f"\n✅ Resultados guardados en: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Análisis LIE por múltiples poses sin GUI")
    parser.add_argument("--ligand_dir", default="ligand", help="Ruta al directorio con carpetas por pose del ligando")
    parser.add_argument("--complex_dir", default="complex", help="Ruta al directorio con carpetas por pose del complejo")
    parser.add_argument("--alpha", type=float, default=0.18, help="Valor de α")
    parser.add_argument("--beta", type=float, default=0.50, help="Valor de β")
    parser.add_argument("--gamma", type=float, default=0.00, help="Valor de γ")
    parser.add_argument("--output", default="LIE_results.csv", help="Nombre del archivo de salida CSV")
    parser.add_argument("--ligand_name", default="LIG", help="Nombre del ligando")
    parser.add_argument("--dg_exp", type=float, default=0.0, help="Valor experimental de ΔG")
    parser.add_argument("--n_replicas", type=int, default=3, help="Número de réplicas a analizar por pose")

    args = parser.parse_args()

    main(args.ligand_dir, args.complex_dir, args.alpha, args.beta, args.gamma,
         args.output, args.ligand_name, args.dg_exp, args.n_replicas)

