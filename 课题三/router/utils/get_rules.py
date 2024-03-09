import os
import os.path as osp
import random
  
dataset = 'rules_2'
filename = osp.join('..','..','data','task3', dataset,dataset, 'raw.txt')
write_filename =  osp.join('..','..','data','task3',dataset,dataset,'rules.txt')
f = open(filename, 'r')
wf = open(write_filename, 'w')


lines = f.readlines()
is_case = False

for line in lines:
    if line[0] == '#':
        is_case = False if is_case else True
        continue
    if is_case:
        continue
    if line[0] == 't':
        wf.write(line)
    elif line[0] == 'v':
        wf.write(line)
    elif line[0] == 'e':
        wf.write(line)
    elif line[0] == 'S':
        wf.write(f'Risk:{random.randint(0,1)}\n')
    else:
        wf.write(line)


