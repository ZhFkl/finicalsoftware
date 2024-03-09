from typing import List
import grakel
import os.path as osp
import os
import time
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.svm import LinearSVC, SVC
from sklearn.metrics import accuracy_score



def clique_expansion(hypergraphs: List):
    for hypergraph in hypergraphs:
        old_hyperedges = hypergraph['hyperedge']
        new_edges = []
        new_edge_labels = []
        for hyperedge, hyperedge_label in zip(old_hyperedges,hypergraph['hyperedge_label']):
            # double-link edge
            for u in hyperedge:
                for v in hyperedge:
                    if u != v:
                        new_edges.append((u, v))
                        new_edge_labels.append(hyperedge_label)
        hypergraph['edges'] = new_edges
        hypergraph['edge_label'] = new_edge_labels
    return hypergraphs

def load_hypergraph_rules(dataset:str):
    base_dir = osp.join('data','task3',dataset,f'{dataset}-H','raw')
    f_A = open(osp.join(base_dir,f'{dataset}-H_A.txt'), 'r')
    f_EL = open(osp.join(base_dir,f'{dataset}-H_edge_labels.txt'), 'r')
    f_GI = open(osp.join(base_dir,f'{dataset}-H_graph_indicator.txt'), 'r')
    f_GL = open(osp.join(base_dir,f'{dataset}-H_graph_labels.txt'), 'r')
    f_NL = open(osp.join(base_dir,f'{dataset}-H_node_labels.txt'), 'r')
    
    hypergraphs = []
    lines = f_GI.readlines()
    node_indicator = [int(x.strip('\n')) for x in lines]
    lines = f_EL.readlines()
    edge_label = [int(x.strip('\n')) for x in lines]
    lines = f_NL.readlines()
    node_label = [int(x.strip('\n')) for x in lines]
    lines = f_GL.readlines()
    graph_label = [int(x.strip('\n')) for x in lines]
    
    node_size = [0 for _ in range(max(node_indicator) + 1)]
    for x in node_indicator:
        node_size[x] += 1    
    for i in range(len(node_size) - 1):
        node_size[i + 1] += node_size[i]
    
    lines = f_A.readlines()
    current_hypergraph = {}
    graph_size = 0
    for line_id, line in enumerate(lines):
        hyperedge = list(map(int,line.strip('\n').split(',')))
        gid = node_indicator[hyperedge[0]]
        if graph_size != gid:
            if current_hypergraph != {}:
                hypergraphs.append(current_hypergraph)
            current_hypergraph = {}
            current_hypergraph['hyperedge'] = []
            current_hypergraph['node_label'] = []
            current_hypergraph['hyperedge_label'] = []
            current_hypergraph['hypergraph_label'] = graph_label[graph_size]
            graph_size += 1
        hyperedge = [(x - node_size[gid - 1]) for x in hyperedge]
        current_hypergraph['hyperedge'].append(hyperedge)
        current_hypergraph['hyperedge_label'].append(edge_label[line_id])   
    if current_hypergraph != {}:
        hypergraphs.append(current_hypergraph)
    # print(len(node_indicator), len(node_label), len(hypergraphs))
    for gid, label in zip(node_indicator, node_label):
        hypergraphs[gid - 1]['node_label'].append(label)
    
    f_A.close()
    f_EL.close()
    f_GI.close()
    f_GL.close()
    f_NL.close()
    
    return hypergraphs


# 10-CV for kernel svm and hyperparameter selection.
def svm_evaluation(mat, classes, num_repetitions=10,
                          C=[10 ** 3, 10 ** 2, 10 ** 1, 10 ** 0, 10 ** -1, 10 ** -2, 10 ** -3]):
    # Acc. over all repetitions.
    accuracy_all = []

    for i in tqdm(range(num_repetitions),desc='run svm'):
    # for i in range(num_repetitions):
        # Test acc. over all folds.
        kf = KFold(n_splits=10, shuffle=True, random_state=42 + i)
        accuracy = []
        for train_index, test_index in kf.split(list(range(len(classes)))):
            # Determine hyperparameters
            train = mat[train_index, :]
            train = train[:, train_index]
            test = mat[test_index, :]
            test = test[:, train_index]
            c_train = classes[train_index]
            c_test = classes[test_index]

            params = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}
            clf = GridSearchCV(
                SVC(kernel='precomputed'), params, cv=5, scoring='accuracy', verbose=0,n_jobs=1)
            clf.fit(train, c_train)
            c_pred = clf.predict(test)
            best_test_acc = accuracy_score(c_test, c_pred) * 100.0
            accuracy.append(best_test_acc)
        accuracy_all.append(np.array(accuracy).mean())

    return np.array(accuracy_all).mean(), np.array(accuracy_all).std()

def to_grakel_graph(graph):
    bi_edge_list = graph['edges']
    node_feat, edge_feat = graph['node_label'], graph['edge_label']
    node_feat = {i : x for i, x in enumerate(node_feat)}
    edge_feat = {(u, v): x for (u, v), x in zip(bi_edge_list, edge_feat)}
    return [bi_edge_list, node_feat, edge_feat]

def run_grakel_kernel(graphs, method):
    kernel_method = {
        'VH': grakel.VertexHistogram(normalize=True),
        'WL': grakel.WeisfeilerLehman(normalize=True, n_iter=5),
        'GL': grakel.GraphletSampling(normalize=True,k=3,sampling={'n_samples':500},random_state=123),
        'SP': grakel.ShortestPath(normalize=True,algorithm_type='dijkstra'),
    }
    
    tic = time.process_time()
    grk = kernel_method[method]        
    mat = grk.fit_transform(graphs)
    time_cost = time.process_time() - tic
    print(f'run {method} kernel, time cost: {time_cost:.2f}(s)')
    return mat