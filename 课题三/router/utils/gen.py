import os
import os.path as osp
import json
import random

dataset = 'rules_3'
MAX_NODE_SIZE = 10
MAX_EDGE_SIZE = 20
MAX_NODE_LABEL = 1
MAX_EDGE_LABEL = 1
GRAPH_SIZE = 100000

def gen_cycle():
    n = random.randint(4, MAX_NODE_SIZE)
    m = random.randint(2, n - 1)
    edge_size = random.randint(m, n)
    graph = {'edge': [], 'node_size':n, 'edge_size':edge_size}
    for i in range(edge_size):
        graph['edge'].append([(i + j) % n for j in range(m)])
    return graph

def gen_triangle():
    n = random.randint(3, MAX_NODE_SIZE)
    graph = {'edge': [], 'node_size':n, 'edge_size':3}
    x = [_ for _ in range(n)]
    random.shuffle(x)
    x = sorted([x[0], x[1], x[2]])
    x, y, z = x[0], x[1], x[2]
    graph['edge'].append([_ for _ in range(y)])
    graph['edge'].append([_ for _ in range(x,z+1)])
    graph['edge'].append([_ if _ < n else _ - n for _ in range(z,n+x)])
    return graph

def gen_star():
    n = random.randint(4, MAX_NODE_SIZE)
    graph = {'edge': [], 'node_size':n, 'edge_size':3}
    m = random.randint(1, n-3)
    x = [_ for _ in range(n)]
    random.shuffle(x)
    cn = x[:m]
    random.shuffle(x)
    a = [x[_] for _ in range(n // 3)]
    b = [x[_] for _ in range(n // 3, n * 2 // 3)]
    c = [x[_] for _ in range(n * 2 // 3, n)]
    a.extend(cn)
    b.extend(cn)
    c.extend(cn)
    a = list(set(a))
    b = list(set(b))
    c = list(set(c))
    graph['edge'].append(a)
    graph['edge'].append(b)
    graph['edge'].append(c)
    return graph

def gen_random():
    n = random.randint(3, MAX_NODE_SIZE)
    m = random.randint(n, min(n * (n - 1) // 2, MAX_EDGE_SIZE))
    graph = {'edge': [], 'node_size':n, 'edge_size':m}
    x = [_ for _ in range(n)]
    avail_set = set()
    for i in range(m):
        p = random.randint(2, n - 1)
        random.shuffle(x)
        graph['edge'].append(x[:p])
        for y in x[:p]:
            avail_set.add(y)
    if len(avail_set) != n:
        graph['node_size'] += 1
        graph['edge_size'] += 1
        graph['edge'].append(x)
    return graph
        

rule_filename = osp.join('..','..','data','task3',dataset,dataset,'rules.txt')
case_filename = osp.join('..','..','data','task3',dataset,'cases.json')
f_rule = open(rule_filename, 'w')
f_case = open(case_filename, 'w')
cases = {}

template_case_filename = osp.join('..', '..', 'data', 'task3', 'rules_2', 'pattern_list.json')

with open(template_case_filename, 'r') as f:
    template_json = json.load(f)

entity_list = []
for pattern_list in template_json['patterns_list']:
    for instance in pattern_list['instances']:
            for edge in instance:
                for vertex in edge['ids']:
                    entity_list.append({
                        'label': '公司',
                        'name':vertex['name'],
                        'risk':vertex['risk']
                    })
num_entity = len(entity_list)
for gid in range(GRAPH_SIZE):
    cases[str(gid)] = {'edge':{},'vertex':{}}
    r = random.randint(0, 4)
    if r == 0 and False:
        graph = gen_cycle()
    elif r == 1 and False:
        graph = gen_triangle()
    elif r == 2 and False:
        graph = gen_star()
    else:
        graph = gen_random()
    f_rule.write(f't # {gid}\n')
    for x in range(graph['node_size']):
        f_rule.write(f'v {x} {random.randint(0,MAX_NODE_LABEL)}\n')
        cases[str(gid)]['vertex'][str(x)] = entity_list[random.randint(0,num_entity-1)]
    for i, edge in enumerate(graph['edge']):
        f_rule.write(f'e')
        for x in edge:
            f_rule.write(f' {x}')
        f_rule.write(f' {random.randint(0,MAX_EDGE_LABEL)}\n')
        cases[str(gid)]['edge'][str(i)] = {'label':'关系','name':'供货'}
    f_rule.write(f'\nRisk:{random.randint(0,1)}\n')
    f_rule.write(f'-----------------\n\n')
        
cases_str = json.dumps(cases,indent=4,ensure_ascii=False)
f_case.write(cases_str)
f_rule.close()
