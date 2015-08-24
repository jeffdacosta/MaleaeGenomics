#!/usr/bin/env python3

import os, sys, argparse, subprocess

print()

#create variables that can be entered as arguments in command line
parser = argparse.ArgumentParser(description='This script uses the GATK VariantFiltration function to filter variants in a given vcf file. '+
'Masked variants are retained in the vcf file, but a mask name is added to the FILTER column. These variants can later be removed with the GATK_VariantFiltration_excludeFiltered.py script. 
'+
' This script needs to be run separately for each vcf input/mask file.')

parser.add_argument('-i', type=str, metavar='input_vcf', required=True, help='REQUIRED: Full path to input vcf file')
parser.add_argument('-o', type=str, metavar='output_vcf', required=True, help='REQUIRED: Full path to output vcf file')
parser.add_argument('-R', type=str, metavar='reference_path', required=True, help='REQUIRED: Full path to reference genome')
parser.add_argument('-m', type=str, metavar='mask_vcf', required=True, help='REQUIRED: Full path to vcf file with variants to mask')
parser.add_argument('-mn', type=str, metavar='mask_name', default='Mask', help='Name of mask to be entered in Filter column [Mask]')
parser.add_argument('-suffix', type=str, metavar='suffix', default='Mask', help='Suffix to append to output filename [Mask]')
parser.add_argument('-mem', type=str, metavar='memory', default='15000', help='Total memory for each job (Mb) [15000]')
parser.add_argument('-time', type=str, metavar='time', default='0-4:00', help='Time for job [0-4:00]')
parser.add_argument('-print', type=str, metavar='print', default='false', help='If changed to true then shell files are printed to screen and not launched [false]')
args = parser.parse_args()

print('\nCreating shell file and sending job to Odyssey cluster\n\n')

basename = args.o.replace('.vcf','')

#write slurm shell file
sh_file = open(basename+'.sh','w')
sh_file.write('#!/bin/bash\n'+
              '#SBATCH -J M.'+basename+'\n'+
              '#SBATCH -o '+basename+'.out\n'+
              '#SBATCH -e '+basename+'.err\n'+
              '#SBATCH -p serial_requeue\n'+
              '#SBATCH -n 1\n'+
              '#SBATCH -t '+args.time+'\n'
              '#SBATCH --mem='+args.mem+'\n'+
              'module load bio/GenomeAnalysisTK-2.7-2\n'+
              'java -Xmx12g -jar /n/sw/GenomeAnalysisTK-2.7-2-g6bda569/GenomeAnalysisTK.jar -T VariantFiltration -V '+args.i+' -R '+args.R+
              ' --mask '+args.m+' --maskName "'+args.mn+'" -o '+args.o+'\n'+
              'printf "\\nFinished\\n\\n"\n')
sh_file.close()

#check if slurm shell file should be printed or sent to Odyssey
if args.print == 'false':
    #send slurm job to Odyssey cluster
    cmd = ('sbatch '+basename+'.sh')
    p = subprocess.Popen(cmd, shell=True)
    sts = os.waitpid(p.pid, 0)[1]
    print('\nJob to the Odyssey cluster\n\nFinished!!\n\n')
else:
    file = open(basename+'.sh','r')
    data = file.read()
    print(data)
    print()
