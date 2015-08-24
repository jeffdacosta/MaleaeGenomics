#!/bin/bash

#SBATCH -p bigmem             # partition (queue)
#SBATCH -N 1                  # number of nodes
#SBATCH -n 4                  # number of cores
#SBATCH --mem 200000          # memory pool for each cores
#SBATCH -t 0-12:00            # time (D-HH:MM)
#SBATCH -o PrepAllPaths.out   # STDOUT

module load centos6/allpathslg-50081
PrepareAllPathsInputs.pl DATA_DIR=/n/regal/mathews_lab/Malus_ioensis/AllPaths IN_GROUPS_CSV=in_groups.csv IN_LIBS_CSV=in_libs.csv PLOIDY=2 HOSTS=4 JAVA_MEM_GB=50 OVERWRITE=True
