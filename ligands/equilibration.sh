#!/bin/bash

# ###### SLURM Resource Request Zone ############################
#
#SBATCH --job-name=EQ-RCD
#SBATCH -p long
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=1
#SBATCH --mem=10000
#SBATCH --time=30:10:00
#SBATCH --mail-user=m.castillot@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH -o BOX_cpu.o%j
#
#################################################################

# ################## Module Load Zone ###########################

# Loop over ligands 1 to 38
for i in $(seq 1 38); do
    echo "Running EQ simulations for ligand $i"

    if [[ -f eq1_${i}.inp ]]; then
        Qdyn6 eq1_${i}.inp > eq1_${i}.log
    else
        echo "eq1_${i}.inp not found, skipping..."
        continue
    fi

    if [[ -f eq2_${i}.inp ]]; then
        Qdyn6 eq2_${i}.inp > eq2_${i}.log
    else
        echo "eq2_${i}.inp not found, skipping..."
        continue
    fi

    if [[ -f eq3_${i}.inp ]]; then
        Qdyn6 eq3_${i}.inp > eq3_${i}.log
    else
        echo "eq3_${i}.inp not found, skipping..."
        continue
    fi

    echo "Finished ligand $i"
done

