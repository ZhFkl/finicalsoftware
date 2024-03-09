import json
import copy
from fastapi import APIRouter

task2 = APIRouter(prefix='/task2')

dataset_dict = {
    # 'finance1': 'data/task2/subgraph_1',
    'DATA2.1-公司合伙关系1': 'data/task2/subgraph_2',
    'DATA2.1-公司合伙关系2': 'data/task2/subgraph_3',
    'DATA2.1-公司合伙关系3': 'data/task2/subgraph_4'
}
result_dict = {
    'HyperE': 'infer/hyper.json',
    'TransE': 'infer/trans.json',
    'CompE': 'infer/comp.json'
}

info_dict = {
    'HyperE': 'data/task2/model/hyper.png',
    'TransE': 'data/task2/model/trans.png',
    'CompE': 'data/task2/model/comp.png'
}

@task2.get('/')
def hello(task: int=1):
    if task == 1:
        available_dataset = ['DATA2.1-公司合伙关系1', 'DATA2.1-公司合伙关系2', 'DATA2.1-公司合伙关系3']
        available_method = ['TransE', 'HyperE']
    elif task == 2:
        available_dataset = ['DATA2.1-公司合伙关系1', 'DATA2.1-公司合伙关系2', 'DATA2.1-公司合伙关系3']
        available_method = ['TransE', 'CompE']
    return {
        'available_dataset': available_dataset,
        'available_method': available_method
    }

@task2.get('/rule/origin')
def rule_origin():
    return json.load(open('data/task2/data_origin.json', 'r', encoding='utf-8'))

@task2.get('/rule/infer')
def rule_infer():
    return json.load(open('data/task2/data_now.json', 'r', encoding='utf-8'))

@task2.get('/rule/path')
def rule_infer_path():
    return json.load(open('data/task2/data_tuili.json', 'r', encoding='utf-8'))

@task2.get('/rule/origin_new')
def rule_origin_new(guize : int):
    return json.load(open('data/task2/rule/data_origin_new_{}.json'.format(guize), 'r', encoding='utf-8'))

@task2.get('/rule/infer_new')
def rule_infer_new(guize : int):
    return json.load(open('data/task2/rule/data_now_new_{}.json'.format(guize), 'r', encoding='utf-8'))

@task2.get('/rule/path_new')
def rule_infer_path_new(guize : int):
    return json.load(open('data/task2/rule/data_tuili_new_{}.json'.format(guize), 'r', encoding='utf-8'))

def get_entity(dataset='DATA2.1-公司合伙关系1'):
    if dataset not in dataset_dict.keys():
        return {
            'error': 'Invalid dataset'
        }
    entity = {}
    data = json.load(open(f'{dataset_dict[dataset]}/entity.json', 'r', encoding='utf-8'))
    for x in data:
        entity[x['entity_id']] = x
    return entity

def get_relation(dataset='DATA2.1-公司合伙关系1'):
    if dataset not in dataset_dict.keys():
        return {
            'error': 'Invalid dataset'
        }
    relation = {}
    data = json.load(open(f'{dataset_dict[dataset]}/relation.json', 'r', encoding='utf-8'))
    for x in data:
        relation[x['relation_id']] = x
    return relation

@task2.get('/knowledge_graph')
def get_knowledge_graph(dataset='DATA2.1-公司合伙关系1'):
    if dataset not in dataset_dict.keys():
        return {
            'error': 'Invalid dataset'
        }
    entity = get_entity(dataset)
    relation = get_relation(dataset)
    ans = []
    edges = json.load(open(f'{dataset_dict[dataset]}/edge.json', 'r', encoding='utf-8'))
    for edge in edges:
        res = {
            "hyper_edge_id": edge['hyper_edge_id'],
            'relation': relation[edge['relation_id']],
            'start_time': edge['start_time'],
            'end_time': edge['end_time'],
            'entities': []
        }
        for x in edge['entities']:
            res['entities'].append(entity[x])
        ans.append(res)
    return ans

