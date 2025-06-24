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
#SBATCH --array=1-72%2
#SBATCH --mail-user=m.castillot@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH -o BOX_cpu.o%j
#
#################################################################

# ################## Module Load Zone ###########################

#Qdyn6 production_1.inp > ligand1/1/production_1.log &
#Qdyn6 production_1-2.inp > ligand1/1/production_1-2.log &
# Obtener el número de ligando actual
ligand_num=$SLURM_ARRAY_TASK_ID

# Crear carpetas para la producción
mkdir -p ligand_$ligand_num/1
mkdir -p ligand_$ligand_num/2

# Ejecutar producción réplica 1
Qdyn6 production_${ligand_num}.inp > ligand_$ligand_num/1/production_${ligand_num}.log

# Ejecutar producción réplica 2
Qdyn6 production_${ligand_num}-2.inp > ligand_$ligand_num/2/production_${ligand_num}-2.log