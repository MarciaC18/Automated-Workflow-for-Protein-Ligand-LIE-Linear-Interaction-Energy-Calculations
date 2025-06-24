#!/bin/bash
#SBATCH --job-name=ligand-energy
#SBATCH --output=logs/ligand-energy_%j.out
#SBATCH --error=logs/ligand-energy_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2   # usa 2 CPUs para que sea igual
#SBATCH --mem=8G
#SBATCH --time=02:00:00
#SBATCH -p long

# Carga el módulo correcto de python y activa tu entorno
module load python/3.8
#source ~/yourenv/bin/activate  # o conda activate tu_env

# Crea carpetas antes de correr
mkdir -p logs
mkdir -p results

# Variables para ligando 1 (ejemplo)
i=1
LIGAND_DIR="1.ligprep/ligand_${i}"
COMPLEX_DIR="complex/complex_${i}"
OUTPUT_FILE="results/LIE_result_${i}.csv"
LIGAND_NAME="ligand_${i}"

echo "Ejecutando ligando $i..."

python analyze_LIE_noqgui.py \
  --ligand_dir "$LIGAND_DIR" \
  --complex_dir "$COMPLEX_DIR" \
  --output "$OUTPUT_FILE" \
  --ligand_name "$LIGAND_NAME" \
  --dg_exp 0.0 \
  --alpha 0.68 \
  --beta 0.11 \
  --gamma 0.0

echo "Ligando $i terminado."

