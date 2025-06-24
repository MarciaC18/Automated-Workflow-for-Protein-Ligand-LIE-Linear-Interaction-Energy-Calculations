"""
This script generates input files for molecular dynamics production runs,
based on two template files: 'production.inp' and 'production2.inp'.

For each ligand number from 1 to N (configurable), it creates customized input
files named:
  - production1_#.inp from production.inp
  - production2_#.inp from production2.inp

The script replaces all instances of placeholder names (like 'complexdiz_w.top')
with names that include the specific ligand number (e.g., 'complex_1_w.top').

This is useful for automating the setup of multiple simulations with different ligands.

You can change the number of ligands below to fit your case.
"""

import os

# === CONFIGURATION ===
# Change this to the total number of ligands you want to process
total_ligands = 38  # <-- Change this if needed
ligands = range(1, total_ligands + 1)

# === FUNCTION TO GENERATE INPUT FILES ===
def generate_inp(template_file, output_prefix, ligand_number):
    with open(template_file, 'r') as f:
        content = f.read()

    # Dictionary of text replacements based on ligand number
    replacements = {
        'complexdiz_w.top': f'complex_{ligand_number}_w.top',
        'eqdiz3.re': f'eq3_{ligand_number}.re',
        'prod1_complexdiz.re': f'prod1_complex_{ligand_number}.re',
        'prod2_complexdiz.re': f'prod2_complex_{ligand_number}.re',
        'diz.fep': f'{ligand_number}.fep',
        'prod1_complexdiz.dcd': f'prod1_complex_{ligand_number}.dcd',
        'prod2_complexdiz.dcd': f'prod2_complex_{ligand_number}.dcd',
        'prod1_complexdiz.en': f'prod1_complex_{ligand_number}.en',
        'prod2_complexdiz.en': f'prod2_complex_{ligand_number}.en',
    }

    # Apply replacements
    for original, new in replacements.items():
        content = content.replace(original, new)

    # Save new file
    output_filename = f'{output_prefix}_{ligand_number}.inp'
    with open(output_filename, 'w') as f:
        f.write(content)
    print(f"Generated: {output_filename}")

# === MAIN LOOP TO PROCESS ALL LIGANDS ===
for ligand in ligands:
    generate_inp('production.inp', 'production1', ligand)
    generate_inp('production2.inp', 'production2', ligand)

