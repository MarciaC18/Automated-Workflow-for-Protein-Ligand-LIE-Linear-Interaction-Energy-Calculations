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
  - `#` represents the ligand number identifier, for example `L1.pdb`, `L2.pdb`, etc.
- `bind_prm.py`: Custom script that processes OPLS parameters to create `OPLSA_#_all.prm`.
- `copy_generate.py`: Script to copy and adapt input files with specific modifications for `boundary sphere` and `solvate` parameters for each ligand.
- `generate_ligand_fep.py`: Script to generate `.fep` files for FEP calculations.
- `prepared.sh`: Script to launch the preparation on the cluster using `sbatch`.

## Workflow

1. Prepare `L#.pdb` files (where `#` is the ligand number).
2. Have the `OPLS2005_all.prm` file ready.
3. Run `generate_oplsa.py` to create `.lib` and `.prm` files.  
   **Note:** Requires Schrödinger installation and license.
4. Run `bind_prm.py` to generate `OPLSA_#_all.prm`.
5. Use `copy_generate.py` to adjust `boundary sphere` and `solvate` parameters for each ligand.
6. Run `prepared.sh` to execute the preparation for create #_w.top #_w.pdb y #_w.log.
7. Generate `.fep` files using `generate_ligand_fep.py`.

## Important Notes

- Correct configuration of the Schrödinger path is necessary for `generate_oplsa.py` to work.
- `lig.fep` is the base file required for Free Energy Perturbation.
- `boundary sphere` and `solvate` parameters must be manually adjusted in `copy_generate.py` according to the characteristics of each ligand.

