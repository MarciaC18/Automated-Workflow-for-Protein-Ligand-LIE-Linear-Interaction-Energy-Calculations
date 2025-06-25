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

To get a summary of interaction energy errors >1 kcal/mol, run:
```bash
python check_high_errors.py
``` 
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

- `../../ligands/#_w.top`
- `../../ligands/eq#_3.re`
- `../../ligands/#.fep`

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
```bash
- individuals_plot/
  ├── production1_#_plot.png
  └── production2_#_plot.png
  ```

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
---
# 3. LIE Calculation Analysis

## 3.1 Evaluation of the Accuracy and Precision of Calculated ΔG vs. Experimental ΔG

**Objective:**  
Assess the predictive quality of the calculated binding free energies (ΔG<sub>calc</sub>) by analyzing their correlation and error against the experimental values (ΔG<sub>exp</sub>).

**How to Run:**  
Execute the regression analysis with the following command:

```bash
python DG_regression_reference_ligands.py
```
## Inputs

Within the script, modify the following arrays to match your reference ligand data:

```python
DG_exp = np.array([-8.7, -11.18, -11.46])   # Experimental ΔG values
DG_calc = np.array([-8.39, -11.56, -12.56]) # Calculated ΔG values
std_dev = np.array([0.45, 0.32, 0.55])      # Standard deviations for ΔG_calc
```
## Requirements

A Python environment with the following libraries installed:

- numpy
- matplotlib
- seaborn
- scikit-learn

---

## Output

`DG_regression_for_references.png`

This high-resolution plot visualizes the linear regression between ΔG<sub>exp</sub> and ΔG<sub>calc</sub> for reference ligands.  
It includes:

- Error bars based on standard deviations.
- Regression line with equation.
- Key metrics:
  - Coefficient of determination (R²)
  - Mean Absolute Error (MAE)
  - Root Mean Square Error (RMSE)

Use this analysis to evaluate the reliability of your LIE-calculated binding energies before proceeding with predictions for new ligands.
---
## 3.2 Comparison of Calculated ΔG for Test Ligands and Reference Inhibitors

**Objective:**  
Evaluate the relative binding affinity of test ligands by comparing their calculated binding free energies (ΔG<sub>calc</sub>) against known reference ligands.

---

**How to Run:** 

Execute the script with the following command:

```bash
python plot-analyze-LIE.py
```
## Inputs

Please review your result files in the `results/` directory. The script reads CSV files with the following naming format:

