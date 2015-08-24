#!/usr/bin/env python3

## For usage and help: ./batch_cutadapt1.8_PE.py -h

import os, sys, argparse, subprocess

#create variables that can be entered as arguments in command line
parser = argparse.ArgumentParser()
parser.add_argument('-list', type=str, metavar='', required=True, help='REQUIRED: Full path to text file with input fastq filename (column1) and output fastq filename (column2). Ensure that
 output directory exists.')
parser.add_argument('-type', type=str, metavar='', required=True, help='REQUIRED: Type of adapters: "Nextera" or "TruSeq"')
parser.add_argument('-mem', type=str, metavar='', default='10000', help='Total memory for each job (Mb) [10000]')
parser.add_argument('-time', type=str, metavar='', default='0-4:00', help='Time for job [0-4:00]')
args = parser.parse_args()

#read input list file, populate lists of input and output file names
in1_list = []
in2_list = []                    
out1_list = []
out2_list = []
listfile = open(args.list,'r')
for line in listfile:
    data = line.split()
    in1_list.append(data[0])
    in2_list.append(data[1])
    out1_list.append(data[2])
    out2_list.append(data[3])
listfile.close()

print('\nFound '+str(len(in1_list))+' paired fastq files to process in cutadapter')
print('\nProcessing:')

count = 0

# adapter seqeunces
R1_Nex_adapt = 'CTGTCTCTTATACACATCTCCGAGCCCACGAGAC'
R2_Nex_adapt = 'CTGTCTCTTATACACATCTGACGCTGCCGACGA'
R1_TS_adapt = 'CAAGCAGAAGACGGCATACGAGAT'
R2_TS_adapt = 'AGATCGGAAGAGCGTCGTGTAGGGAAAGAG'

#create slurm shell file for each input file
for i in range(len(in1_list)):
    sh = open('ca'+str(i)+'.sh','w')
    print(in1_list[i]+' and '+in2_list[i])
    if 'R1.fastq' in in1_list[i]:
        baseoutname = out1_list[i].replace('.R1.fastq','')
    if 'R1.fastq.gz' in in1_list[i]:    
        baseoutname = out1_list[i].replace('.R1.fastq.gz','')
    sh.write('#!/bin/bash\n'+
             '#SBATCH -J CA.'+in1_list[i]+'\n'+
             '#SBATCH -e '+baseoutname+'.err\n'+
             '#SBATCH -o '+baseoutname+'.stats\n'+
             '#SBATCH -p serial_requeue\n'+
             '#SBATCH -n 1\n'+
             '#SBATCH -t '+args.time+'\n'+
             '#SBATCH --mem='+args.mem+'\n'+
#             'source new-modules.sh\n'+
#             'module load cutadapt\n'+
#             'module load legacy\n'+
             '/n/mathews_lab/software/cutadapt-1.8.1/bin/cutadapt -e 0.15 -O 4 -m 25 -a ')

    if args.type == 'Nextera':
        sh.write(R1_Nex_adapt)
    elif args.type == 'TruSeq':
        sh.write(R1_TS_adapt)
    else:
        print('ERROR: type must be either "Nextera" or "TruSeq"\n')
        quit()

    sh.write(' -A ')
    
    if args.type == 'Nextera':
        sh.write(R2_Nex_adapt)
    elif args.type == 'TruSeq':
        sh.write(R2_TS_adapt)
    else:
        print('ERROR: type must be either "Nextera" or "TruSeq"\n')
        quit()


    sh.write(' -o '+out1_list[i]+' -p '+out2_list[i]+' '+in1_list[i]+' '+in2_list[i])

    sh.close()

    #send slurm job to Odyssey cluster
    cmd = ('sbatch ca'+str(i)+'.sh')
    p = subprocess.Popen(cmd, shell=True)
    sts = os.waitpid(p.pid, 0)[1]

    count +=1

print('\nSubmitted '+str(count)+' shell scripts to the cluster!\nFinished!!\n')
