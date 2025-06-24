# -*- coding: utf-8 -*-
"""
This script concatenates a common protein structure (protein.pdb) 
with the ligand residue LIG from each ligand PDB file (../1.ligprep/#_w.pdb).

For each ligand from 1 to 38, it writes the combined PDB file 
(protein + LIG) as protein-L#.pdb in the current directory.

A 'TER' line is added between the protein and ligand residues.

To use this with more or fewer ligands, just change the value of `num_ligands`.

Author: Marcia C
"""

import os

# Change this to match the number of ligands you have
num_ligands = 38

# Protein file
protein_file = "protein.pdb"

# Read the protein structure once
with open(protein_file, "r") as f:
    protein_lines = [line for line in f if line.startswith(("ATOM", "HETATM"))]

# Process each ligand
for i in range(1, num_ligands + 1):
    ligand_file = f"../1.ligprep/{i}_w.pdb"
    output_file = f"protein-L{i}.pdb"

    if not os.path.isfile(ligand_file):
        print(f"⚠️  File not found: {ligand_file} — skipping ligand {i}")
        continue

    # Extract only LIG atoms from the ligand PDB
    with open(ligand_file, "r") as f:
        lig_lines = [line for line in f if line.startswith(("ATOM", "HETATM")) and " LIG " in line]

    # Write the combined protein-ligand structure with TER separator
    with open(output_file, "w") as f:
        f.writelines(protein_lines)
        f.write("TER\n")  # Separator between protein and ligand
        f.writelines(lig_lines)
        f.write("END\n")

    print(f"✅ Created: {output_file}")
