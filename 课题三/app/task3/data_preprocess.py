import json
import os
import os.path as osp

raw_file = osp.join('..','..','data','task3','rules_2','rules_2','raw.txt')
cases_file = osp.join('..','..','data','task3','rules_2','cases.json')
rules_file = osp.join('..','..','data','task3','rules_2','rules_2','rules.txt')

with open(cases_file, 'r') as f:
    cases = json.load(f)

with open(raw_file, 'r') as f1:
    with open(rules_file, 'w') as f2:
        lines = f1.readlines()
        ok = True
        for line in lines:
            if line[0] == '#':
                ok = False if ok else True
                continue
            if not ok:
                continue
            if line[0] == 't':
                c, _, id = line.split(' ')
                id = id.strip('\n')
                vertex = cases[id]['vertex']
                risk_cnt = 0
                for x in vertex:
                    if vertex[x]['risk'] == 1:
                        risk_cnt += 1
                if risk_cnt > 1 or risk_cnt > len(vertex) * 0.5:
                    current_risk = 1
                else:
                    current_risk = 0
                f2.write(line)
            elif line[0] == 'v':
                f2.write(line)
            elif line[0] == 'e':
                f2.write(line)
            elif line[0] == 'S':
                f2.write('\n' + f'Risk:{current_risk}\n' + '-----------------\n\n')
            else:
                continue