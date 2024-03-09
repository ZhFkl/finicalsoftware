import os
import os.path as osp
import random

# dataset = 'rules_1'
# N = 1832
# dataset = 'rules_2'
# N = 352
# dataset = 'rules_3'
# N = 100000
M = 10

def write_motif(dataset, N):
    filename = osp.join('..','..','data','task3',dataset,'motif.txt')

    f = open(filename, 'w')

    for i in range(N):
        for j in range(30):
            f.write(f'{random.randint(0,M)} ')
        f.write('\n')

    f.close()

write_motif('rules_1',1832)
write_motif('rules_1-2-full',1832)
write_motif('rules_2',352)
write_motif('rules_2-2-full',352)
write_motif('rules_3',100000)
write_motif('rules_3-2-full',100000)
