import request from '@/utils/request2'

// 频繁子图挖掘
export function getTopic2Data(data) {
    return request({
        // datatype: 'json',
        url: '/task2/knowledge_graph',
        method: 'get',
        params:data
    })
}

// 查询方法列表
export function fetchMethodList(data) {
    return request({
        url: '/task2?task='+data,
        method: 'get'
    })
}

// 推理
export function fetchInferResult(data) {
    return request({
        url: '/task2/infer',//?method='+data.method+'&entity='+data.entity,
        method: 'post',
        params:data
    })
}
// 推理
export function fetchInferMetric(data) {
    return request({
        url: '/task2/metric',//?method='+data.method+'&entity='+data.entity,
        method: 'get',
        params:data
    })
}

export function getDataInfer() {
    return request({
        // datatype: 'json',
        url: '/task2/rule/infer',
        method: 'get'
    })
}
export function getRulePath() {
    return request({
        // datatype: 'json',
        url: '/task2/rule/path',
        method: 'get'
    })
}
export function getDataOrigin() {
    return request({
        // datatype: 'json',
        url: '/task2/rule/origin',
        method: 'get'
    })
}

export function getNodeInfo(data) {
    return request({
        // datatype: 'json',
        url: '/task2/entity',
        // url: '/task2/entity?entity_id='+data.entity_id+"&available_dataset="+data.dataset,
        method: 'get',
        params:data
    })
}
export function getRulePathNew(guize) {
    return request({
        // datatype: 'json',
        url: '/task2/rule/path_new?guize='+guize,
        method: 'get'
    })
}
export function getDataOriginNew(guize) {
    return request({
        // datatype: 'json',
        url: '/task2/rule/origin_new?guize='+guize,
        method: 'get'
    })
}
export function getDataInferNew(guize) {
    return request({
        // datatype: 'json',
        url: '/task2/rule/infer_new?guize='+guize,
        method: 'get'
    })
}
export function getHypergraph() {
    return request({
        url: '/task2/hypergraph',
        method: 'get'
    })
}
export function getEditDistance(data) {
    return request({
        url: '/task2/editdistance?f_node_id='+data.fId+'&t_node_id='+data.tId,
        method: 'get'
    })
}
export function getHyedgePredict(data) {
    return request({
        url: '/task2/hyperedgepredict?l='+data.lambda+'&delta='+data.tau,
        method: 'get'
    })
}

export function getMetricDetail(model) {
    return request({
        // datatype: 'json',
        url: '/task2/info?method='+model,
        method: 'get'
    })
}