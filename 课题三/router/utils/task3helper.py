import json
import os
import os.path as osp
from typing import List

import numpy as np
import sklearn


from ExKMC.Tree import Tree
import matplotlib.pyplot as plt
from sklearn import manifold
from sklearn import preprocessing
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import minmax_scale
# from app.task3.ExKMC_utils import calc_cost, plot_kmeans, plot_tree_boundary

import app.task3.kernel as kernel
import app.task3.filtration as filtration

def get_all_dataset():
    ans = []
    for dirs in os.listdir('data/task3'):
        if 'rules' in dirs:
            ans.append(dirs)
    return sorted(ans)

def preprocess_for_GraphRule(path, DS):
    graph_id = 0
    node_size = 0
    edge_size = 0
    current_node_size = 0
    
    # if osp.exists(osp.join(path, DS + '-H', 'raw')):
    #     return
    
    os.makedirs(osp.join(path, DS + '-H', 'raw'), exist_ok=True)
    
    f_A = open(osp.join(path,  DS + '-H', 'raw', DS + '-H_A.txt'), 'w+')
    f_GI = open(osp.join(path, DS + '-H', 'raw', DS + '-H_graph_indicator.txt'), 'w+')
    f_GL = open(osp.join(path, DS + '-H', 'raw', DS + '-H_graph_labels.txt'), 'w+')
    f_NL = open(osp.join(path, DS + '-H', 'raw', DS + '-H_node_labels.txt'), 'w+')
    f_EL = open(osp.join(path, DS + '-H', 'raw', DS + '-H_edge_labels.txt'), 'w+')
    f_INFO = open(osp.join(path, 'info.txt'), 'w')

    info_json = {}
    node_label = {}
    edge_label = {}
    graph_label = {}
    
    with open(osp.join(path, DS, 'rules.txt'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line[0] == '\n' or line[0] == '-':
                continue
            line = line.strip('\n')
            if line[0] == 't':
                graph_id += 1
                node_size += current_node_size
                current_node_size = 0
            elif line[0] == 'v':
                c, v, l = line.split(' ')
                current_node_size += 1
                f_GI.write(str(graph_id)+'\n')
                f_NL.write(str(l)+'\n')
                if l not in node_label:
                    node_label[l] = 0
                node_label[l] += 1
            elif line[0] == 'e':
                lst = line.split(' ')
                c, l = lst[0], lst[-1]
                f_EL.write(str(l)+'\n')
                hyperedge = ''
                for i in range(1, len(lst) - 1):
                    hyperedge = hyperedge + str(int(lst[i])+node_size) + ","
                hyperedge = hyperedge.strip(',')
                edge_size += 1
                f_A.write(hyperedge+'\n')
                if l not in edge_label:
                    edge_label[l] = 0
                edge_label[l] += 1
            elif line[0] == 'R':
                c, l = line.split(':')
                f_GL.write(str(l)+'\n')
                if l not in graph_label:
                    graph_label[l] = 0
                graph_label[l] += 1
            else:
                pass
        info_json['node_size'] = node_size
        info_json['edge_size'] = edge_size
        info_json['graph_size'] = graph_id
        info_json['node_label'] = node_label
        info_json['edge_label'] = edge_label
        info_json['graph_label'] = graph_label
        print(info_json)
        f_INFO.write(json.dumps(info_json, indent=4))

        f_A.close()
        f_GI.close()
        f_GL.close()
        f_NL.close()
        f_EL.close()
        f_INFO.close()

def parse_data_and_get_info(dataset: str)->str:
    # base_dir = osp.join('..','..','data','task3',dataset)
    base_dir = osp.join('data', 'task3', dataset)
    info_file = osp.join(base_dir, 'info.txt')
    if not osp.exists(info_file):
        preprocess_for_GraphRule(base_dir, dataset)
    with open(info_file, 'r') as f:
        # res = json.dumps(json.load(f), indent=4)
        res = json.load(f)
    return res

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

# fake cases
def get_rules(dataset: str):
    base_dir = osp.join('data','task3',dataset)
    filename = osp.join(base_dir, 'rules.json')
    if not osp.exists(filename):
        hypergraphs = load_rules(dataset)
        rules = {}
        for gid, _ in enumerate(hypergraphs):
            rules[str(gid)] = {'edges':[]}
            hyperedges = hypergraphs[gid]['edges']
            # print(hyperedges)
            for eid in hyperedges:
                rules[str(gid)]['edges'].append({
                    'relation':hyperedges[eid]['relation'],
                    'entities':hyperedges[eid]['list']
                })
        json_str = json.dumps(rules,indent=4)
        with open(filename, 'w') as f:
            f.write(json_str)
        return rules
    else:
        with open(filename, 'r') as f:
            rules = json.load(f)
            return rules
        

def build_cases(dataset: str):
    case_path = osp.join('data','task3',dataset,'cases.json')
    rules = get_rules(dataset)
    if not osp.exists(case_path):
        return rules
    with open(case_path, 'r') as f:
        case_mapping = json.load(f)
    for id in rules:
        new_edges = []
        for i, edge in enumerate(rules[id]['edges']):
            new_edge = edge
            new_edge['relation'] = case_mapping[str(id)]['edge'][str(i)]['name']
            for j, x in enumerate(edge['entities']):
                print(j, x)
                new_edge['entities'][j] = case_mapping[str(id)]['vertex'][str(x)]['name']
            new_edges.append(new_edge)
        rules[id]['edges'] = new_edges
    return rules

def run_filtration(dataset:str, layer:int, is_full:bool)->str:
    reweight_method = 'hyperedge_strength'
    # 1. 加载规则
    hypergraphs = filtration.load_rules(dataset)
    print(hypergraphs)
    # 2. 赋权值
    hypergraphs = filtration.reweight(hypergraphs, reweight_method)
    # 3. 做filtration
    filtrated_hypergraphs, old2new_map = filtration.filtration(hypergraphs, layer, is_full)
    # print(filtrated_hypergraphs)
    # print(old2new_map)
    # 4. 保存结果
    dataset_name = f'{dataset}-{layer}-{"full" if is_full else "partial"}'
    filtration.save(filtrated_hypergraphs, old2new_map, dataset_name)
    return dataset_name

def load_model():
    return 0

def run_model(dataset:str, model):
    hypergraphs = kernel.load_hypergraph_rules(dataset)
    y = [g['hypergraph_label'] for g in hypergraphs]
    emb_file = osp.join('data','task3', dataset, 'model_emb.npy')
    emb = np.load(emb_file)
    
    return emb, np.array(y)

def run_kernel(dataset:str, method:str):
    hypergraphs = kernel.load_hypergraph_rules(dataset)
    y = [g['hypergraph_label'] for g in hypergraphs]
    graphs = kernel.clique_expansion(hypergraphs)
    graphs = [kernel.to_grakel_graph(graph) for graph in graphs]
    mat = kernel.run_grakel_kernel(graphs, method)
    # acc, std = kernel.svm_evaluation(mat, np.array(y))
    # print(acc, std)
    return mat
    
def load_dbscan_emb(dataset:str):
    emb_file = osp.join('data','task3', dataset, 'model_emb.npy')
    emb = np.load(emb_file)
    return emb

def save_emb(emb, dataset, filename):
    base_dir = osp.join('data','task3',dataset)
    emb_file = osp.join(base_dir, filename)
    np.save(emb, emb_file)

def run_exkmeans(emb, dataset, method, k):
    emb = np.array(emb,dtype=np.double)
    tree = Tree(k=k, max_leaves=2*k)
    prediction = tree.fit_predict(emb)
    filename = f'{dataset}-{method}-{k}-tree'
    tree.plot(osp.join('data','task3',dataset,filename))
    return osp.join('data','task3',dataset, filename + '.gv.png'), prediction.tolist()

def calc_SSE(emb, label):
    if isinstance(emb, dict):
        assert len(emb) == len(label)
        new_emb = []
        for x in emb:
            new_emb.append(emb[x])
        emb = np.array(new_emb)
    num_label = int(max(label)) + 1
    cluster_size = [0 for _ in range(num_label)]
    cluster_center = [np.zeros([emb.shape[1]]) for _ in range(num_label)]
    for i, x in enumerate(label):
        cluster_size[int(x)] += 1
        cluster_center[int(x)] += emb[i]
    for i in range(len(cluster_center)):
        cluster_center[i] /= cluster_size[i]
    SSE = 0
    print(num_label, cluster_size, cluster_center)
    for i in range(emb.shape[0]):
        SSE += np.linalg.norm(emb[i] - cluster_center[int(label[i])], 2)
    return SSE

def draw_scatter(emb, y, dataset, method, k):
    tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
    emb = tsne.fit_transform(emb)  # 转换后的输出
    emb = np.array(emb,dtype=np.double)
    # plt.scatter(Y[:, 0], Y[:, 1], c=y, cmap=plt.cm.Spectral)
    filename = f'{dataset}-{method}-{k}-scatter'
    # plt.savefig(fname=osp.join('data','task3',dataset,filename))

    kmeans = KMeans(k, random_state=42)
    kmeans.fit(emb)
    # plot_kmeans(kmeans, emb, filename=osp.join('data','task3',dataset,filename + '.png'))
    tree_2k = Tree(k, max_leaves=2*k)
    # print(kmeans)
    tree_2k.fit(emb, kmeans)
    out_filename = osp.join('data','task3',dataset,filename + '.png')
    plot_tree_boundary(tree_2k, k, emb, kmeans, filename=out_filename, plot_mistakes=True)
    
    return out_filename

def load_matrix(dataset:str, method:str):
    base_dir = osp.join( 'data', 'task3', dataset)
    mat_file = osp.join(base_dir, dataset, 'matrices', f'{method}.txt')
    with open(mat_file, 'r') as f:
        lines = f.readlines()
        mat = []
        for line in lines:
            line = list(map(float,line.strip('\n').strip(' ').split(' ')))
            mat.append(line)
    return mat

def svd(mat):
    mat = np.array(mat)
    print(mat)
    _, vecs = np.linalg.eig(mat)
    return vecs

def dimension_reduction(emb):
    # tsne
    X_tsne = manifold.TSNE(n_components=2, random_state=42).fit_transform(emb).tolist()
    new_emb = {}
    for i, x in enumerate(X_tsne):
        new_emb[str(i)] = x
    return new_emb

def get_rules_and_emb_by_ids(rules, cases, emb, ids):
    new_rules = {}
    new_emb = {}
    new_cases = {}
    for id in ids:
        new_rules[str(id)] = rules[str(id)]
        new_cases[str(id)] = cases[str(id)]
        new_emb[str(id)] = emb[str(id)]
    return new_rules, new_cases, new_emb

def run_dbscan(emb):
    if isinstance(emb, dict):
        emb_list = []
        for x in emb:
            emb_list.append(emb[x])
        emb = emb_list
    minmax_scale = preprocessing.MinMaxScaler(feature_range=(-1, 1)).fit(np.array(emb))
    emb = minmax_scale.transform(emb)
    print(emb)
    db = DBSCAN(eps=0.2).fit(emb)
    labels = db.labels_
    return labels


def reformat_result(rules, cases, emb, labels, ids):
    if isinstance(emb, List):
        emb_dict = {}
        for i, x in enumerate(emb):
            emb_dict[str(i)] = x
        emb = emb_dict
    ans = {
        'embedding': emb,
        'rules': rules,
        'cases': cases,
    }
    labels = labels.tolist()
    # print('labels:',labels)
    # print('ids:',ids)
    for i, x in zip(ids, labels):
        # print(i, x)
        ans['rules'][str(i)]['label'] = x
        ans['cases'][str(i)]['label'] = x
    return ans

def combine_cases_and_labels(ids, cases, labels):
    for i, x in zip(ids, labels):
        cases[str(i)]['label'] = x
    return cases

# emb = np.array([[1, 2], [2, 3], [3, 4], [4, 5]], dtype=np.float)
# label = [0, 1, 1, 0]
# calc_SSE(emb, label)
