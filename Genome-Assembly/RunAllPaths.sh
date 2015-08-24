#!/bin/bash

#SBATCH -p bigmem               # partition (queue)
#SBATCH -N 1                    # number of nodes
#SBATCH -n 64                   # number of cores
#SBATCH --mem 450000            # memory pool for each cores
#SBATCH -t 10-00:00             # time (D-HH:MM)
#SBATCH -o RunAllpaths.out     # STDOUT

module load centos6/allpathslg-50081
RunAllPathsLG PRE=/n/regal/mathews_lab/ DATA_SUBDIR=AllPaths RUN=2libHap REFERENCE_NAME=Malus_ioensis TARGETS=standard EVALUATION=BASIC VAPI_WARN_ONLY=True HAPLOIDIFY=True OVERWRITE=True THREADS=64
