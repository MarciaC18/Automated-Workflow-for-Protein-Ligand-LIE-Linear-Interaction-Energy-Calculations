#!/usr/bin/env python3
"""
Author: Marcia Yineth Castillo Tarazona  
Date: 2025-06-25

Description:
This script analyzes absolute errors between predicted and experimental binding free energies (ΔG)
from LIE simulations, grouped by both replicas and poses. It calculates summary statistics and performs
Kruskal–Wallis H-tests to assess whether absolute errors vary significantly across replicas and poses.

Inputs:
- Data_RP_LIE.csv (columns required: Ligand, Replica, Pose, DG_calculated, DG_experimental, N_poses)

Outputs:
- summary_by_replica.csv: statistics per ligand and replica
- summary_by_pose.csv: statistics per ligand and pose
- kruskal_test_results_replicas.csv: Kruskal-Wallis result for replicas
- kruskal_test_results_poses.csv: Kruskal-Wallis result for poses
"""

import pandas as pd
import numpy as np
from scipy.stats import kruskal

# Load dataset
df = pd.read_csv('Data_RP_LIE.csv')

# Ensure numeric columns are properly typed (decimal point)
df['DG_calculated'] = pd.to_numeric(df['DG_calculated'], errors='coerce')
df['DG_experimental'] = pd.to_numeric(df['DG_experimental'], errors='coerce')

# Drop rows with missing ΔG values
df = df.dropna(subset=['DG_calculated', 'DG_experimental'])

# Compute absolute error
df['abs_error'] = (df['DG_calculated'] - df['DG_experimental']).abs()

# === Summary by replica ===
summary_replica = df.groupby(['Ligand', 'Replica']).agg(
    mean_DG_calculated=('DG_calculated', 'mean'),
    std_DG_calculated=('DG_calculated', 'std'),
    mean_abs_error=('abs_error', 'mean'),
    count=('DG_calculated', 'count')
).reset_index()

summary_replica.to_csv('summary_by_replica.csv', index=False)
print("Saved 'summary_by_replica.csv'.")

# Kruskal-Wallis test by replica
replicas = sorted(df['Replica'].unique())
errors_by_replica = [df[df['Replica'] == r]['abs_error'].values for r in replicas]
H_replica, p_replica = kruskal(*errors_by_replica)

print(f"Kruskal–Wallis test on absolute error across replicas: H = {H_replica:.3f}, p = {p_replica:.3e}")

pd.DataFrame({
    'Test': ['Kruskal-Wallis H-test (Replicas)'],
    'H_statistic': [H_replica],
    'p_value': [p_replica]
}).to_csv('kruskal_test_results_replicas.csv', index=False)
print("Saved 'kruskal_test_results_replicas.csv'.")

# === Summary by pose ===
summary_pose = df.groupby(['Ligand', 'Pose']).agg(
    mean_DG_calculated=('DG_calculated', 'mean'),
    std_DG_calculated=('DG_calculated', 'std'),
    mean_abs_error=('abs_error', 'mean'),
    count=('DG_calculated', 'count')
).reset_index()

summary_pose.to_csv('summary_by_pose.csv', index=False)
print("Saved 'summary_by_pose.csv'.")

# Kruskal-Wallis test by pose
poses = sorted(df['Pose'].unique())
errors_by_pose = [df[df['Pose'] == p]['abs_error'].values for p in poses]
H_pose, p_pose = kruskal(*errors_by_pose)

print(f"Kruskal–Wallis test on absolute error across poses: H = {H_pose:.3f}, p = {p_pose:.3e}")

pd.DataFrame({
    'Test': ['Kruskal-Wallis H-test (Poses)'],
    'H_statistic': [H_pose],
    'p_value': [p_pose]
}).to_csv('kruskal_test_results_poses.csv', index=False)
print("Saved 'kruskal_test_results_poses.csv'.")

