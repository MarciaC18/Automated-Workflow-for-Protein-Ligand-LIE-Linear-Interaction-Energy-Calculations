#!/usr/bin/env python3
"""
combine_LIE_results.py

Author: Your Name
Date: 2025-06-25
Description:
    This script loads individual LIE (Linear Interaction Energy) calculation results
    from CSV files corresponding to different poses and replicas, standardizes and
    combines them into a single CSV file for further analysis.

    Each input CSV is expected to be named in the format:
        results_LIE-pose{pose}-r{replica}.csv

    The output CSV will include columns for ligand name, replica number, pose number,
    calculated binding free energy (DG_calculated), experimental binding free energy
    (DG_experimental, which can be manually assigned later), and the total number of
    entries per file (N_poses).

Usage:
    python combine_LIE_results.py -p 1 2 -r 1 2 -o combined_results.csv

"""

import os
import argparse
import pandas as pd

def load_results(pose, replica, root_dir='.'):
    """
    Load and process a single LIE results CSV file for a given pose and replica.

    Parameters:
        pose (int): Pose number.
        replica (int): Replica number.
        root_dir (str): Directory where CSV files are stored.

    Returns:
        pd.DataFrame: DataFrame with standardized and selected columns.

    Raises:
        FileNotFoundError: If the expected CSV file does not exist.
    """
    filename = f"results_LIE-pose{pose}-r{replica}.csv"
    filepath = os.path.join(root_dir, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    df = pd.read_csv(filepath)
    
    # Rename columns for standardization
    df.rename(columns={
        'ligand_name': 'Ligand',
        'dG_calc': 'DG_calculated',
        # 'dG_exp' may be missing and can be filled manually later
    }, inplace=True)
    
    # Add columns for pose and replica identifiers
    df['Pose'] = pose
    df['Replica'] = replica

    # Add empty experimental DG column if not present
    if 'DG_experimental' not in df.columns:
        df['DG_experimental'] = pd.NA

    # Add column with total number of entries in this file
    df['N_poses'] = len(df)
    
    # Return only relevant columns for final output
    return df[['Ligand', 'Replica', 'Pose', 'DG_calculated', 'DG_experimental', 'N_poses']]

def main(poses, replicas, output_csv='Data_RP_LIE.csv', root_dir='.'):
    """
    Combine LIE results for specified poses and replicas into one CSV file.

    Parameters:
        poses (list of int): List of pose numbers to process.
        replicas (list of int): List of replica numbers to process.
        output_csv (str): Filename for the combined output CSV.
        root_dir (str): Directory where input CSV files are located.
    """
    combined_df = pd.DataFrame()
    for pose in poses:
        for replica in replicas:
            try:
                df = load_results(pose, replica, root_dir)
                combined_df = pd.concat([combined_df, df], ignore_index=True)
                print(f"Loaded pose {pose} replica {replica} with {len(df)} entries.")
            except FileNotFoundError as e:
                print(e)

    # Example: manually assign experimental DG values if desired
    # combined_df.loc[combined_df['Ligand'] == 'lig1', 'DG_experimental'] = -7.5

    combined_df.to_csv(output_csv, index=False)
    print(f"Combined CSV saved as {output_csv}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Combine LIE results into a single CSV file")
    parser.add_argument('-p', '--poses', type=int, nargs='+', required=True,
                        help='List of pose numbers to process, e.g. 1 2 3')
    parser.add_argument('-r', '--replicas', type=int, nargs='+', required=True,
                        help='List of replica numbers to process, e.g. 1 2')
    parser.add_argument('-o', '--output', type=str, default='Data_RP_LIE.csv',
                        help='Output CSV filename')
    args = parser.parse_args()

    main(args.poses, args.replicas, args.output)