@task2.get('/entity')
def entity_info(dataset: str='DATA2.1-公司合伙关系1', entity_id: str="2003011597"):
    if dataset not in dataset_dict.keys():
        return {
            'error': 'Invalid dataset'
        }
    entity_dict = get_entity(dataset)
    if entity_id not in entity_dict.keys():
        return {
            'error': 'Invalid entity'
        }
    return entity_dict[entity_id]

@task2.post('/infer')
def infer(dataset: str='DATA2.1-公司合伙关系1', method: str='TransE', entity: str="2003011597"):
    if dataset not in dataset_dict.keys():
        return {
            'error': 'Invalid dataset'
        }
    if method not in result_dict.keys():
        return {
            'error': 'Invalid infer method'
        }
    entity_dict = get_entity(dataset)
    relation_dict = get_relation(dataset)
    infer_results = json.load(open(f'{dataset_dict[dataset]}/{result_dict[method]}', 'r', encoding='utf-8'))
    ans = []
    for data in infer_results:
        if entity == data['entities'][0]:
            res = {
                'relation': relation_dict[data['relation_id']],
                'entity': [entity_dict[x] for x in data['entities']],
                'score': data['score']
            }
            if method == 'CompE':
                res['weights'] = data['weights']
            ans.append(res)
    ans = sorted(ans, key=lambda x: x['score'], reverse=True)
    return ans

@task2.get('/metric')
def metric(dataset='DATA2.1-公司合伙关系1'):
    if dataset not in dataset_dict.keys():
        return {
            'error': 'Invalid dataset'
        }
    return json.load(open(f'{dataset_dict[dataset]}/metric.json', 'r', encoding='utf-8'))

@task2.get('/info')
def info(method: str='TransE'):
    if method not in info_dict.keys():
        return {
            'error': 'Invalid infer method'
        }
    return {
        'graph': info_dict[method],
        'info': 'Hit@n: Link Prediction中分数排名小于n的多元组的平均占比 (越高越好)\n'
                'MRR: Link Prediction中真实多元组分数排名倒数的平均值 (越高越好)\n'
                'AUC: 分类任务中评价分类器的性能 (越高越好)\n'
                'ACC: 分类任务中分类器的准确率, 即预测正确的样本占总数据的比例 (越高越好)'
    }

@task2.get('/hypergraph')
def hypergraph(dataset: str='DATA2.1-公司合伙关系3'):
    entity = get_entity(dataset)
    relation = get_relation(dataset)
    ans = []
    edges = json.load(open(f'{dataset_dict[dataset]}/edge.json', 'r', encoding='utf-8'))
    for edge in edges:
        res = {
            "hyper_edge_id": edge['hyper_edge_id'],
            'relation': relation[edge['relation_id']],
            'start_time': edge['start_time'],
            'end_time': edge['end_time'],
            'entities': []
        }
        for x in edge['entities']:
            res['entities'].append(entity[x])
        ans.append(res)
    return ans

@task2.get('/editdistance')
def editdistance(f_node_id: int= 53391742, t_node_id: int=32786872):
    text = "实体" + str(f_node_id) + "和实体" + str(t_node_id) + "的编辑距离为 5"
    return text

@task2.get('/hyperedgepredict')
def hyperedgepredict(dataset: str='DATA2.1-公司合伙关系3', l: int= 3, tau: float = 0.8):
    entity = get_entity(dataset)
    relation = get_relation(dataset)
    ans = []
    edges = json.load(open(f'{dataset_dict[dataset]}/edge.json', 'r', encoding='utf-8'))
    for edge in edges:
        res = {
            "hyper_edge_id": edge['hyper_edge_id'],
            'relation': relation[edge['relation_id']],
            'start_time': edge['start_time'],
            'end_time': edge['end_time'],
            'entities': []
        }
        for x in edge['entities']:
            res['entities'].append(entity[x])
        ans.append(res)
    return ans

