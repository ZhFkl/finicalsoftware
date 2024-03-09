import enum
import os
import os.path as osp
import numpy as np
import json
import time

from typing import List

from sklearn import datasets
from fastapi import APIRouter

import router.utils.task3helper as task3helper

task3 = APIRouter(prefix="/task3")

OLD_RULES_RATIO = 0.8
available_kernel = ['VH', 'WL']

@task3.get("/")
def hello():
    return 'hello'

@task3.get("/datalist")
def get_all_datalist() -> List[str]:
    ans = []
    for dirs in os.listdir('data/task3'):
        if 'rules' in dirs and '-' not in dirs:
            ans.append(dirs)
    return sorted(ans)

@task3.get("/datainfo/{dataset}")
def get_datainfo(dataset: str)->str:
    # 返回json格式的数据信息
    return task3helper.parse_data_and_get_info(dataset)

@task3.get("/moredatainfo/{dataset}")
def get_data(dataset:str):
    return task3helper.build_cases(dataset)

@task3.get("/filtration")
def filtration(dataset:str, layer:int, full_or_partial:str):
    if full_or_partial != 'full' and full_or_partial != 'partial':
        print(f'unknown method: {full_or_partial} and default as full')
        full_or_partial = 'full'
    if layer < 2 or layer > 5:
        print('layer is too small or too large and default as 2')
        layer = 2
    new_dataset = task3helper.run_filtration(dataset, layer, True if full_or_partial == 'full' else False)
    return new_dataset

@task3.get("/cluster/kernel")
def run_kernel(dataset:str, method: str, k: int, use_filtration=False)->str:
    available_dataset = ['rules_1', 'rules_2']
    if dataset not in available_dataset:
        raise TimeoutError("dataset too large!")
    if method == None:
        method = 'WL'
    if k == None:
        k = 3
    if method not in available_kernel:
        method = 'WL'
    all_dataset = task3helper.get_all_dataset()
    if use_filtration:
        if dataset + '-2-full' not in all_dataset:
            task3helper.run_filtration(dataset, 2, 'full')
        dataset = dataset + '-2-full'
        task3helper.parse_data_and_get_info(dataset)
    # # 1. 调用对应的exe得到结果
    # task3helper.run_kernel(dataset, method)
    # # 2. 加载生成的矩阵
    # mat = task3helper.load_matrix(dataset, method)
    # # 3. 将得到的矩阵分解得到emb
    # emb = task3helper.svd(mat)
    # # 4. 离线存储emb
    # task3helper.save_emb(emb, dataset, 'kernel_emb.npz')

    tic = time.time()
    emb_file = osp.join('data','task3', dataset, f'kernel_{method}_emb.npy')
    emb = np.load(emb_file)
    _, y = task3helper.run_model(dataset, 1)

    # mat = task3helper.run_kernel(dataset, method)
    # qwq = task3helper.svd(mat)
    # print(qwq)

    # 5. 生成决策树和散点图
    tree_path, labels = task3helper.run_exkmeans(emb, dataset, method, k)
    # scatter_path = task3helper.draw_scatter(emb, y, dataset, method, k)

    # TODO(陈子健):修一下embedding生成和数据返回
    new_emb = task3helper.dimension_reduction(emb)
    #cases = task3helper.get_rules(dataset)
    cases = task3helper.build_cases(dataset)
    assert len(cases) == len(labels)
    cases = task3helper.combine_cases_and_labels(list(range(len(cases))), cases, labels)

    res = {
        'tree_path':tree_path,
        'embedding': new_emb,
        'cases': cases,
        'time': time.time() - tic,
        'SSE': task3helper.calc_SSE(new_emb, labels)
    }
    return res
    

@task3.get("/cluster/infohyper")
def run_model(dataset:str, k: int, use_filtration=False)->str:
    available_dataset = ['rules_1', 'rules_2']
    if dataset not in available_dataset:
        raise TimeoutError("dataset too large!")
    all_dataset = task3helper.get_all_dataset()
    if use_filtration:
        if dataset + '-2-full' not in all_dataset:
            task3helper.run_filtration(dataset, 2, 'full')
        dataset = dataset + '-2-full'
        task3helper.parse_data_and_get_info(dataset)
    tic = time.time()
    # FIXME: model的路径
    model_path = ''
    # 1. 加载模型 (注意只需要加载一次)
    model = task3helper.load_model()
    # 2. 将数据加载进模型，并且运行出结果
    emb, y = task3helper.run_model(dataset, model)
    # 3. 生成决策树和散点图
    tree_path, labels = task3helper.run_exkmeans(emb, dataset, 'model', k)
    # scatter_path = task3helper.draw_scatter(emb, y, dataset, 'model', k)
    
    # TODO(陈子健):修一下embedding生成和数据返回
    new_emb = task3helper.dimension_reduction(emb)
    #cases = task3helper.get_rules(dataset)
    cases = task3helper.build_cases(dataset)
    assert len(cases) == len(labels)
    cases = task3helper.combine_cases_and_labels(list(range(len(cases))), cases, labels)

    res = {
        'tree_path':tree_path,
        'embedding': new_emb,
        'cases': cases,
        'time': time.time() - tic,
        'SSE': task3helper.calc_SSE(new_emb, labels)
    }
    return res


