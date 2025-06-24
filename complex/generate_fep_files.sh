#!/bin/bash

for i in {1..38}; do
    pdb_file="complex_${i}_w.pdb"
    fep_file="${i}.fep"

    # Extract atom numbers of ligand atoms (assuming column 4 in PDB is residue name 'LIG' and column 2 is atom number)
    atom_numbers=($(awk '$0 ~ /^ATOM/ && $4 == "LIG" {print $2}' "$pdb_file"))

    echo "[FEP]" > "$fep_file"
    echo "states 1" >> "$fep_file"
    echo "[atoms]" >> "$fep_file"

    count=1
    for atom_num in "${atom_numbers[@]}"; do
        echo "$count $atom_num" >> "$fep_file"
        ((count++))
    done

    echo "Generated $fep_file with ${#atom_numbers[@]} atoms from $pdb_file"
done

