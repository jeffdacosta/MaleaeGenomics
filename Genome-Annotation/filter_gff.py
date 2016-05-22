import os, sys

infile = open(sys.argv[1],'r')
type = sys.argv[2]
outfile = open(sys.argv[3],'w')

parent_list = []

if type == 'default':
    print('\n\nExtacting annotations with AED score <1:')
    for line in infile:
        if '\tmaker\tmRNA' in line:
            data = line.split()
            aed = data[8].split('_AED=')
            if aed[1][0] == '0':
                parent = data[8].split('Parent=')
                parent = parent[1].split(';')[0]
                parent_list.append(parent)
    infile.close()

    parent_list.sort()
    
    print('\nFound '+str(len(parent_list))+' annotations\nExtracting annotations...\n')

    parentfile = open('default_parent.list','w')
    for parent in parent_list:
        parentfile.write(parent+'\n')
    parentfile.close()

    count = 0
    target = 1000
    
    for parent in parent_list:
        infile = open(sys.argv[1],'r')
        for line in infile:
            if parent in line:
                outfile.write(line)
                for i in range(1000000):
                    data = infile.readline()
                    if parent in data:
                        outfile.write(data)
                    else:
                        break
                count += 1
                if count == target:
                    print(count)
                    target = target+1000
                break

    outfile.close()

if type == 'standard':
    print('\n\nExtacting annotations with AED score <1 OR a Pfam domain:')
    for line in infile:
        if '\tmaker\tmRNA' in line:
            data = line.split()
            aed = data[8].split('_AED=')
            if aed[1][0] == '0':
                parent = data[8].split('Parent=')
                parent = parent[1].split(';')[0]
                parent_list.append(parent)
            else:
                if 'Dbxref=' in line:
                    parent = data[8].split('Parent=')
                    parent = parent[1].split(';')[0]
                    parent_list.append(parent)                    
    infile.close()

    parent_list.sort()
    
    print('\nFound '+str(len(parent_list))+' annotations\nExtracting annotations...\n')

    parentfile = open('standard_parent.list','w')
    for parent in parent_list:
        parentfile.write(parent+'\n')
    parentfile.close()

    count = 0
    target = 1000
    
    for parent in parent_list:
        infile = open(sys.argv[1],'r')
        for line in infile:
            if parent in line:
                outfile.write(line)
                for i in range(1000000):
                    data = infile.readline()
                    if parent in data:
                        outfile.write(data)
                    else:
                        break
                count += 1
                if count == target:
                    print(count)
                    target = target+1000
                break

    outfile.close()
            
if type == 'standard-us':
    print('\n\nExtacting annotations with AED score <1 OR a Pfam domain OR a uniprot-swissprot hit:')
    for line in infile:
        if '\tmaker\tmRNA' in line:
            data = line.split()
            aed = data[8].split('_AED=')
            if aed[1][0] == '0':
                parent = data[8].split('Parent=')
                parent = parent[1].split(';')[0]
                parent_list.append(parent)
            else:
                if 'Dbxref=' in line:
                    parent = data[8].split('Parent=')
                    parent = parent[1].split(';')[0]
                    parent_list.append(parent)                    
                else:
                    if 'Note=Similar' in line:
                        parent = data[8].split('Parent=')
                        parent = parent[1].split(';')[0]
                        parent_list.append(parent)
    infile.close()

    parent_list.sort()
    
    print('\nFound '+str(len(parent_list))+' annotations\nExtracting annotations...\n')

    parentfile = open('standard-us_parent.list','w')
    for parent in parent_list:
        parentfile.write(parent+'\n')
    parentfile.close()

    count = 0
    target = 1000
    for parent in parent_list:
        infile = open(sys.argv[1],'r')
        for line in infile:
            if parent in line:
                outfile.write(line)
                for i in range(1000000):
                    data = infile.readline()
                    if parent in data:
                        outfile.write(data)
                    else:
                        break
                count += 1
                if count == target:
                    print(count)
                    target = target+1000
                break

    outfile.close()

print('\nFinished!!\n\n')
