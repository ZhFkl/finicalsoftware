import os
import os.path as osp
import json

input_filename = osp.join('..','..','data','task3','rules_3','rules_3','rules.txt')
output_filename = 'rules.json'


in_f = open(input_filename, 'r')
out_f = open(output_filename, 'w')

lines = in_f.readlines()
rules = {}
gid = 0
for line in lines:
    if line[0] == 't':
        edges = []
    elif line[0] == 'R':
        rules[str(gid)] = {}
        rules[str(gid)]['edges'] = edges
        # rules[str(gid)] = edges
        gid += 1
    elif line[0] == 'e':
        edge_raw = line.strip('\n').split(' ')
        edge = {'relation':int(edge_raw[-1]),'entities':[]}

        for x in edge_raw[1:-1]:
            edge['entities'].append(int(x))
        edges.append(edge)
    else:
        continue
json_ans = json.dumps(rules,indent=4)
out_f.write(json_ans)
