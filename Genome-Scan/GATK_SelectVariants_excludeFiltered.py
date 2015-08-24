#!/usr/bin/env python3

import os, sys, argparse, subprocess

print()

#create variables that can be entered as arguments in command line
parser = argparse.ArgumentParser(description='This script uses the GATK SelectVariants function to extract data for variants with "PASSED" in the '+
'filter column of vcf files. A separate slurm shell script is created and sent to Odyssey for each input vcf file. Output vcf files '+
'are given a suffix and written to the specified output directory, which is automatically created if it does not exist.')

parser.add_argument('-i', type=str, metavar='inputdir_path', required=True, help='REQUIRED: Full path to directory with input vcf files')
parser.add_argument('-o', type=str, metavar='outputdir_path', required=True, help='REQUIRED: Full path to directory for output vcf files')
parser.add_argument('-R', type=str, metavar='reference_path', required=True, help='REQUIRED: Full path to reference genome')
parser.add_argument('-suffix', type=str, metavar='suffix', default='PASS', help='Suffix to append to output filename [PASS]')
parser.add_argument('-nt', type=str, metavar='num_threads', default='6', help='Number of requested threads/cores for job [6]')
parser.add_argument('-mem', type=str, metavar='memory', default='10000', help='Total memory for each job (Mb) [10000]')
parser.add_argument('-time', type=str, metavar='time', default='0-4:00', help='Time for job [0-4:00]')
parser.add_argument('-print', type=str, metavar='print', default='false', help='If changed to true then shell files are printed to screen and not launched [false]')
args = parser.parse_args()

#gather list of input vcf files
in_vcf_list = []
for file in os.listdir(args.i):
    if file.endswith('.vcf'):
        in_vcf_list.append(file)
in_vcf_list.sort()

print('\nFound '+str(len(in_vcf_list))+' input vcf files')
for in_vcf in in_vcf_list:
    print('\t'+in_vcf)
print('Creating shell files and sending jobs to Odyssey cluster\n\n')

#check if output directory exists, create it if necessary
if os.path.exists(args.o) == False:
    os.mkdir(args.o)

#Loop through input vcf files
count = 0
for in_vcf in in_vcf_list:
    basename = in_vcf.replace('.vcf','')
    sh_file = open(args.o+basename+'_'+args.suffix+'.sh','w')


    #write slurm shell file
    sh_file.write('#!/bin/bash\n'+
                  '#SBATCH -J SF.'+basename+'\n'+
                  '#SBATCH -o '+args.o+basename+'_'+args.suffix+'.out\n'+
                  '#SBATCH -e '+args.o+basename+'_'+args.suffix+'.err\n'+
                  '#SBATCH -p general\n'+
                  '#SBATCH -n '+args.nt+'\n'+
                  '#SBATCH -t '+args.time+'\n'
                  '#SBATCH --mem='+args.mem+'\n'+
                  'module load bio/GenomeAnalysisTK-2.7-2\n'+
                  'java -Xmx12g -jar /n/sw/GenomeAnalysisTK-2.7-2-g6bda569/GenomeAnalysisTK.jar -T SelectVariants -V '+args.i+in_vcf+' -R '+args.R+' -nt '+args.nt+
                  ' --excludeFiltered -o '+args.o+basename+'_'+args.suffix+'.vcf\n'+
                  'printf "\\nFinished\\n\\n"\n')
    sh_file.close()

    #check if slurm shell file should be printed or sent to Odyssey
    if args.print == 'false':
    	#send slurm job to Odyssey cluster
    	cmd = ('sbatch '+args.o+basename+'_'+args.suffix+'.sh')
    	p = subprocess.Popen(cmd, shell=True)
    	sts = os.waitpid(p.pid, 0)[1]
    else:
        file = open(args.o+basename+'_'+args.suffix+'.sh','r')
        data = file.read()
        print(data)

    count += 1

#if appropriate, report how many slurm shell files were sent to Odyssey
if args.print == 'false':
    print('\nSent '+str(count)+' jobs to the Odyssey cluster\n\nFinished!!\n\n')