```
- `results/LIE_result_#.csv``
```

Each file must contain at least the following columns:

- `ligand_name`: name or identifier of the ligand  
- `dG_calc`: calculated binding free energy  
- `stderr`: standard error of the ΔG_calc  

> **NOTE**: If you want to compare your test ligands against reference ligands, ensure their names follow this format:  
> `ligand_1, ligand_2, ligand_3, ...`  
> These references must be included from the beginning of the protocol.
## Outputs
```
- results/LIE_dG_comparison.png 
```
---
## 3.3 Analysis of Reproducibility, Accuracy, and Precision of the LIE Method According to Ligand Conformational Changes

## 3.3.1 LIE Calculation for reference ligands 

**Objective**  
Perform a thorough analysis of the reproducibility, accuracy, and precision of the LIE method to determine whether ligand conformational changes affect the statistical data obtained, and to assess if the best docking pose is the most suitable starting point for the LIE model.

---

**How to run the analysis**  
Run the following command from the directory containing the scripts and analysis folders:

```bash
python analyze_LIE_poses_replica.py --ligand_dir ligand --complex_dir complex --alpha 0.68 --beta 0.11 --gamma 0.00 --ligand_name DIZ --n_replicas 2 --n_poses 2
```
***The parameters --alpha, --beta, --gamma, --ligand_name, --n_replicas, and --n_poses can be adjusted as needed.***

## Inputs

Create a folder named `analysis-by-R-P` with the following structure:
~~~
analysis-by-R-P/
│
├── ligand/
│   ├── pose1/
│   │   ├── 1/      <-- replica 1 (subfolder with .log files)
│   │   │   ├── file1.log
│   │   │
│   │   ├── 2/      <-- replica 2
│   │   │
│   │   └── ...
│   ├── pose2/
│   │   └── 1/
│   │
│   └── ...
│
├── complex/
│   ├── pose1/
│   │   ├── 1/      <-- replica 1
│   │   │
│   │   ├── 2/      <-- replica 2
│   │   │
│   │   └── ...
│   ├── pose2/
│   │   └── 1/
│   │
│   └── ...
│
├── analyze_LIE_poses_replica.py   <-- analysis script
└── mdlog_energies.py              <-- module with get_q_energies function
~~~

***Make sure the necessary .log files for each replica and pose are correctly placed in their respective folders.***
## Requirements

- Python 3.x
- Required libraries installed (e.g., `numpy`, `csv`)
- Scripts `analyze_LIE_poses_replica.py` and `mdlog_energies.py` located in the root `analysis-by-R-P` folder
- `.log` files for each replica and pose of ligand and complex organized as described

## Outputs

The script will generate CSV files with results for each pose and replica in the current folder, named like:

´´´
results_LIE-poseX-rY.csv
´´´

where `X` is the pose number and `Y` is the replica number according to the input parameters.

---

### Notes

- Carefully verify the folder structure and correct placement of `.log` files.  
- The parameters `alpha`, `beta`, and `gamma` should be set according to the experimental values or the LIE model used.  
- This calculation allows comparison of statistical variability between replicas and poses to evaluate the robustness of the LIE method against ligand conformational changes.
---

## 3.3.2 Saving calculated ΔG values for comparative analysis across poses and replicas

***Objective**
To generate and store a dataset with ΔG values from multiple poses and replicas for future analysis of their impact on the accuracy of binding free energy predictions.

---
***How to Run**

Run the following command to create a unified dataset:

```bash
python combine_LIE-results.py -p 1 2 -r 1 2 -o Data_RP_LIE.csv
```
- p: Pose numbers to include (e.g., 1 2)

- r: Replica numbers to include (e.g., 1 2)

- o: Name of the output file

***Adjust -p and -r according to your data.**

## Inputs

- Multiple `.csv` files with LIE calculation results, named in the format:  
  `resultados_LIE-poseX-rY.csv`  
  (where `X` is the pose number, and `Y` is the replica number)

- Python script to combine the results:  
  `combine_LIE-results.py`
  
---
## Outputs
**File:** `Data_RP_LIE.csv`  
A merged table with the following columns:

- **Ligand**: Name of the ligand.
- **Replica**: Replica number from which the data was obtained.
- **Pose**: Docking pose number.
- **DG_calculated**: Binding free energy calculated using the LIE method.
- **DG_experimental**: Experimental binding free energy (optional; can be filled manually).
- **N_poses**: Number of entries (rows) from the source file.
---
## 3.3.3 Linear Regression Analysis: DG_calculated vs. DG_experimental and Absolute Error by Number of Poses

***Objective**
To evaluate the correlation between the calculated and experimental binding free energies (DG) using linear regression, and to analyze the absolute error across different docking poses.
***How to Run**
```bash
python plot_DG_correlation.py
```
## Inputs
- `Data_RP_LIE.csv`: A CSV file containing the columns `DG_calculated` and `DG_experimental` for each ligand, pose, and replica.
---
## Requirements

- matplotlib  
- seaborn  
- pandas  
- numpy  

You can install them with:

```bash
pip install matplotlib seaborn pandas numpy
```
---
## Outputs

- `DG_calc_vs_exp_by_pose.png`

A plot showing the correlation between **DG_calculated** and **DG_experimental** per pose, including an ideal correlation line and mean absolute error bands.

---

### Notes

Make sure the **DG_experimental** column in `Data_RP_LIE.csv` is filled for all entries, as missing values will be ignored in the plot.
---
## 3.3.4 Statistical Analysis with Kruskal-Wallis Test

***Objective**
Perform a non-parametric Kruskal-Wallis test to determine whether the variables **Pose** and **Replica** cause significant changes in the results when the data does not follow a normal distribution.

***How to Run**
```bash
python kruskal-wallis-test.py
```
## Inputs
- `Data_RP_LIE.csv` (must include experimental DG values)
---
## Requirements
- `pandas`
- `numpy`
- `scipy`

You can install them with:

```bash
pip install pandas numpy scipy
```
---
## Outputs

- `summary_by_replica.csv`: Mean, standard deviation, and absolute error per ligand and replica.

- `summary_by_pose.csv`: Mean, standard deviation, and absolute error per ligand and pose.

- `kruskal_test_results_replicas.csv`: Kruskal-Wallis test results comparing replicas.

- `kruskal_test_results_poses.csv`: Kruskal-Wallis test results comparing poses.
### Notes

If the p-value < 0.05 (95% confidence), this indicates a significant difference between the studied variables (poses or replicas), and attention should be given to how many poses or replicas generate more accurate results for the system.

In this case, the null hypothesis is rejected.




























