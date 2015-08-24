#!/usr/bin/env python3

import os, sys, argparse, subprocess

print()

#create variables that can be entered as arguments in command line
parser = argparse.ArgumentParser(description='This script uses picard-tools to fix names in deduplicated bam files. '+
'It searches for files ending in dedup.bam in the input directory, and a separate slurm shell script is created and sent to Odyssey for each input file. '+
' One dedupName.bam file is generated in the output direcotry for each input file. ')

parser.add_argument('-i', type=str, metavar='inputdir_path', required=True, help='REQUIRED: Full path to directory with input fastq files')
parser.add_argument('-o', type=str, metavar='outputdir_path', required=True, help='REQUIRED: Full path to directory for output bam files')
parser.add_argument('-nt', type=str, metavar='num_threads', default='12', help='Number of requested threads [12]')
parser.add_argument('-part', type=str, metavar='partition', default='general', help='Requested partition on Odyssey [general]')
parser.add_argument('-mem', type=str, metavar='memory', default='10000', help='Total memory for each job (Mb) [10000]')
parser.add_argument('-time', type=str, metavar='time', default='0-4:00', help='Time for job [0-4:00]')
parser.add_argument('-print', type=str, metavar='print', default='false', help='If changed to true then shell files are printed to screen and not launched [false]')
args = parser.parse_args()

#gather list of paired fastq files
bam_list = []
for file in os.listdir(args.i):
    if file.endswith('dedup.bam'):
        bam_list.append(file)
bam_list.sort()

print('\nFound '+str(len(bam_list))+' deduplicated bam files:')
for i in range(len(bam_list)):
    print('\t'+bam_list[i])

print('\nCreating shell files and sending jobs to Odyssey cluster\n\n')

#check if output directory exists, create it if necessary
if os.path.exists(args.o) == False:
    os.mkdir(args.o)

#loop through input vcf files
count = 0
for i in range(len(bam_list)):
    basename = bam_list[i].replace('_dedup.bam','')

    sh_file = open(args.o+basename+'.sh','w')

    #write slurm shell file
    sh_file.write('#!/bin/bash\n'+
                  '#SBATCH -J PT.'+basename+'\n'+
                  '#SBATCH -o '+args.o+basename+'.out\n'+
                  '#SBATCH -e '+args.o+basename+'.err\n'+
                  '#SBATCH -p '+args.part+'\n'+
                  '#SBATCH -n '+args.nt+'\n'+
                  '#SBATCH -t '+args.time+'\n'
                  '#SBATCH --mem='+args.mem+'\n'+
                  'module load legacy/0.0.1-fasrc01\n'+
                  'module load bio/picard-tools-1.98\n'+
                  'java -Xmx4g -jar /n/sw/picard-tools-1.98/AddOrReplaceReadGroups.jar I='+args.i+bam_list[i]+' O='+args.o+basename+'_dedupNamed.bam '+ 
                  'SORT_ORDER=coordinate CREATE_INDEX=True VALIDATION_STRINGENCY=LENIENT RGLB='+basename+' RGPL=illumina RGPU=AAAAAA RGSM='+basename+'\n'+
                  'printf "\\nFinished\\n\\n"\n')
    sh_file.close()

    #check if slurm shell file should be printed or sent to Odyssey
    if args.print == 'false':
    	#send slurm job to Odyssey cluster
    	cmd = ('sbatch '+args.o+basename+'.sh')
    	p = subprocess.Popen(cmd, shell=True)
    	sts = os.waitpid(p.pid, 0)[1]
    else:
        file = open(args.o+basename+'.sh','r')
        data = file.read()
        print(data)

    count += 1

#if appropriate, report how many slurm shell files were sent to Odyssey
if args.print == 'false':
    print('\nSent '+str(count)+' jobs to the Odyssey cluster\n\nFinished!!\n\n')
