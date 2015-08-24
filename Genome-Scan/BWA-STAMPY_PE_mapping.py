#!/usr/bin/env python3

import os, sys, argparse, subprocess

print()

#create variables that can be entered as arguments in command line
parser = argparse.ArgumentParser(description='This script maps paired-end reads to a reference genome using BWA and STAMPY. '+
'It searches for paired R1 and R2 fastq files in the input directory, and a separate slurm shell script is created and sent to Odyssey for each input pair. '+
' One sorted bam, bam index, and idxstats file is generated in the output directory for each input pair. ')

parser.add_argument('-i', type=str, metavar='inputdir_path', required=True, help='REQUIRED: Full path to directory with input fastq files')
parser.add_argument('-o', type=str, metavar='outputdir_path', required=True, help='REQUIRED: Full path to directory for output bam files')
parser.add_argument('-ref', type=str, metavar='reference_path', required=True, help='REQUIRED: Full path to reference genome')
parser.add_argument('-nt', type=str, metavar='num_threads', default='12', help='Number of requested threads [12]')
parser.add_argument('-sub', type=str, metavar='substit_rate', default='0.001', help='Divergence from reference, substitution per site [0.001]')
parser.add_argument('-part', type=str, metavar='partition', default='general', help='Requested partition on Odyssey [general]')
parser.add_argument('-mem', type=str, metavar='memory', default='10000', help='Total memory for each job (Mb) [10000]')
parser.add_argument('-time', type=str, metavar='time', default='0-4:00', help='Time for job [0-4:00]')
parser.add_argument('-print', type=str, metavar='print', default='false', help='If changed to true then shell files are printed to screen and not launched [false]')
args = parser.parse_args()

if args.ref.endswith('.fasta') == True:
    ref_base = args.ref.replace('.fasta','')
elif args.ref.endswith('.fa') == True:
    ref_base = args.ref.replace('.fa','')
else:
    print('\nWARNING: '+args.ref+' does not end with .fasta or .fa!\n')
    quit()

#gather list of paired fastq files
R1_list = []
R2_list = []
for file in os.listdir(args.i):
    if 'R1.fastq' in file:
        R1_list.append(file)
        R2_list.append(file.replace('R1.fastq','R2.fastq'))
R1_list.sort()
R2_list.sort()

if len(R1_list) != len(R2_list):
    print('\nWARNING: number of R1 and R2 files found are not equal!\n')
    quit()

print('\nFound '+str(len(R1_list))+' paired fastq files:')
for i in range(len(R1_list)):
    print('\t'+R1_list[i]+' - '+R2_list[i])

print('\nCreating shell files and sending jobs to Odyssey cluster\n\n')

#check if output directory exists, create it if necessary
if os.path.exists(args.o) == False:
    os.mkdir(args.o)

#loop through input vcf files
count = 0
for i in range(len(R1_list)):
    if R1_list[i].endswith('.R1.fastq.gz') == True:
        basename = R1_list[i].replace('.R1.fastq.gz','')
    elif R1_list[i].endswith('.R1.fastq') == True:
        basename = R1_list[i].replace('.R1.fastq','')
    else:
        print('\nWARNING: input file '+R1_list[i]+' does not end in .R1.fastq or .R1.fastq.gz!\n')
        quit()

    sh_file = open(args.o+basename+'.sh','w')

    #write slurm shell file
    sh_file.write('#!/bin/bash\n'+
                  '#SBATCH -J BS.'+basename+'\n'+
                  '#SBATCH -o '+args.o+basename+'.out\n'+
                  '#SBATCH -e '+args.o+basename+'.err\n'+
                  '#SBATCH -p '+args.part+'\n'+
                  '#SBATCH -n '+args.nt+'\n'+
                  '#SBATCH -t '+args.time+'\n'
                  '#SBATCH --mem='+args.mem+'\n'+
                  'module load legacy/0.0.1-fasrc01\n'+
                  'module load bio/samtools-0.1.18\n'+
                  'module load centos6/python-2.7.1_full_stack\n'+
                  '/n/mathews_lab/software/bwa-0.7.12/./bwa aln -q10 -t'+args.nt+' '+ref_base+' '+args.i+R1_list[i]+' > '+args.o+basename+'1.sai\n'+
                  '/n/mathews_lab/software/bwa-0.7.12/./bwa aln -q10 -t'+args.nt+' '+ref_base+' '+args.i+R2_list[i]+' > '+args.o+basename+'2.sai\n'+
                  '/n/mathews_lab/software/bwa-0.7.12/./bwa sampe '+ref_base+' '+args.o+basename+'1.sai '+args.o+basename+'2.sai '+args.i+R1_list[i]+' '+args.i+R2_list[i]+' | /n/mathews_lab
/software/samtools-1.2/bin/./samtools view -Sb - > '+args.o+basename+'.bam\n'+
                  'rm '+args.o+basename+'1.sai '+args.o+basename+'2.sai\n'+
                  '/n/mathews_lab/software/stampy-1.0.27/./stampy.py -g '+ref_base+' -h '+ref_base+' --substitutionrate='+args.sub+' -t'+args.nt+' --bamkeepgoodreads -M '+args.o+basename+'.
bam > '+args.o+basename+'.temp.sam\n'+                  
                  'rm '+args.o+basename+'.bam\n'+
                  '/n/mathews_lab/software/samtools-1.2/bin/./samtools view -S '+args.o+basename+'.temp.sam -b > '+args.o+basename+'.temp.bam\n'+
                  'rm '+args.o+basename+'.temp.sam\n'+
                  '/n/mathews_lab/software/samtools-1.2/bin/./samtools sort '+args.o+basename+'.temp.bam '+args.o+basename+'.sort\n'+
       	       	  'rm '+args.o+basename+'.temp.bam\n'+
                  '/n/mathews_lab/software/samtools-1.2/bin/./samtools index '+args.o+basename+'.sort.bam\n'+
                  '/n/mathews_lab/software/samtools-1.2/bin/./samtools idxstats '+args.o+basename+'.sort.bam > '+args.o+basename+'.idxstats\n'+
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
