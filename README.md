# Automated Workflow for Protein-Ligand LIE (Linear Interaction Energy) Calculations

## Description

This protocol provides an **automated workflow using Q6 MD** to perform **Linear Interaction Energy (LIE)** calculations. It prepares ligands and protein-ligand systems, performs equilibration, runs molecular dynamics simulations of complexes and ligands in solution, extracts interaction energies, checks for errors that may require extending MD steps, calculates binding free energies, and analyzes the LIE-derived ΔG values — enabling fast, consistent, and reproducible affinity predictions.

The protocol is structured to include **two main folders** in addition to the root:

- `ligands/` — for ligand-in-water simulations
- `complex/` — for protein-ligand complex-in-water simulations

This is because LIE calculations require separate MD simulations of both systems. Automated tutorials to obtain the MDs for each ligand and complex are included in the respective `README.md` files inside the `ligands/` and `complex/` folders.

Once all MD simulations have been completed for both ligands and complexes, follow the instructions below to **validate interaction energy stability** (van der Waals and electrostatics) and proceed to **calculate LIE binding free energies** and **analyze the results**.

---

## General Requirements

- [Q6](https://github.com/qusers/Q6/tree/master)
- [QLigFEP](https://github.com/qusers/qligfep/tree/master)
- `python` (version 3.8)
- `SLURM` (for executing `.sh` files via `sbatch`)

Clone the GitHub repository to get started:

```bash
git clone https://github.com/MarciaC18/Automated-Workflow-for-Protein-Ligand-LIE-Linear-Interaction-Energy-Calculations
```
> **Important:**  
> Make sure you have the `ligands/` and `complex/` folders set up according to the instructions in their respective tutorials before continuing.
---
# 1. Evaluation and Verification of van der Waals and Electrostatic Interactions
---

### Check_errors Protocol

To ensure valid LIE calculations, the production MD of the protein-ligand complexes must yield stable van der Waals and electrostatic interaction energies with error **< 1 kcal/mol**.

This criterion is based on:

> Gutiérrez-de-Terán, H., & Åqvist, J. (2012). *Linear interaction energy: method and applications in drug design*. Computational Drug Discovery and Design, 305–323.

---

### Step 1: Plot Interaction Energies

Run the script:

```bash
sbatch plot-energy.sh
```
This script calls:

```bash
python ligand-surrounding-energies.py
```
It reads .log files from:
```bash
complex/complex_#/1/
complex/complex_#/2/
```
And generates:
```bash
individuals_plot/
├── production1_#_plot.png
└── production2_#_plot.png
```
Each plot helps verify whether the interaction energy errors are **< 1 kcal/mol** .
A summary of simulations with error > 1 kcal/mol is saved in:
```bash
individuals_plot/high_errors_report.txt
```
*** If yes, the MD is valid — proceed to number 2 (LIE Calculations).***

*** If not, the MD must be extended - proceed to sept 2 (If Error > 1 kcal/mol — Extend the MD).***

## Step 2: If Error > 1 kcal/mol — Extend the MD

1. Generate Extended Production Input Files
Run:
```bash
python prueba_2.py
```
## Inputs

- `ligands/`
- `complex/`
- `prueba_2.py`

 **Inside the function def replace_steps(content):, you can adjust the number of MD steps.**

 ## Outputs

```bash
 check_errors/
├── 1.ligprep/
│   ├── production_#.inp
│   ├── production_#-2.inp
│   └── production_ligands.sh
└── complex/
    ├── production1_#.inp
    ├── production2_#.inp
    └── production_complex.sh
```
*** In this protocol, we will use # to indicate the number of the ligand to be studied*** 
    
2. Run Extended Production Simulations

## Inputs
- `check_errors/1.ligprep/production_ligands.sh`
-`check_errors/complex/production_complex.sh`

-`../../ligands/#_w.top`
-`../../ligands/eq#_3.re`
-`../../ligands/#.fep`

- `../../complex/complex_#_w.top`
- `../../complex/eq3_#.re`
- `../../complex/#.fep`

*** Make sure the original ligands/ and complex/ folders are present and correctly populated. ***

Navigate to each folder and run:

```bash
sbatch production_ligands.sh
sbatch production_complex.sh
```

## Outputs

### Ligand simulations:

- `ligand_#/1/production_#.log`
- `ligand_#/2/production_#-2.log`
- `prod1_#.re`
- `prod1_#.dcd`
- `prod1_#.en`
- `prod2_#.re`
- `prod2_#.dcd`
- `prod2_#.en`

### Complex simulations:
- `complex_#/1/production1_#.log`
- `complex_#/2/production2_#.log`
- `prod1_complex_#.re`
- `prod1_complex_#.dcd`
- `prod1_complex_#.en`
- `prod2_complex_#.re`
- `prod2_complex_#.dcd`
- `prod2_complex_#.en`

In this step, repeat **Step 1: Plot Interaction Energies** and check again:

- `individuals_plot/high_errors_report.txt`
- `individuals_plot/`
  ├── `production1_#_plot.png`
  └── `production2_#_plot.png`

Continue extending the MD until the error is < 1 kcal/mol.

# 2. Binding Free Energy Calculation Using the LIE Method

### Objective
Calculate the binding free energy (ΔG) between different ligands and a protein using the Linear Interaction Energy (LIE) method.

---

### Preparation

Before running the LIE calculations, ensure the following folders exist in the root directory:

- `logs/` — To store log files  
- `results/` — To store output results  
- `ligands/ligand_#/` — Folder with ligand data  
- `complex/complex_#/` — Folder with protein-ligand complex data

---

### Required Scripts and Files

- `analyze_LIE_noqgui.py` (custom script)  
- `mdlog_energies.py` (external script from [Qgui GitHub](https://github.com/qusers/qgui/tree/Qgui3))  
  - **Important:** This script must be placed in the root directory alongside the others. It is called by `analyze_LIE_noqgui.py`.  
- `analyze_LIE_ligands.sh` (shell script to launch the analysis)

---

### Parameters

You can modify the following parameters inside `analyze_LIE_ligands.sh` according to your needs:

```bash
--dg_exp 0.0 \
--alpha 0.68 \
--beta 0.11 \
--gamma 0.0
```

## How to Run

Execute the LIE calculation by submitting the job with Slurm:

```bash
sbatch analyze_LIE_ligands.sh
```

## Output

- `results/LIE_result_#.csv`

  Contains the calculated binding free energy (ΔG) values along with their Standard Error of the Mean (SEM).

- `logs/*.log`

  Log files with detailed output of the calculations.

Make sure all required input folders and files are correctly set up before running the script to avoid errors.














