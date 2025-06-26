import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

"""
Plot Calculated ΔG Values with Error Bars Highlighting Specific Ligands

Author: Marcia C
Date: 2025-06-23

Description:
------------
This script reads calculated binding free energy results (ΔG) with associated 
standard errors from multiple CSV files matching the pattern 'results/LIE_result_*.csv'. 
It then plots these ΔG values with error bars for all ligands.

Special attention is given to reference ligands identified by their names, 
which by default are 'ligand_1', 'ligand_2', and 'ligand_3'. These reference ligands 
are plotted in red at the beginning of the x-axis. Horizontal dashed red lines are 
drawn across the full width of the plot at the ΔG values of these reference ligands 
for easy visual comparison.

If additional reference ligands are present in the data (i.e., ligands matching the 
reference naming pattern), they will also be highlighted in red and included in the 
plot legend.

The x-axis shows ligand names ordered such that the reference ligands appear first 
and the rest follow sorted numerically based on the ligand number extracted from the 
ligand name.

Usage:
------
- Ensure all input CSV files are placed in the 'results' directory and follow the naming 
  convention 'LIE_result_#.csv', where # can be any number.
- Each CSV file must contain at least the following columns: 'ligand_name', 'dG_calc', 'stderr'.
- Run the script in an environment with pandas, matplotlib, numpy, and glob installed.
- The resulting plot is saved as 'results/LIE_dG_comparison_publication.png' with 300 dpi resolution.

This plot is suitable for publication-quality figures in journals like Biophysical 
Chemistry or ACS journals.

"""

def read_results(file_pattern):
    """
    Reads all CSV files matching the pattern and concatenates them into a single DataFrame.
    Expects columns: ligand_name, dG_calc, stderr.
    """
    files = sorted(glob.glob(file_pattern))
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        dfs.append(df[['ligand_name', 'dG_calc', 'stderr']])
    return pd.concat(dfs, ignore_index=True)

def ligand_num(ligand_name):
    """
    Extracts ligand number from ligand_name (e.g., 'ligand_12' -> 12).
    Returns a large number if no number found to push non-numbered ligands to the end.
    """
    m = re.search(r'ligand_(\d+)', ligand_name)
    return int(m.group(1)) if m else 9999

# Read all LIE result CSV files
results_df = read_results('results/LIE_result_*.csv')

# Define reference ligands based on ligand_name (e.g. ligand_1, ligand_2, ligand_3)
reference_ligands = {'ligand_1', 'ligand_2', 'ligand_3'}

# Check if there are more reference ligands in the data matching ligand_# pattern
refs_found = set(results_df['ligand_name']).intersection(reference_ligands)

# Identify all reference ligands present in the data
def is_reference_ligand(name):
    return name in refs_found

# Create columns to sort by:
# Reference ligands get priority (appear first), others sorted by ligand number ascending
results_df['is_ref'] = results_df['ligand_name'].apply(is_reference_ligand)
results_df['ligand_num'] = results_df['ligand_name'].apply(ligand_num)

# Separate reference and non-reference ligands
ref_df = results_df[results_df['is_ref']].copy()
other_df = results_df[~results_df['is_ref']].copy()

# Sort reference ligands by their ligand number (to keep order ligand_1, ligand_2, ligand_3 ...)
ref_df.sort_values('ligand_num', inplace=True)
ref_df.reset_index(drop=True, inplace=True)

# Sort other ligands by ligand number ascending
other_df.sort_values('ligand_num', inplace=True)
other_df.reset_index(drop=True, inplace=True)

# Combine for final plotting order: reference ligands first, then others
final_df = pd.concat([ref_df, other_df], ignore_index=True)

ligands = final_df['ligand_name'].values
dG_calc = final_df['dG_calc'].values
stderr = final_df['stderr'].values
x = np.arange(len(ligands))

# Color scheme: red for reference ligands, blue for others
colors = ['red' if is_reference_ligand(name) else 'blue' for name in ligands]

plt.figure(figsize=(14, 7))

# Plot each point with error bars
for xi, dg, err, c in zip(x, dG_calc, stderr, colors):
    plt.errorbar(xi, dg, yerr=err, fmt='o', color=c, capsize=5)

# Draw horizontal dashed red lines at ΔG of reference ligands
for xi, dg, c in zip(x, dG_calc, colors):
    if c == 'red':
        plt.axhline(y=dg, color='red', linestyle='--', alpha=0.7, xmin=0, xmax=1)

# Format x-axis
plt.xticks(x, ligands, rotation=45, ha='right')
plt.ylabel('ΔG (kcal/mol)')
plt.title(f'Calculated ΔG values with error bars\nRed reference ligands: {", ".join(sorted(refs_found))}')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# Ensure output directory exists
os.makedirs('results', exist_ok=True)

# Save figure
plt.savefig("results/LIE_dG_comparison.png", dpi=300)

# Show plot
plt.show()
