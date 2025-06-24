# Module 1 - Complex Preparation

## Objective
Generate the `complex_#.top` file for LIE (Linear Interaction Energy) calculations using Q6.

---

## Requirements
- [Q6](https://github.com/qusers/Q6/tree/master)
- [QLigFEP](https://github.com/qusers/qligfep/tree/master)
- Python (for the helper scripts)

---

## Inputs

1. **Protein.pdb**  
   Preprocessed protein structure (no water or ligands), generated using Schrodinger’s Protein Preparation Wizard.

2. **../ligands/#_w.pdb**  
   The ligand structure from the ligprep module. Only the atoms of the `LIG` residue will be used.

3. **../ligands/OPLS2005.lib**  
   Force field library (same as used in ligands module).

4. **../ligands/OPLS2005_#_all.prm**  
   Parameter file for each ligand.

---

## Workflow

### 1. Concatenate Protein and Ligand

Use the script to combine `Protein.pdb` with `#_w.pdb`:

```bash
python concat_protein_ligands.py
```

Output:
- `protein-L#.pdb`  
  Combined protein-ligand structure, with ligand atoms from `LIG` residue only, ending in `END`.

---

### 2. Generate Q6 Input File

Generate the Q6 input file to prepare the complex:

```bash
python generate_complex.py
```

Output:
- `generate_complex_#.inp`  
  Q6 input file for the complex.

Note: You may modify the solvent and boundary residue/atom if needed inside the `generate_complex.py` file.

---

### 3. Prepare Complex with Q6

Run the preparation script:

```bash
bash prepared_complex.sh
```

Outputs:
- `generate_complex_#.log`  
- `complex_#_w.top`  
- `complex_#_w.pdb`  
- `complex_#_w.log`

---

### 4. Generate .fep File for LIE

Use your script to create the `.fep` file. No alchemical transformation is needed for LIE (states = 1):

```bash
sbatch generate_fep_files.sh
```

Input:
- `complex_#_w.pdb`

Output:
- `#.fep`  
  A two-column file:
  - Column 1: Atom indices of the `LIG` residue (starting from 1)
  - Column 2: Corresponding atom numbers in `complex_#_w.pdb`

The file should be named `#.fep` where `#` matches the complex number.

---

