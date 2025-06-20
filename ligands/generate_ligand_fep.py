import os

# Read the header of lig.fep up to [atoms]
with open("lig.fep", "r") as f:
    lines = f.readlines()

header = []
for i, line in enumerate(lines):
    header.append(line)
    if line.strip() == "[atoms]":
        break  # until the line '[atoms]' is found

# Process from 1 to 38
for i in range(1, 39):
    pdb_file = f"{i}_w.pdb"
    if not os.path.exists(pdb_file):
        print(f"{pdb_file} not found, skipping.")
        continue

    atom_lines = []
    atom_counter = 0

    with open(pdb_file, "r") as f:
        for line in f:
            if line.startswith(("ATOM", "HETATM")):
                residue_name = line[17:20].strip()
                if residue_name == "LIG":
                    atom_counter += 1
                    atom_lines.append(f"{atom_counter} {atom_counter}\n")

    if atom_lines:
        with open(f"{i}.fep", "w") as out:
            out.writelines(header)
            out.writelines(atom_lines)
        print(f"{i}.fep generated with {atom_counter} atoms.")
    else:
        print(f"No LIG atoms found in {pdb_file}.")
