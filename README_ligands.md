# Module 1 – Ligand Preparation (LIE)

This module prepares ligands for LIE simulations by generating the necessary parameter and topology files for Q6 simulations.

## Input Files

- `L#.pdb`: PDB file for each ligand (where `#` is the ligand number). These files should come from crystallography or docking with prior preparation (e.g., using Schrödinger’s LigPrep).
- `OPLS2005_all.prm`: Base OPLS parameter file required to generate specific ligand parameters.
- `lig.fep`: Base file for Free Energy Perturbation (FEP).

## Scripts and Tools

- `generate_oplsa.py`: Script provided by QligFEP that must be pre-installed. It generates `.lib` and `.prm` files for each ligand.  
  - **Requires** Schrödinger software installed and the environment variable or path correctly set for its usage.
  - This script should be run from the corresponding ligand folder.
  - `#` represents the ligand number identifier, for example `1.pdb`, `2.pdb`, etc.
- `bind_prm.py`: Custom script that processes OPLS parameters to create `OPLSA_#_all.prm`.
- `copy_generate.py`: Script to copy and adapt input files with specific modifications for `boundary sphere` and `solvate` parameters for each ligand.
- `generate_ligand_fep.py`: Script to generate `.fep` files for FEP calculations.
- `prepared.sh`: Script to launch the preparation on the cluster using `sbatch`.

## Workflow

1. Prepare `#.pdb` files (where `#` is the ligand number).
2. Have the `OPLS2005_all.prm` file ready.
3. Run `generate_oplsa.py` to create `.lib` and `.prm` files.  
   **Note:** Requires Schrödinger installation and license.
4. Run `bind_prm.py` to generate `OPLSA_#_all.prm`.
5. Use `copy_generate.py` to adjust `boundary sphere` and `solvate` parameters for each ligand.
6. Run `prepared.sh` to execute the preparation for create #_w.top y #_w.pdb.
7. Generate `.fep` files using `generate_ligand_fep.py`.

## Important Notes

- Correct configuration of the Schrödinger path is necessary for `generate_oplsa.py` to work.
- `lig.fep` is the base file required for Free Energy Perturbation.
- `boundary sphere` and `solvate` parameters must be manually adjusted in `copy_generate.py` according to the characteristics of each ligand.
---

# Module 2 – Ligand Equilibration (LIE)

This module performs the equilibration phase for each ligand prior to LIE simulations. It uses topology and FEP files generated in Module 1. The protocol follows a 3-step equilibration based on the methodology described by Warshel, with a total equilibration time of 40 ps.

### Input Files

- `#_w.top`: Topology file for each ligand in water (output from Module 1).
- `#.fep`: FEP input file for each ligand.
- `inputs-equilibration.py`: Custom script to automatically generate equilibration input files:
  - `eq1.inp`: Minimization stage
  - `eq2.inp`: Heating stage
  - `eq3.inp`: Equilibration stage
- `equilibration.sh`: SLURM batch script to execute all three equilibration stages per ligand.

### Workflow

1. Make sure the files `#_w.top` and `#.fep` are present in each ligand folder (`1/`, `2/`, etc.).

2. Generate the equilibration input files in each folder:
   
   python inputs-equilibration.py This script will generate:
    - 'eq1.inp'
    -'eq2.inp'
    -'eq3.inp'

3. Submit the equilibration jobs for all ligands:
   sbatch equilibration.sh This script will generate:
   -'eq1_#.re': Restart file after minimization.
   -'eq2_#.re': Restart file after heating.
   -'eq3_#.re': Restart file after equilibration (used as input for production phase).

### Notes
 Equilibration stages:
   -'eq1': Energy minimization
   -'eq2': Heating from 0 K to target temperature (e.g., 300 K)
   -'eq3': Constant temperature equilibration
Total simulation time is 40 ps, typically split as:
   -5 ps (eq1)
   -10 ps (eq2)
   -25 ps (eq3)
Adjust equilibration parameters directly in inputs-equilibration.py as needed.
