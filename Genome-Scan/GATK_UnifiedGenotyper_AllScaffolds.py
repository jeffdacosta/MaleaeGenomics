#!/usr/bin/env python3

import os, sys, argparse, subprocess

print()

#create variables that can be entered as arguments in command line
parser = argparse.ArgumentParser(description='This script uses the GATK functions RealignerTargetCreator and IndelRealigner to perform local realignment of bam files in regions with a large
 number of '+
'mismatches, which is usually around indels. It searches for files ending in dedupNamed.bam in the input directory, and a separate slurm shell script is created and sent to Odyssey for each
 input file. '+
' One IndelRealigner.intervals, realigned.bam, and realigned.bam.bai file is generated in the output direcotry for each input file. ')

parser.add_argument('-i', type=str, metavar='inputdir_path', required=True, help='REQUIRED: Full path to directory with input fastq files')
parser.add_argument('-o', type=str, metavar='outputdir_path', required=True, help='REQUIRED: Full path to directory for output vcf file')
parser.add_argument('-vcf', type=str, metavar='vcf_filename', required=True, help='REQUIRED: Name for output vcf file')
parser.add_argument('-ref', type=str, metavar='reference_path', required=True, help='REQUIRED: Full path to reference genome')
parser.add_argument('-dcov', type=str, metavar='downsampling_coverage', default = '200', help='Downsampling coverage per sample [200]')
parser.add_argument('-glm', type=str, metavar='genotype_likelihoods_model', default = 'SNP', help='Genotype likelihoods calculation model (SNP, INDEL, BOTH) to employ [SNP]')
parser.add_argument('-mbq', type=str, metavar='min_base_quality_score', default = '25', help='Minimum base quality required to consider a base for calling [25]')
parser.add_argument('-mmq', type=str, metavar='min_mapping_quality_score', default = '25', help='Minimum mapping quality required to consider a base for calling [25]')
parser.add_argument('-om', type=str, metavar='output_mode', default = 'EMIT_ALL_SITES', help='Specifies which type of calls we should output [EMIT_ALL_SITES]')
parser.add_argument('-ploidy', type=str, metavar='sample_ploidy', default='2', help='Ploidy of samples [2] - all samples in set should have the same ploidy')
parser.add_argument('-scc', type=str, metavar='stand_call_conf', default = '25.0', help='The minimum phred-scaled confidence threshold at which variants should be called [25.0]')
parser.add_argument('-sec', type=str, metavar='stand_emit_conf', default = '13.0', help='The minimum phred-scaled confidence threshold at which variants should be emitted [13.0]')
parser.add_argument('-nt', type=str, metavar='num_threads', default='32', help='Number of requested threads [32]')
parser.add_argument('-part', type=str, metavar='partition', default='general', help='Requested partition on Odyssey [general]')
parser.add_argument('-mem', type=str, metavar='memory', default='10000', help='Total memory for each job (Mb) [10000]')
parser.add_argument('-time', type=str, metavar='time', default='0-4:00', help='Time for job [0-4:00]')
parser.add_argument('-print', type=str, metavar='print', default='false', help='If changed to true then shell files are printed to screen and not launched [false]')
args = parser.parse_args()

#gather list of paired fastq files
bam_list = []
for file in os.listdir(args.i):
    if file.endswith('realigned.bam'):
        bam_list.append(file)
bam_list.sort()

print('\nFound '+str(len(bam_list))+' realigned bam files:')
for i in range(len(bam_list)):
    print('\t'+bam_list[i])

#check if output directory exists, create it if necessary
if os.path.exists(args.o) == False:
    os.mkdir(args.o)

print('\nCreating shell file and sending job to Odyssey cluster\n\n')

#write slurm file
sh_file = open(args.o+'UG.sh','w')

sh_file.write('#!/bin/bash\n'+
              '#SBATCH -J UG\n'+
              '#SBATCH -o '+args.o+'UG.out\n'+
              '#SBATCH -e '+args.o+'UG.err\n'+
              '#SBATCH -p '+args.part+'\n'+
              '#SBATCH -n '+args.nt+'\n'+
              '#SBATCH -t '+args.time+'\n'
              '#SBATCH --mem='+args.mem+'\n'+
              'module load legacy/0.0.1-fasrc01\n'+
              'module load bio/GenomeAnalysisTK-2.7-2\n'+
              'java -Xmx8g -jar /n/sw/GenomeAnalysisTK-2.7-2-g6bda569/GenomeAnalysisTK.jar -T UnifiedGenotyper -nt '+args.nt+' -nct 3 -R '+args.ref+
              ' --min_base_quality_score '+args.mbq+' -rf MappingQuality --min_mapping_quality_score '+args.mmq+' -rf DuplicateRead -rf BadMate -rf BadCigar'+
              ' -ploidy '+args.ploidy+' -glm SNP -stand_emit_conf '+args.sec+' -stand_call_conf '+args.scc+' --output_mode '+args.om+' -dcov '+args.dcov+
              ' -o '+args.o+args.vcf)

for i in range(len(bam_list)):
    sh_file.write(' -I '+args.i+bam_list[i])

sh_file.write('\nprintf "\\nFinished\\n\\n"\n')
sh_file.close()

#check if slurm shell file should be printed or sent to Odyssey
if args.print == 'false':
    #send slurm job to Odyssey cluster
    cmd = ('sbatch '+args.o+'UG.sh')
    p = subprocess.Popen(cmd, shell=True)
    sts = os.waitpid(p.pid, 0)[1]
else:
    file = open(args.o+'UG.sh','r')
    data = file.read()
    print(data)

#if appropriate, report how many slurm shell files were sent to Odyssey
if args.print == 'false':
    print('\nSent UG job to the Odyssey cluster\n\nFinished!!\n\n')
