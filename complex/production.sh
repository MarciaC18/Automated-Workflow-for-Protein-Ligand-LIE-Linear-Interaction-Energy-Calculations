#!/bin/bash

# ###### SLURM Resource Request Zone ############################
#
#SBATCH --job-name=EQ-RCD
#SBATCH -p long
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=1
#SBATCH --mem=10000
#SBATCH --time=50:10:00
#SBATCH --array=1-38%2
#SBATCH --mail-user=m.castillot@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH -o BOX_cpu.o%j
#
#################################################################

# ################## Module Load Zone ###########################
# (Agrega aquí los módulos necesarios si aplica, por ejemplo `module load qdyn/6`)

# Obtener el número de ligando actual
ligand_num=$SLURM_ARRAY_TASK_ID

# Crear carpetas para la producción
mkdir -p complex_$ligand_num/1
mkdir -p complex_$ligand_num/2

# Ejecutar producción réplica 1
Qdyn6 production1_${ligand_num}.inp > complex_$ligand_num/1/production1_${ligand_num}.log

# Ejecutar producción réplica 2
Qdyn6 production2_${ligand_num}.inp > complex_$ligand_num/2/production2_${ligand_num}.log

