"""
LIE Analysis Script for Multiple Poses and Replicas (No GUI)

Description:
------------
This script performs Linear Interaction Energy (LIE) calculations for molecular dynamics
simulation results of ligands and their complexes. It processes multiple poses and replicas,
extracting energies from log files, calculating binding free energies (ΔG) using the
LIE method, and saving the results in CSV files for each pose and replica.

The LIE equation used is:
    ΔG = β * ((EL_w_complex + EL_p_complex) - EL_w_ligand) + α * ((VDW_w_complex + VDW_p_complex) - VDW_w_ligand) + γ

Where:
- EL_w and VDW_w correspond to electrostatic and van der Waals interaction energies of the ligand in water.
- EL_p and VDW_p correspond to the same energies for the protein complex.
- α, β, and γ are empirical parameters.

Inputs:
-------
- Directories containing pose subfolders for ligand and complex.
- Number of replicas per pose.
- LIE parameters α, β, γ.
- Experimental ΔG value for comparison.
- Optional number of poses to analyze.

Outputs:
--------
- CSV files with calculated ΔG and error estimates per pose and replica.

Author:
--------
Marcia C

Date:
------
2025-06-25
"""

import argparse
import csv
import os
import numpy as np
import mdlog_energies as mdle  # Assumed to be available in your environment

def get_pose_dirs(path):
    """
    Retrieve all subdirectories representing poses within the given directory.

    Parameters:
    -----------
    path : str
        Path to the parent directory containing pose subfolders.

    Returns:
    --------
    list of str
        Sorted list of full paths to each pose directory.
    """
    return sorted([os.path.join(path, d) for d in os.listdir(path)
                   if os.path.isdir(os.path.join(path, d))])

def get_logfiles(pose_dir, n_replicas):
    """
    Find log files within replica subdirectories of a pose directory.

    Parameters:
    -----------
    pose_dir : str
        Path to the pose directory containing replica subfolders.
    n_replicas : int
        Expected number of replica folders.

    Returns:
    --------
    list of str
        List of paths to the .log files found in each replica directory.
        Returns an empty list if any expected log file is missing.
    """
    replica_dirs = sorted([os.path.join(pose_dir, d) for d in os.listdir(pose_dir)
                           if os.path.isdir(os.path.join(pose_dir, d))])
    
    if len(replica_dirs) < n_replicas:
        print(f"❌ Not enough replica folders found in {pose_dir} "
              f"(expected {n_replicas}, found {len(replica_dirs)})")
        return []
    
    logfiles = []
    for i in range(n_replicas):
        replica_dir = replica_dirs[i]
        logs = [os.path.join(replica_dir, f) for f in os.listdir(replica_dir) if f.endswith('.log')]
        if not logs:
            print(f"❌ No .log file found in replica directory {replica_dir}")
            return []
        logfiles.append(logs[0])  # Take the first .log file found
    
    return logfiles

def main(ligand_dir, complex_dir, alpha, beta, gamma, output_file, ligand_name, dg_exp, n_replicas, n_poses=None):
    """
    Main function to run the LIE analysis on all poses and replicas.

    Parameters:
    -----------
    ligand_dir : str
        Directory containing ligand pose subfolders.
    complex_dir : str
        Directory containing complex pose subfolders.
    alpha : float
        LIE alpha parameter.
    beta : float
        LIE beta parameter.
    gamma : float
        LIE gamma parameter.
    output_file : str
        Output CSV filename (not used in this version).
    ligand_name : str
        Name identifier for the ligand.
    dg_exp : float
        Experimental ΔG value for comparison.
    n_replicas : int
        Number of replicas to process for each pose.
    n_poses : int or None
        Number of poses to analyze (defaults to all if None).
    """
    ligand_poses = get_pose_dirs(ligand_dir)
    complex_poses = get_pose_dirs(complex_dir)

    if not ligand_poses or not complex_poses:
        print("❌ No pose directories found in ligand or complex folders.")
        return

    if len(ligand_poses) != len(complex_poses):
        print("❌ Number of poses does not match between ligand and complex directories.")
        return

    if n_poses is not None:
        ligand_poses = ligand_poses[:n_poses]
        complex_poses = complex_poses[:n_poses]

    for i, (lig_pose, comp_pose) in enumerate(zip(ligand_poses, complex_poses), start=1):
        ligand_logs = get_logfiles(lig_pose, n_replicas)
        complex_logs = get_logfiles(comp_pose, n_replicas)

        if not ligand_logs or not complex_logs:
            print(f"❌ Pose {i}: Insufficient .log files found, skipping.")
            continue

        for r in range(n_replicas):
            output_file_pose_replica = f"results_LIE-pose{i}-r{r+1}.csv"

            with open(output_file_pose_replica, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['ligand_name', 'pose', 'replica', 'alpha', 'beta', 'gamma', 'dG_calc', 'stderr', 'dG_exp'])

                lig_qene, lig_ave, lig_stderr = mdle.get_q_energies([ligand_logs[r]])
                comp_qene, comp_ave, comp_stderr = mdle.get_q_energies([complex_logs[r]])

                print(f"\n📌 Pose {i} replica {r+1}")
                print(f"Ligand EL_w: {lig_ave[2][0]}, VDW_w: {lig_ave[2][1]}")
                print(f"Complex EL_w: {comp_ave[2][0]}, VDW_w: {comp_ave[2][1]}")
                print(f"Complex EL_p: {comp_ave[1][0]}, VDW_p: {comp_ave[1][1]}")

                dg = (beta * ((comp_ave[2][0] + comp_ave[1][0]) - lig_ave[2][0]) +
                      alpha * ((comp_ave[2][1] + comp_ave[1][1]) - lig_ave[2][1]) +
                      gamma)

                dg_stderr = np.sqrt(beta**2 * (lig_stderr[2][0]**2 + comp_stderr[2][0]**2 + comp_stderr[1][0]**2) +
                                    alpha**2 * (lig_stderr[2][1]**2 + comp_stderr[2][1]**2 + comp_stderr[1][1]**2))

                print(f"✅ ΔG = {dg:.2f} ± {dg_stderr:.2f} kcal/mol")

                writer.writerow([ligand_name, i, r+1, alpha, beta, gamma, round(dg, 2), round(dg_stderr, 2), dg_exp])

    print(f"\n✅ Results saved in separate CSV files per pose and replica.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LIE analysis for multiple poses and replicas without GUI")
    parser.add_argument("--ligand_dir", default="ligand", help="Directory with ligand pose subfolders")
    parser.add_argument("--complex_dir", default="complex", help="Directory with complex pose subfolders")
    parser.add_argument("--alpha", type=float, default=0.18, help="Alpha parameter")
    parser.add_argument("--beta", type=float, default=0.50, help="Beta parameter")
    parser.add_argument("--gamma", type=float, default=0.00, help="Gamma parameter")
    parser.add_argument("--output", default="LIE_results.csv", help="Output CSV file (not used in this version)")
    parser.add_argument("--ligand_name", default="LIG", help="Ligand name identifier")
    parser.add_argument("--dg_exp", type=float, default=0.0, help="Experimental ΔG value")
    parser.add_argument("--n_replicas", type=int, default=3, help="Number of replicas per pose")
    parser.add_argument("--n_poses", type=int, default=None, help="Number of poses to analyze (default: all)")

    args = parser.parse_args()

    main(args.ligand_dir, args.complex_dir, args.alpha, args.beta, args.gamma,
         args.output, args.ligand_name, args.dg_exp, args.n_replicas, args.n_poses)
