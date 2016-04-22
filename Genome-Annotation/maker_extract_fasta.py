import os, sys

infile = open(sys.argv[1],'r')
listfile = open(sys.argv[2],'r')
outfile = open(sys.argv[3],'w')

list = []
for line in listfile:
    data = line.split()
    list.append(data[0])
list.sort()

for line in infile:
    if line[1:11] in list:
        outfile.write(line)
        seq = infile.readline()
        outfile.write(seq)
    else:
        infile.readline()
outfile.close()
