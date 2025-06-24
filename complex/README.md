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
## Module 2 - Equilibration

### Objective
This module performs the equilibration phase for each protein–ligand complex prior to LIE (Linear Interaction Energy) simulations. It uses topology and FEP files generated in **Module 1** and produces restart (`.re`) files needed for production simulations in the next module.

---

### Inputs

The following **base input files must be available** (included in this repository):

- `eq1.inp` — minimization
- `eq2.inp` — heating
- `eq3.inp` — equilibration

Also required from **Module 1**:

- `complex_#_w.top`
- `#.fep`

Here, `#` refers to the ligand number (e.g., `1`, `2`, etc.).

---

### Workflow 
### 1. Generate equilibration input files

Run:

```bash
sbatch generate_eq_inp.sh
```
This script uses the base input files (`eq1.inp`, `eq2.inp`, `eq3.inp`) to generate individual input files for each protein–ligand complex.  
If you need to change any equilibration parameter (e.g., time, temperature, restraints), modify the base `.inp` files before running the script.

### Outputs:
- `eq1_#.inp`
- `eq2_#.inp`
- `eq3_#.inp`

Each file corresponds to a specific stage in the equilibration process for complex `#`.

---

### 2.Run the equilibration

Submit all equilibration stages for each complex using:

```bash
sbatch equilibration.sh
```
### Inputs:
- `eq1_#.inp`
- `eq2_#.inp`
- `eq3_#.inp`

### Outputs:
- `eq1_#.re`, `eq1_#.log`
- `eq2_#.re`, `eq2_#.log`
- `eq3_#.re`, `eq3_#.log`

Each `.re` file is a **restart file** used to continue the simulation in the next stage,  
while `.log` files contain runtime information.

---

### Equilibration Stages Overview

| Stage | Description                          | Typical Duration |
|-------|--------------------------------------|------------------|
| eq1   | Energy minimization                  | 5 ps             |
| eq2   | Heating (0 K → target temperature)   | 10 ps            |
| eq3   | Constant temperature equilibration   | 25 ps            |

> You can adjust simulation durations and other parameters by editing `eq1.inp`, `eq2.inp`, and `eq3.inp` before running the workflow.




