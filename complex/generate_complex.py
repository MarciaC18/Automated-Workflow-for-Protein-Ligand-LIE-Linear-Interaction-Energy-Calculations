# -*- coding: utf-8 -*-
"""
Generates 38 input files named generate_complex_#.inp
with the commented lines replaced by the corresponding
ligand number from 1 to 38.

Each file corresponds to the ligand number and updates
the relevant lines accordingly.

Autor Marcia C
"""

template = """rl  ../1.ligprep/OPLS2005.lib
rl   ../1.ligprep/{lig_num}.lib

#Read the parameter 
rff ../1.ligprep/OPLS2005_{lig_num}_all.prm
#Read the starting, usually precleaned pdb file.
rp  protein-L{lig_num}.pdb

ls
lr 1
preferences

#you need to create the sulfur-sulfur bridges.
#addbond atomnum atomnum y

#Create water sphere
boundary sphere 79:CB 30
solvate 79:CB 30 1 HOH

mt complex_{lig_num}_w
wt complex_{lig_num}_w.top

#checkbonds 6
#checkangs  6
#checktors  6
#checkimps  6

wp complex_{lig_num}_w.pdb y
quit
"""

for lig_num in range(1, 39):
    filename = f"generate_complex_{lig_num}.inp"
    with open(filename, "w") as f:
        f.write(template.format(lig_num=lig_num))
    print(f"Created {filename}")