@task3.get("/cluster/motif")
def run_motif(dataset:str, k:int, use_filtration=False)->str:
    exe_file = 'app/task3/motif_count'
    in_file = f'data/task3/{dataset}/{dataset}/rules.txt'
    out_file = f'data/task3/{dataset}/motif.txt'
    tic = time.time()
    all_dataset = task3helper.get_all_dataset()
    if use_filtration:
        if dataset + '-2-full' not in all_dataset:
            task3helper.run_filtration(dataset, 2, 'full')
        dataset = dataset + '-2-full'
        task3helper.parse_data_and_get_info(dataset)
    if not osp.exists(out_file):
        os.system(f'./{exe_file} {in_file} {out_file}')
        print(f'./{exe_file} {in_file} {out_file}')
    motif_count = []
    with open(out_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n').strip(' ')
            motif_count.append(list(map(int, line.split(' '))))
    motif_count = np.array(motif_count)
    # FIXME(chenzijian):现在还不是超图，motif embedding怪怪的
    print(motif_count)
    if 'rules_3' in dataset:
        emb = motif_count
    else:
        emb_file = osp.join('data','task3', dataset, f'kernel_VH_emb.npy')
        emb = np.load(emb_file)
    print(emb.shape)

    # TODO(chenzijian):修一下embedding生成和数据返回
    tree_path, labels = task3helper.run_exkmeans(emb, dataset, 'motif', k)

    if 'rules_3' in dataset:
        labels = labels[:1000]
        emb = emb[:1000,:]

    new_emb = task3helper.dimension_reduction(emb)
    #cases = task3helper.get_rules(dataset)
    cases = task3helper.build_cases(dataset)
    
    if 'rules_3' in dataset:
        new_cases = {}
        for i in range(1000):
            new_cases[str(i)] = cases[str(i)]
        cases = new_cases
    assert len(cases) == len(labels)

    cases = task3helper.combine_cases_and_labels(list(range(len(cases))), cases, labels)

    res = {
        'tree_path':tree_path,
        'embedding': new_emb,
        'cases': cases,
        'time': time.time() - tic,
        'SSE': task3helper.calc_SSE(new_emb, labels)
    }
    return res


@task3.get("/cluster/dataset")
def get_cluster_data(dataset:str):
    rules = task3helper.get_rules(dataset)
    cases = task3helper.build_cases(dataset)
    emb = task3helper.load_dbscan_emb(dataset)
    emb = task3helper.dimension_reduction(emb)

    ids = list(range(int(len(rules) * OLD_RULES_RATIO)))
    old_rules, old_cases, old_emb = task3helper.get_rules_and_emb_by_ids(rules, cases, emb, ids)

    old_label = task3helper.run_dbscan(old_emb)
    ans = task3helper.reformat_result(old_rules, old_cases, old_emb, old_label, ids)
    return ans

@task3.get("/cluster/new_rules")
def get_new_rules(dataset:str):
    rules = task3helper.get_rules(dataset)
    cases = task3helper.build_cases(dataset)

    ans = {'rules':{},'cases':{}}
    for id in rules:
        if float(id) > len(rules) * OLD_RULES_RATIO:
            ans['rules'][id] = rules[id]
            if rules is not None:
                ans['cases'][id] = cases[id]
            else:
                ans['cases'][id] = rules[id]
    return ans

@task3.get("/cluster/dbscan")
def dynamic_dbscan(dataset:str, new_ids: str):    
    new_ids = new_ids.strip('[').strip(']')
    print(new_ids)
    new_ids = list(map(int,new_ids.split(',')))

    rules = task3helper.get_rules(dataset)
    cases = task3helper.build_cases(dataset)
    emb = task3helper.load_dbscan_emb(dataset)
    emb = task3helper.dimension_reduction(emb)

    old_ids = list(range(int(len(rules) * OLD_RULES_RATIO)))
    _, _, old_emb = task3helper.get_rules_and_emb_by_ids(rules, cases, emb, old_ids)
    old_label = task3helper.run_dbscan(old_emb).tolist()
    # old_ans = task3helper.reformat_result(old_rules, old_emb, old_label)

    old_ids.extend(new_ids)
    new_ids = old_ids
    _, _, new_emb = task3helper.get_rules_and_emb_by_ids(rules, cases, emb, new_ids)
    new_label = task3helper.run_dbscan(new_emb).tolist()
    diff_dict = {'embedding':{},'label':{}}

    for i, x in enumerate(old_label):
        if old_label[i] != new_label[i]:
            diff_dict['label'][str(new_ids[i])] = new_label[i]
            diff_dict['embedding'][str(new_ids[i])] = new_emb[str(new_ids[i])]
    
    # print(len(new_label), len(new_ids))
    for i in range(len(old_label), len(new_label)):
        diff_dict['label'][str(new_ids[i])] = new_label[i]
        diff_dict['embedding'][str(new_ids[i])] = new_emb[str(new_ids[i])]
    
    return diff_dict

