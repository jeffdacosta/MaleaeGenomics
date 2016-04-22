#!/bin/bash

#SBATCH -J MI4maker
#SBATCH -p bigmem                # partition (queue)
#SBATCH -N 1                      # number of nodes
#SBATCH -n 48                     # number of cores
#SBATCH --mem 50000        # memory pool for each cores
#SBATCH -t 3-0:00                 # time (D-HH:MM)
#SBATCH -o maker4.out        # STDOUT
#SBATCH --mail-type=ALL           # notifications for job
#SBATCH --mail-user=jdacosta@oeb.harvard.edu   # send-to address

module load gcc/4.8.2-fasrc01 openmpi/1.8.3-fasrc02 maker/2.31.8-fasrc01
export AUGUSTUS_CONFIG_PATH=/n/mathews_lab/software/augustus-3.1/config
mpiexec -mca btl ^openib -np 48 maker -fix_nucleotides -base Mioensis_run4 maker_opts4.ctl
