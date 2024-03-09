# coding=utf-8 
import os
import os.path as osp
import json

filename = osp.join('..','..','data','task3','rules_2','pattern_list.json')
rule_filename = osp.join('..','..','data','task3','rules_2','rules_2','rules.txt')
case_filename = osp.join('..','..','data','task3','rules_2','cases.json')

f = open(filename, 'r', encoding='utf-8')
rule_f = open(rule_filename, 'w', encoding='utf-8')
case_f = open(case_filename, 'w', encoding='utf-8')
patterns = json.load(f)

pattern_num = patterns['patterns_num']

pattern_list = patterns['patterns_list']

case_json = {}

for gid, pattern in enumerate(pattern_list):
    hyperedges = pattern['pattern_edge']
    case = pattern_list[gid]['instances'][0]
    id_dict = {}
    case_json[str(gid)] = {}
    case_json[str(gid)]['vertex'] = {}
    case_json[str(gid)]['edge'] = {}
    # print(hyperedges)
    # print(pattern)
    for i, (edge, case_edge) in enumerate(zip(hyperedges, case)):
        # print(edge)
        # print(case_edge)
        ids = edge['ids']
        case_json[str(gid)]['edge'][str(i)] = {'label':'关系','name':case_edge['label']}
        for x, y in zip(ids, case_edge['ids']):
            id, label, risk = x['id'], int(x['label']) - 1, x['risk']
            id_dict[id] = label
            case_json[str(gid)]['vertex'][str(id)] = {'label':'公司','name':y['name'],'risk':risk}

    rule_f.write(f't # {id}\n')
    for x in id_dict:
        rule_f.write(f'v {x} {id_dict[x]}\n')
    
    for edge in hyperedges:
        ids = [x['id'] for x in edge['ids']]
        label = 0
        rule_f.write('e')
        for id in ids:
            rule_f.write(f' {id}')
        rule_f.write(f' {label}\n')
    label = pattern['risk']
    rule_f.write(f'\nRisk:{label}\n-----------------\n\n')

json_res = json.dumps(case_json, indent=4, ensure_ascii=False)
case_f.write(json_res)
            

