#!/bin/bash
#SBATCH --job-name=ligand-energy
#SBATCH --output=logs/ligand-energy_%j.out
#SBATCH --error=logs/ligand-energy_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH -p long

module load python/3.8  # Cambia a la versión que tengas disponible

# Si usas conda
# source ~/miniconda3/etc/profile.d/conda.sh
# conda activate myenv

mkdir -p logs
mkdir -p results

for i in $(seq 1 38); do
    LIGAND_DIR="ligands/ligand_${i}"
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
done

echo "Todos los ligandos procesados."
