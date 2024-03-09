from ast import Not
import os
import os.path as osp
import numpy as np
import bisect



'''
单个超图的json实例格式
hypergraph = [
    'nodes': {
        node_id: label
    },
    'edges': [
        0: {
            'relation': label,
            'list': [node_id ..],
            'weight': 0,
        }, 
        1: {
            ..
        }
    ]
    'label': 0
]
'''
def load_rules(dataset):
    dataset_dir = osp.join('data', 'task3', dataset)
    rules_file = osp.join(dataset_dir, dataset, 'rules.txt')
    hypergraphs = []
    hypergraph = {}
    graph_idx = 0
    edge_idx = 0
    with open(rules_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line[0] == '-':
                hypergraphs.append(hypergraph)
                continue
            if line[0] == '\n' or line[0] == '-':
                continue
            line = line.strip('\n')
            if line[0] == 't':
                graph_idx += 1
                edge_idx = 0
                hypergraph = {
                    'nodes':{},
                    'edges':{},
                    'label':0
                }
            elif line[0] == 'v':
                c, v, l = line.split(' ')
                hypergraph['nodes'][int(v)] = int(l) 
            elif line[0] == 'e':
                lst = line.split(' ')
                c, l = lst[0], lst[-1]
                hypergraph['edges'][edge_idx] = {
                    'relation':int(l),
                    'list':[],
                    'weight':0
                }
                for i in range(1, len(lst) - 1):
                    hypergraph['edges'][edge_idx]['list'].append(int(lst[i]))
                edge_idx += 1
            elif line[0] == 'R':
                r, l = line.split(':')
                hypergraph['label'] = int(l)
            else:
                continue
    # print(hypergraphs[0])
    return hypergraphs


def reweight_with_hyperedge_strength(hypergraphs):
    for hypergraph in hypergraphs:
        for edge_id in hypergraph['edges']:
            hypergraph['edges'][edge_id]['weight'] = len(hypergraph['edges'][edge_id]['list'])
    return hypergraphs

def reweight(hypergraphs, method:str):
    if method == 'hyperedge_strength':
        return reweight_with_hyperedge_strength(hypergraphs)
    else:
        raise NotImplementedError(f'unknown method: {method}')


def lower_bound(arr: np.array, x):
    return bisect.bisect_left(list(arr), x, lo=0, hi=len(list(arr)))

def upper_bound(arr: np.array, x):
    return bisect.bisect_right(list(arr), x, lo=0, hi=len(list(arr)))

def find_interval(weights, filter_value_l, filter_value_r):
    idx_l = upper_bound(weights, filter_value_l)
    idx_r = upper_bound(weights, filter_value_r)
    if idx_r < len(weights) and weights[idx_r] == filter_value_r:
        idx_r += 1
    return idx_l, idx_r

'''
单个超图的json实例格式
hypergraph = [
    'nodes': {
        node_id: label
    },
    'edges': {
        0: {
            'relation': label,
            'list': [node_id ..],
            'weight': 0,
        }, 
        1: {
            ..
        }
    }
    'label': 0
]

'''
def filtration(hypergraphs, layer:int, is_full:bool):
    weights_collection = [-1e9]
    for hypergraph in hypergraphs:
         for edge_idx in hypergraph['edges']:
             weights_collection.append(hypergraph['edges'][edge_idx]['weight'])
    weights_collection = sorted(set(weights_collection))

    LINK_RELATION_MAGIC_NUM = 114514

    node_new_2_old_map_all = {}
    

    filtrated_graphs = {}
    for gid, hypergraph in enumerate(hypergraphs):
        filtrated_graph = {'edges':[], 'nodes':{}}
        edge_weights = np.array([hypergraph['edges'][id]['weight'] for id in hypergraph['edges']])
        edge_indices = np.argsort(edge_weights, kind='stable')
        n_edges = edge_weights.shape[0]
        n_nodes = len(hypergraph['nodes'])
        vid_cnt, vid_map = 0, {}
        node_new_2_old_map = {}

        last_upd_nodes = {}
        for i in range(n_nodes):
            last_upd_nodes[i] = -1

        # print(edge_weights, edge_indices, hypergraph['edges'])

        for l in range(layer):
            filter_value_l = weights_collection[l]
            filter_value_r = weights_collection[l + 1]
            idx_l, idx_r = find_interval(edge_weights[edge_indices], filter_value_l, filter_value_r)
            idx = range(0, idx_r) if is_full else range(idx_l, idx_r)
            # print(idx_l, idx_r, filter_value_l, filter_value_r)
            upd_nodes = set()

            for i, (edge_index, edge_weight) in enumerate(zip(edge_indices[idx], edge_weights[edge_indices[idx]])):
                hyperedge = hypergraph['edges'][edge_index]['list']
                new_hyperedge = []
                for u in hyperedge:
                    if (l, u) not in vid_map:
                        vid_map[(l, u)] = vid_cnt
                        node_new_2_old_map[vid_cnt] = u
                        vid_cnt += 1
                    new_hyperedge.append(vid_map[(l, u)])
                filtrated_graph['edges'].append({
                    'relation': hypergraph['edges'][edge_index]['relation'],
                    'weight': 0,
                    'list': new_hyperedge
                })

            for u in upd_nodes:
                if last_upd_nodes[u] != -1:
                    filtrated_graph['edges'].append({
                        'relation': LINK_RELATION_MAGIC_NUM,
                        'weight': 0,
                        'list': [last_upd_nodes[u], vid_map[(l, u)]]
                    })
                last_upd_nodes[u] = vid_map[(l, u)]
            
            if idx_r == len(edge_weights):
                break
        
        filtrated_graph['label'] = hypergraph['label']
        filtrated_graphs[gid] = filtrated_graph
        for x in node_new_2_old_map:
            # print(x, node_new_2_old_map[x])
            filtrated_graph['nodes'][x] = hypergraph['nodes'][node_new_2_old_map[x]]
        node_new_2_old_map_all[gid] = node_new_2_old_map
    return filtrated_graphs, node_new_2_old_map_all

'''
单个超图的json实例格式
hypergraph = [
    'nodes': {
        node_id: label
    },
    'edges': {
        0: {
            'relation': label,
            'list': [node_id ..],
            'weight': 0,
        }, 
        1: {
            ..
        }
    }
    'label': 0
]
'''
def save(filtrated_hypergraphs, old2new_map, dataset_name:str):
    base_dir = osp.join('data','task3',dataset_name,dataset_name)
    if not osp.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
    with open(osp.join(base_dir,'rules.txt'), 'w') as f:
        for gid in filtrated_hypergraphs:
            f.write(f't # {gid}\n')
            graph = filtrated_hypergraphs[gid]
            nodes = graph['nodes']
            edges = graph['edges']
            label = graph['label']
            for id in nodes:
                f.write(f'v {id} {nodes[id]}\n')
            for edge in edges:
                line = 'e'
                #  (edges)
                edge_label = edge['relation']
                for l in edge['list']:
                    line = line + " " + str(l)
                line = line + f" {edge_label}\n"
                f.write(line)
            f.write(f"\nRisk:{label}\n-----------------\n")
            


        